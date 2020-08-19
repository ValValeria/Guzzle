from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseForbidden
from firstapp.response import Response
import json
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginFun
from django.contrib.auth.decorators import user_passes_test
from firstapp.form import Authenticate,SignUpForm,AddPostForm,AddCommentForm
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,FormView
from django.views import View
from django import forms
from firstapp.models import Post,Comments,Order,Category
from django.core.paginator import Paginator
from django.core.files import File
from django.core import serializers
from django.template.response import TemplateResponse
import firstapp.viewsFolder.file
from django.core import serializers



@require_http_methods(['POST','OPTIONS'])
def login(request):
    
    if request.user.is_authenticated:
        message={"status":"Added","messages":[],"errors":[]}    
    else :
        form =Authenticate(request.POST,request.FILES)
        message={"status":"","messages":[],"errors":[]}    

        if form.is_valid():
           message['status']="Added"
           loginFun(request,form.cleaned_data['user_m'])
        else:
           message['errors']=form.errors
        
    return JsonResponse(message)



@require_http_methods(['POST','OPTIONS'])
def signup(request):

          message={"status":"","messages":[],"errors":[]}   

          if request.user.is_authenticated:
              message['status']="Added"
              return JsonResponse(message)
           
          if request.content_type.count('application/json'):
              try:
                form = SignUpForm(json.loads(request.body))
              except :  pass
          else:
              form=SignUpForm(request.POST,request.FILES)

          if form.is_valid():
             user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
             user.save()
             message['status']="Added"
             message['messages'].insert(0,user.id)
             loginFun(request,user)
          else :
             message['errors']=form.errors

          return JsonResponse(message)


@method_decorator(login_required,name="post")
class AddPost(ListView):
    form=AddPostForm
    response=Response(messages=[])

    def post(self,request,*args,**kw):
         form=self.AddPostForm(request.POST,request.FILES)
        
         if form.is_valid():
             post=Post(title=form.cleaned_data['title'],img=form.cleaned_data['img'],descr=form.cleaned_data['descr'])
             post.user=request.user
             categories=request.POST.getlist('categories')

             if isinstance(categories,(tuple,list)):

                 for cat_name in categories:
                     if not  post.categories.filter(can_name=cat_name).exists():
                        post.categories.create(cat_name=cat_name)

             post.save()
             response.status="Added"
         else:
             response.status="Not Added"
             response.errors.extends(form.errors)

         return HttpResponse(json.dumps(response,default=response.toJson))





class Posts(ListView):
       
      def get_queryset(self):
          number=self.request.GET.get('page')
          page=number if number else "1"
          posts=Post.objects.all().select_related('user').order_by("id")
          paginator=Paginator(posts,5)
          self.p=paginator.page(int(page))

          allData=list()

          for key,post in enumerate(list(self.p.object_list.values())):
              post['user']={"name":posts[key].user.username,"id":posts[key].user.id}
              allData.append(post)
                
          return allData
     
      def get_context_data(self,**kw):
          context={}
          context['posts']=list(self.get_queryset())
          context['has_next']= 1 if self.p.has_next() else 0
          context['has_prev']= 1 if self.p.has_previous() else 0
          return context

      def get(self,request):
          data=json.dumps(dict(self.get_context_data()),sort_keys=False,  indent=4, ensure_ascii=False)
          return HttpResponse(data)


class PostView(DetailView):
      model=Post
      context_object_name="post"
      template_name="post.html"

      def get_context_data(self, **kwargs):
            context= super().get_context_data(**kwargs)
            return context
    
      def get(self,request,*args,**kw):
           return super().get(request,*args,**kw)



class CommentsView(DetailView):

    def get(self,request):

        post_id=request.GET.get('post_id')

        if not post_id:
            return HttpResponse('Invalid request')

        comments=Comments.objects.filter(post__id__exact=post_id).select_related('author')

        allData=list()

        for key,post in enumerate(list(comments.values())):
              post['user']={"username":comments[key].author.username,"id":comments[key].author.id}
              allData.append(post)

        data=json.dumps(allData,sort_keys=False,  indent=4, ensure_ascii=False)
        return HttpResponse(data)

    
    def post(self,request):
       
        if not request.user.is_authenticated: 
              return HttpResponse("Forbidden")

        if "application/json" in request.headers['Content-Type']:
            #json
            form = AddCommentForm(json.loads(request.body))
        else:
            form = AddCommentForm(request.POST,request.FILES)

        response={"status":"","messages":[],"errors":[]}

        if form.is_valid():
            comment=Comments(content=form.cleaned_data['content'],author=request.user,replyWhom=0,post=form.cleaned_data['post'])
            comment.save()
            response['status']="Added"
            response['messages'].insert(0,{"id":comment.id,"content":form.cleaned_data['content'],"user":{
                "username":request.user.username,
                "id":request.user.id
            }})
        else:
            response['errors']=form.errors
        
        return HttpResponse(json.dumps(response))




