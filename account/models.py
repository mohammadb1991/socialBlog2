from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class profilee(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.PositiveSmallIntegerField(null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    phone=models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.user}"

@receiver(post_save,sender=User)
def profileCreate(sender,**kwargs):
    if kwargs['created']:
        p1=profilee(user=kwargs['instance'])
        p1.save()


class Relation(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-created',)

    def __str__(self):
        return f"{self.from_user} following {self.to_user}"


# post_save.connect(profileCreate,sender=User)

# Create your models here.
