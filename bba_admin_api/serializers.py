from rest_framework import serializers
from bba_admin.models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import APIException

class CorporateMenuSerializer(serializers.ModelSerializer):

    location_menu_name = serializers.SerializerMethodField()
    class Meta:
        model= Menu
        fields = '__all__'

    def get_location_menu_name(self, obj):
        try:
            if obj:
                location_menu_name = obj.location_menu_id.location_menu_name
            else:
                return None
        except Exception:
            return None
        return location_menu_name
    



class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model= Enquiry
        fields = '__all__'



class CorporatePagesSerializer(serializers.ModelSerializer):

    class Meta:
        model= CorporatePages
        fields = '__all__'



class LocationWebsiteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= LocationWebsite
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    location_website = serializers.SerializerMethodField()
    # postal_code = serializers.SerializerMethodField()

    class Meta:
        model= Location
        fields = '__all__'

    def get_location_website(self, obj):
        try:
            if obj:
                # website_obj = obj.locationwebsite_set.first().values()
                return LocationWebsiteSerializer(obj.locationwebsite_set.first()).data
            else:
                return None
        except:
            return None
        
    # def get_postal_code(self, obj):
    #     try:
    #         if obj:
    #             # website_obj = obj.locationwebsite_set.first().values()
    #             return LocationPostalCodeMapping.objects.filter(location_id=obj.id).values_list('postal_code', flat=True)
    #         else:
    #             return None
    #     except:
    #         return None



class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model= Settings
        fields = '__all__'
        
class CorporateBannerSerializer(serializers.ModelSerializer):
    page_title_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model= CorporateBanners
        fields = '__all__'


    def get_page_title_name(self, obj):
        try:
            page_title = obj.page_title.page_title
        except Exception:
            page_title = ''
        return page_title
    
class HomeBlockSectionSerializer(serializers.ModelSerializer):
    """
    HomeBlockSection Model Serializer
    """
    class Meta:
        model = HomeBlockSection
        fields = '__all__'


    
class BlogSerializer(serializers.ModelSerializer):
    """
    Blog Model Serializer
    """
    class Meta:
        model = Blog
        fields = '__all__'



class CareerSerializer(serializers.ModelSerializer):
    """
    Career Model Serializer
    """
    class Meta:
        model = Career
        fields = '__all__'


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(
#             username=data['username'], password=data['password'], active_check=True)
#         if user is not None:
#             if user.is_active:
#                 return user
#             else:
#                 raise APIException('The account has been disabled!')
#         else:
#             raise APIException('Please check the username and password')

