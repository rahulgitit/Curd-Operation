from django.contrib import admin
from account.models import Account
# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_no', 'address', )