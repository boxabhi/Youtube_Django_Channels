from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse


# Create your views here.


def home(request):
    pizza = Pizza.objects.all()
    context = {'pizza' : pizza}
    return render(request, 'index.html', context)

def order(request , order_id):
    order = Order.objects.filter(order_id=order_id).first()
    
    if order is None:
        return redirect('/')
    
    context = {'order' : order}
    return render(request , 'order.html', context)
    

def order_pizza(request):
    user = request.user
    data = json.loads(request.body)
    try:
        pizza =  Pizza.objects.get(id=data.get('pizza_id'))
        order = Order(user=user, pizza=pizza , amount = pizza.price)
        order.save()
    except Pizza.DoesNotExist:
        return JsonResponse({'error': 'Something went wrong'})
    
    