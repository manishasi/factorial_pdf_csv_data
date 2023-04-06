from django.contrib import admin
from .models import fact,factmulti

# Register your models here.
@admin.register(fact)
class FactAdmin(admin.ModelAdmin):
    list_display=('id','factorial','value')

@admin.register(factmulti)
class FactmultiAdmin(admin.ModelAdmin):
    list_display=('id','factorial_id','multifactorial','photo','image_tag')

