from firstapp.models import Order
import django.dispatch
from django.core.mail import send_mail

order_add=django.dispatch.Signal(providing_args=("post","email","num",))

def sendEmail(sender,**kw):
    data=''
    send_mail("Ваш товар добавлен в корзину",'Ваш товар "'+kw['post'].title+'" добавлен в корзину . Число товаров равно'+str(kw['num']),"admiadmin@g.com",[kw['email']],fail_silently=False)

order_add.connect(receiver=sendEmail,sender=Order)