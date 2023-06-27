from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.create_view,name="create_view"),
    path('home/',views.home_view,name="home_view"),
    path('myform/',views.myform_view,name="myform_view"),
    path('chatbot/',views.chatbot_view,name="chatbot_view"),
]
