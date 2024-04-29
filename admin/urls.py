from django.urls import path
from . import views



urlpatterns = [
path('',views.cadmin,name='cadmin'),
    

    #list users
    path('cadmin/list', views.user_list,name='userlist'),
    path('cadmin/block/<id>', views.block_user,name='blockuser'),
    path('cadmin/unblock/<id>', views.unblock_user,name='unblockuser'),
    

    #list categories
    path('cadmin/category', views.category_list,name='categorylist'),
    path('cadmin/category/add/', views.addcategory,name='addcategory'),
    path('cadmin/category/edit/<pk>', views.editcategory,name='editcategory'),
    path('cadmin/category/delete/<pk>', views.deletecategory,name='deletecategory'),
   
   

   #list products
    path('cadmin/products', views.product_list,name='productlist'),
    path('cadmin/products/add/', views.addproduct,name='addproduct'),
    path('cadmin/products/edit/<pk>', views.editproduct,name='editproduct'),
    path('cadmin/products/delete/<pk>', views.deleteproduct,name='deleteproduct'),
    

]