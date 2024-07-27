from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Location, LocationWebsite, LocationMenuAssignment, Employee, EmployeeLocationAssignment, Menu, LocationMenuMaster, CorporatePages, AdminMenuPermission, AdminMenu, HomeBlockSection)
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import ast
# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def manage_location_website(request):
    
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    location_website = LocationWebsite.objects.filter(deleted=False).order_by('id')
    context = {
        'location_website': location_website,
        'menu_permission': menu_permission
    }
    return render(request, 'location_website/location-website.html', context)





@login_required(login_url='user-login')
def add_location_website(request):
    location = Location.objects.exclude(type='Corporate').values('id', 'loc_name')
    context = {
        'location': location
    }
    if request.method =="POST":
        location_id = request.POST.get('location')
        location_admin_id = request.POST.get('location_admin')
        url_abbr = request.POST.get('url_abbr')

        if LocationWebsite.objects.filter(location=location_id).exists():
            messages.error(request, "Location Website with this location already exists")
            return redirect('add-location-website')
        
        if LocationWebsite.objects.filter(url_abbr=url_abbr).exists():
            messages.error(request, "Location Website with this url_abbr already exists")
            return redirect('add-location-website')


        location_website_details = {
            'location_id': location_id,
            'location_admin_id': location_admin_id,
            'url_abbr': url_abbr
        }
        
    
        return redirect('launch-location-website', location_website_details)
            
    return render(request, 'location_website/add-location-website-screen1.html', context)


def create_location_page(menu_id, loc_obj):
    # Create new location page same as corporate page for new location menu
    location_menu_obj = LocationMenuMaster.objects.filter(id=menu_id).first()
    location_menu_name = location_menu_obj.location_menu_name
    corporate_menu_obj = Menu.objects.filter(name=location_menu_name, location__type="Corporate").first()
    corporate_page_obj = corporate_menu_obj.page
    if corporate_page_obj:
    # Create pages for location_menu
        loc_page_obj = CorporatePages.objects.create(page_title=corporate_page_obj.page_title,page_slug=corporate_page_obj.page_slug, description=corporate_page_obj.description, meta_title=corporate_page_obj.meta_title, meta_keywords=corporate_page_obj.meta_keywords, meta_description=corporate_page_obj.meta_description, location=loc_obj )
        
        Menu.objects.create(location_menu_id=location_menu_obj, location=loc_obj, page=loc_page_obj,menu_link_url=corporate_menu_obj.menu_link_url, menu_link_type=corporate_menu_obj.menu_link_type, )
    else:
        # If menu link external then just copy the link to new location menu
        Menu.objects.create(location_menu_id=location_menu_obj, location=loc_obj, menu_link_type=corporate_menu_obj.menu_link_type, menu_link_url=corporate_menu_obj.menu_link_url)


def create_location_home_blocks(loc_obj):
    corporate_blocks = HomeBlockSection.objects.filter(location__type="Corporate")
    for item in corporate_blocks:
        HomeBlockSection.objects.create(block_name=item.block_name, description=item.description, meta_title=item.meta_title, meta_keywords=item.meta_keywords, meta_description=item.meta_description, location=loc_obj)





@login_required(login_url='user-login')
def launch_location_website(request, location_website_details):
    details = ast.literal_eval(location_website_details)
    location_website_menu = LocationMenuMaster.objects.all()
    
    loc_obj = Location.objects.filter(id=int(details['location_id'])).first()
    context = {
        'location_website_menu': location_website_menu,
        'location': loc_obj.loc_name 
    }
    
    if request.method =="POST":

        location_website_menu_id_list = request.POST.getlist('location_website_menu')
        
        loc_admin_obj = Employee.objects.filter(id=int(details['location_admin_id'])).first()

        if not location_website_menu_id_list:
            messages.error(request, "Please select any menu to proceed")
            return redirect('launch-location-website', location_website_details)
        
        # Add Home Menu as default menu for location website
        location_home_menu_id = LocationMenuMaster.objects.filter(location_menu_name="HOME").first().id
        location_website_menu_id_list.append(location_home_menu_id)
        
      
        # '''Create Location Website'''
        LocationWebsite.objects.create(location_admin=loc_admin_obj, url_abbr=details['url_abbr'], location=loc_obj, status="Active")

        ''' LocationWebsite with Menu Assignment'''

        for menu_id in location_website_menu_id_list:
            
            # Create new location page same as corporate page for new location menu
            create_location_page(menu_id, loc_obj)
        
        ''' create new location homeblocks same as corporate home blocks '''
        create_location_home_blocks(loc_obj)


        return redirect('manage-location-website')
            
    return render(request, 'location_website/add-location-website-screen2.html', context)