from django.contrib.auth.mixins import UserPassesTestMixin

class DelComment(ListView,LoginRequiredMixin):
      response={"messages":[],"status":"","errors":[]}

      def test_func(self):
          comment_id=self.request.GET.get('comment_id')
          self.comment=Comments.objects.filter(id=comment_id).first()

          if not self.comment:
              return False;
          
          isUserComment= True if self.comment.author.id==self.request.user.id else False

          return isUserComment


      def get(self,request):

          if self.test_func() or request.user.is_superuser:
              self.response['status']="Deleted"
              self.comment.delete()
          else:
              self.response['status']="Not Deleted"

          return JsonResponse(self.response)


class Search (ListView):

    def get(self,request):

        search=request.GET.get('search_query')

        if not len(search):
             return JsonResponse([],safe=False)
       
        posts=Post.objects.filter(Q(title__icontains=search)|Q(user__username__icontains=search)).select_related("user").all()

        allData=list()

        for key,post in enumerate(list(posts.values()[:5])):
              post['user']={"name":"Anonim","id":posts[key].user.id}
              allData.append(post)

        return JsonResponse(allData if allData else [],safe=False)



class UserPosts(ListView):
    
    def get(self,request):

         user_id=request.GET.get('user_id')

         if user_id:
             posts=Post.objects.select_related().filter(user__id__exact=user_id).values().order_by('id')
             list_posts=list()

             for key,item in enumerate(posts.iterator()):
                 new_val=list(posts.values)[key]
                 orders=Order.objects.filter(products__id=new_val.get('id'))
                 count=0 

                 for order in orders.iterator():
                     count+=orders.products.all().count()

                 new_val.update({"count":count})
                 list_posts.append(new_val)

             return JsonResponse(list(posts if posts else []),safe=False)
         else:
             return JsonResponse({'status':'not found'})


class DeletePost(ListView,LoginRequiredMixin):
    
    def get(self,request):
        post_id=request.GET.get('post_id')
        
        if  post_id.isdigit():

            obj=Post.objects.filter(id__exact=post_id).first()

            if obj.user.id is request.user.id or (request.user.is_superuser ):
                obj.delete()
                return JsonResponse({"status":"Deleted"})

            return JsonResponse({"status":"Not deleted","errors":['The post doesnt belong to you']})

        else:
            return JsonResponse({"error":"post_id is not specified"})
            


class UpdatePost(FormView,LoginRequiredMixin):
    response={"status":"","errors":[]}

    def post(self,request):
        form= AddPostForm(request.POST,request.FILES)
        number=request.POST.get('post_id')

        if form.is_valid() and number :

            updated=Post.objects.filter(id=number).first()

            if not updated:
                self.response['errors'].append("The required post doesn't exist")
            else:
                if request.user.id==updated.user.id or request.user.is_superuser:
                   rows=updated.update(title=form.cleaned_data['title'],img=form.cleaned_data['img'],descr=form.cleaned_data['descr'],
                   price=form.cleaned_data['price'])
                   self.response['status']="Updated" if rows else "Not updated"

        else:
            self.response['errors']=form.errors if form.errors else [{"email":"You are not authenticated  or the post doesn't belong to you ."}]

        return JsonResponse(self.response)



class UserOrders(ListView,LoginRequiredMixin):

      def get(self,request):
          user_id=request.GET.get('user_id')
          response=list()
          isUser=request.user.id == user_id

          if not user_id or isUser:
              response.append({"errors":["Invalid user_id"]})
          else:
              if not request.user.id==user_id or not request.user.is_superuser:
                    response.append({"errors":["You can see the orders of other users"]})
                    return JsonResponse(response,safe=False)

              orders=Order.objects.filter(user__id=user_id)
              
              if orders.exists():
                  products=list()

                  for key in range(0,len(orders),1):
                      try:
                          obj={"counter":orders[key].quantity}
                          obj.update(orders[key].products.values()[0])
                          products.append(obj)
                      except IndexError:
                          pass
              else:
                  products=[]

              response.extend(list(products))
            
          return JsonResponse(response,safe=False)
          
    
              
