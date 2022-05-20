from django.contrib import admin
from recommender import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'PR', 'CR', 'PQ', 'CQ')
    search_fields = ('id', 'name')

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company')
    search_fields = ('id', 'name', 'company')

@admin.register(models.Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'price')
    search_fields = ('id', 'name', 'company')

@admin.register(models.PReview)
class PReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'productId')
    search_fields = ('id', 'userId', 'productId')


@admin.register(models.CReview)
class CReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'companyId')
    search_fields = ('id', 'userId', 'companyId')


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'productId')
    search_fields = ('id', 'userId', 'productId')

