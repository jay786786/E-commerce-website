from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,Orderplaced
from .forms import CustomerRegistrationForm,CUstomerProfileView
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwear=Product.objects.filter(category='TW')
        bottomwear=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category='L')
        
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            
        return render(request,'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})
    

class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False        
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))    
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('pro_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))    
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        
        amount=0.0
        shipping_charge=70.0
        total_amount=0.0
        cart_product=[p  for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quentity*p.product.discount_price)
                amount+=tempamount
                totalamount=amount+shipping_charge
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html')
        
def plus_cart(request):
    if request.method=="GET":
        pro_id=request.GET['pro_id']
        c=Cart.objects.get(Q(product=pro_id) & Q(user=request.user))    
        c.quentity +=1    
        c.save()
        
        amount=0.0
        shipping_charge=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quentity*p.product.discount_price)
            amount +=tempamount
            
            
        data={
           'quentity':c.quentity,
           'amount':amount,
           'totalamount':amount+shipping_charge
            }
            
        return JsonResponse(data)
            
def minus_cart(request):
    if request.method=="GET":
        pro_id=request.GET['pro_id']
        c=Cart.objects.get(Q(product=pro_id) & Q(user=request.user))    
        c.quentity -=1    
        c.save()
        
        amount=0.0
        shipping_charge=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quentity*p.product.discount_price)
            amount +=tempamount
            
        data={
           'quentity':c.quentity,
           'amount':amount,
           'totalamount':amount+shipping_charge
            }
            
        return JsonResponse(data)
            

def remove_cart(request):
    if request.method=="GET":
        pro_id=request.GET['pro_id']
        c=Cart.objects.get(Q(product=pro_id) & Q(user=request.user))    
        c.delete()
        
        amount=0.0
        shipping_charge=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quentity*p.product.discount_price)
            amount +=tempamount
            
        data={
        
           'amount':amount,
           'totalamount':amount+shipping_charge
            }
            
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=Orderplaced.objects.filter(user=request.user)    
    return render(request, 'app/orders.html',{'order_placed':op})


def mobile(request,data=None):
    if data ==None:
        mobiles=Product.objects.filter(category='M')
    
    elif data=='Redmi' or data=='Samsung' or data=='Apple':
         mobiles=Product.objects.filter(category='M').filter(brand=data)
    
    elif data=='below':
         mobiles=Product.objects.filter(category='M').filter(discount_price__lt=10000)
         
    elif data=='above':
         mobiles=Product.objects.filter(category='M').filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})


def topwear(request,data=None):
    if data ==None:
        topwears=Product.objects.filter(category='TW')
    
    elif data=='JackandJones' or data=='Levis':
         topwears=Product.objects.filter(category='TW').filter(brand=data)
    
    elif data=='below':
         topwears=Product.objects.filter(category='TW').filter(discount_price__lt=1000)
         
    elif data=='above':
        topwears=Product.objects.filter(category='TW').filter(discount_price__gt=1000)
    return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request,data=None):
    if data ==None:
        bottomwears=Product.objects.filter(category='BW')
    
    elif data=='Kingcopper' or data=='Raymond'or data=='levis':
         bottomwears=Product.objects.filter(category='BW').filter(brand=data)
    
    elif data=='below':
         bottomwears=Product.objects.filter(category='BW').filter(discount_price__lt=1000)
         
    elif data=='above':
        bottomwears=Product.objects.filter(category='BW').filter(discount_price__gt=1000)
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})

def laptop(request,data=None):
    if data ==None:
        laptops=Product.objects.filter(category='L')
    
    elif data=='Apple' or data=='ASUS' or data=='Dell':
         laptops=Product.objects.filter(category='L').filter(brand=data)
    
    elif data=='below':
         laptops=Product.objects.filter(category='L').filter(discount_price__lt=1000)
         
    elif data=='above':
        laptops=Product.objects.filter(category='L').filter(discount_price__gt=1000)
    return render(request, 'app/laptop.html', {'laptops':laptops})




class CustomerRegistrationView(View):
  def get(self,request):
        form=CustomerRegistrationForm()
    
        return render(request,'app/customerregistration.html',{'form':form})
 
  def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations You have Successfully Registered.")
            form.save()
    
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_charge=70.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quentity*p.product.discount_price)
            amount +=tempamount
            totalamount=amount+shipping_charge
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user,customer=customer,product=c.product,quentity=c.quentity).save()
        c.delete()
    return redirect("orders")
    
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CUstomerProfileView()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form=CUstomerProfileView(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congretulations!! Your Profie Has been Updated..")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
            
        