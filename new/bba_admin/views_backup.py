# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from . import views
# from django.contrib import messages
# from .models import (Role, Employee, Location, EmployeeLocationAssignment, 
#                      MenuPermission, Menu, Country, State, City, CorporatePages, CorporateBanners)
# import logging
# from django.contrib.auth.decorators import login_required
# # Create your views here.

# logger = logging.getLogger(__name__)


# def user_login(request):

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email, password)
#         try:
#             user = User.objects.get(username=email)
#         except:
#             messages.error(request, "Email does not exist")
#             return render(request, 'login.html', {})
        
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)

#             return redirect('dashboard')
#         else:
#             messages.error(request, "Username or Password is incorrect")
#             return redirect('user-login')
        
#     return render(request, 'login.html', {})

# @login_required(login_url='user-login')
# def user_logout(request):
#     logout(request)
#     return redirect('user-login')


# @login_required(login_url='user-login')
# def dashboard(request):
#     return render(request, 'dashboard.html', {})

# @login_required(login_url='user-login')
# def admin_users(request):
#     employee = Employee.objects.all()
#     context = {
#         'employee_list': employee
#     }
#     return render(request, 'admin-users.html', context)

# @login_required(login_url='user-login')
# def admin_role(request):
#     role = Role.objects.all()
#     context = {
#         'role_list': role
#     }
#     return render(request, 'admin-roles.html', context)



# @login_required(login_url='user-login')
# def add_admin_user(request):
#     user_type = Role.objects.filter(status="Active").values('id', 'name').exclude(name="Super Admin")
#     location = Location.objects.all().values('id', 'loc_name')
#     context = {
#         'user_type': user_type,
#         'location': location
#     }
#     if request.method =="POST":
#         user_type = request.POST.get('user_type')
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         profile_image = request.FILES.get('image')
#         address = request.POST.get('address')
#         location = request.POST.getlist('location')
        
#         user = User.objects.filter(username=email).first()
#         if user:
#             messages.error(request, 'User already exists with this email')
#         else:
#             role_obj = Role.objects.get(id=user_type)
            
#             logger.info(f'Add Admin User Post Data: user_type-{user_type}, name-{name},phone-{phone} email-{email}, password-{password}, image-{profile_image}, address-{address}, location-{location}, role_obj-{role_obj}')
            
#             '''Create User'''
#             user_obj = User.objects.create(username=email, email=email)
#             user_obj.set_password(password)
#             user_obj.save()
            
#             '''Create Employee'''
#             employee_obj = Employee.objects.create(name=name, email=email, profile_image=profile_image, emp_address=address, role=role_obj, status="Active", phone=phone, user=user_obj)

#             '''Employee Location Mapping'''
#             for loc in location:
#                 loc_obj = Location.objects.get(id=loc)
#                 emp_loc = EmployeeLocationAssignment.objects.create(employee_id=employee_obj, location_id=loc_obj)
            
            
            
#             return redirect('admin-users')
            
#     return render(request, 'add-admin-user.html', context)


# @login_required(login_url='user-login')
# def add_role_permission(request, id):
#     if request.method == "POST":
#         data = request.POST
#     permission_set = MenuPermission.objects.filter(employee_id=id).values("menu_id__name", "menu_id", "employee_id", "can_add",
#                                                                           "can_delete", "can_edit")
#     print(permission_set)
#     context = {
#         "permission_set": permission_set,
#         "employee_id": id
#     }
#     return render(request, 'roles-permissions.html', context)


# @login_required(login_url='user-login')
# def get_location_list(request):
#     location = Location.objects.all()
#     context = {
#         'location_list': location
#     }
#     return render(request, 'location.html', context)


# @login_required(login_url='user-login')
# def add_location(request):
#     country_list = Country.objects.all()
#     state_list = State.objects.all()
#     city_list = City.objects.all()
#     if request.method == "POST":
#         loc_name = request.POST.get('loc_name')
#         city_id = request.POST.get('city')
#         state_id = request.POST.get('state')
#         country_id = request.POST.get('country')
#         pincode = request.POST.get('pincode')
#         address = request.POST.get('address')
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')

#         logger.info(f'Add Location Post Data: loc_name-{loc_name}, city-{city_id},state-{state_id} country-{country_id}, pincode-{pincode}, address-{address}, latitude-{latitude}, longitude-{longitude}')

#         city = City.objects.get(id=city_id)
#         state = State.objects.get(id=state_id)
#         country = Country.objects.get(id=country_id)

