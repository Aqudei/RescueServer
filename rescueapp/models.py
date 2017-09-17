from django.db import models

# Create your models here.


class EvacuationCenter(models.Model):
    centerName = models.CharField(max_length=128)
    address = models.TextField()
    limit = models.IntegerField(default=100)


class Person(models.Model):
    firstName = models.CharField(max_length=32)
    middleName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    birthday = models.DateField(blank=True, null=True)
    bloodType = models.CharField(max_length=4)
    address = models.TextField(default='', blank=True)


class Incident(models.Model):
    incidentName = models.CharField(max_length=32)
    dateOccured = models.DateTimeField(auto_now_add=True)


class CheckIn(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    incident = models.ForeignKey(Incident, related_name='check_ins')
    person = models.ForeignKey(Person, related_name='check_ins')
    center = models.ForeignKey(EvacuationCenter, related_name='check_ins')
