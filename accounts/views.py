from django.shortcuts import render,redirect,get_object_or_404
from .utils import generate_otp, send_otp_email
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from orders.models import Order
from cart.views import _cart_id
from cart.models import Cart,CartItem
import requests




# Create your views here.
@never_cache
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            request.session['email'] = email

            otp = generate_otp()

            # Store OTP in session
            request.session['otp'] = otp
            send_otp_email(email, otp)
            messages.success(request,'Registration successful.An OTP has been sent to your registered email')
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request,'accounts/register.html',context)


@never_cache
def login(request):
    if request.user.is_authenticated:
         return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        value = Account.objects.get(email=email)
        
        user = auth.authenticate(email=email,password=password)
        if value.is_blocked :
             messages.error(request,'User is blocked !')
             return redirect('login')
        elif user is not None:
                try:
                    
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        #Getting product variation
                        product_variation = []
                        for item in cart_item:
                             variation = item.variations.all()
                             product_variation.append(list(variation))
                        
                        #Get the cart item from the user to access his products
                        cart_item = CartItem.objects.filter( user=user)

                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        for pr in product_variation:
                            if pr in ex_var_list:
                                  index =ex_var_list.index(pr)
                                  item_id = id[index]
                                  item = CartItem.objects.get(id=item_id)
                                  item.quantity +=1
                                  item.user = user
                                  item.save()
                            else:
                                 cart_item = CartItem.objects.filter(cart=cart)
                                 for item in cart_item:
                                    item.user = user
                                    item.save()
                            
                             
                except:
                    
                    pass
            
                auth.login(request,user)
                request.session['user_id'] = user.id 
                
                
                #messages.success(request,'You are now logged in')
                url = request.META.get('HTTP_REFERER')
                try:
                   query = requests.utils.urlparse(url).query
                   params = dict(x.split('=') for x in query.split('&'))
                   if 'next' in params:
                       nextPage = params['next']
                       return redirect(nextPage)
                       
                   
                except:
                   return redirect('home')
        
        else:
                messages.error(request,'Invalid login credentials')
                return redirect('login')

    return render(request,'accounts/login.html')

@never_cache
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    request.session.flush()  
    messages.success(request,'You are logged out')
    return redirect('login')

def otp(request):
    if request.method == 'POST':
        # Get the OTP stored in the session during registration
        stored_otp = request.session.get('otp')
        
        # Get the entered OTP from the form
        entered_otp = request.POST.get('otp')

        if stored_otp == entered_otp:
            # OTP is correct, activate user and redirect to home page
            email = request.session.get('email')
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully!')
            return redirect('login')
        else:
            # OTP is incorrect, render the OTP verification page again
            messages.error(request,'OTP ENTERED IS WRONG!!!')
            return render(request, 'accounts/otp.html')
    else:
        # If the request method is not POST, render the OTP verification page
        return render(request, 'accounts/otp.html')

@login_required(login_url='login')
def dashboard(request):
     orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id,is_ordered = True)
     orders_count = orders.count()
     context ={
          'orders_count' : orders_count,
             }
     
     return render(request,'accounts/dashboard.html',context)

def myorders(request):
     return render(request,'accounts/myorders.html')