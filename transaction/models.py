from django.db import models

# Create your models here.

'''
Transaction model
---transactionId
---amount
---type
---parentId(optional)

AncestryTransaction model
---transactionId
---amount
---type
---ancestry transactionid string(eg:- 1/2/3)


rest services
---PUT /transactionservice/transaction/10 { "amount": 5000, "type":"cars" } => { "status": "ok" } 
---PUT /transactionservice/transaction/11 { "amount": 10000, "type": "shopping", "parent_id": 10} => { "status": "ok" } 
---GET /transactionservice/types/cars => [10] 
---GET /transactionservice/sum/10 => {"sum":15000} 
---GET /transactionservice/sum/11 => {"sum":10000}

'''


class AncestryTransaction(models.Model):
	class Meta:
		app_label = "transaction"
		db_table = "transaction_ancestrytransaction"


	amount = models.DecimalField(max_digits=15, decimal_places=6, default=0.00)
	transaction_type = models.CharField(max_length=20,  default='default_type')##here default can be choices
	ancestry_transactions = models.CharField(max_length=100, default='/')

	'''
	To keep parent_id, need foreign key to self.id
	also how to create serializer for the same
	'''




