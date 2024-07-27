from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Settings)
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)





@login_required(login_url='user-login')
def manage_settings(request):
    if request.method =="POST":
        corporate_site_title = request.POST.get('site_title')
        logo = request.FILES.get('logo')
        footer_copyright = request.POST.get('footer_copyright')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        youtube = request.POST.get('youtube')
        twitter = request.POST.get('twitter')

        Settings.objects.update_or_create(id=1, defaults={"corporate_site_title": corporate_site_title, "logo":logo, "footer_copyright": footer_copyright, "email":email, "phone":phone, "facebook":facebook, "instagram":instagram, "youtube":youtube, "twitter":twitter})
        

    settings = Settings.objects.first()
    context = {
        'settings': settings
    }

    return render(request, 'general_settings/manage-settings.html', context)