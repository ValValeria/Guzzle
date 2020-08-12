from django.http import FileResponse
import os
from django.http import HttpResponseNotFound,HttpResponse

dirn = os.path.dirname(os.path.dirname(__file__))



def file(request,folder,filename):
    
    filepath=os.path.join(os.path.join(dirn,'public'),folder,filename)

    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'))
    else:
        return HttpResponse(filepath)