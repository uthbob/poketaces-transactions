'''
rest services
---PUT /transactionservice/transaction/10 { "amount": 5000, "type":"cars" } => { "status": "ok" } 
---PUT /transactionservice/transaction/11 { "amount": 10000, "type": "shopping", "parent_id": 10} => { "status": "ok" } 
---GET /transactionservice/types/cars => [10] 
---GET /transactionservice/sum/10 => {"sum":15000} 
---GET /transactionservice/sum/11 => {"sum":10000}

---db services---
get transactionId list for a given transaction type

update transaction for a given transaction id
____transaction amount changes
____transaction type changes
____transaction parent changes(this needs to be handled)

insert a transaction

get sum/totalamount for given transaction node's transitive children


'''
from django.db import transaction, OperationalError, IntegrityError
from rest_framework import serializers
from exceptions import *
from .models import AncestryTransaction

def getAncestryStringFromParentId(parent_id=None):
	'''
	find the transaction with given parent_id,
	get ancestry string, then append '/$parent_id' to the string 

	error handling, logger TODO
	'''

	try:
		#import pdb;pdb.set_trace()
		ancestry_string = "/"
		if parent_id:
			try:
				parent_transaction = AncestryTransaction.objects.get(id=parent_id)
			except AncestryTransaction.DoesNotExist as e:
				raise serializers.ValidationError("Transaction doesn't exist for parent_id")

			parent_ancestry_string = parent_transaction.ancestry_transactions
			if parent_ancestry_string:
				ancestry_string = parent_ancestry_string + str(parent_id) + '/'
			else:
				ancestry_string = '/' + str(parent_id) + '/'

		# ancestryTransactionObj = AncestryTransaction(amount=amount, transaction_type=transaction_type, ancestry_transactions=ancestry_string)
		# ancestryTransactionObj.save()
		return ancestry_string
	except Exception as e:
		raise e


@transaction.atomic
def updateTransactionParentId(transaction_id=None, parent_id=None):
	'''
	updating parent_id of transaction, means updating transaction, and its descendants
	get ancestry_string for new parent
	get all transitive child transactions, update them

	'''
	try:
		transaction_pattern = "/" + str(transaction_id) + "/"
		ancestry_string = "/"

		##get ancestry string of transaction from parent transaction
		try:
			parent_transaction = AncestryTransaction.objects.get(id=parent_id)
		except AncestryTransaction.DoesNotExist as e:
			raise serializers.ValidationError("Transaction doesn't exist for parent_id")
		parent_ancestry_string = parent_transaction.ancestry_transactions ##check
		if parent_ancestry_string:
			ancestry_string = parent_ancestry_string + str(parent_id) + "/"
		else:
			ancestry_string = '/' + str(parent_id) + '/'
		
		try:
			transaction = AncestryTransaction.objects.select_for_update().get(id=transaction_id)
		except AncestryTransaction.DoesNotExist as e:
			raise serializers.ValidationError("Transaction doesn't exist for parent_id")

		###fetch descendants transactions
		descendants_transactions = AncestryTransaction.objects.filter(ancestry_transactions__contains=transaction_pattern)
		for descendant in descendants_transactions:
			descendant_ancestry_string = descendant.ancestry_transactions
			transaction_ancestry_index = descendant_ancestry_string.rfind(transaction_pattern) + len(transaction_pattern) - 1

			post_index_string = descendant_ancestry_string[transaction_ancestry_index:]
			pre_index_string = ancestry_string + str(transaction_id) 
			new_descendant_ancestry_string = pre_index_string+post_index_string
			descendant.ancestry_transactions = new_descendant_ancestry_string
			descendant.save()

		###update transaction ancestry string after updating descendants ancestry string
		# transaction.ancestry_transactions = ancestry_string
		# transaction.save()

		return ancestry_string
	except Exception as e:
		raise e


# def updateTransactionAmount(transaction_id=None, transaction_amount=None):
# 	try:
# 		transaction = AncestryTransaction.objects.select_for_update().get(id=transaction_id)
# 		transaction.amount = transaction_amount
# 		transaction.save()

# 	except AncestryTransaction.DoesNotExist as e:
# 		raise e
# 	except Exception as e:
# 		raise e


# def updateTransactionType(transaction_id=None, transaction_type=None):
# 	try:
# 		transaction = AncestryTransaction.objects.select_for_update().get(id=transaction_id)
# 		transaction.transaction_type = transaction_type
# 		transaction.save()

# 	except AncestryTransaction.DoesNotExist as e:
# 		raise e
# 	except Exception as e:
# 		raise e

# @transaction.atomic
# def updateTransaction(transaction_id=None, transaction_type=None, amount=None, parent_id=None):
# 	try:
# 		if parent_id:
# 			updateTransactionParentId(transaction_id,parent_id)
# 		if transaction_type:
# 			updateTransactionType(transaction_id,transaction_type)
# 		if transaction_amount:
# 			updateTransactionAmount(transaction_id,amount)

# 	except Exception as e:
# 		raise e

def getTransactionListByType(transaction_type=None):
	try:
		transaction_list = []
		transactions = AncestryTransaction.objects.filter(transaction_type=transaction_type)
		for transaction in transactions:
			transaction_list.append(transaction.id)

	except Exception as e:
		raise e
	return transaction_list

		
def getTransactionChildSum(transaction_id=None):
	try:
		descendant_sum = 0
		transaction_pattern = '/' + str(transaction_id) + '/'
		descendant_transactions = AncestryTransaction.objects.filter(ancestry_transactions__contains=transaction_pattern)
		for descendant in descendant_transactions:
			descendant_sum += descendant.amount

	except Exception as e:
		raise e

	return descendant_sum

