from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib.auth.decorators import login_required
import pycountry
import re
import random
from .utils import get_current_date_and_time

import smtplib
import imghdr
from email.message import EmailMessage

# Create your views here.

EMAIL_HOST_USER = "opanahub@gmail.com"
EMAIL_HOST_PASSWORD = "sxsodrjxlyqczlqy"


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        # Authenticate the user
        auth_user = auth.authenticate(username=username, password=password)
        
        if auth_user is not None:
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Retrieve email from authenticated user
            email = auth_user.email

            msg = EmailMessage()
            msg['Subject'] = "A New Login Detected."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = email
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">{username}</b>, we have detected a new login to your account on GCTrade</p>
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            # Send the email
            smtp.send_message(msg)

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
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            msg = EmailMessage()
            msg['Subject'] = "Welcome To GCTrade"
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = email


            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize;">{username}</b>, welcome to GCTrade</p>
                        <small style=" color:#646060c7">Ready for a whole new way of trading unsed Gift Cards for money?</small>
                    </div>

                        <b style="font-style: oblique; font-size:1.2rem;  color:#646060c7;">💸💰We give you 60$ free for registration, which you can withdraw when you make a deposite.💰💸</b><br><br><br>
                        <a href="http://gctraders.pythonanywhere.com" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">Redeem Cash 💸</a>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")
            smtp.send_message(msg)
            # Close the SMTP connection
            smtp.quit()
           
            
            # Establish SMTP connection
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            msg = EmailMessage()
            msg['Subject'] = "A New Registered Account."
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = "gctrade7@gmail.com"
            msg.add_alternative(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>

                    <div style="margin-bottom: 3rem;">
                        <p>Username: <b style="color: #FFD700; text-transform: capitalize;">{username}</b></p>
                        <p>Email: <b style="color: #FFD700; text-transform: capitalize;"{email}</b></p>
                        <p>Number: <b style="color: #FFD700; text-transform: capitalize;">{number}</b></p>
                        <p>Country: <b style="color: #FFD700; text-transform: capitalize;">{country}</b></p>
                    </div>

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>

                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
            """, subtype="html")

            smtp.send_message(msg)
            # Close the SMTP connection
            smtp.quit()

            
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
        status = "Pending"
        
        # Establish SMTP connection
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = "Thank you for your purchase! Finish with the payment."
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = email
        msg.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>
                    
                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize; text-align:left;">{request.user}</b>,</p>
                        <p>Your order has been received, your tracking number will be sent once payment has been made. Thank you!</p>
                        <a href="http://gctraders.pythonanywhere.com" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">View your order 💸</a>
                    </div>

                    <h3>Order Summary</h3>
                        <b>{giftCardType.capitalize()} {otherGiftCardType.capitalize()}</b> x 1 <br><br>
                        <b>Amount in ${giftCardAmount}</b><br><br>
                        <b>Amount in GHC {payoutDetails}</b><br><br>
                        <b>Taxes  (1%):</b> USD$0.10<br><br>
                        <b>Status: </b>{status} <br><br>

                        <b>Total amount : GHC {payoutDetails}</b><br><br>
                        <hr>

                        

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>
                        
                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
        """, subtype="html")

        smtp.send_message(msg)
            # Close the SMTP connection
        smtp.quit()
        
        
        
        
        buy = UserSellorBuy.objects.create(
            user = profile,
            email=email,
            giftCardType=giftCardType,
            otherGiftCardType=otherGiftCardType,
            amount = payoutDetails,
            giftCardAmount=giftCardAmount,
            trans_type=trans_type,
            status = status,
            
        )
        
        buy.save()
        return redirect('verify_payment')
        
        
    else:
        return render(request, 'buy.html', context)
        
        
