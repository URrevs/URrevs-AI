from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS
from recommenderApi.settings import MIN_ITEM, MAX_PREVIEW, MAX_CREVIEW, MAX_PQUESTION, MAX_CQUESTION

# Create your models here.
class User(models.Model):
    id   = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, default='')
    
    PR = models.IntegerField(default=2*ROUND_NUM_OF_REVIEWS//5, 
            validators=[MinValueValidator(MIN_ITEM), MaxValueValidator(MAX_PREVIEW)])
    CR = models.IntegerField(default=ROUND_NUM_OF_REVIEWS//5, 
            validators=[MinValueValidator(MIN_ITEM), MaxValueValidator(MAX_CREVIEW)])
    PQ = models.IntegerField(default=3*ROUND_NUM_OF_REVIEWS//10, 
            validators=[MinValueValidator(MIN_ITEM), MaxValueValidator(MAX_PQUESTION)])
    CQ = models.IntegerField(default=ROUND_NUM_OF_REVIEWS//10, 
            validators=[MinValueValidator(MIN_ITEM), MaxValueValidator(MAX_CQUESTION)])

    def __str__(self) -> str:
        return f"{self.id} {self.name}"
#-----------------------------------------------------------------------------------------------------
class Company(models.Model):
    id      = models.CharField(max_length=100, primary_key=True)
    name    = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name}"
#-----------------------------------------------------------------------------------------------------
class Product(models.Model):
    id          = models.CharField(max_length=100, primary_key=True)
    name        = models.CharField(max_length=100, default='')
    company     = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return f"{self.id} {self.name}"
#-----------------------------------------------------------------------------------------------------
class Mobile(Product):
    price = models.FloatField(default=0.0, null=True, validators=[MinValueValidator(0.0)])
#-----------------------------------------------------------------------------------------------------
class PReview(models.Model):
    id              = models.CharField(max_length=100, primary_key=True)
    userId          = models.ForeignKey(User, on_delete=models.CASCADE)
    productId       = models.ForeignKey(Mobile, on_delete=models.CASCADE)

    pros            = models.TextField(default='')
    cons            = models.TextField(default='')

    time            = models.FloatField()

    rating          = models.IntegerField(default=0)
    rating1         = models.IntegerField(default=0)
    rating2         = models.IntegerField(default=0)
    rating3         = models.IntegerField(default=0)
    rating4         = models.IntegerField(default=0)
    rating5         = models.IntegerField(default=0)
    rating6         = models.IntegerField(default=0)
    
    likesCounter    = models.IntegerField(default=0)
    commentsCounter = models.IntegerField(default=0)
    hatesCounter    = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.userId} review {self.productId}"
#-----------------------------------------------------------------------------------------------------
class Prev_Likes(models.Model):
    userId      = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewId    = models.ForeignKey(PReview, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('userId', 'reviewId'))

    def __str__(self) -> str:
        return f"{self.userId} likes {self.reviewId}"
#-----------------------------------------------------------------------------------------------------
class CReview(models.Model):
    id              = models.CharField(max_length=100, primary_key=True)
    userId          = models.ForeignKey(User, on_delete=models.CASCADE)
    companyId       = models.ForeignKey(Company, on_delete=models.CASCADE)

    pros            = models.TextField(default='')
    cons            = models.TextField(default='')

    time            = models.FloatField()

    rating          = models.IntegerField(default=0)

    likesCounter    = models.IntegerField(default=0)
    commentsCounter = models.IntegerField(default=0)
    hatesCounter    = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.userId} review {self.companyId}"
#-----------------------------------------------------------------------------------------------------
class Crev_Likes(models.Model):
    userId      = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewId    = models.ForeignKey(CReview, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('userId', 'reviewId'))

    def __str__(self) -> str:
        return f"{self.userId} likes {self.reviewId}"
#-----------------------------------------------------------------------------------------------------
class Question(models.Model):
    id                  = models.CharField(max_length=100, primary_key=True)
    userId              = models.CharField(max_length=100)
    productId           = models.CharField(max_length=100)

    question            = models.TextField(default='')
    hasAcceptedAnswer   = models.BooleanField(default=False)

    time                = models.FloatField()

    upvotesCounter      = models.IntegerField(default=0)
    answersCounter      = models.IntegerField(default=0)
    hatesCounter        = models.IntegerField(default=0)

    isProduct           = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.userId} add question on {self.productId}"
