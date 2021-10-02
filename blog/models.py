from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = ForeignKey(
        'auth.User', on_delete=models.CASCADE
    )
    body = models.TextField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

class Comment(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=150)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)

