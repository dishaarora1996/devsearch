from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Career)
from django.conf import settings
from django.core.mail import send_mail
import logging
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
# Create your views here.

logger = logging.getLogger(__name__)




@login_required(login_url='user-login')
def manage_career(request):

    career = Career.objects.all().order_by('id')
    context = {
        'career_list': career
    }
    return render(request, 'career.html', context)


@login_required(login_url='user-login')
def career_detail(request, id):

    career = Career.objects.filter(id=id).first()
    
    context = {
        'career': career
    }
    return render(request, 'career-detail.html', context)


@login_required(login_url='user-login')
def career_file_download(request, id):

    career = Career.objects.filter(id=id).first()


    obj = Career.objects.filter(id=id).first()
    filename = obj.career_file.path
    response = FileResponse(open(filename, 'rb'))
    return response

    context = {
        'career': career
    }
    return render(request, 'career-detail.html', context)