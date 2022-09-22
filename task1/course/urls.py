from django.urls import path
from .views import *

urlpatterns = [path("", Course.as_view()), path("<str:id>", Course.as_view())]
