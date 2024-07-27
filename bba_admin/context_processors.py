from django.conf import settings # import the settings file
from bba_admin.models import AdminMenuPermission, AdminMenu, Role, Employee
from django.contrib.auth.decorators import login_required

def image_url(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'IMAGE_MEDIA_PATH': settings.IMAGE_MEDIA_PATH}

def user_profile_image(request):
    if request.user.is_authenticated:
        user = request.user
        emp_obj = Employee.objects.filter(user=user).first()
        return {"user_profile_image": emp_obj.profile_image}
    return {"user_profile_image": ""}


def menu_permission(request):
    
    if request.user.is_authenticated:
        user = request.user
        emp_obj = Employee.objects.filter(user=user).first()
        admin_menu_permission = AdminMenuPermission.objects.filter(role_id=emp_obj.role_id) if emp_obj else []
        
        menu_permission_list = []
        # for admin_menu in admin_menu_permission:
        #     print(f"****************{AdminMenu.objects.filter(admin_menu_id=admin_menu.admin_menu_id.admin_menu_id)}")
        #     menu_set = {}
        #     menu_obj = AdminMenu.objects.filter(admin_menu_id=admin_menu.admin_menu_id.admin_menu_id).first()
        #     parent_menu_name = menu_obj.parent_id.admin_menu_name
        #     menu_set['parent_menu_name'] = parent_menu_name
        #     menu_set['child_menu'] = menu_obj
        #     menu_permission_list.append(menu_set)
        all_menus = AdminMenu.objects.filter(parent_id__isnull=True).order_by("admin_menu_id")
        
        # import pdb;pdb.set_trace()
        for menu in all_menus:
            menu_set = {}
            
            child_menu = AdminMenu.objects.filter(parent_id=menu.admin_menu_id).order_by('admin_menu_id')
            
            temp = []
            for child in child_menu:
                child_temp = {}
                if child.admin_menu_id in admin_menu_permission.values_list("admin_menu_id", flat=True):
                    child_temp["child_menu"] = child.admin_menu_name
                    child_temp["url"] = child.menu_url
                    child_temp["menu_icon"] = child.menu_icon
                    temp.append(child_temp)
                    menu_set['parent_menu_name'] = menu.admin_menu_name
            if temp:
                menu_set["child_menu"] = temp
                menu_permission_list.append(menu_set)
            
        
        return {"admin_menu_permission": menu_permission_list}
    return {"admin": ""}
