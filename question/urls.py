from django.contrib import admin
from django.urls import path
from question import views

app_name ='question'

urlpatterns = [
    # path('', admin.site.urls),
    path('', views.question,name='home'),
    # path('active/', views.active,name='active'),
]
