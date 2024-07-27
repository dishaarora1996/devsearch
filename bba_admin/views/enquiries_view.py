from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Enquiry, AdminMenu, AdminMenuPermission, Employee)
from django.conf import settings
from django.core.mail import send_mail
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)




@login_required(login_url='user-login')
def manage_enquiries(request):

    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()


    enquiry = Enquiry.objects.all().order_by('id')
    context = {
        'enquiry_list': enquiry,
        'menu_permission': menu_permission
    }
    return render(request, 'enquiries.html', context)


@login_required(login_url='user-login')
def reply_enquiry(request):
    enquiry_id = request.POST.get("enquiry_id")
    email_subject = request.POST.get("email_subject")
    email_body = request.POST.get("email_body")
    enquiry = Enquiry.objects.filter(id=enquiry_id).first()

    email_to = enquiry.email
    subject = 'welcome to BBA'
    message = f'Hi, thank you for registering in.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_to, ]
    # send_mail( subject, message, email_from, recipient_list )
    
    return redirect('manage-enquiries')
