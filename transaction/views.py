# Create your views here.
'''
rest services
---PUT /transactionservice/transaction/10 { "amount": 5000, "type":"cars" } => { "status": "ok" } 
---PUT /transactionservice/transaction/11 { "amount": 10000, "type": "shopping", "parent_id": 10} => { "status": "ok" } 
---GET /transactionservice/types/cars => [10] 
---GET /transactionservice/sum/10 => {"sum":15000} 
---GET /transactionservice/sum/11 => {"sum":10000}
'''


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_swagger import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.serializers import ValidationError
from .models import AncestryTransaction
from .serializers import AncestryTransactionSerializer
from .services import getTransactionListByType, getTransactionChildSum

@csrf_exempt
@api_view(['PUT'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def update_transaction(request, transaction_id):

	# --- YAML below for swagger ---
	'''
	description: This API updates given transaction.
	parameters:
		- name: amount
	      type: double
	      required: true
	      location: form
	    - name: transaction_type
	      type: string
	      required: true
	      location: form
	    - name: parent_id
	      type: int
	      required: true
	      location: form
	'''

	try:
		ancestryTransaction = AncestryTransaction.objects.get(id=transaction_id)
	except AncestryTransaction.DoesNotExist:
		return JsonResponse({"message":e.args}, status=404)

	if request.method == 'PUT':
		try:
			request_data = request.data
			context = {}
			context['parent_id'] = request_data.get("parent_id", None)
			serializer = AncestryTransactionSerializer(ancestryTransaction, data=request.data, context=context)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({"status":"ok"}, status=201)
			return JsonResponse(serializer.errors, status=400)
		except ValidationError as e:
			return JsonResponse({"message":e.args}, status=400)



@csrf_exempt
@api_view(['POST'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def create_transaction(request):

	# --- YAML below for swagger ---
	'''
	description: This API creates transaction.
	parameters:
		- name: amount
	      type: double
	      required: true
	      location: form
	    - name: transaction_type
	      type: string
	      required: true
	      location: form
	    - name: parent_id
	      type: int
	      required: true
	      location: form
	'''
	try:
		if request.method == 'POST':
			request_data = request.data
			context = {}
			context['parent_id'] = request_data.get("parent_id", None)
			serializer = AncestryTransactionSerializer(data=request.data, context=context)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({"status":"ok"}, status=201)
			return JsonResponse(serializer.errors, status=400)
	except ValidationError as e:
		return JsonResponse({"message":e.args}, status=400)
	except Exception as e:
		return JsonResponse({"message":"some error occurred"}, status=500)



@csrf_exempt
@api_view(['GET'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def transaction_type_list(request, transaction_type):
	'''

	get transaction list by type

	'''
	#serializer = AncestryTransactionSerializer(data=request.data)
	if request.method == 'GET':
		try:
			transaction_list = getTransactionListByType(transaction_type)
			return JsonResponse({"transactions_list":transaction_list})
		except Exception as e:
			return JsonResponse({"message":e.args}, status=400)



@csrf_exempt
@api_view(['GET'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def transaction_transitive_sum(request, transaction_id):
	# ---- YAML below for swagger ----
	'''
	description: This API updates given transaction
	parameters:
	name: transaction_id
		type: int
		required: true
		location: form
	'''
	#serializer = AncestryTransactionSerializer(data=request.data)
	try:
		ancestryTransaction = AncestryTransaction.objects.get(id=transaction_id)
	except AncestryTransaction.DoesNotExist as e:
		return JsonResponse({"message":e.args}, status=400)

	if request.method == 'GET':
		try:
			descendant_sum = getTransactionChildSum(transaction_id)
			return JsonResponse({"sum":descendant_sum})
		except Exception as e:
			return JsonResponse({"message":"some error occurred"}, status=500)




