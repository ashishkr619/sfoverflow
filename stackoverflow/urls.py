
from django.contrib import admin
from django.urls import path,include
from question import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('question.urls'),name='question'),

]
