from django.db import models

# Create your models here.


class EvacuationCenter(models.Model):
    CenterName = models.CharField(max_length=128)
    Address = models.TextField()
    Limit = models.IntegerField(default=100)
    Photo = models.ImageField(null=True)


class Household (models.Model):
    Barangay = models.CharField(max_length=24)
    HouseholdNumber = models.IntegerField()
    Category = models.CharField(max_length=16)
    Location = models.CharField(max_length=16)
    Address = models.TextField()
    Photo = models.ImageField(null=True)


class Person(models.Model):
    _Household = models.ForeignKey(
        Household, null=True, related_name='members')
    IsHead = models.BooleanField(default=False)
    FirstName = models.CharField(max_length=32)
    MiddleName = models.CharField(max_length=32)
    LastName = models.CharField(max_length=32)
    Birthday = models.CharField(
        max_length=16, blank=True, null=True, default='')
    BloodType = models.CharField(max_length=4)
    Photo = models.ImageField(null=True)
    Contact = models.CharField(max_length=32)
    Email = models.EmailField(null=True)
    Vulnerabilities = models.TextField(blank=True, null=True)
    IDNumber = models.CharField(max_length=128, blank=True, null=True)
    Sickness = models.CharField(max_length=128, blank=True, null=True)
    Sex = models.CharField(max_length=8)


class Incident(models.Model):
    IncidentName = models.CharField(max_length=32)
    DateOccured = models.DateTimeField(auto_now_add=True)
    Photo = models.ImageField(null=True)


class CheckIn(models.Model):
    When = models.DateTimeField(auto_now_add=True)
    Incident = models.ForeignKey(Incident, related_name='check_ins')
    Person = models.ForeignKey(Person, related_name='check_ins')
    Center = models.ForeignKey(EvacuationCenter, related_name='check_ins')
