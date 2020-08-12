"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from firstapp import views
from firstapp.viewsFolder.file import file

urlpatterns = [
    
    path('admin/', admin.site.urls),
    re_path(r'^login',views.login),
    re_path(r'^signup',views.signup),
    re_path(r'^addpost',views.AddPost.as_view()),
    re_path(r"^posts",views.Posts.as_view()),
    re_path(r"^post/(?P<pk>[0-9]{0,4})",views.PostView.as_view()),
    re_path(r"^comments/",views.CommentsView.as_view()),
    re_path(r"^delcomment",views.DelComment.as_view()),
    re_path(r"^search",views.Search.as_view()),
    re_path(r"^userposts",views.UserPosts.as_view()),
    re_path(r"^deletepost",views.DeletePost.as_view()),
    re_path(r"^update_post",views.UpdatePost.as_view()),
    re_path(r"^orderproducts",views.UserOrders.as_view()),
    re_path(r"^addorderproducts",views.AddOrder.as_view()),
    path("public/<folder>/<filename>",file),
]
