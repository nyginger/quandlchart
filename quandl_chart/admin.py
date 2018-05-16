from django.contrib import admin

from .models import API_keys,Items_table, Countries, Indicators

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['category','dataset','symbol','description']
    list_filter = ('dataset','category')
    list_display = ('description','category','subcategory','country','dataset','symbol')

class CountryAdmin(admin.ModelAdmin):
    search_fields=['code','name']
    list_filter=('code','name')
    list_display=('code','name')

admin.site.register(API_keys)
admin.site.register(Items_table, ItemAdmin)
admin.site.register(Countries, CountryAdmin)
admin.site.register(Indicators)
