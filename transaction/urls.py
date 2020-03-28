# from django.urls import path
# from transaction import views

# urlpatterns = [
#     path('transaction/<int:transaction_id>/', views.update_transaction),
#     path('types/<str:transaction_type>/', views.transaction_type_list),
#     path('sum/<int:transaction_id>/', views.transaction_transitive_sum),

# ]





'''
rest services
---PUT /transactionservice/transaction/10 { "amount": 5000, "type":"cars" } => { "status": "ok" } 
---PUT /transactionservice/transaction/11 { "amount": 10000, "type": "shopping", "parent_id": 10} => { "status": "ok" } 
---GET /transactionservice/types/cars => [10] 
---GET /transactionservice/sum/10 => {"sum":15000} 
---GET /transactionservice/sum/11 => {"sum":10000}
'''