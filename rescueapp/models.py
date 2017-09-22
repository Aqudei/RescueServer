from django.db import models

# Create your models here.


class EvacuationCenter(models.Model):
    CenterName = models.CharField(max_length=128)
    Address = models.TextField()
    Limit = models.IntegerField(default=100)
    Photo = models.ImageField(null=True)


class Household(models.Model):
    Address = models.CharField(max_length=128)
    EconomicStatus = models.CharField(max_length=32, blank=True, null=True)
    HouseNumber = models.CharField(max_length=8)


class Person(models.Model):
    FirstName = models.CharField(max_length=32)
    MiddleName = models.CharField(max_length=32)
    LastName = models.CharField(max_length=32)
    Birthday = models.CharField(
        max_length=16, blank=True, null=True, default='')
    BloodType = models.CharField(max_length=4)
    Photo = models.ImageField(null=True)
    Contact = models.CharField(max_length=32)
    Email = models.EmailField(null=True, blank=True)
    Vulnerabilities = models.TextField(null=True, blank=True)
    NationalIdNumber = models.CharField(
        max_length=128, blank=True, default='None')
    _Household = models.ForeignKey(
        Household, related_name='members', null=True)
    IsHead = models.BooleanField(default=False)
    Gender = models.CharField(max_length=8, default='MALE')
    EducationalAttainment = models.CharField(
        max_length=64, blank=True, null=True)
    Allergies = models.CharField(max_length=64, blank=True, null=True)
    CivilStatus = models.CharField(max_length=64, default='SINGLE')
    Occupation = models.CharField(max_length=64, blank=True, null=True)
    # MedicalRecord
    Allergies = models.CharField(blank=True, null=True, max_length=64)
    MedicalCondition = models.CharField(blank=True, null=True, max_length=64)
    MedicineRequired = models.CharField(blank=True, null=True, max_length=64)

    def __is_vulnerable(self):
        return len(self.Vulnerabilities) > 0

    is_vulnerable = property(__is_vulnerable)


class Incident(models.Model):
    IncidentName = models.CharField(max_length=32)
    DateOccured = models.DateTimeField(auto_now_add=True)
    Photo = models.ImageField(null=True)


class CheckIn(models.Model):
    When = models.DateTimeField(auto_now_add=True)
    Incident = models.ForeignKey(Incident, related_name='check_ins')
    Person = models.ForeignKey(Person, related_name='check_ins')
    Center = models.ForeignKey(EvacuationCenter, related_name='check_ins')
