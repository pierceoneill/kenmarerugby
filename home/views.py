from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

def index(request):
    posts = Post.objects.order_by('-published_date').filter()[:3]

    context = {
        'posts': posts,
    }
  
    return render(request, 'index.html', context)
