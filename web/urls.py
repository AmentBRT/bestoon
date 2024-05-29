from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit/expense/', views.submit_expense, name='submit_expense'),
    path('submit/income/', views.submit_income, name='submit_income'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', lambda request: (), name='logout'),
]