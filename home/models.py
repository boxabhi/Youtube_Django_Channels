from django.db import models
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
# Create your models here.


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    image = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = (
    ("Order Recieved", "Order Recieved"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Order recieved", "Order recieved"),
    
    
    
    
)
    
class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100 , blank=True)
    amount = models.IntegerField(default=100)
    status = models.CharField(max_length=100 , choices = CHOICES , default="Order Recieved")
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):  
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order, self).save(*args, **kwargs) 


    @staticmethod
    def give_order_details(order_id):
        instance = Order.objects.filter(order_id=order_id).first()
        data  = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['date'] = str(instance.date)
        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for delivery':
            progress_percentage = 80
        elif instance.status == 'Order recieved':
            progress_percentage = 100
            
        data['progress'] = progress_percentage
        
        return data
        
    
    def __str__(self):
        return self.order_id


@receiver(post_save, sender=Order)
def order_status_handler(sender, instance,created , **kwargs):
    
    if not created:
        print("###################")
        channel_layer = get_channel_layer()
        data  = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['date'] = str(instance.date)
        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for delivery':
            progress_percentage = 80
        elif instance.status == 'Order recieved':
            progress_percentage = 100
    
        
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )
        
        
    
    
    
# @receiver(post_save, sender=Order)
# def order_handler(sender , instance,created,**kwargs): 
#     if created :
#         channel_layer = channels.layers.get_channel_layer()
#         data = {}
#         data['order_id'] = instance.order_id
#         data['amount'] = instance.amount
#         data['status'] = instance.status
#         data['date'] = str(instance.date)
#         async_to_sync(channel_layer.group_send)(
#             'order_data',{
#                 'type': 'send_order',
#                 'value': json.dumps(data)
#             }
#         )