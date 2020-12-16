
from django.urls import path, include
from .views import *


urlpatterns = [
    path('' ,home, name='home' ),
    path('<order_id>/' , order , name='order')
]
