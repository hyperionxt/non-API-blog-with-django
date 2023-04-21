from django.urls import path

from . import views


urlpatterns = [
    
    path('<str:community>/subscribe/', views.subscriptions, name="subscribe"),
    path('<str:community>/unsubscribe/', views.unsubscribtions, name="unsubscribe"),
]