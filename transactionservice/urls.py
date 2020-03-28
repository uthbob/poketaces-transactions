"""transactionservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from transaction import views
from .swagger_schema import SwaggerSchemaView

schema_view = get_swagger_view(title='Transaction Service')
urlpatterns = [
    #path('admin/', admin.site.urls),
    #path(r'swagger-docs/', schema_view),
    #path(r'^docs/', include('rest_framework_swagger.urls')),
    #path(r'transactionservice/', include('transaction.urls')),
    path(r'swagger/', SwaggerSchemaView.as_view()),
    path(r'transactionservice/transaction/<int:transaction_id>/', views.update_transaction),
    path(r'transactionservice/transaction/create', views.create_transaction),
    path(r'transactionservice/types/<str:transaction_type>/', views.transaction_type_list),
    path(r'transactionservice/sum/<int:transaction_id>/', views.transaction_transitive_sum),
]
