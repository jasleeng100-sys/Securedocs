from django.contrib import admin
from .models import Student, Document, AdminUser, Contact



@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'admin_id', 'password')
    search_fields = ('name', 'admin_id', 'password')
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'f_name',
        'email',
        'mobile',
        'roll',
        'branch',
        'year',        
        'semester'    
    )

    search_fields = (
        'first_name',
        'f_name',
        'email',
        'roll'
    )

    list_filter = (
        'branch',
        'year',     
        'semester'     
    )

    ordering = ('first_name',)
    list_per_page = 5


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'aadhar',
        'caste',
        'tenth',
        'plus2',
        'income'
    )
    search_fields = ('student__first_name', 'student__roll')
    list_filter = ('student__branch',)
    list_per_page = 5


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


