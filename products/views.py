from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from .forms import ContactForm,RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


# def list(request):
#     products = [
#     # الفئة 1: إلكترونيات
#     {"id": 1, "name": "MacBook Pro", "category_id": 1, "price": 2500.25, "image": "https://images.unsplash.com/photo-1517336714460-4c50d917842a?q=80&w=500"},
#     {"id": 2, "name": "iPhone 15", "category_id": 1, "price": 999, "image": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?q=80&w=500"},
#     {"id": 3, "name": "Sony Headphones", "category_id": 1, "price": 350, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=500"},
#     {"id": 4, "name": "Samsung Monitor 27'", "category_id": 1, "price": 300, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?q=80&w=500"},
    
#     # الفئة 2: ملابس
#     {"id": 5, "name": "Cotton T-shirt", "category_id": 2, "price": 25, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=500"},
#     {"id": 6, "name": "Leather Jacket", "category_id": 2, "price": 120, "image": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?q=80&w=500"},
#     {"id": 7, "name": "Blue Jeans", "category_id": 2, "price": 45, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?q=80&w=500"},
#     {"id": 8, "name": "Winter Scarf", "category_id": 2, "price": 15, "image": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?q=80&w=500"},
    
#     # الفئة 3: كتب
#     {"id": 10, "name": "Atomic Habits", "category_id": 3, "price": 22, "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=500"},
#     {"id": 11, "name": "Python Programming", "category_id": 3, "price": 40, "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=500"},
    
#     # الفئة 4: رياضة
#     {"id": 13, "name": "Adidas Football", "category_id": 4, "price": 35, "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=500"},
#     {"id": 14, "name": "Yoga Mat", "category_id": 4, "price": 20, "image": "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?q=80&w=500"},
    
#     # الفئة 5: أدوات منزلية
#     {"id": 17, "name": "Espresso Machine", "category_id": 5, "price": 150, "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?q=80&w=500"},
#     {"id": 18, "name": "Air Fryer", "category_id": 5, "price": 110, "image": "https://images.unsplash.com/photo-1626075133930-07755a50787e?q=80&w=500"},
# ]
    
   

#     cat_id=request.GET.get('category_id')

#     if cat_id:
#         filterd_products=[p for p in products  if p["category_id"]==int(cat_id)]
#     else:
#         filterd_products=products
    

#     context={
#         'prod':filterd_products
#     }

#     return render(request,'products/list.html',context)



#============== Exampe No 1 ====================
# def list(request):
#     product=Product.objects.all() #قراءة البيانات من database 

#     context={
#         "prod":product
#     }


#     return render(request,"products/list.html",context)




# def list(request):
 
#     cat_id=request.GET.get("category_id")

#     if cat_id:
#         f_product=Product.objects.filter(Category_id=cat_id)
#     else :
#         f_product=Product.objects.all()

   

#     context={
#         "prod":f_product
#     }


#     return render(request,"products/list.html",context)

def list(request):
    print(request.session['m'])
    tax=request.session['price']
    request.session['value']="welcome"
    tax=tax+(tax*(0.15))
    request.session['price']=tax
    cat_id=request.GET.get("category_id")
    user=request.COOKIES.get('user')
    print(user)
    _search=request.GET.get("search")

    products=Product.objects.all()
    if cat_id:
        f_product=Product.objects.filter(Category_id=cat_id)
    else :
        f_product=Product.objects.all()

        

    if _search:
        products=Product.objects.filter(name__icontains=_search)

    context={
        "prod":products,
        
       
    }

    
    return render(request,"products/list.html",context)



def product_details(request,product_id):

    product = get_object_or_404(
        Product.objects.select_related('details'),
        id=product_id
    )
    print(Product)

    context={
        "product":product
    }

    return render(request,"products/product_info.html",context)

def cart_view(request):
    cart=request.session.get('cart',{})  # جلب المنتجات 
    context={
        "cart":cart
    }
    return render(request,"products/cart.html",context)

@login_required
def checkout(request):
    
    return render(request,"products/checkout.html")

def send_email(request,email):
    send_mail(
        'شركة المنار للتسويق الإليكتروني',
        'تم استلام بريدك الإليكتروني وسيم معالجة طلبك خلال ثلاثة ايام عمل شكراً لتواصلكم',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False

    )



















def add_to_cart(request,pid):
   
    prod = get_object_or_404(Product, pk=pid)

    cart=request.session.get('cart',{})  # جلب المنتجات 
   
    #product_id=str(Product.id)

    if pid in cart:
        cart[pid]['quantity'] +=1
    else:
        cart[pid]={
            'id': pid,
            'name': prod.name,
            'price': float(prod.price),
            'quantity':1

        }

    request.session['cart']=cart
    
    counter=request.session.get('cart_count',0)
    counter +=1
    request.session['cart_count']=counter
    return redirect(request.META.get('HTTP_REFERER', '/')) 


def auth_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("checkout")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})




def register(request):
    pass

def contact(request):
    form=ContactForm()
    
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
           email=form.cleaned_data['email']
           send_email(request,email)
           # حفظ البيانات في الجدول 
           messages.success(request, 'تم إرسال رسالتك بنجاح! شكراً لتواصلك معنا.')
           messages.success(request, 'سعداء لتواصلك معنا ')
           return render(request,'contact.html',{'form':ContactForm(),
                'success':True
                })
        else:
             messages.error(request, 'يرجى التأكد من صحة البيانات المرسلة ')
        

        form=ContactForm()

    return render(request,'contact.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect("/")


def auth_register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("list")
    else:
        form=RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

    


