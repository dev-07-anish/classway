from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('bypass/', views.home_page_bypass, name="home_page_bypass"),

    path('home/', views.home_page, name="home_page"),

    # path('about/', views.about_page, name="about_page"),
    path('faq/', views.faq_page, name="faq_page"),
    path('register/', views.register_page, name="register_page"),
    path('login/', views.login_page, name="login_page"),

]
