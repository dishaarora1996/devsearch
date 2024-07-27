from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Blog, AdminMenu, AdminMenuPermission, Employee, Location)
from django.conf import settings
from django.core.mail import send_mail
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)




@login_required(login_url='user-login')
def manage_blog(request):
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    blog = Blog.objects.all().order_by('id')
    context = {
        'blog_list': blog,
        'menu_permission': menu_permission
    }
    return render(request, 'blog_section/blog.html', context)


@login_required(login_url='user-login')
def add_blog(request):
    location = Location.objects.all().order_by('id')
    
    if request.method == "POST":
        blog_title = request.POST.get('blog_title')
        location_id = request.POST.get('location')
        short_description = request.POST.get('short_description')
        blog_image = request.FILES.get('blog_image')
        decription_editor = request.POST.get('decription_editor')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keyword = request.POST.get('meta_keyword')

        if location_id == 'All Location':
             Blog.objects.create(blog_title=blog_title, loc_all=True, short_description=short_description, blog_image=blog_image, long_description=decription_editor, meta_title=meta_title, meta_description=meta_description, meta_keyword=meta_keyword)
        else:
            loc_obj = Location.objects.filter(id=location_id).first()

            Blog.objects.create(blog_title=blog_title, location=loc_obj, short_description=short_description, blog_image=blog_image, long_description=decription_editor, meta_title=meta_title, meta_description=meta_description, meta_keyword=meta_keyword)

        return redirect('manage-blog')

    context ={
        'location': location
    }

    return render(request, 'blog_section/add_blog.html', context)


@login_required(login_url='user-login')
def edit_blog(request, blog_id):
    blog = Blog.objects.filter(id=blog_id)
    blog_obj = blog.first()
    location = Location.objects.all().order_by('id')
    context ={
        'blog': blog_obj,
        'location': location
    }

    if request.method == "POST":
        blog_title = request.POST.get('blog_title')
        location_id = request.POST.get('location')
        short_description = request.POST.get('short_description')
        blog_image = request.FILES.get('blog_image')
        decription_editor = request.POST.get('decription_editor')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keyword = request.POST.get('meta_keyword')
        

        if blog_image is None or blog_image == '':
            blog_image = blog_obj.blog_image
        

        if location_id == 'All Location':
            blog.update(blog_title=blog_title, loc_all=True, short_description=short_description, blog_image=blog_image, long_description=decription_editor, meta_title=meta_title, meta_description=meta_description, meta_keyword=meta_keyword, location=None)
        else:
            loc_obj = Location.objects.filter(id=location_id).first()

            blog.update(blog_title=blog_title, location=loc_obj, short_description=short_description, blog_image=blog_image, long_description=decription_editor, meta_title=meta_title, meta_description=meta_description, meta_keyword=meta_keyword, loc_all=False)

        return redirect('manage-blog')


    return render(request, 'blog_section/edit_blog.html', context)




@login_required(login_url='user-login')
def delete_blog(request, blog_id):
    blog = Blog.objects.filter(id=blog_id).first()

    blog.delete()

    return redirect('manage-blog')
