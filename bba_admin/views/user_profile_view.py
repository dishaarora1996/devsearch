from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Enquiry, LocationWebsite, Employee)
import logging
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes  
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

logger = logging.getLogger(__name__)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, "Email does not exist")
            return render(request, 'login.html')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('user-login')
        
    return render(request, 'accounts/login.html')

@login_required(login_url='user-login')
def user_logout(request):
    logout(request)
    return redirect('user-login')


@login_required(login_url='user-login')
def dashboard(request):
    loc_web_count = LocationWebsite.objects.filter(status="Active", deleted=False).count()
    admin_users_count = Employee.objects.filter(status="Active").count()
    enquiry_count = Enquiry.objects.all().count()
    enquiry = Enquiry.objects.all().order_by('-id')[:10]
    context = {
        'enquiry_list': enquiry,
        'loc_web_count': loc_web_count,
        'admin_users_count': admin_users_count,
        'enquiry_count': enquiry_count
    }
    return render(request, 'dashboard.html', context)


def recover_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email, username=email).exists():
            user = User.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset Password"
            data = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            }
            message = render_to_string('accounts/reset_password_email.html', data)
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            messages.success(request,"Password reset email has been sent to your email address")
            return redirect('user-login')
        else:
            messages.error(request, "Account does not exist")
            return redirect('recover-password')
        
    return render(request, 'accounts/recover-password.html', {})


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, "Please reset your password")
            return redirect('reset-password')
        else:
            messages.error(request, "the link has been expired")
            return redirect('user-login')
        

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect('user-login')
        else:
            messages.error(request, "Password does not match")
            return redirect('reset-password')
        
    return render(request, 'accounts/reset-password.html')

        
