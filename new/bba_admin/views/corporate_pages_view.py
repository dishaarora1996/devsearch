from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import *
import logging
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
# Create your views here.

logger = logging.getLogger(__name__)



@login_required(login_url='user-login')
def manage_corporate_pages(request, location):
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).split('/')[1]).first()
    
    role = Employee.objects.filter(user=request.user).first().role
   
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()
    
    corporate_pages = CorporatePages.objects.filter(location__loc_name=location).order_by('id')
    location_type = "Corporate" if location=="Corporate" else "Location"
    context = {
        'corporate_pages': corporate_pages,
        'location_name': location,
        'location_type': location_type,
        'menu_permission': menu_permission
    }
    return render(request, 'corporate_pages/manage-corporate-pages.html', context)





@login_required(login_url='user-login')
def add_corporate_pages(request):

    if request.method == "POST":
        page_title = request.POST.get('page_title')
        description = request.POST.get('decription_editor')
        meta_title = request.POST.get('meta_title')
        meta_keywords = request.POST.get('meta_keywords')
        meta_description = request.POST.get('meta_description')

        location_obj = Location.objects.filter(type="Corporate").first()
        
        page_slug =  slugify(page_title)

        if CorporatePages.objects.filter(page_title=page_title, location=location_obj).exists():
            messages.error(request, "Corporate Page with this name already exists")
            return redirect("add-corporate-pages")

        CorporatePages.objects.create(page_title=page_title, page_slug=page_slug, description=description,
                                                                   meta_title=meta_title, meta_keywords=meta_keywords, meta_description=meta_description,
                                                                   location = location_obj, created_by=request.user, updated_by=request.user)

        return redirect("manage-pages", location="Corporate")

    
    return render(request, 'corporate_pages/add-corporate-pages.html', {})



@login_required(login_url='user-login')
def edit_corporate_pages(request, page_id):
    menu_obj = Menu.objects.filter(page=page_id).first()
    location_name = menu_obj.location.loc_name
    location_type = menu_obj.location.type
    corporate_page = CorporatePages.objects.filter(id=page_id).first()
    context = {
        'page': corporate_page,
        'location_name': location_name,
        'location_type': location_type
    }

    if request.method == "POST":
        page_title = request.POST.get('page_title')
        description = request.POST.get('decription_editor')
        meta_title = request.POST.get('meta_title')
        meta_keywords = request.POST.get('meta_keywords')
        meta_description = request.POST.get('meta_description')
    

        CorporatePages.objects.filter(id=page_id).update(page_title=page_title, description=description,
                                                                   meta_title=meta_title, meta_keywords=meta_keywords, meta_description=meta_description)

        return redirect("manage-pages", location=location_name)

    
    return render(request, 'corporate_pages/edit-corporate-pages.html', context)




def change_corporate_pages_status(request):
    page_id = request.GET.get('page_id')
    page_status = request.GET.get('page_status')
    location = request.GET.get('location')
    page_obj = CorporatePages.objects.filter(id=page_id).update(status=page_status)

    return redirect("manage-pages", location=location)