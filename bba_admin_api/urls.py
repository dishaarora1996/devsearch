from django.urls import path
from .views import *


urlpatterns = [
    path('get-general-settings/', GetSettings.as_view(), name='get_general_settings'),
    path('get-page-banner/', GetPageBanner.as_view(), name='get_page_banner'),

    path('get-menu/', GetCorporateMenu.as_view(), name='get_corporate_menu'),
    path('create-enquiry/', CreateEnquiry.as_view(), name='create_enquiry'),
    path('create-career/', CreateCareer.as_view(), name='create_career'),
    path('get-page-content/', GetPageContent.as_view(), name='get_page_content'),
    path('get-location/', GetLocation.as_view(), name='get_location'),
    path('get-home-blocks/', GetHomeBlocks.as_view(), name='get-home-blocks'),
    path('get-blogs/', GetBlogs.as_view(), name='get-blogs'),

    # path('login/', LoginView.as_view(), name='knox_login'),
    # path('logout/', LogoutView.as_view(), name='knox_logout'),
    # path('blocks/', BlockSectionAPIView.as_view(), name='get_block'),
    ]