
from django.urls import path
from . import views

urlpatterns = [
    
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('otp/',views.otp,name='verify_otp'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    
    
    path('myorders/',views.myorders,name='myorders'),
    
    
    
    

]
