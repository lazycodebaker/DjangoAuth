
from django.contrib import admin
from user.models import UserModel

@admin.register(UserModel)
class UserAdminModel(admin.ModelAdmin):
    list_display = ('id','user','is_verified','joined_on')
