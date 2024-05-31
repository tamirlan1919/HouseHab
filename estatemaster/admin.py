from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (CustomUser, PromotionConfig, Builder, SaleResidential, Promotion, RentLongAdvertisement, RentDayAdvertisement, SaleCommercialAdvertisement,
                     Image,RentCommercialAdvertisement,Location)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Number of extra forms to display

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone_number', 'account_type', 'is_staff', 'is_active']
    list_filter = ['account_type', 'is_staff', 'is_active']
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'photo', 'account_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'account_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class PromotionConfigAdmin(admin.ModelAdmin):
    list_display = ['promotion_type', 'cost_per_day', 'discount_7_days', 'discount_14_days', 'discount_30_days']
    search_fields = ['promotion_type']
    ordering = ['promotion_type']

class BuilderAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

class SaleResidentialAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'deal_type', 'type_of_property', 'obj', 'address', 'price']
    list_filter = ['account_type', 'deal_type', 'type_of_property', 'obj']
    search_fields = ['address', 'user__email', 'user__phone_number']
    ordering = ['address']

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['promotion_type', 'duration', 'config', 'calculate_total_cost']
    list_filter = ['promotion_type', 'duration']
    search_fields = ['promotion_type']
    ordering = ['promotion_type']

class RentLongAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'deal_type', 'type_of_property', 'obj', 'address', 'rent_per_month']
    list_filter = ['account_type', 'deal_type', 'type_of_property', 'obj']
    search_fields = ['address', 'user__email', 'user__phone_number']
    ordering = ['address']

class RentDayAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'type_of_deal', 'type_of_property', 'obj', 'address', 'price_day']
    list_filter = ['account_type', 'type_of_deal', 'type_of_property', 'obj']
    search_fields = ['address', 'user__email', 'user__phone_number']
    ordering = ['address']

class SaleCommercialAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'deal_type', 'type_of_property', 'obj', 'address', 'price_all']
    list_filter = ['account_type', 'deal_type', 'type_of_property', 'obj']
    search_fields = ['address', 'user__email', 'user__phone_number']
    ordering = ['address']

class RentCommercialAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'deal_type', 'type_of_property', 'obj', 'address', 'rent_month']
    list_filter = ['account_type', 'deal_type', 'type_of_property', 'obj']
    search_fields = ['address', 'email', 'phone_number']
    ordering = ['address']

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')  # Поля, которые будут отображаться в списке объектов
    search_fields = ('name',)  # Поля, по которым можно выполнить поиск в админ-панели
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение поля slug на основе поля name
    list_filter = ('name',)  # Добавление фильтра по имени
    ordering = ('name',)  # Добавление сортировки по имени
admin.site.register(Location, LocationAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PromotionConfig, PromotionConfigAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(SaleResidential, SaleResidentialAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(RentLongAdvertisement, RentLongAdvertisementAdmin)
admin.site.register(RentDayAdvertisement, RentDayAdvertisementAdmin)
admin.site.register(SaleCommercialAdvertisement, SaleCommercialAdvertisementAdmin)
admin.site.register(RentCommercialAdvertisement, RentCommercialAdvertisementAdmin)
admin.site.register(Image)
