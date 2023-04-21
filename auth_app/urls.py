from django.urls import path
from . import views


urlpatterns = [
    
path('signup/', views.signup, name='sign_up'),
path('logout/',views.log_out, name='log_out_session'),
path('login/',views.log_in, name='log_in_session'),
path('profile/<username>/',views.profile, name='profile'),

path('activate/<uidb64>/<token>', views.activate_account, name='activate'),

path("change_pass/", views.change_pass, name='change_pass'),
path('pass_reset/', views.pass_reset_request, name='pass_reset'),
path('reset/<uidb64>/<token>', views.pass_reset_confirm, name='pass_reset_confirm'),
path('social/signup/', views.signup_redirect, name='signup_redirect'),



   
]