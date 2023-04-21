from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import user_is_superuser_or_author
from django.contrib import messages
from .models import Comment
from .forms import CommentForm, EditCommentForm
from home_app.models import Post


def comments_view(request, match):
    
    comments = Comment.objects.filter(post=match).all()
    
    return comments


@login_required
def create_comment(request, community, post):
    
    match = Post.objects.filter(community__slug=community, post_slug=post).first()
    
    if request.method == "POST":
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = match
            comment.save()
            return redirect(f"/{community}/{post}")
    else:
        form = CommentForm(initial={'post':match})
    
    return render(request, 'new_comments.html',{"type":"new","form": form})


@login_required
def reply_create(request, post, id, community):
    
    match = Comment.objects.filter(post__post_slug=post,id=id).first()
    p_match = Post.objects.filter(post_slug=post).first()
    
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.parent = match
            reply_comment.post = p_match
            reply_comment.save()
            return redirect(f"/{community}/{post}")
    else:
        form = CommentForm(initial={'parent':match}) 
           
    return render(request, 'new_comments.html', {"form": form})
    


@login_required
@user_is_superuser_or_author
def comments_update(request, post, author, id):
    
    p_match = Post.objects.get(post_slug=post)
    match = Comment.objects.filter(post=p_match, id=id).first()
    
    if request.method=='POST':
        form = EditCommentForm(request.POST, instance=match)
        if form.is_valid():
            edit=form.save(commit=False)
            edit.edited = True
            edit.save()
            return redirect(f'/{p_match.slug}')
            
    else:   
        form = EditCommentForm(instance=match)
        
    return render(request, 'new_comments.html', {"type":"update",'form': form})

@login_required
@user_is_superuser_or_author
def comments_delete(request, post, author, id):
    
    p_match = Post.objects.get(post_slug=post)
    match = Comment.objects.filter(post=p_match, id=id).first()
    
    if request.method=='POST':
        match.delete()
        return redirect(f"/{p_match.community.slug}/{post}")
    else:
        return render(request, 'confirm_delete_comment.html', {'object':match})