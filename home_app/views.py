from django.shortcuts import render, redirect
from .models import Post, Community,Category, Sub_Category
from subscribe.models import Subscriptions
from subscribe.views import subscriptions_list
from .decorators import *
from .forms import CreateCommunity, CreatePost, EditCommunity, EditPost
import os
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from comments.views import comments_view





def homepage(request):
    
    match=Post.objects.all()  
    
    if request.user.is_authenticated: 
        subscriptions=subscriptions_list(request)
    else:
        subscriptions= None
        
    return render(request, "home_app/home.html", {"objects": match, "subs":subscriptions})


def communities(request, community):
    
    c_match=Community.objects.filter(slug=community).first()
    p_match=Post.objects.filter(community__slug=community).all()
    
    if request.user.is_authenticated:
        s_match=Subscriptions.objects.filter(username=request.user.username, community=c_match).exists()
    else:
        s_match = None
    return render(request, "home_app/community.html", {"comm_object":c_match,"p_objects": p_match, 'sub':s_match})



def post_details(request, community, post):
     
    match=Post.objects.filter(community__slug=community, post_slug=post).first()
    comments = comments_view(request, match)
    
    return render(request, "home_app/posts.html", {"object": match, "comments": comments})



def category_filter(request, category):
    
    c_match = Category.objects.filter(slug=category).first()
    p_match = Post.objects.filter(post_category=c_match).all()
    
    return render(request, "home_app/home.html", {"objects": p_match, "type":"category", "cat":c_match})



@login_required
def new_community(request):
    
    categories=Category.objects.all()
    subcategories=Sub_Category.objects.all()
    
    if request.method =="POST":
        form = CreateCommunity(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            category_id = request.POST.get('category')
            subcategory_id = request.POST.get('subcategory')

            if category_id:
                category = Category.objects.get(id=category_id)
                community.category = category
            
                if subcategory_id:
                    subcategory = Sub_Category.objects.get(id=subcategory_id)
                    community.subcategory = subcategory
            
            community.save()
            return redirect("home")
    else:
        form = CreateCommunity()
            
    return render(request, "home_app/new_objects.html",{"object": "Community", "form": form, "categories":categories,"subcategories":subcategories})


@login_required
def community_edit(request, community):
    
    categories=Category.objects.all()
    subcategories=Sub_Category.objects.all()    
    match=Community.objects.filter(slug=community).first()
    
    if request.method =="POST":
        form = EditCommunity(request.POST, request.FILES, instance=match)
        if form.is_valid():
            community_form = form.save(commit=False)
            category_id = request.POST.get('category')
            subcategory_id = request.POST.get('subcategory')
            
            if category_id:
                category = Category.objects.get(id=category_id)
                community.category = category
            
                if subcategory_id:
                    subcategory = Sub_Category.objects.get(id=subcategory_id)
                    community.subcategory = subcategory
            
            community_form.save()
            return redirect("home")
    else:
        form = EditCommunity(instance=match)
        return render(request, "home_app/new_objects.html", {"type": "update", "object": "Community", "form": form, "categories":categories,"subcategories":subcategories})


@login_required
@user_is_superuser_or_author
def community_delete(request, community, author):
    match=Community.objects.filter(slug=community).first()
    
    if request.method =="POST":
        match.delete()
        return redirect('/')
    else:
        return render(request, "home_app/confirm_delete.html", {"object": match, "type": "community"})


@login_required
def new_post(request, community:str):
    
    community_obj=Community.objects.get(slug=community)
    
    if request.method == "POST":
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post_slug = slugify(form.cleaned_data['title'])
            
            form.instance.post_slug = post_slug
            form.instance.community= community_obj
            form.save()
            return redirect(f"/{community}/{post_slug}")          
    else:
        form = CreatePost(initial={'community':community})
    return render(request, "home_app/new_objects.html", {"object": "Post", "form": form})


@login_required
def post_edit(request, post, community):
    match=Post.objects.filter(community__slug=community, post_slug=post).first()
    
    if request.method =="POST":
        form = EditPost(request.POST, request.FILES, instance=match)
        if form.is_valid():
            form.save()
            return redirect(f'/{match.slug}')
    else:
        form = EditPost(instance=match)
        return render(request, "home_app/new_objects.html", {"type":"update", "object": "Post", "form": form})


@login_required
@user_is_superuser_or_author
def post_delete(request, post, community, author):
    match=Post.objects.filter(community__slug=community, post_slug=post).first()
    
    if request.method =="POST":
        match.delete()
        return redirect('/')
    else:
        return render(request, "home_app/confirm_delete.html", {"object": match, "type": "post"})
        





    