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
def manage_home_blocks(request, location):
    home_blocks = HomeBlockSection.objects.filter(location__loc_name=location).order_by('id')
    
    context = {
        'block_section': home_blocks
    }
    return render(request, 'home_block_section/manage-home-blocks.html', context)


def change_home_block_status(request, location):
    block_id = request.GET.get('block_id')
    block_status = request.GET.get('block_status')
    
    block_obj = HomeBlockSection.objects.filter(id=block_id).update(status=block_status)

    return redirect("manage-home-blocks", location=location)




@login_required(login_url='user-login')
def edit_home_block(request, block_id, location):
    _block = HomeBlockSection.objects.filter(id=block_id).first()
    field_names = [field.name for field in HomeBlockSection._meta.fields]
    context = {field: getattr(_block, field) for field in field_names if _block}

    if request.method == "POST":
        block_name = request.POST.get('block_name', None)
        description = request.POST.get('description_editor', None)
        meta_title = request.POST.get('meta_title', None)
        meta_keywords = request.POST.get('meta_keywords', None)
        meta_description = request.POST.get('meta_description', None)

        HomeBlockSection.objects.filter(id=block_id).update(block_name=block_name, description=description, meta_title=meta_title, meta_keywords=meta_keywords, meta_description=meta_description)

        return redirect("manage-home-blocks", location=location)

    return render(request, 'home_block_section/edit-home-block.html', context)





# @login_required(login_url='user-login')
# def edit_home_block(request, block_id):
#     _block = HomeBlockSection.objects.filter(id=block_id).first()
#     field_names = [field.name for field in BlockSection._meta.fields]
#     context = {field: getattr(_block, field) for field in field_names if _block}

#     if request.method == "POST":
#         block_name = request.POST.get('block_name', None)
#         description = request.POST.get('description_editor', None)
#         meta_title = request.POST.get('meta_title', None)
#         meta_keywords = request.POST.get('meta_keywords', None)
#         meta_description = request.POST.get('meta_description', None)

#         BlockSection.objects.filter(id=block_id).update(block_name=block_name, description=description, meta_title=meta_title, meta_keywords=meta_keywords, meta_description=meta_description)

#         return redirect("corporate-home-blocks")

#     return render(request, 'block_section/edit-corporate-block.html', context)