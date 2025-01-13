from django.contrib import admin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name')