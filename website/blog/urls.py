from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('test/', test),
    path('api-auth/', include('rest_framework.urls'))
]