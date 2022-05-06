from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class User(models.Model):
    id   = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, default='')
    mobile = models.ForeignKey('Mobile', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.id} {self.name}"

class Company(models.Model):
    id      = models.CharField(max_length=100, primary_key=True)
    name    = models.CharField(max_length=100, default='')

    def __str__(self) -> str:
        return f"{self.name}"

class Product(models.Model):
    id          = models.CharField(max_length=100, primary_key=True)
    name        = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.name}"

class Mobile(Product):
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

class Review(models.Model):
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
    
    likesCounter    = models.IntegerField(default=0)
    commentsCounter = models.IntegerField(default=0)
    hatesCounter    = models.IntegerField(default=0)

    isProduct       = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.userId} review {self.productId}"

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
