from django.contrib import admin
from django.urls import path
from . import views






app_name = "user"

urlpatterns = [
    #enterpriseuser
    path('ent_register/', views.enterpriseRegister, name="ent_register"),
    path('mail_control/<str:uid>/<str:token>', views.mail_control, name="mail_control"),

    #personaluser
    path('per_register/', views.personalRegister, name="per_register"),

    path('enterpriseuser_account/', views.enterpriseuser_account, name="enterpriseuser_account"),
    path('enterpriseuser_settings/', views.enterpriseuser_settings, name="enterpriseuser_settings"),
    path('enterprisepassword_change/', views.enterprisepassword_change, name="enterprisepassword_change"),


    path('personaluser_account/', views.personaluser_account, name="personaluser_account"),
    path('personaluser_settings/', views.personaluser_settings, name="personaluser_settings"),
    path('personalpassword_change/', views.personalpassword_change, name="personalpassword_change"),

    
    path('logout/', views.logoutUser, name="logout"),
]
