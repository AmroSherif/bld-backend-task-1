from django.urls import path
from .views import *

urlpatterns = [path("", User.as_view()), path("<str:id>", SingleUser.as_view())]