def get_location_admin_list(request):
    location_id = request.GET.get('selected_location')
    employee_id_list = EmployeeLocationAssignment.objects.filter(location_id=location_id).values_list('employee_id', flat=True)
    employee_list = list(Employee.objects.filter(id__in=employee_id_list).values('id', 'name'))

    return JsonResponse({'data': employee_list})


def change_location_website_status(request):
    loc_id = request.GET.get('loc_id')
    loc_status = request.GET.get('loc_status')
    LocationWebsite.objects.filter(id=loc_id).update(status=loc_status)

    return redirect("manage-location-website")


@login_required(login_url='user-login')
def delete_location_website(request, location_website_id):
    location_website = LocationWebsite.objects.filter(id=location_website_id)

    location_website.update(deleted=True)

    return redirect('manage-location-website')




@login_required(login_url='user-login')
def edit_location_website(request, location_website_id):
    location_website = LocationWebsite.objects.filter(id=location_website_id).first()
    location_obj = Location.objects.filter(id=location_website.location.id).first()

    '''get location admin list'''
    employee_id_list = EmployeeLocationAssignment.objects.filter(location_id=location_obj).values_list('employee_id', flat=True)
    employee_list = list(Employee.objects.filter(id__in=employee_id_list).values('id', 'name'))

    '''get checked location menu list'''
    # selected_menu_list_name = LocationMenuAssignment.objects.filter(location_id=location_website.location.id).values('menu_id', 'menu_id__name')
    
    selected_menu_list_name = Menu.objects.filter(location=location_obj.id).values('location_menu_id', 'location_menu_id__location_menu_name')

    selected_menu_list = list(Menu.objects.filter(location=location_obj.id).values_list('location_menu_id',flat=True))
    
    location_website_menu = LocationMenuMaster.objects.exclude(id__in=selected_menu_list)

    # Remove home menu from selected menu list as home menu is default menu and cannot be removed
    home_location_menu = Menu.objects.filter(location=location_obj.id, location_menu_id__location_menu_name="HOME").first().location_menu_id.id

    selected_menu_list.remove(home_location_menu)

    if request.method == 'POST':
        location_website_menu_id_list = request.POST.getlist('location_website_menu')
        location_website_menu_id_list = [int(i) for i in location_website_menu_id_list] 
        location_admin = request.POST.get('location_admin')    
    
        
        if not location_website_menu_id_list:
            messages.error(request, "Please select any menu to proceed")
            return redirect('edit-location-website', location_website_id)
        
        loc_admin_obj = Employee.objects.filter(id=location_admin).first()
        
        LocationWebsite.objects.filter(id=location_website_id).update(location_admin=loc_admin_obj)

        

        menu_diff_list =set(selected_menu_list)^set(location_website_menu_id_list)
        

        if menu_diff_list:
            for menu_id in menu_diff_list:
                if menu_id in selected_menu_list:
                    loc_menu_obj = Menu.objects.filter(location=location_obj, location_menu_id=menu_id).first()
                    if loc_menu_obj.page:
                        loc_menu_obj.page.delete()
                    loc_menu_obj.delete()
                else:
                    # Create new location page same as corporate page for new location menu
                    create_location_page(menu_id, location_obj)

        
        
        return redirect("manage-location-website")


    
    
    context= {
        'employee_list': employee_list, 
        'location_website': location_website,
        'location_website_menu': location_website_menu,
        'selected_menu_list_name': selected_menu_list_name
        
    }
    
            
    return render(request, 'location_website/edit-location-website.html', context)

