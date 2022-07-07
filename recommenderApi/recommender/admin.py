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

@admin.register(models.CompanyOwner)
class CompanyOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    search_fields = ('user', 'company')

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company')
    search_fields = ('id', 'name', 'company')

@admin.register(models.ProductOwner)
class ProductOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user', 'product')

@admin.register(models.Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'price')
    search_fields = ('id', 'name', 'company')

@admin.register(models.PReview)
class PReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'productId')
    search_fields = ('id', 'userId', 'productId')
    list_filter = ('productId',)

@admin.register(models.Prev_Likes)
class Prev_LikesAdmin(admin.ModelAdmin):
    list_display = ('userId', 'reviewId')
    search_fields = ('userId', 'reviewId')
    list_filter = ('userId', 'reviewId')

@admin.register(models.CReview)
class CReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'companyId')
    search_fields = ('id', 'userId', 'companyId')
    list_filter = ('companyId',)

@admin.register(models.Crev_Likes)
class Crev_LikesAdmin(admin.ModelAdmin):
    list_display = ('userId', 'reviewId')
    search_fields = ('userId', 'reviewId')
    list_filter = ('userId', 'reviewId')

@admin.register(models.PQuestion)
class PQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'productId')
    search_fields = ('id', 'userId', 'productId')
    list_filter = ('productId',)

@admin.register(models.Pques_Upvotes)
class Pques_UpvotesAdmin(admin.ModelAdmin):
    list_display = ('userId', 'questionId')
    search_fields = ('userId', 'questionId')
    list_filter = ('userId', 'questionId')

@admin.register(models.CQuestion)
class CQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'companyId')
    search_fields = ('id', 'userId', 'companyId')
    list_filter = ('companyId',)

@admin.register(models.Cques_Upvotes)
class Cques_UpvotesAdmin(admin.ModelAdmin):
    list_display = ('userId', 'questionId')
    search_fields = ('userId', 'questionId')
    list_filter = ('userId', 'questionId')

