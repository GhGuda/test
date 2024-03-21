from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib.auth.decorators import login_required
import pycountry, re, random, requests, json, base64
from django.conf import settings
from .utils import get_current_date_and_time

# Create your views here.

API_KEY_USERNAME = '65e89d55d06c990c64ae8c56'
API_KEY_PASSWORD = 'puNtpe7ChJaWTvuvi4BetArB'

url = "https://live.waypointapi.com/v1/email_messages"





def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        # Authenticate the user
        auth_user = auth.authenticate(username=username, password=password)
        
        if auth_user is not None:
            auth.login(request, auth_user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('index')
        
    return render(request, 'index.html')



def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    all_countries = list(pycountry.countries)
    country_names = [country.name for country in all_countries]
    if request.method == "POST":
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        number = request.POST['number']
        country = request.POST['country']

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, "Username can only contain letters, numbers, and underscores!")
            return redirect('register')
        
        elif username.isdigit(): 
            messages.error(request, "Username cannot consist of only numbers!")
            return redirect('register')
        
        elif len(username) <= 0:
            messages.error(request, "Enter username!")
            return redirect('register')
        
        elif ' ' in username:
            messages.error(request, "Username cannot contain spaces, can only contain letters, numbers, and underscores!")
            return redirect('register')
        
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username taken!")
            return redirect('register')
        
        elif password == username:
            messages.error(request, "Password similar to username!")
            return redirect('register')
        
        elif len(email) <= 0:
            messages.error(request, "Enter email!")
            return redirect('register')
        
        elif len(password) < 8:
            messages.error(request, "Password is weak, enter strong password!")
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email taken!")
            return redirect('register')
        elif password != password2:
            messages.error(request, "Password doesn't match")
            return redirect('register')            
        else:
            
            # headers = {
            #     "Content-Type": "application/json"
            # }
            # auth =( API_KEY_USERNAME, API_KEY_PASSWORD)

            
            # data ={
            #     "templateId": "wptemplate_9dYCukUBxFiUVGKV",
            #     "to": email,
            #     # "from":"toyboipressure1@gmail.com",
                
                
            #     "variables":{
            #         "displayName": username.capitalize(),
            #     }
            # }
            
            # response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
            # print(response.text)
            
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            
            profile = Profile.objects.create(user=new_user, country=country, mobile_number=number)
            profile.save()
            
            return redirect('home')
    context ={
        'country_names': country_names,
    }

    return render(request, 'register.html', context)
    
    
