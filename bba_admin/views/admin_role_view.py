from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Role, AdminMenuPermission, AdminMenu, Employee)
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)



@login_required(login_url='user-login')
def admin_role(request):

    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    user = request.user
    emp_obj = Employee.objects.filter(user=user).first()

    '''Check if user is Super Admin'''
    if emp_obj.role.name == "Super Admin":
        role = Role.objects.all().order_by('id')
    else:
        role = Role.objects.exclude(name="Super Admin").order_by('id')

    context = {
        'role_list': role,
        'menu_permission': menu_permission
    }
    return render(request, 'admin_role/admin-roles.html', context)


@login_required(login_url='user-login')
def add_admin_role(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        logger.info(f'Add Role Post Data: name-{name}, description-{description}')
                    
        role  = Role.objects.create(name=name, description=description, status="Active")
        
        # Assign dashboard menu as default menu for the new role
        admin_menu = AdminMenu.objects.filter(admin_menu_name="Dashboard").first()
        AdminMenuPermission.objects.create(role_id=role, admin_menu_id=admin_menu, can_add=True, can_edit=True, can_delete=True, can_view=True)
        
        return redirect('admin-role')
    
    return render(request, 'admin_role/add-admin-role.html', {})


@login_required(login_url='user-login')
def edit_admin_role(request, role_id):
    role = Role.objects.filter(id=role_id).first()

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
                    
        Role.objects.filter(id=role_id).update(name=name, description=description)
        
        return redirect('admin-role')
    
    context = {
        'role': role
    }
    return render(request, 'admin_role/edit-admin-role.html', context)






def change_admin_role_status(request):
    role_id = request.GET.get('role_id')
    role_status = request.GET.get('role_status')
    role_obj = Role.objects.filter(id=role_id).update(status=role_status)

    return redirect("admin-role")


@login_required(login_url='user-login')
def delete_admin_role(request, role_id):
    role = Role.objects.filter(id=role_id).first()

    role.delete()

    return redirect('admin-role')



@login_required(login_url='user-login')
def manage_role_permission(request, role_id):
    role_obj = Role.objects.filter(id=role_id).first()
    if request.method == "POST":
        data = request.POST
        
        if int(role_id) > 0:
            AdminMenuPermission.objects.filter(role_id=role_id).delete()
        for key, value in data.items():
            if key != "csrfmiddlewaretoken":
                split_string = key.split('_')
                permission_type = '_'.join(split_string[0:2])
                permission_menu = ''.join(split_string[2:])
                admin_menu_create_obj = {
                    "admin_menu_id": AdminMenu.objects.filter(admin_menu_name__exact=permission_menu).first(),
                    "role_id": Role.objects.filter(id=role_id).first(),
                    permission_type: value
                }
                exsting_permission = AdminMenuPermission.objects.filter(
                    role_id=role_id, admin_menu_id__admin_menu_name__exact=permission_menu).first()
                if exsting_permission:
                    if permission_type ==  "can_add":
                        exsting_permission.can_add = value
                    elif permission_type ==  "can_edit":
                        exsting_permission.can_edit = value
                    elif permission_type ==  "can_delete":
                        exsting_permission.can_delete = value
                    elif permission_type ==  "can_view":
                        exsting_permission.can_view = value
                    elif permission_type ==  "update_permission":
                        exsting_permission.update_permission = value
                    exsting_permission.save()
                else:
                    AdminMenuPermission.objects.create(**admin_menu_create_obj)
            else:
                AdminMenuPermission.objects.filter(role_id=role_id).delete()

        return redirect('admin-role')

    permission_set = []
    for parent_id in AdminMenu.objects.exclude(
        parent_id__isnull=True).exclude(admin_menu_name="Dashboard").distinct().values_list("parent_id", flat=True):
        temp_list = []
        permission_dict = {}
        parent_menu_list = AdminMenu.objects.filter(parent_id=parent_id)
        parent_menu_name = AdminMenu.objects.filter(admin_menu_id=parent_id).first().admin_menu_name
        for parent_menu in parent_menu_list:
            temp = {}
            temp["menu_name"] = parent_menu.admin_menu_name if parent_menu else None
            set_menu = AdminMenuPermission.objects.filter(admin_menu_id=parent_menu, role_id=role_id).first()
            if set_menu:
                temp["can_add"] = set_menu.can_add
                temp["can_edit"] = set_menu.can_edit
                temp["can_view"] = set_menu.can_view
                temp["can_delete"] = set_menu.can_delete
                temp["update_permission"] = set_menu.update_permission
            else:
                temp["can_add"] = False
                temp["can_edit"] = False
                temp["can_view"] = False
                temp["can_delete"] = False
                temp["update_permission"] = False
            temp_list.append(temp)
        permission_dict["parent_menu_name"] = parent_menu_name
        permission_dict["child_menu"] = temp_list

        permission_set.append(permission_dict)
    
    
    context = {
        'role_obj': role_obj,
        'permission_set': permission_set
    }
    return render(request, 'admin_role/manage-roles-permissions.html', context)