@login_required(login_url='/')   
def verify_payment(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    sell = UserSellorBuy.objects.filter(user=profile)
    
    context = {
        'profile': profile,
        'sell': sell,
    }
    
    if request.method == 'POST':
        provider = request.POST.get('giftCardType')
        image = request.FILES.get('giftCardImage')
        
        if not image:  # Check if image is provided
            messages.error(request, "Please upload a gift card image.")
            return redirect('makepayment')  # Redirect to the payment page
            
        new_payment = Payments.objects.create(
            user=profile,  # Assign the logged-in user directly
            momo_provider=provider,
            image=image
        )

        # Establish SMTP connection
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = "Payment Received, Verifying Payment!"
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = profile.user.email
        
        # Add HTML content to the email message
        msg.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>
                    
                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize; text-align:left;">{user}</b>,</p>
                        <p>Your Payments has been received, your tracking number will be sent once payment has been verified. Thank you!</p>
                        <a href="http://gctraders.pythonanywhere.com" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">View your order 💸</a>
                    </div>

                    <h3>Payments Done, Verifying please!</h3>
                        
                        <b style="text-transform: capitalize;">Provider: {provider}</b><br><br>
                        <hr>

                        

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>
                        
                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
        """, subtype="html")
        
        smtp.send_message(msg)
        
        
        
        # Establish SMTP connection
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = "Payment Received, Check Payment!"
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = 'gctrade7@gmail.com'
        
        # Add HTML content to the email message
        msg.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Message</title>
            </head>
            <body>
                <div class="cont"
                
                style="
                background: rgba(0, 0, 0, 0.089);
                padding:  1rem;
                padding-top: 4rem;
                text-align: center;
                ">
                    <div class="log" style=" margin-bottom: 4rem;">
                        <a href="http://gctraders.pythonanywhere.com" 
                        style="
                        text-decoration: none;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #000000;"><span style="color: #FFD700;">GC</span>Trade</a>

                    </div>
                    
                    <div style="margin-bottom: 3rem;">
                        <p>Hello <b style="color: #FFD700; text-transform: capitalize; text-align:left;">Admin</b>,</p>
                        <p>A Payments has been received, please confirm, Thank you!</p>
                    </div>

                    <h3 style="text-transform: capitalize;">Payment from {profile.user}</h3>
                        
                        <b style="text-transform: capitalize;">Username: {profile.user}</b><br><br>
                        <b style="text-transform: capitalize;">Provider: {provider}</b><br><br>
                        
                        <a href="http://127.0.0.1:8000/admin/gctrade/payments/" style="margin-top: 1rem; text-decoration: none;background:#FFD700; width:10rem; border-radius: 1rem; padding:.5rem; text-align:center; color:#000000; font-weight:900">Check here</a><br><br><br>
                        
                        <hr>

                        

                        <p style="margin: 2rem 0; font-size: 1rem;  color:#646060c7">Weare a vibrant community of gift card enthusiasts providing a platform to buy and sell gift cards with ease.</p>
                        
                    
                            <strong style=" color:#646060c7">Locate Us</strong><br>
                            <b>12345 Kaohsiung city, Taiwan</b><br><br>

                            <strong style=" color:#646060c7">Phone</strong><br>
                            <b>+1 8374858098459</b><br><br>

                            <strong style=" color:#646060c7">Email</strong><br>
                            <a href="mailto:info@gctrade.com" style="color: #000000;">info@gctrade.com</a>

                        <p style="font-size: 1.2rem; color:#646060c7;">GCTrade, All rights reserved.</p>
                </div>
            </body>
            </html>
        """, subtype="html")
        
        smtp.send_message(msg)

        new_payment.save()
        return redirect('transactions')
    
    return render(request, 'makepayment.html', context)


    
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
    
    
    
@login_required(login_url='/')
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


# def makepayment(request):
#     user = User.objects.get(username=request.user)
#     profile = Profile.objects.get(user=user)
    
#     context={
#         'profile' : profile,
#     }
#     return render(request, "makepayment.html", context)