from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Menu, CorporatePages, CorporateBanners, Location, AdminMenu, AdminMenuPermission, Employee)
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)




def change_corporate_banner_status(request):
    banner_id = request.GET.get('banner_id')
    banner_status = request.GET.get('banner_status')
    location = request.GET.get('location')
    page_obj = CorporateBanners.objects.filter(id=banner_id).update(status=banner_status)

    return redirect("manage-banners", location=location)


@login_required(login_url='user-login')
def add_banners(request, location):
    pages = CorporatePages.objects.filter(location__loc_name=location)
    
    location_obj = Location.objects.filter(loc_name=location).first()
    if request.method == "POST":
        page_title_id = request.POST.get('page_title')
        banner_image = request.FILES.get('banner_image')

        page_obj = CorporatePages.objects.filter(id=page_title_id).first()

        if CorporateBanners.objects.filter(page_title=page_obj, location=location_obj).exists():
            messages.error(request, "Page Banner already exists")
            return redirect('add-banners', location=location)
        else:
            corporate_banner  = CorporateBanners.objects.create(page_title=page_obj, banner_image=banner_image, location=location_obj, status="Active")
        
        return redirect('manage-banners', location=location)
    
    location_type = "Corporate" if location=="Corporate" else "Location"
    context = {
        'corporate_pages': pages,
        'location_name': location,
        'location_type': location_type,

    }
    return render(request, 'corporate_banner/add-corporate-banners.html', context)


@login_required(login_url='user-login')
def edit_banners(request, banner_id, location):
    corporate_banner = CorporateBanners.objects.filter(id=banner_id).first()
    corporate_pages = CorporatePages.objects.filter(location__loc_name=location)
    
    location_type = "Corporate" if location=="Corporate" else "Location"
    context = {
        'corporate_banner': corporate_banner,
        'corporate_pages': corporate_pages,
        'location_type': location_type,
        'location_name': location
    }

    if request.method == "POST":
        page_title_id = request.POST.get('page_title')
        banner_image = request.FILES.get('banner_image')
        

        
        page_title_obj = CorporatePages.objects.filter(id=page_title_id).first()

        if banner_image is None or banner_image == '':
            banner_image = CorporateBanners.objects.get(id=banner_id).banner_image

        banner_obj = CorporateBanners.objects.filter(id=banner_id).update(page_title=page_title_obj, banner_image=banner_image)

        return redirect("manage-banners", location=location)

    
    return render(request, 'corporate_banner/edit-corporate-banners.html', context)




@login_required(login_url='user-login')
def manage_banners(request, location):
    # get menu permission for admin user menu
    
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).split('/')[1]).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    corporate_banners = CorporateBanners.objects.filter(location__loc_name=location).order_by('id')
    location_type = "Corporate" if location=="Corporate" else "Location"
    context = {
        'corporate_banners': corporate_banners,
        'location_name': location,
        'location_type': location_type,
        'menu_permission': menu_permission
    }
    return render(request, 'corporate_banner/manage-corporate-banners.html', context)




@login_required(login_url='user-login')
def delete_banners(request, banner_id, location):
    banner = CorporateBanners.objects.filter(id=banner_id).first()

    banner.delete()

    return redirect('manage-banners', location=location)