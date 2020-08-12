from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from firstapp.models import Post


class Authenticate(forms.Form):
     username=forms.CharField(max_length=30,min_length=10)
     password=forms.CharField(max_length=20,min_length=6)

     def clean_username(self):
          user=User.objects.filter(username__exact=self.cleaned_data.get('username'))
          if not user.exists():
                self.add_error("username","We can't find you in our database")
          else :
               self.cleaned_data['user_m']=user.first()
               


class SignUpForm(forms.Form):
     email=forms.EmailField(max_length=30,min_length=10)
     username=forms.CharField(max_length=30,min_length=10)
     password=forms.CharField(max_length=20,min_length=6)

     def clean(self):
          user=User.objects.filter(email=self.cleaned_data.get('email')).filter(username=self.cleaned_data.get('username'))
          if user:
             self.add_error("email","The user with such email or name has already existed in our database")



class AddPostForm(forms.Form):
     title=forms.CharField(max_length=20)
     img=forms.ImageField()
     descr=forms.CharField(max_length=300)


class AddCommentForm(forms.Form):
     content = forms.CharField(max_length=100)
     post_id=forms.IntegerField(max_value=4000)

     def clean_post_id(self):
        post_id=self.cleaned_data['post_id']
        post=Post.objects.filter(id__exact=post_id)
        self.cleaned_data['post']=post.first()

        if not post.exists():
             self.add_error('content',"The post doesn't exist")
            
