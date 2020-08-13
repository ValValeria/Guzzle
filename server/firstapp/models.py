from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User



class Post(models.Model):
    title = models.CharField(max_length=20)
    img = models.ImageField(upload_to="img")
    descr = models.CharField(max_length=300)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    price= models.IntegerField(default=0)

    @property
    def orderCount(self):
       return self.order_set.count()


class Comments(models.Model):
    content = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    replyWhom = models.IntegerField()
    post = models.ForeignKey(Post,on_delete=models.DO_NOTHING)

class Order(models.Model):
    quantity=models.IntegerField(default=1)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ManyToManyField(Post)