#         location  = Location.objects.create(loc_name=loc_name, city=city, state=state, country=country, pincode=pincode, address=address, latitude=latitude, longitude=longitude, status='Active')

#         return redirect('location')
    
#     context ={
#         'country_list': country_list,
#         'state_list': state_list,
#         'city_list': city_list
#     }
#     return render(request, 'add-location.html', context)


# @login_required(login_url='user-login')
# def add_admin_role(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')

#         logger.info(f'Add Role Post Data: name-{name}, description-{description}')
                    
#         role  = Role.objects.create(name=name, description=description, status="Active")
        
#         return redirect('admin-role')
    
#     return render(request, 'add-admin-role.html', {})



# @login_required(login_url='user-login')
# def edit_admin_user(request, emp_id):
#     employee = Employee.objects.filter(id=emp_id).first()
#     user_type = Role.objects.filter(status='Active').values('id', 'name').exclude(name__in=["Super Admin", employee.role])
#     user = User.objects.filter(id=employee.user.id).first()

#     if request.method =="POST":
#         user_type = request.POST.get('user_type')
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         profile_image = request.FILES.get('image')
#         address = request.POST.get('address')
#         location = request.POST.getlist('location')

#         if User.objects.filter(email=email, username=email).exclude(id=employee.user.id).exists():
#             messages.error(request, 'User already exists with this email')
        
#         role_obj = Role.objects.filter(id=user_type).first()

#         if profile_image is None or profile_image == '':
#             profile_image = Employee.objects.get(id=emp_id).profile_image
        
#         emp_obj = Employee.objects.filter(id=emp_id).update(name=name, email=email, profile_image=profile_image, emp_address=address, role=role_obj, status="Active", phone=phone)

#         if password != None or password != '':
#             user.set_password(password)
#             user.save()
        
#         return redirect('admin-users')

    
#     context = {
#         'employee': employee,
#         'user_type': user_type
#     }
#     print(f"***********{employee.role}")
            
#     return render(request, 'edit-admin-user.html', context)


# @login_required(login_url='user-login')
# def delete_admin_user(request, emp_id):
#     employee = Employee.objects.filter(id=emp_id).first()
#     user = User.objects.filter(id=employee.user.id).first()

#     employee.delete()
#     user.delete()

#     return redirect('admin-users')


# def get_city_list(request):
#     state_id = request.GET.get('selected_value')
#     state_obj = State.objects.filter(id=state_id).first()
#     city_list = list(City.objects.filter(state=state_obj).values('id', 'name'))

#     return JsonResponse({'data': city_list})

# @login_required(login_url='user-login')
# def manage_corporate_pages(request):
#     corporate_pages = CorporatePages.objects.all().order_by('id').values()
#     context = {
#         'corporate_pages': corporate_pages
#     }
#     return render(request, 'manage-corporate-pages.html', context)

# @login_required(login_url='user-login')
# def edit_corporate_pages(request, page_id):
#     corporate_page = CorporatePages.objects.filter(id=page_id).first()
#     context = {
#         'page': corporate_page
#     }

#     if request.method == "POST":
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         meta_title = request.POST.get('meta_title')
#         meta_keywords = request.POST.get('meta_keywords')
#         meta_description = request.POST.get('meta_description')

#         emp_obj = CorporatePages.objects.filter(id=page_id).update(title=title, description=description,
#                                                                    meta_title=meta_title, meta_keywords=meta_keywords, meta_description=meta_description)

#         return redirect("manage-corporate-pages")

    
#     return render(request, 'edit-corporate-pages.html', context)


# def change_corporate_pages_status(request):
#     page_id = request.GET.get('page_id')
#     page_status = request.GET.get('page_status')
#     page_obj = CorporatePages.objects.filter(id=page_id).update(status=page_status)

#     return redirect("manage-corporate-pages")


# def change_corporate_banner_status(request):
#     banner_id = request.GET.get('banner_id')
#     banner_status = request.GET.get('banner_status')
#     page_obj = CorporateBanners.objects.filter(id=banner_id).update(status=banner_status)

#     return redirect("manage-corporate-banners")


# @login_required(login_url='user-login')
# def add_corporate_banners(request):
#     corporate_pages = CorporatePages.objects.all()
#     if request.method == "POST":
#         page_name = request.POST.get('page_name')
#         banner_image = request.FILES.get('banner_image')
#         corporate_banner  = CorporateBanners.objects.create(page_name=page_name, banner_image=banner_image, status="Active")
        
