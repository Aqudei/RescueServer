from django.db import models

# Create your models here.


class EvacuationCenter(models.Model):
    CenterName = models.CharField(max_length=128)
    Address = models.TextField()
    Limit = models.IntegerField(default=100)
    Photo = models.ImageField(null=True)


class Person(models.Model):
    FirstName = models.CharField(max_length=32)
    MiddleName = models.CharField(max_length=32)
    LastName = models.CharField(max_length=32)
    Birthday = models.CharField(max_length=32, null=True, blank=True)
    BloodType = models.CharField(max_length=4)
    Address = models.TextField(default='', blank=True)
    Photo = models.ImageField(null=True)


class Incident(models.Model):
    IncidentName = models.CharField(max_length=32)
    DateOccured = models.DateTimeField(auto_now_add=True)
    Photo = models.ImageField(null=True)


class CheckIn(models.Model):
    When = models.DateTimeField(auto_now_add=True)
    Incident = models.ForeignKey(Incident, related_name='check_ins')
    Person = models.ForeignKey(Person, related_name='check_ins')
    Center = models.ForeignKey(EvacuationCenter, related_name='check_ins')
