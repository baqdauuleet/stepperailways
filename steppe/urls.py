"""
URL configuration for steppe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name='index'),
    path("index", views.index, name='index'),
    path("about", views.about, name='about'),
    path("contacts", views.contacts, name='contacts'),
    path("registration", views.RegisterUser.as_view(), name='registration'),
    path("login", views.LoginUser.as_view(), name='login'),
    path('success_form/', views.success_form, name='success_form'),
    path('find_trains/', views.find_trains, name='find_trains'),
    path('buy_ticket/<int:train_id>/', views.buy_ticket, name='buy_ticket'),
    path('payment/test/', views.payment_test, name='payment_test'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('reviews/', views.reviews, name='reviews'),
    path('logout/', views.logout_user, name='logout'),
    path("create/", views.create, name='create'),
    path('delete/<int:rid>/', views.delete, name='delete'),
    path('select_wagon/', views.select_wagon, name='select_wagon'),
    path('question_save/', views.question_save, name='question_save'),
]
