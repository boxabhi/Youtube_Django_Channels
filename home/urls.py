
from django.urls import path, include
from .views import *


urlpatterns = [
    path('' ,home, name='home' ),
    path('api/order' , order_pizza , name='order_pizza'),
    path('<order_id>/' , order , name='order')
]
