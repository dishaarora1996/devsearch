from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from bba_admin.models import (Role, Employee, Location, 
                     Country, State, City,  LocationPostalCodeMapping, AdminMenu, AdminMenuPermission)
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='user-login')
def manage_location(request):
    
    # get menu permission for admin user menu
    admin_menu = AdminMenu.objects.filter(menu_url=(request.path).strip("/")).first()
    role = Employee.objects.filter(user=request.user).first().role
    menu_permission = AdminMenuPermission.objects.filter(admin_menu_id=admin_menu.id, role_id=role.id).first()

    location = Location.objects.exclude(type='Corporate').order_by('id')
    context = {
        'location_list': location,
        'menu_permission': menu_permission
    }
    return render(request, 'location/location.html', context)


@login_required(login_url='user-login')
def add_location(request):
    country_list = Country.objects.all()
    state_list = State.objects.all()
    city_list = City.objects.all()
    if request.method == "POST":
        loc_name = request.POST.get('loc_name')
        city_id = request.POST.get('city')
        state_id = request.POST.get('state')
        country_id = request.POST.get('country')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        

        if Location.objects.filter(loc_name=loc_name).exists():
            messages.error(request, "Location Name already exists")
            return redirect('add-location')

        city = City.objects.get(id=city_id)
        state = State.objects.get(id=state_id)
        country = Country.objects.get(id=country_id)

        location  = Location.objects.create(loc_name=loc_name, city=city, state=state, country=country, address=address, latitude=latitude, longitude=longitude, status='Active')

        if pincode:
            pincode = pincode.split(",")
            pincode_list = [i.strip()  for i in pincode]

            for pincode in pincode_list:
                LocationPostalCodeMapping.objects.create(location_id=location, postal_code=pincode)

        return redirect('location')
    
    context ={
        'country_list': country_list,
        'state_list': state_list,
        'city_list': city_list
    }
    return render(request, 'location/add-location.html', context)



@login_required(login_url='user-login')
def edit_location(request, location_id):
    location_obj = Location.objects.filter(id=location_id)
    loc_obj = location_obj.first()
    # Get pincode list of location
    pincode_list = LocationPostalCodeMapping.objects.filter(location_id=loc_obj.id).values_list('postal_code', flat=True)
    pincode_text = ','.join(pincode_list)
    country_list = Country.objects.all()
    state_list = State.objects.all()
    city_list = City.objects.all()
    if request.method == "POST":
        loc_name = request.POST.get('loc_name')
        city_id = request.POST.get('my_city')
        state_id = request.POST.get('my_state')
        country_id = request.POST.get('my_country')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = City.objects.filter(id=city_id).first()
        state = State.objects.filter(id=state_id).first()
        country = Country.objects.filter(id=country_id).first()
        
        if Location.objects.filter(loc_name=loc_name).exclude(id=location_id).exists():
            messages.error(request, "Location Name already exists")
            return redirect('add-location')


        location  = location_obj.update(loc_name=loc_name, city=city, state=state, country=country, address=address, latitude=latitude, longitude=longitude)

        loc_mapping = LocationPostalCodeMapping.objects.filter(location_id=loc_obj)
        loc_mapping.delete()


        if pincode:
            pincode = pincode.split(",")
            pincode_list = [i.strip()  for i in pincode]

            for pincode in pincode_list:
                LocationPostalCodeMapping.objects.create(location_id=loc_obj, postal_code=pincode)
                
        return redirect('location')
    
    context ={
        'location': loc_obj,
        'country_list': country_list,
        'state_list': state_list,
        'city_list': city_list,
        'pincode_text': pincode_text
    }
    return render(request, 'location/edit-location.html', context)


def get_city_list(request):
    state_id = request.GET.get('selected_value')
    state_obj = State.objects.filter(id=state_id).first()
    city_list = list(City.objects.filter(state=state_obj).values('id', 'name'))

    return JsonResponse({'data': city_list})




@login_required(login_url='user-login')
def delete_location(request, location_id):
    location = Location.objects.filter(id=location_id).first()

    location.delete()

    return redirect('location')


def change_location_status(request):
    location_id = request.GET.get('location_id')
    location_status = request.GET.get('location_status')
    loc_obj = Location.objects.filter(id=location_id).update(status=location_status)

    return redirect("location")



@login_required(login_url='user-login')
def location_search(request):

    search = request.GET.get('search')

    query= Q()

    if search:
        query |= Q(loc_name__icontains=search)
        query |= Q(city__name__icontains=search)
        query |= Q(country__name__icontains=search)
        query |= Q(state__name__icontains=search)
        query |= Q(address__icontains=search)



    results = Location.objects.filter(query).order_by('id')

    context = {
        'search_value': search,
        'location_list': results
    }

    return render(request, "location/location.html", context)