from django.contrib import admin
from . import models

# Register your models here.
class User_attribute(admin.ModelAdmin):
    list_display = ['user_email']
    list_per_page = 10  

class Pregnat_ban_list(admin.ModelAdmin):
    list_display = ['pregnat_medicine_code']
    list_per_page = 10   

class Overlap_ban_list(admin.ModelAdmin):
    list_display = ['over_medicine_code']
    list_per_page = 10 

class Overlap_caution_list(admin.ModelAdmin):
    list_display = ['over_caution_medicine_code_A', 'over_caution_medicine_name_A']
    list_per_page = 10 

class Medicine_list(admin.ModelAdmin):
    list_display = ['pre_medicine','item_name', 'edi_code']
    list_per_page = 10 

class Disease_list(admin.ModelAdmin):
    list_display = ['disease_code','disease_name', 'disease_prescription']
    list_per_page = 30 

class Open_over_ban_list(admin.ModelAdmin):
    list_display = ['ingr_code', 'ingr_kor_name', 'item_name']
    list_per_page = 30 

class Open_Efficacy_group_overlap_list(admin.ModelAdmin):
    list_display = ['ingr_code','item_name']
    list_per_page = 30 

class Open_pregnat_ban_list(admin.ModelAdmin):
    list_display = ['ingr_code', 'ingr_kor_name', 'item_name']
    list_per_page = 30 

admin.site.register(models.User, User_attribute)
admin.site.register(models.Family)
admin.site.register(models.Disease, Disease_list)
admin.site.register(models.Pregnat_ban, Pregnat_ban_list)
admin.site.register(models.Overlap_ban, Overlap_ban_list)
admin.site.register(models.Overlap_caution, Overlap_caution_list)
admin.site.register(models.Prescription)
admin.site.register(models.Medicine, Medicine_list)
admin.site.register(models.OpenOverBan, Open_over_ban_list)
admin.site.register(models.OpenEfficacyGroupOverlap, Open_Efficacy_group_overlap_list)
admin.site.register(models.OpenPregnatBan, Open_pregnat_ban_list)
