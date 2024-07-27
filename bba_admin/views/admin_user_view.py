from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Role, Employee, Location, EmployeeLocationAssignment, 
                     Country, State, City, CorporatePages, CorporateBanners, AdminMenu, AdminMenuPermission)
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def admin_users(request):
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()
    

    role = Role.objects.all()
    location_list = Location.objects.all()
    employee = Employee.objects.exclude(role__name="Super Admin").order_by('id').values('id', 'role__name', 'name', 'email', 'status', 'phone')
    for emp in employee:
        emp_loc_list = list(EmployeeLocationAssignment.objects.filter(employee_id=emp['id']).values_list('location_id__loc_name', flat=True))
        emp['emp_loc_list'] = emp_loc_list

    context = {
        'employee_list': employee,
        'user_type_list': role,
        'location_list': location_list,
        'menu_permission': menu_permission
        
    }
    return render(request, 'admin_user/admin-users.html', context)


@login_required(login_url='user-login')
def add_admin_user(request):
    user_type = Role.objects.filter(status="Active").values('id', 'name').exclude(name="Super Admin")
    location = Location.objects.all().values('id', 'loc_name')
    context = {
        'user_type': user_type,
        'location': location
    }
    if request.method =="POST":
        user_type = request.POST.get('user_type')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        profile_image = request.FILES.get('image')
        address = request.POST.get('address')
        location = request.POST.getlist('location')
        
        user = User.objects.filter(username=email).first()
        if user:
            messages.error(request, 'User already exists with this email')
        else:
            role_obj = Role.objects.get(id=user_type)
            
            logger.info(f'Add Admin User Post Data: user_type-{user_type}, name-{name},phone-{phone} email-{email}, password-{password}, image-{profile_image}, address-{address}, location-{location}, role_obj-{role_obj}')
            
            '''Create User'''
            user_obj = User.objects.create(username=email, email=email)
            user_obj.set_password(password)
            user_obj.save()
            
            '''Create Employee'''
            employee_obj = Employee.objects.create(name=name, email=email, profile_image=profile_image, emp_address=address, role=role_obj, status="Active", phone=phone, user=user_obj)

            '''Employee Location Mapping'''
            for loc in location:
                loc_obj = Location.objects.get(id=loc)
                emp_loc = EmployeeLocationAssignment.objects.create(employee_id=employee_obj, location_id=loc_obj)
            
            
            
            return redirect('admin-users')
            
    return render(request, 'admin_user/add-admin-user.html', context)



@login_required(login_url='user-login')
def edit_admin_user(request, emp_id):
    employee = Employee.objects.filter(id=emp_id).first()
    user_type = Role.objects.filter(status='Active').values('id', 'name').exclude(name__in=["Super Admin", employee.role])
    user = User.objects.filter(id=employee.user.id).first()
    emp_loc = EmployeeLocationAssignment.objects.filter(employee_id=emp_id)
    location = Location.objects.exclude(id__in=emp_loc.values_list('location_id', flat=True))
    if request.method =="POST":
        user_type = request.POST.get('user_type')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        profile_image = request.FILES.get('image')
        address = request.POST.get('address')
        location = request.POST.getlist('location')

        if User.objects.filter(email=email, username=email).exclude(id=employee.user.id).exists():
            messages.error(request, 'User already exists with this email')
        
        else:
        
            role_obj = Role.objects.filter(id=user_type).first()
            
            if profile_image is None or profile_image == '':
                profile_image = Employee.objects.get(id=emp_id).profile_image
            
            emp_obj = Employee.objects.filter(id=emp_id)

            emp_obj.update(name=name, email=email, profile_image=profile_image, emp_address=address, role=role_obj, status="Active", phone=phone)

            if password != None or password != '':
                user.set_password(password)
                user.save()

            '''Employee Location Mapping'''
            if location:
                a = EmployeeLocationAssignment.objects.filter(employee_id=emp_id)
                a.delete()
                for loc in location:
                    loc_obj = Location.objects.get(id=loc)
                    emp_loc = EmployeeLocationAssignment.objects.create(employee_id=emp_obj.first(), location_id=loc_obj)
            
            
            return redirect('admin-users')

    
    context = {
        'employee': employee,
        'user_type': user_type,
        'location': location,
        'emp_loc': emp_loc
    }
            
    return render(request, 'admin_user/edit-admin-user.html', context)


@login_required(login_url='user-login')
def delete_admin_user(request, emp_id):
    employee = Employee.objects.filter(id=emp_id).first()
    user = User.objects.filter(id=employee.user.id).first()

    employee.delete()
    user.delete()

    return redirect('admin-users')



def change_admin_user_status(request):
    employee_id = request.GET.get('employee_id')
    employee_status = request.GET.get('employee_status')
    employee_obj = Employee.objects.filter(id=employee_id)
    employee_obj.update(status=employee_status)
    user_id = employee_obj.first().user.id

    if employee_status == 'Active':
        user_obj = User.objects.filter(id=user_id).update(is_active=True)
    else:
        user_obj = User.objects.filter(id=user_id).update(is_active=False)



    return redirect("admin-users")



@login_required(login_url='user-login')
def admin_user_search(request):
    role = Role.objects.all()
    location_list = Location.objects.all()

    search = request.GET.get('search')
    user_type = request.GET.get('user_type')
    location_search = request.GET.get('location')

    query= Q()

    if search:
        query |= Q(name__icontains=search)
        query |= Q(email__icontains=search)
        query |= Q(phone__icontains=search)

    if user_type:
        query &= Q(role__name__iexact=user_type)
    
    if location_search:
        location_obj_list = EmployeeLocationAssignment.objects.filter(location_id__loc_name=location_search).values_list('employee_id', flat=True)
        query &= Q(id__in=location_obj_list)


    employee = Employee.objects.filter(query).order_by('id').values('id', 'role__name', 'name', 'email', 'status', 'phone')
    for emp in employee:
        emp_loc_list = list(EmployeeLocationAssignment.objects.filter(employee_id=emp['id']).values_list('location_id__loc_name', flat=True))
        emp['emp_loc_list'] = emp_loc_list


    context = {
        'search_value': search,
        'employee_list': employee,
        'user_type_list': role,
        'user_type': user_type, 
        'location_list': location_list,
        'location': location_search
    }

    return render(request, "admin_user/admin-users.html", context)