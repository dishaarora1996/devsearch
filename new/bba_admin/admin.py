from django.contrib import admin
from .models import *

admin.site.register(Location)
admin.site.register(Role)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(CorporateBanners)
admin.site.register(Enquiry)
admin.site.register(Settings)
admin.site.register(Career)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
     list_display=('name','email','role', 'profile_image')

@admin.register(EmployeeLocationAssignment)
class EmployeeLocationAssignmentAdmin(admin.ModelAdmin):
     list_display=('employee_id','location_id')

     
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
     list_display=('name','location', 'location_menu_id')



@admin.register(LocationMenuMaster)
class LocationMenuMasterAdmin(admin.ModelAdmin):
     list_display=('id', 'location_menu_name')


@admin.register(CorporatePages)
class CorporatePagesAdmin(admin.ModelAdmin):
     list_display=('page_title','location')

@admin.register(LocationMenuAssignment)
class LocationMenuAssignmentAdmin(admin.ModelAdmin):
     list_display=('menu_id','location_id')


@admin.register(LocationPostalCodeMapping)
class LocationPostalCodeMappingAdmin(admin.ModelAdmin):
     list_display=('location_id','postal_code')


@admin.register(LocationWebsite)
class LocationWebsiteAdmin(admin.ModelAdmin):
     list_display=('location','deleted', 'location_admin', 'url_abbr')

@admin.register(PagesMenuAssignment)
class PagesMenuAssignmentAdmin(admin.ModelAdmin):
     list_display=('menu_id', 'page_id')


@admin.register(AdminMenu)
class SidebarMenuAdmin(admin.ModelAdmin):
     list_display=('admin_menu_id', 'admin_menu_name', 'parent_id', 'can_add', 'can_edit', 'can_delete', 'can_view', 'update_permission')


@admin.register(AdminMenuPermission)
class AdminMenuPermissionAdmin(admin.ModelAdmin):
     list_display=('admin_menu_id', 'role_id', 'can_add', 'can_edit', 'can_delete', 'can_view', 'update_permission')



class BlogAdmin(admin.ModelAdmin):
    list_display = ("blog_title", "location","loc_all")
    prepopulated_fields = {"blog_slug": ("blog_title",)}  # new

admin.site.register(Blog, BlogAdmin)

class HomeBlockSectionAdmin(admin.ModelAdmin):
    list_display = ("block_name", "slug")
    prepopulated_fields = {"slug": ("block_name",)}  # new

admin.site.register(HomeBlockSection, HomeBlockSectionAdmin)