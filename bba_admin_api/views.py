import collections

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.core.paginator import Paginator
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import  get_object_or_404
from rest_framework.views import APIView

from bba_admin_api.helper import custom_filters
from bba_admin_api.serializers import *
from bba_admin.models import *
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


# Create your views here.
def get_location_obj(location_name):
    if location_name == "Corporate":
        loc_obj = Location.objects.filter(loc_name="Corporate").first()
    else:
        loc_website = LocationWebsite.objects.filter(url_abbr=location_name).first()
        if not loc_website:
            return Response({"message": "No Location Found"}, status=status.HTTP_400_BAD_REQUEST)
        else:   
            location_id = loc_website.location.id
            loc_obj = Location.objects.filter(id=location_id).first()

    return loc_obj

class GetCorporateMenu(GenericAPIView):

    queryset = Menu.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            location_name = request.GET.get("location_name")

            if location_name is None or location_name == '':
                return Response({"message": "Provide Location Name"}, status=status.HTTP_400_BAD_REQUEST)

            loc_obj = get_location_obj(location_name)

            if loc_obj:
                menu = Menu.objects.filter(location=loc_obj)
                # bottom_menu = Menu.objects.filter(menu_position="Bottom")
                serializers = CorporateMenuSerializer(menu, many=True)
                return Response(serializers.data)
            else:
                return Response({"message": "Requested Menu Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as exp:
            logger.exception(exp)
            return Response({"message": "Server Error"})
    

class CreateEnquiry(GenericAPIView):
     serializer_class = EnquirySerializer

     def post(self, request, *args, **kwargs):
        try:
            serializer = EnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Enquiry created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exp:
            return Response({"message": "Server Error"})
        


class CreateCareer(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]
    
    serializer_class = CareerSerializer

    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            message = request.data.get('message')
            location_name = request.data.get('location_name')
            career_file = request.data.get('career_file')
            

            loc_obj = get_location_obj(location_name)
            career = Career.objects.create(name=name, email=email, phone=phone, message=message, career_file=career_file, location=loc_obj)
            return Response({"message": "Career submitted successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exp:
            return Response({"message": "Server Error"})
        

class GetPageContent(GenericAPIView):
    
    queryset = CorporatePages.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            location_name = request.GET.get("location_name")
            page_slug = request.GET.get("page_slug")

            if location_name is None or location_name == '':
                return Response({"message": "Provide Location Name"}, status=status.HTTP_400_BAD_REQUEST)
            if  page_slug is None or page_slug == '':
                return Response({"message": "Provide Page Slug"}, status=status.HTTP_400_BAD_REQUEST)
            
            loc_obj = get_location_obj(location_name)
            
            page_obj = CorporatePages.objects.filter(page_slug=page_slug, location=loc_obj).first()
            
            
            if page_obj:
                serializer = CorporatePagesSerializer(page_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Requested Page Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exp:
            logger.exception(exp)
            return Response({"message": "Server Error"})


class GetLocation(GenericAPIView):
    
    queryset = Location.objects.all()
    def get(self, request, *args, **kwargs):
        postal_code = request.GET.get('postal_code')
        if postal_code:
            location_id_list = LocationPostalCodeMapping.objects.filter(postal_code__icontains = postal_code).values_list('location_id', flat=True)
            loc_obj_list = Location.objects.filter(id__in=location_id_list)

            serializer = LocationSerializer(loc_obj_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else: 
            location = Location.objects.all()
            
            serializers = LocationSerializer(location, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        

class GetSettings(GenericAPIView):
    
    queryset = Settings.objects.all()
    def get(self, request, *args, **kwargs):
        general_settings = Settings.objects.first()
        
        serializers = SettingsSerializer(general_settings)
        return Response(serializers.data)
    
class GetPageBanner(GenericAPIView):
    
    queryset = CorporateBanners.objects.all()
    def get(self, request, *args, **kwargs):
        try: 
            location_name = request.GET.get("location_name")
            page_slug = request.GET.get("page_slug")

            if location_name is None or location_name == '':
                return Response({"message": "Provide Location Name"}, status=status.HTTP_400_BAD_REQUEST)
            if  page_slug is None or page_slug == '':
                return Response({"message": "Provide Page Slug"}, status=status.HTTP_400_BAD_REQUEST)
            
            loc_obj = get_location_obj(location_name)

            banner_obj = CorporateBanners.objects.filter(page_title__page_slug=page_slug, location=loc_obj).first()
            
            
            if banner_obj:
                serializer = CorporateBannerSerializer(banner_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Page Banner Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exp:
            logger.exception(exp)
            return Response({"message": "Server Error"})
        

class GetHomeBlocks(GenericAPIView):
    queryset = HomeBlockSection.objects.all()
    def get(self, request, *args, **kwargs):
        try: 
            location_name = request.GET.get("location_name")

            if location_name is None or location_name == '':
                return Response({"message": "Provide Location Name"}, status=status.HTTP_400_BAD_REQUEST)
            
            loc_obj = get_location_obj(location_name)

            # location_obj = Location.objects.filter(loc_name=location_name).first()

            home_block_obj_list = HomeBlockSection.objects.filter(location=loc_obj)
            if home_block_obj_list:
                serializer = HomeBlockSectionSerializer(home_block_obj_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Home Block Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as exp:
            logger.exception(exp)
            return Response({"message": "Server Error"})
        

 
class GetBlogs(GenericAPIView):
    queryset = Blog.objects.all()
    def get(self, request, *args, **kwargs):
        try: 
            location_name = request.GET.get("location_name")
            blog_id = request.GET.get("id")

            if blog_id:
                blog_obj = Blog.objects.filter(id=blog_id).first()
                if blog_obj:
                    serializer = BlogSerializer(blog_obj)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Blog Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            else:

                if location_name is None or location_name == '':
                    return Response({"message": "Provide Location Name"}, status=status.HTTP_400_BAD_REQUEST)
                
                loc_obj = get_location_obj(location_name)

                # location_obj = Location.objects.filter(loc_name=location_name).first()
                if blog_id is None or blog_id == '':
                    blog_obj_list = Blog.objects.filter(Q(location=loc_obj) | Q(loc_all=True))
                    if blog_obj_list:
                        serializer = BlogSerializer(blog_obj_list, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Blog Not Found"}, status=status.HTTP_400_BAD_REQUEST)                
            
        
        except Exception as exp:
            logger.exception(exp)
            return Response({"message": "Server Error"})
        

       







#####################################
# class BlockSectionAPIView(APIView):
#     """
#         CRUD API for BlockSection model
#     """

#     def get(self, request):
#         """
#         Get a list BlockSection
#         """
#         id = self.request.query_params.get('id', None)
#         all = self.request.query_params.get('all', None)
#         if id:
#             _details = BlockSection.objects.filter(id=id).first()
#             serializer = BlockSectionSerializer(_details)
#             return Response(serializer.data)

#         search = {}
#         search = custom_filters(self.request, search, [])

#         _list = BlockSection.objects.filter(**search).order_by('-id')
#         page_size = int(request.query_params.get('page_size', 10))
#         paginator = Paginator(_list, page_size)
#         page_number = self.request.query_params.get('page', 1)
#         page = paginator.get_page(page_number)
#         serializer = BlockSectionSerializer(page, many=True)

#         if all == 'true':
#             serializer = BlockSectionSerializer(_list, many=True)
#             return Response({'results': serializer.data})

#         return Response({
#             'count': paginator.count,
#             'next': page.next_page_number() if page.has_next() else None,
#             'previous': page.previous_page_number() if page.has_previous() else None,
#             'results': serializer.data,
#         })


#####################################################
# class LoginView(KnoxLoginView):
#     def post(self, request, *args, **kwargs):

#         if 'id' in request.data:
#             user = User.objects.get(pk=request.data['id'])
#             return Response(user)
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         if user:
#             odict = self.getUserDetails(user, request)
#             return Response(odict)

#     def getUserDetails(self, user, request):

#         odict = collections.OrderedDict()

#         odict['user_id'] = user.pk
#         odict['token'] = AuthToken.objects.create(user)[1]
#         odict['username'] = user.username
#         odict['first_name'] = user.first_name
#         odict['last_name'] = user.last_name
#         return odict

# class LogoutView(APIView):

#     def get(self, request, format=None):
#         import datetime
#         token = request.META.get('HTTP_AUTHORIZATION').replace('Token ', '')
#         request._auth.delete()
#         return Response({'request_status': 1, 'msg': "Logout Success..."}, status=status.HTTP_200_OK)
