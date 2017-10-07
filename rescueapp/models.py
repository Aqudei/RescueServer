from django.db import models

# Create your models here.


class EvacuationCenter(models.Model):
    CenterName = models.CharField(max_length=128)
    Address = models.TextField()
    Limit = models.IntegerField(default=100)
    Photo = models.ImageField(null=True)
    Longitude = models.DecimalField(
        null=True, max_digits=18, decimal_places=15)
    Latitude = models.DecimalField(
        null=True, max_digits=18, decimal_places=15)
    InCharge = models.CharField(max_length=128, null=True, blank=True)
    InChargeCellphone = models.CharField(max_length=32, null=True, blank=True)
    Amenities = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.CenterName


class Household(models.Model):
    Address = models.CharField(max_length=128)
    HouseCategory = models.CharField(max_length=32, blank=True, null=True)
    HouseNumber = models.CharField(max_length=8)
    Photo = models.ImageField(null=True)
    IsSafeZone = models.BooleanField(default=True)
    IsTsunamiProne = models.BooleanField(default=False)
    IsEarthquakeProne = models.BooleanField(default=False)
    IsFloodProne = models.BooleanField(default=False)
    IsStormSurgeProne = models.BooleanField(default=False)
    HouseOwnership = models.CharField(max_length=64, blank=True, null=True)


class Person(models.Model):
    NamePrefix = models.CharField(max_length=8, blank=True, null=True)
    NameSuffix = models.CharField(max_length=8, blank=True, null=True)
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
        max_length=128, blank=True, null=True)
    _Household = models.ForeignKey(
        Household, related_name='members', null=True)
    _Center = models.ForeignKey(
        EvacuationCenter, related_name='members', null=True)
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
    NamePrefix = models.CharField(blank=True, null=True, max_length=8)
    NameSuffix = models.CharField(blank=True, null=True, max_length=8)

    def __is_vulnerable(self):
        return len(self.Vulnerabilities) > 0

    is_vulnerable = property(__is_vulnerable)


class Incident(models.Model):
    IncidentName = models.CharField(max_length=32)
    DateOccured = models.DateTimeField(auto_now_add=True)
    Photo = models.ImageField(null=True)
    IsActive = models.BooleanField(default=False)


class CheckIn(models.Model):
    When = models.DateTimeField(auto_now_add=True)
    Incident = models.ForeignKey(Incident, related_name='check_ins')
    Person = models.ForeignKey(Person, related_name='check_ins')
    Center = models.ForeignKey(EvacuationCenter, related_name='check_ins')


class PersonStatus(models.Model):
    Incident = models.ForeignKey(Incident)
    Person = models.ForeignKey(Person)
    Status = models.CharField(blank=True, null=True, max_length=16)

class HouseholdStatus(models.Model):
    Incident = models.ForeignKey(Incident)
    Household = models.ForeignKey(Household)
    Status = models.CharField(blank=True, null=True, max_length=16)
