from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseForbidden, HttpResponseRedirect
from blog.models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from blog.forms import PostForm, CommentForm
from django.contrib import messages
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.template import RequestContext
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from .models import Post

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    redirect_field_name = 'post_list.html'
    

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post



class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@requires_csrf_token  
def PostDeleteView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if not(request.user == post.author or request.user.is_superuser):
        return render(request, '403.html')
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', post.pk)        
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})
    
  
@requires_csrf_token 
def PostUpdateView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if not(request.user == post.author or request.user.is_superuser):
        return render(request, "403.html")
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', post.pk)        
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Thanks for your feedback. Your comment will appear once approved")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not request.user.is_superuser :
        return HttpResponseForbidden('You do not have permission to approve!')
    else:
        comment.approve()
    return redirect('post_detail', pk=comment.post.pk)



@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if not request.user.is_superuser :
        return HttpResponseForbidden('You do not have permission to delete!')
    else:
        comment.delete()
    return redirect('post_detail', pk=post_pk)

