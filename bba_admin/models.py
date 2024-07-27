from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


STATUS = (
    ("Active", "Active"),
    ("Inactive", "Inactive")
)

TYPE = (
    ("Corporate", "Corporate"),
    ("Location", "Location")
)

LINK_TYPE = (
    ("Internal", "Internal"),
    ("External", "External"),
)

MENU_POSITION = (
    ("Top", "Top"),
    ("Bottom", "Bottom"),
    ("Both", "Both")
)

MENU_SUB_POSITION = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3)
)


class Country(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="country")

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,
                              null=True, blank=True, related_name="state")

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    loc_name = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    type = models.CharField(max_length=20, choices=TYPE, default="Location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loc_name
    


class LocationPostalCodeMapping(models.Model):
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_id.loc_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_image/", null=True, blank=True)
    emp_address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmployeeLocationAssignment(models.Model):
    employee_id = models.ForeignKey('Employee', on_delete=models.CASCADE, blank=True, null=True)
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menu(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    location_menu_id = models.ForeignKey('LocationMenuMaster', on_delete=models.CASCADE, blank=True, null=True)
    menu_position = models.CharField(max_length=200, choices=MENU_POSITION, default="Top")
    menu_sub_position = models.CharField(max_length=200, choices=MENU_SUB_POSITION, default=0)
    top_ordering = models.IntegerField(blank=True, null=True)
    bottom_ordering = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    menu_link_type = models.CharField(max_length=100, choices=LINK_TYPE, null=True, blank=True, default="Internal")
    menu_link_url = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    page = models.ForeignKey('CorporatePages', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'location')

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return str(self.location_menu_id.location_menu_name)
    
class LocationMenuMaster(models.Model):
    location_menu_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_menu_name


class AdminMenuPermission(models.Model):
    admin_menu_id = models.ForeignKey('AdminMenu', on_delete=models.CASCADE, blank=True, null=True)
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, blank=True, null=True)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="permission_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="permission_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdminMenu(models.Model):
    admin_menu_id = models.IntegerField()
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    admin_menu_name = models.CharField(max_length=255, blank=True, null=True)
    menu_url = models.CharField(max_length=255, blank=True, null=True)
    menu_icon = models.CharField(max_length=255, blank=True, null=True)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin_menu_name


class CorporatePages(models.Model):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    page_slug = models.SlugField(max_length=200)
    description = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="corporate_pages_location", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="corporate_pages_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="corporate_pages_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_title


class HomeBlockSection(models.Model):
    block_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="block_section_location",  blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="block_section_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="block_section_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"{self.block_name} {self.location}"

    class Meta:
        unique_together = ('slug', 'location',)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.block_name)
        return super().save(*args, **kwargs)



class CorporateBanners(models.Model):
    page_title = models.ForeignKey('CorporatePages', on_delete=models.CASCADE, blank=True, null=True)
    banner_image = models.ImageField(upload_to="banner_image/", null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="corporate_banners_location", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="corporate_banners_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="corporate_banners_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_title.page_title


class LocationWebsite(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    url_abbr = models.CharField(max_length=255, blank=True, null=True)
    location_admin = models.ForeignKey('Employee', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    deleted = models.BooleanField(null=True, blank=True, default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="location_website_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="location_website_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location.loc_name


class LocationMenuAssignment(models.Model):
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    menu_id = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_id.loc_name


class PagesMenuAssignment(models.Model):
    page_id = models.ForeignKey('CorporatePages', on_delete=models.CASCADE, blank=True, null=True)
    menu_id = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=True, null=True)
    menu_link_type = models.CharField(max_length=20, choices=LINK_TYPE, null=True, blank=True)
    menu_link_url = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_id.name


class Enquiry(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Settings(models.Model):
    corporate_site_title = models.CharField(max_length=255, null=True, blank=True)
    footer_copyright = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to="website_logo/", null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.corporate_site_title
    

class Career(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    career_file = models.FileField(upload_to='career/', null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    

class Blog(models.Model):
    blog_title = models.CharField(max_length=255, null=True, blank=True)
    blog_slug = models.SlugField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    blog_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    meta_keyword = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    loc_all = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_title
    
    def save(self, *args, **kwargs):
        value = self.blog_title
        self.blog_slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


    


