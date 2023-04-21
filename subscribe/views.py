from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from home_app.models import Community
from .models import Subscriptions
from django.contrib.auth.decorators import login_required


@login_required
def subscriptions_list(request):
    
    subscriptions=Subscriptions.objects.filter(username=request.user.username).all()
    
    return subscriptions

@login_required
def subscriptions(request, community):
    
    c_match=Community.objects.filter(slug=community).first()
    
    Subscriptions.objects.create(username=request.user, community=c_match)

    return redirect(reverse('community', kwargs={'community': community}))

@login_required
def unsubscribtions(request, community):
    
    c_match=Community.objects.filter(slug=community).first()
    
    Subscriptions.objects.filter(username = request.user, community=c_match).delete()
    
    return redirect(reverse('community', kwargs={'community': community}))
