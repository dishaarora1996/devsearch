from django.urls import path
from bba_admin.views.admin_role_view import *
from .views.admin_user_view import *
from .views.corporate_banner_view import *
from .views.corporate_menu_view import *
from .views.corporate_pages_view import *
from .views.location_website_view import *
from .views.location_view import *
from .views.user_profile_view import *
from .views.enquiries_view import *
from .views.settings_view import *
from .views.career_view import *
from .views.home_blocks_view import *
from .views.blog_view import *





urlpatterns = [
    path('login', user_login, name='user-login'),
    path('logout', user_logout, name='user-logout'),
    path('', dashboard, name='dashboard'),
    path('recover-password', recover_password, name='recover-password'),
    path('reset-password', reset_password, name='reset-password'),
    path('admin-users', admin_users, name='admin-users'),
    path('admin-role', admin_role, name='admin-role'),
    path('add-admin-user', add_admin_user, name='add-admin-user'),
    path('edit-admin-user/<int:emp_id>', edit_admin_user, name='edit-admin-user'),
    path('delete-admin-user/<int:emp_id>', delete_admin_user, name='delete-admin-user'),
    path('admin-user-search', admin_user_search, name='admin-user-search'),
    path('add-admin-role', add_admin_role, name='add-admin-role'),
    path('edit-admin-role/<int:role_id>', edit_admin_role, name='edit-admin-role'),
    path('delete-admin-role/<int:role_id>', delete_admin_role, name='delete-admin-role'),
    path('manage-role-permission/<int:role_id>', manage_role_permission, name='manage-role-permission'),
    path('manage-location', manage_location, name='manage-location'),
    path('location-search', location_search, name='location-search'),
    path('add-location', add_location, name='add-location'),
    path('edit-location/<int:location_id>', edit_location, name='edit-location'),
    path('delete-location/<int:location_id>', delete_location, name='delete-location'),
    path('get_city_list', get_city_list, name='get_city_list'),
    path('get_location_admin_list', get_location_admin_list, name='get_location_admin_list'),
    path('manage-pages/<str:location>', manage_corporate_pages, name='manage-pages'),
    path('manage-home-blocks/<str:location>', manage_home_blocks, name='manage-home-blocks'),
    path('add-corporate-pages', add_corporate_pages, name='add-corporate-pages'),
    path('edit-corporate-pages/<int:page_id>', edit_corporate_pages, name='edit-corporate-pages'),
    path('edit-home-block/<int:block_id>/<str:location>', edit_home_block, name='edit-home-block'),
    path('change-home-block-status/<str:location>', change_home_block_status, name='change-home-block-status'),
    path('change-corporate-pages-status', change_corporate_pages_status, name='change-corporate-pages-status'),
    path('change-corporate-banner-status', change_corporate_banner_status, name='change-corporate-banner-status'),
    path('change-admin-role-status', change_admin_role_status, name='change-admin-role-status'),
    path('change-admin-user-status', change_admin_user_status, name='change-admin-user-status'),
    path('change-location-status', change_location_status, name='change-location-status'),
    path('change-location-website-status', change_location_website_status, name='change-location-website-status'),
    path('manage-banners/<str:location>', manage_banners, name='manage-banners'),
    path('edit-banners/<int:banner_id>/<str:location>', edit_banners, name='edit-banners'),
    path('delete-banners/<int:banner_id>/<str:location>', delete_banners, name='delete-banners'),
    path('add-banners/<str:location>', add_banners, name='add-banners'),
    
    path('manage-corporate-menu', manage_corporate_menu, name='manage-corporate-menu'),
    path('link-corporate-menu', link_corporate_menu, name='link-corporate-menu'),
    path('delete-corporate-menu/<int:menu_id>', delete_corporate_menu, name='delete-corporate-menu'),
    path('edit-corporate-menu/<int:menu_id>', edit_corporate_menu, name='edit-corporate-menu'),
    path('manage-location-website', manage_location_website, name='manage-location-website'),
    path('add-location-website', add_location_website, name='add-location-website'),
    # path('edit-location-pages/<int:location_id>', edit_location_pages, name='edit-location-pages'),
    path('launch-location-website/<location_website_details>', launch_location_website, name='launch-location-website'),
    path('delete-location-website/<int:location_website_id>', delete_location_website, name='delete-location-website'),
    path('edit-location-website/<int:location_website_id>', edit_location_website, name='edit-location-website'),
    path('manage-enquiries', manage_enquiries, name='manage-enquiries'),
    path('manage-career', manage_career, name='manage-career'),
    path('career-detail/<int:id>', career_detail, name='career-detail'),
    path('career-file-download/<int:id>', career_file_download, name='career-file-download'),
    path('reply_enquiry', reply_enquiry, name='reply-enquiry'),
    path('manage-settings', manage_settings, name='manage-settings'),
    path('manage-blog', manage_blog, name='manage-blog'),
    path('add-blog', add_blog, name='add-blog'),
    path('edit-blog/<int:blog_id>', edit_blog, name='edit-blog'),
    path('delete-blog/<int:blog_id>', delete_blog, name='delete-blog')

]