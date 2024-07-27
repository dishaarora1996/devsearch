from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from . import views
from django.contrib import messages
from .models import (Role, Employee, Location, EmployeeLocationAssignment, 
                      Menu, Country, State, City, CorporatePages, CorporateBanners)
import logging
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)