@login_required(login_url='/')
def home(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    current_datetime = get_current_date_and_time()
    
    card = list(GiftCard.objects.all())
    random.shuffle(card)
    context ={
        'profile' : profile,
        'card' : card,
        'time' : current_datetime,
    }
    

    return render(request, 'main.html', context)


@login_required(login_url='/')
def dashboard(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
   
    context ={
        'profile' : profile,
        'sell' : sell,
    }
    

    return render(request, 'dashboard.html', context)


@login_required(login_url='/')
def wallet(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
   
    context ={
        'profile' : profile,
        'sell' : sell,
    }
    

    return render(request, 'wallet.html', context)

@login_required(login_url='/')
def sell(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    context ={
        'profile' : profile,
        # 'card' : card,
    }

    if request.method == 'POST':
        name = request.POST.get('giftCardType')
        ecode = request.POST.get('giftCardECode')
        amount = request.POST.get('giftCardAmount')
        payment_method = request.POST.get('paymentMethod')
        account_number = request.POST.get('accountNumber')
        bank_name = request.POST.get('bank_name')
        momo_provider = request.POST.get('momoProvider')
        momo_number = request.POST.get('momoNumber')
        image_files = request.FILES.getlist('giftCardImage')

        user_sell = UserSellorBuy.objects.create(
            user=profile,
            gift_card_name=name,
            ecode=ecode,
            giftCardAmount=amount,
            amount=amount,
            payment_method=payment_method,
            bank_name=bank_name,
            bank_account_number=account_number,
            momo_number=momo_number,
            momo_provider=momo_provider,
            trans_type="Sold",
            status="Processing",
        )
        
        for image_file in image_files:

            UserSellImage.objects.create(
                user=user_sell,
                image=image_file,
            )
            
        headers = {
                "Content-Type": "application/json"
            }

        # Now you can include the base64 string in your JSON payload
        data ={
            "templateId": "wptemplate_tdAf64tArhaG2WPC",
            "to": 'gctrade7@gmail.com',
            "variables":{
                    "seller": {
                        "displayName": "Hi, Admin"
                    },
                    "item": {
                        "brand": name,
                        "title": name,
                        "price": "$"+amount,
                        "link": "#"
                    }
                }
        }
        
        auth =( API_KEY_USERNAME, API_KEY_PASSWORD)
            
        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
        print(response.text)
        
        return redirect('transactions') 
    else:
        return render(request, 'sell.html', context)



@login_required(login_url='/')
def buy(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    context ={
        'profile' : profile,
        # 'card' : card,
    }
    
    if request.method == "POST":
        email = request.POST.get('email')
        giftCardType = request.POST.get('giftCardType')
        otherGiftCardType = request.POST.get('otherGiftCardType')
        giftCardAmount = request.POST.get('giftCardAmount')
        payoutDetails = request.POST.get('payoutDetails')
        trans_type = "Bought"
        
        buy = UserSellorBuy.objects.create(
            user = profile,
            email=email,
            giftCardType=giftCardType,
            otherGiftCardType=otherGiftCardType,
            amount = payoutDetails,
            giftCardAmount=giftCardAmount,
            trans_type=trans_type,
            status = "Processing",
        )
        buy.save()
        headers = {
                "Content-Type": "application/json"
            }
        
        data ={
            "templateId": "wptemplate_pdjcHiAkWYrJ3LAF",
            "to": email,
            # "from":"toyboipressure1@gmail.com",
                
            "variables":{
                    "store": {
                        "name": "GCTrade"
                    },
                    "order": {
                        "id": "103571871",
                        "customer": {
                            "displayName": request.user.username.upper()
                        },
                        "lineItems": [
                        {
                            "productName": giftCardType+otherGiftCardType, 
                            # "thumbnailUrl": "https://assets.usewaypoint.com/pen.jpg",
                            "qty": "1",
                            "variant": trans_type,
                            "originalPrice": "$"+giftCardAmount,
                            "price": "GHc"+payoutDetails,
                        },
                
                        ],
                    
                        "subtotal": "GHc"+payoutDetails,
                        "taxes": "GHc 0.00",
                        "total": "GHc"+payoutDetails,
                    }
                }  
            
        }
        auth =( API_KEY_USERNAME, API_KEY_PASSWORD)
        
        
        
        
        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
        print(response.text)
        
        return render(request, 'makepayment.html', {'pay':buy, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        return render(request, 'buy.html', context)
        
        
        
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(UserSellorBuy, ref=ref)
    verified = payment.verify_payment()
    
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification failed")
        
    return redirect('transactions')
    
@login_required(login_url='/')
def transactions(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
    context={
        'profile' : profile,
        'sell' : sell,
    }
    
    return render(request, 'transaction.html', context)
    
    
    
    
def setting(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    
    if request.method == 'POST':
        if request.FILES.get('giftCardImage') == None:
            profile_img = profile.profile_img
            name = request.POST['username'].lower()
            email = request.POST['email']

            profile.profile_img = profile_img
            user.username = name
            user.email = email
            profile.save()
            user.save()
            return redirect('setting')
        

        if request.FILES.get('giftCardImage') != None:
            profile_img = request.FILES.get('giftCardImage')
            name = request.POST['username'].lower()
            email = request.POST['email']

            profile.profile_img = profile_img
            user.username = name
            user.email = email
            profile.save()
            user.save()
            return redirect('setting')
    
    context={
        'profile' : profile,
    }
    
    
    return render(request, "settings.html", context)


def makepayment(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    
    context={
        'profile' : profile,
    }
    return render(request, "makepayment.html", context)