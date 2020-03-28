from rest_framework import serializers

from .models import AncestryTransaction
from .services import updateTransactionParentId, getAncestryStringFromParentId

class AncestryTransactionSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	amount = serializers.DecimalField(required=True, max_digits=15, decimal_places=6)
	transaction_type = serializers.CharField(required=True, max_length=20)
	ancestry_transactions = serializers.CharField(required=False, max_length=100, default='/')

	def create(self, validated_data):
		'''
		create and return new AncestryTransaction instance, given validate data
		'''
		#import pdb;pdb.set_trace()
		parent_id = self.context.get("parent_id", None)
		ancestry_transactions = getAncestryStringFromParentId(parent_id)
		validated_data['ancestry_transactions'] = ancestry_transactions
		return AncestryTransaction.objects.create(**validated_data)



	def update(self, instance, validated_data):
		'''
		update and return an existing AncestryTransaction instance, given validated data
		'''
		instance.amount = validated_data.get('amount', instance.amount)
		instance.transaction_type = validated_data.get('transaction_type', instance.transaction_type)
		parent_id = self.context.get("parent_id", None)

		if parent_id:
			if instance.id==int(parent_id):
				raise serializers.ValidationError("Invalid Operation. parent_id should not be equal to instance.id")
			instance.ancestry_transactions = updateTransactionParentId(instance.id, parent_id)
		else:
			instance.ancestry_transactions = instance.ancestry_transactions

		instance.save()
		return instance