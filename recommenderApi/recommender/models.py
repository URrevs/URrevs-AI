from django.db import models

# Create your models here.
class Review():
    id = models.CharField(max_length=100, primary_key=True)
    userId = models.CharField(max_length=100)
    productId = models.CharField(max_length=100)

    pros = models.TextField(default='')
    cons = models.TextField(default='')

    time = models.FloatField()

    rating = models.IntegerField(default=0)
    rating1 = models.IntegerField(default=0)
    rating2 = models.IntegerField(default=0)
    rating3 = models.IntegerField(default=0)
    rating4 = models.IntegerField(default=0)
    rating5 = models.IntegerField(default=0)
    
    likesCounter = models.IntegerField(default=0)
    commentsCounter = models.IntegerField(default=0)
    hatesCounter = models.IntegerField(default=0)

    isProduct = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.userId} review {self.productId}"

class Question():
    id = models.CharField(max_length=100, primary_key=True)
    userId = models.CharField(max_length=100)
    productId = models.CharField(max_length=100)

    question = models.TextField(default='')
    hasAcceptedAnswer = models.BooleanField(default=False)

    time = models.FloatField()

    upvotesCounter = models.IntegerField(default=0)
    answersCounter = models.IntegerField(default=0)
    hatesCounter = models.IntegerField(default=0)

    isProduct = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.userId} add question on {self.productId}"