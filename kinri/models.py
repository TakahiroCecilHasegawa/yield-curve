from django.db import models


# Create your models here.

class Kinri(models.Model):
    curve_name = models.CharField(max_length=200)
    curve_currency = models.CharField(max_length=200)
    interest_type = models.CharField(max_length=200)
    curve_date = models.DateTimeField('date')

class Deposit(models.Model):
    kinri = models.ForeignKey(Kinri, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    rate = models.FloatField()

class Future(models.Model):
    kinri = models.ForeignKey(Kinri, on_delete=models.CASCADE)
    contract = models.CharField(max_length=200)
    price = models.FloatField()
    convexity_adj = models.FloatField()

class Ois(models.Model):
    kinri = models.ForeignKey(Kinri, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    bid = models.FloatField()
    offer = models.FloatField()

