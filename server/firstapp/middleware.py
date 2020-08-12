import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


class Cors:
      def __init__(self,get_response):
           self.get_response=get_response

      def __call__(self,request):

          response=self.get_response(request)
          response['Access-Control-Allow-Origin']="*"
          response['Access-Control-Allow-Methods']="GET, POST, PUT, DELETE"
          response['Access-Control-Allow-Headers']="Content-Type,Auth,Content-Length"
          response['Content-Type']="application/json;charset=utf-8"

          return response


      def process_template_response(self,request,response):
          response.context_data['isinstance']=isinstance
          response.context_data['str']=str
          response.context_data['len']=len
          response.context_data['str']=str
          response.context_data['list']=list
          response.context_data['enumerate']=enumerate

          return response


      def process_view(self,request, view_func, view_args, view_kwargs):
              
          auth=request.headers.get('Auth')

          try:
                auth=json.loads(auth)

                if not auth.get('username') or not auth.get('password'):
                     raise SyntaxError()
                
          except Exception:
                pass
          else:
                user=authenticate(username=auth.get('username'),password=auth.get('password'))

                if user is not None:
                     login(request,user)

          return None