#         return redirect('manage-corporate-banners')
    
#     context = {
#         'corporate_pages': corporate_pages
#     }
#     return render(request, 'add-corporate-banners.html', context)


# @login_required(login_url='user-login')
# def edit_corporate_banners(request, banner_id):
#     corporate_banner = CorporateBanners.objects.filter(id=banner_id).first()
#     corporate_pages = CorporatePages.objects.all()
#     context = {
#         'corporate_banner': corporate_banner,
#         'corporate_pages': corporate_pages
#     }

#     if request.method == "POST":
#         page_name = request.POST.get('page_name')
#         banner_image = request.FILES.get('banner_image')

#         if banner_image is None or banner_image == '':
#             banner_image = CorporateBanners.objects.get(id=banner_id).banner_image

#         banner_obj = CorporateBanners.objects.filter(id=banner_id).update(page_name=page_name, banner_image=banner_image)

#         return redirect("manage-corporate-banners")

    
#     return render(request, 'edit-corporate-banners.html', context)




# @login_required(login_url='user-login')
# def manage_corporate_banners(request):
#     corporate_banners = CorporateBanners.objects.all().order_by('id').values()
#     context = {
#         'corporate_banners': corporate_banners
#     }
#     return render(request, 'manage-corporate-banners.html', context)




# @login_required(login_url='user-login')
# def delete_corporate_banners(request, banner_id):
#     banner = CorporateBanners.objects.filter(id=banner_id).first()

#     banner.delete()

#     return redirect('manage-corporate-banners')




# @login_required(login_url='user-login')
# def manage_role_permission(request, role_id):
#     if request.method == "POST":
#         data = request.POST
#     # permission_set = AdminMenuPermission.objects.filter(
#         # employee_id=id).values("menu_id__name", "menu_id", "employee_id", "can_add",
#     #                                                                       "can_delete", "can_edit")
#     # print(permission_set)
#     # context = {
#     #     "permission_set": permission_set,
#     #     "employee_id": id
#     # }
#     # permission_set = AdminMenuPermission.objects.filter(
#     #     role_id=role_id).values_list(
#     #         "admin_menu_id__admin_menu_id",
#     #         "admin_menu_id__admin_menu_name",
#     #         "can_add", "can_edit", "can_delete", "can_view", "update_permission")
#     permission_set = {}
#     parent_id_list = AdminMenuPermission.objects.filter(
#         role_id=role_id).values_list("admin_menu_id__parent_id", flat=True)
#     if parent_id_list:
#         for parent_id in list(set(parent_id_list)):
#             temp_list = []
#             parent_menu_list = AdminMenu.objects.filter(parent_id=parent_id)
#             parent_menu_name = AdminMenu.objects.filter(admin_menu_id=parent_id).first().admin_menu_name
#             print(parent_menu_list)
#             for parent_menu in parent_menu_list:
#                 temp = {}
#                 temp["menu_name"] = parent_menu.admin_menu_name
#                 set_menu = parent_menu.adminmenupermission_set.first()
#                 temp["can_add"] = set_menu.can_add if set_menu else False
#                 temp["can_edit"] = set_menu.can_edit if set_menu else False
#                 temp["can_view"] = set_menu.can_view if set_menu else False
#                 temp["can_delete"] = set_menu.can_delete if set_menu else False
#                 temp["update_permission"] = set_menu.update_permission if set_menu else False
#                 temp_list.append(temp)
#             permission_set[parent_menu_name] = temp_list
#             print(permission_set)
            
#     else:
#         for i in AdminMenu.objects.all():
#             pass
            

#         # permission_set[parent_menu_name]

# <div class="scrollbar-sidebar header-shadow">
#     <div class="app-sidebar__inner">
#         <ul class="vertical-nav-menu">
#             {% for header_menu in admin_menu_permission%}
#             <li class="app-sidebar__heading">{{header_menu.parent_menu_name}}</li>
#             {% for child_menu in header_menu.child_menu %}
#             <li>
#                 {% url 'dashboard' as url %}
#                 <a href="{{url}}" {% if request.path == url %} class="mm-active" {% endif %}>
#                     <i class="metismenu-icon pe-7s-rocket"></i>
#                     {{child_menu}}
#                 </a>
#             </li>
#             {% endfor %}
#             {% endfor %}
#         </ul>
#     </div>
# </div>