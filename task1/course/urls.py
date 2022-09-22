from django.urls import path
from .views import *

urlpatterns = [path("", Course.as_view()), path("<str:id>", SingleCourse.as_view())]
