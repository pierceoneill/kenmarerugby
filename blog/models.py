from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
import datetime

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images', default='Upload Picture')
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=340)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse('like', kwargs={"slug": self.slug})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
