from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField(max_length=500)
    slug=models.SlugField(max_length=200,allow_unicode=True)
    created=models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.pvoted.count()

    def user_can_like(self,user):
        like=user.uvoted.all()
        qs=like.filter(post=self)
        if qs.exists():
            return True
        else:
            return False

    def __str__(self):
        return f'{self.body}'

    def get_absolute_url(self):
        return reverse('posts:post_detail',args=[self.created.year,self.created.month,self.created.day,self.created.second])


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomment')
    post=models.ForeignKey(post,on_delete=models.CASCADE ,related_name='pcomment')
    reply=models.ForeignKey('self',on_delete=models.CASCADE , null=True , blank=True,related_name='rcomment')
    is_reply= models.BooleanField(default=False)
    body=models.TextField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}  |||    {self.body[:10]}...'

    class Meta:
        ordering=('-created',)


class Voted(models.Model):
    post=models.ForeignKey(post,on_delete=models.CASCADE, related_name='pvoted')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvoted')

    def __str__(self):
        return f'{self.user} like             {self.post.slug}'