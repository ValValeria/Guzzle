from json import dumps

class Response:

    def __init__(self,messages=[],status="Not Added",errors=[]):
            self.messages=messages
            self.status=status
            self.errors=errors
   
    def toJson(self,obj):
            return dumps(self.__dict__)