class AddOrder(ListView,LoginRequiredMixin):

    def get(self,request):

        user_id=request.GET.get('user_id')
        post_id=request.GET.get('post_id')
        num=request.GET.get('num')
        

        if user_id and post_id and int(request.user.id) == int(user_id):

            user_orders_l = Order.objects.filter(user_id=user_id)
            user_order=user_orders_l[0].products.filter(id=post_id)
            post=Post.objects.filter(id=post_id)  

            if post.exists():
                status="Added"
                if user_order.exists():
                    order=user_orders_l.first()

                    if int(num if num else "1") == 0:
                        user_orders_l[0].remove(user_order)
                        status="Deleted"
                    else:     
                        order.quantity=num
                        order.save()
                        user_orders_l[0].save()
                else:
                    new_order=Order(quantity=num);
                    new_order.user=request.user
                    new_order.save();
                    new_order.products.add(post.first())


                return JsonResponse({"status":status})
            else:
                return JsonResponse({"errors":"The post doesn't exist"})
        else :
            return HttpResponseForbidden()



class SortBy(ListView):

    def get(self,request):
        sortBy=request.GET.get('sortBy')
        page=request.GET.get('page')
        filters=['priceDesc','priceBtw',"price"]
        filter_q=request.GET.getlist('filter')
        
        if filters.count(sortBy):
            posts=Post.objects.order_by("price").all()

            if sortBy.count('Desc'):
               posts=posts.reverse()
            elif sortBy.count('Btw') and len(filter_q)==2:
               posts=posts.filter(price__gt=filter_q[0]).filter(price__lt=filter_q[1])
            
            list_new=list()

            for key,item in enumerate(posts.iterator()):
                new_item=list(posts.values())[key]
                new_item.update({"user":{"username":item.user.username}})
                list_new.append(new_item)

            return JsonResponse(list_new,safe=False)
        else:
            return HttpResponseForbidden()
    



class CategoryView(ListView):
       
       def get(self,request):
           cat_name=request.GET.get('category')
           posts=Post.objects.filter(categories__cat_name=cat_name)
           list_new = list()

           for key,item in enumerate(posts.iterator()):
                new_item=list(posts.values())[key]
                new_item.update({"user":{"username":item.user.username},"categories":list(posts[key].categories.values())})
                list_new.append(new_item)

           return JsonResponse(list(list_new),safe=False)


class CategoriesList(ListView):

       def get(self,request):
           categories=list(Category.objects.all().values())
           return JsonResponse(categories,safe=False)



class ProductsBuyers(View):
       permission_denied_message="You need to log in . By the way, the error can be caused by the permission deny. Only users who own the post can access the page"

       def has_permission(self):
           user_id=self.request.user.id;
           post_id=self.request.GET.get('post_id')
           post=Post.objects.filter(id=post_id).first() 

           if post.user.id==user_id or self.request.user.is_superuser:
               return True;

           return False;

       def get(self,request):

           if not self.has_permission():
               return JsonResponse({"error":self.permission_denied_message})

           product_id=request.GET.get('post_id')
           orders=Order.objects.filter(products__id=product_id).all().select_related()
           response=list()

           for target_list in orders.iterator():
               new_item={"user":{"username":target_list.user.username}}
               new_item.update(list(target_list.products.filter(id=product_id).all().values())[0])

               try:
                   new_item.pop('user_id')
               except KeyError:
                   pass

               new_item.update({"count":target_list.quantity})
               response.append(new_item)

           return JsonResponse(response,safe=False)



class UsersList(ListView):
    
    def get(self,request):

        if not request.user.is_superuser:
            return  HttpResponseForbidden()

        page=request.GET.get('page')
        users= list(User.objects.all().values())
        p = Paginator(users,4)
        page_item=p.page(page if page else 1)
        response={"has_next":page_item.has_next(),"has_prev":page_item.has_previous(),"data":page_item.object_list,"endindex":page_item.end_index()}
        return JsonResponse(response,safe=False)


class DeleteUser(ListView):
    
    def get(self,request):
        user_id=request.GET.get('user_id')

        if not request.user.is_superuser and not request.user.id == user_id :
            return  HttpResponseForbidden()

        user=User.objects.filter(id=user_id).first()
        response={"status":""}  

        if user:
            response['status']="Deleted"
            user.delete()

        return JsonResponse(response)   


        
