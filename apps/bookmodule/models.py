from django.db import models
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(default=timezone.now)
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Author)


class Address(models.Model):
    city = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='students')
