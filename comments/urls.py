from django import views
from . import views
from django.urls import path


urlpatterns = [
    
    path('<str:community>/<str:post>/create-comment/', views.create_comment, name='create-comment'),
    path('<str:post>/<str:author>/<int:id>/update/', views.comments_update, name='comments-update'),
    path('<str:post>/<str:author>/<int:id>/delete/', views.comments_delete, name='comments-delete'),
    path('<str:community>/<str:post>/<int:id>/create-reply/', views.reply_create, name='create-reply'),

]