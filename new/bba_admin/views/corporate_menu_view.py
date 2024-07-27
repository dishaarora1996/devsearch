from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Location, Menu, PagesMenuAssignment, CorporatePages, AdminMenu, AdminMenuPermission, Employee)
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.text import slugify
# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def manage_corporate_menu(request):
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    corporate_menu = Menu.objects.filter(location__type="Corporate").order_by("id")

    context = {
        'corporate_menu' : corporate_menu,
        'menu_permission': menu_permission
    }
    return render(request, 'corporate_menu/manage-corporate-menu.html', context)


@login_required(login_url='user-login')
def link_corporate_menu(request):
    location_obj = Location.objects.filter(type="Corporate").first()
    corporate_pages = location_obj.corporate_pages_location.all()
    
    context = {
        'corporate_pages': corporate_pages,
    }

    if request.method == "POST":
        page_id = request.POST.get('page_title')
        menu_name = request.POST.get('menu_name')
        menu_link_type = request.POST.get('menu_link_type')
        menu_link_url = request.POST.get('menu_link_url')
        menu_position = request.POST.get('menu_position')
        menu_sub_position = request.POST.get('menu_sub_position')
        top_ordering = request.POST.get('top_ordering')
        bottom_ordering = request.POST.get('bottom_ordering')
        
        page_obj = CorporatePages.objects.filter(id=page_id).first()

        menu_fields = {
        'name': menu_name,
        'menu_link_type': menu_link_type,
        'menu_position': menu_position,
        'location': location_obj,
        'page': page_obj
        }

        if menu_link_url:
            menu_fields.update({'menu_link_url': menu_link_url})
        else:
            menu_link_url =  page_obj.page_slug
            menu_fields.update({'menu_link_url':menu_link_url})
        
        if menu_sub_position:
            menu_fields.update({'menu_sub_position': menu_sub_position})

        if top_ordering:
            menu_fields.update({'top_ordering': top_ordering})

        if bottom_ordering:
            menu_fields.update({'bottom_ordering': bottom_ordering})
            
        if Menu.objects.filter(name=menu_name, location__type="Corporate").exists():
            messages.error(request, "Menu Name already exists for Corporate Website")
            return redirect('link-corporate-menu')

        menu_obj = Menu.objects.create(**menu_fields)
        
        # page = PagesMenuAssignment.objects.create(page_id=page_obj, menu_id=menu_obj, menu_link_url=menu_link_url, menu_link_type=menu_link_type)
    
        return redirect('manage-corporate-menu')
    return render(request, 'corporate_menu/link-corporate-menu.html', context)



@login_required(login_url='user-login')
def delete_corporate_menu(request, menu_id):
    menu_obj = Menu.objects.filter(id=menu_id).first()
    menu_obj.delete()

    return redirect('manage-corporate-menu')


@login_required(login_url='user-login')
def edit_corporate_menu(request, menu_id):
    
    # page_menu_asgmt_obj = PagesMenuAssignment.objects.filter(id=page_menu_asgmt_id).first()
    # menu_id = page_menu_asgmt_obj.menu_id.id
    menu_obj = Menu.objects.filter(id=menu_id).first()
    
    location_obj = Location.objects.filter(type="Corporate").first()
    corporate_pages = location_obj.corporate_pages_location.all()

    if request.method == "POST":
        page_id = request.POST.get('page_title')
        menu_name = request.POST.get('menu_name')
        menu_link_type = request.POST.get('menu_link_type')
        menu_link_url = request.POST.get('menu_link_url')
        menu_position = request.POST.get('menu_position')
        menu_sub_position = request.POST.get('menu_sub_position')
        
        menu_fields = {
        'name': menu_name,
        'menu_link_type': menu_link_type,
        'menu_position': menu_position
        }
        page_obj = CorporatePages.objects.filter(id=page_id).first()

        if menu_link_type == 'External':
            menu_fields.update({'menu_link_url': menu_link_url})
        else:
            menu_link_url = page_obj.page_slug

            menu_fields.update({'menu_link_url': menu_link_url})
        
        if menu_position == 'Bottom':
            menu_fields.update({'menu_sub_position': menu_sub_position})
        else:
            menu_fields.update({'menu_sub_position': '0'})

            
        if Menu.objects.filter(name=menu_name, location__type="Corporate").exclude(id=menu_id).exists():
            messages.error(request, "Menu Name already exists for Corporate Website")
            return redirect('edit-corporate-menu', menu_id)
        
        menu_obj = Menu.objects.filter(id=menu_id).update(**menu_fields)
        
        
        # page = PagesMenuAssignment.objects.filter(id=page_menu_asgmt_id).update(page_id=page_obj, menu_link_url=menu_link_url, menu_link_type=menu_link_type)

        return redirect('manage-corporate-menu')


    context = {
        'menu_obj': menu_obj,
        'corporate_pages': corporate_pages
    }



    return render(request, 'corporate_menu/edit-corporate-menu.html', context)