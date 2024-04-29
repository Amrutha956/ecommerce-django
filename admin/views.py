
# Create your views here.
from django.shortcuts import render,redirect
from store.models import Product
from django.contrib.auth import authenticate,login,logout
from accounts.models import Account
from category.models import Category
from store.models import Product
from .forms import UserForm,CategoryForm,ProductForm
from django.contrib.auth.decorators import login_required



@login_required
def cadmin(request):
   if request.user.is_admin:
        return render(request,'admin/home.html')
   else:
       return redirect('home')


#list users

def user_list(request):

    records=Account.objects.filter(is_admin = False)
    mydict={'records':records}
    return render(request,'admin/userlist.html',context=mydict)

def block_user(request,id):
    rec = Account.objects.get(id=id)
    rec.is_active = False
    rec.is_blocked = True
    rec.save()
    return redirect('userlist')

def unblock_user(request,id):
    rec = Account.objects.get(id=id)
    rec.is_active = True
    rec.is_blocked = False
    rec.save()
    return redirect('userlist')


#list categories
def category_list(request):
    records=Category.objects.all()
    mydict={'records':records}
    return render(request,'admin/categorylist.html',context=mydict)

def addcategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorylist')
    else:
        
      return render(request,'admin/addcategory.html',{'form' : form })
    
    
    
    
    
    
    
    #mydict={}
    #form=CategoryForm(request.POST or None , request.FILES or None)
    #if form.is_valid():
     #   form.save()
      #  return redirect('/')

    #mydict['form']=form
    #return render(request,'ecommerce/addcategory.html',mydict)

def editcategory(request,pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categorylist')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/editcategory.html', {'form': form,'category':category})

    
    
    
    
    
    #one_rec=Category.objects.get(pk=id)
    #form=CategoryForm(request.POST or None,request.FILES or None, instance=one_rec)
    #if form.is_valid():
     #   form.save()
      #  return redirect('/')
    #mydict= {'form':form}
    #return render(request,'ecommerce/editcategory.html',context=mydict)

def deletecategory(request,pk=None):
    Category.objects.get(pk=pk).delete()
    return redirect('categorylist')
    
    
    
    
    
    #one_rec = Category.objects.get(pk=eid)
    #if  request.method=="POST":
     #    one_rec.delete()
      #   return redirect('/')
    #return render(request,'ecommerce/deletecategory.html',{'one_rec': one_rec})

def viewcategory(request,eid=None):
    mydict={}
    one_rec = Category.objects.get(pk=eid)
    mydict['user']=one_rec
    return render(request,'admin/viewcategory.html',mydict)


#list products
def product_list(request):
    records=Product.objects.all()
    mydict={'records':records}
    return render(request,'admin/productlist.html',context=mydict)

def addproduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productlist')
    else:
        form = ProductForm()
    return render(request,'admin/addproduct.html',{'form' : form })
    
    

def editproduct(request,pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productlist')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/editproduct.html', {'form': form,'product':product})

def deleteproduct(request,pk=None):
    Product.objects.get(pk=pk).delete()
    return redirect('productlist')



