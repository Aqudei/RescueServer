from django.db import models

# Create your models here.


class AddressInfo(models.Model):

    Barangay = models.CharField(max_length=32, blank=True, null=True)
    Municipality = models.CharField(max_length=32, blank=True, null=True)
    Province = models.CharField(max_length=32, blank=True, null=True)
    City = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        abstract = True


class EvacuationCenter(AddressInfo):
    CenterName = models.CharField(max_length=128)
    Address = models.TextField()
    Limit = models.IntegerField(default=100)
    Photo = models.ImageField(null=True)
    Longitude = models.DecimalField(
        null=True, max_digits=18, decimal_places=15)
    Latitude = models.DecimalField(
        null=True, max_digits=18, decimal_places=15)
    InCharge = models.CharField(max_length=256, null=True, blank=True)
    InChargeCellphone = models.CharField(max_length=64, null=True, blank=True)
    Amenities = models.TextField(null=True, blank=True)

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

    def __family_head(self):

        if self.members.filter(IsHead=True).exists():
            return self.members.get(IsHead=True).fullname
        else:
            return ""
    family_head = property(__family_head)

    def __num_fam(self):
        return self.members.count()
    num_fam = property(__num_fam)

    def __num_vulnerable(self):
        return self.members.exclude(Vulnerabilities=u'').exclude(
            Vulnerabilities__isnull=True).count()

    num_vulnerable = property(__num_vulnerable)


class Person(models.Model):
    NamePrefix = models.CharField(max_length=8, blank=True, null=True)
    NameSuffix = models.CharField(max_length=8, blank=True, null=True)
    FirstName = models.CharField(max_length=32)
    MiddleName = models.CharField(max_length=32, blank=True, null=True)
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

    def __fullname(self):
        return "%s, %s %s" % (self.LastName, self.FirstName, self.MiddleName)

    fullname = property(__fullname)


class Incident(models.Model):
    IncidentName = models.CharField(max_length=32)
    DateOccured = models.DateTimeField(auto_now_add=True)
    DateFinished = models.DateTimeField(null=True)
    Photo = models.ImageField(null=True)
    IsActive = models.BooleanField(default=False)
    IncidentType = models.CharField(
        max_length=64, null=True, blank=True)
    EarthquakeMagnitude = models.CharField(
        max_length=8, null=True, blank=True)
    EarthquakeEpicenter = models.CharField(
        max_length=32, null=True, blank=True)
    TyphoonSignal = models.CharField(
        max_length=8, null=True, blank=True)


class CheckIn(models.Model):
    When = models.DateTimeField(auto_now_add=True)
    Incident = models.ForeignKey(Incident, related_name='check_ins')
    Person = models.ForeignKey(Person, related_name='check_ins')
    Center = models.ForeignKey(EvacuationCenter, related_name='check_ins')
    Status = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        default='safe'
    )
    ViaSMS = models.BooleanField(default=False)


class PersonStatus(models.Model):
    Incident = models.ForeignKey(Incident)
    Person = models.ForeignKey(Person)
    Status = models.CharField(blank=True, null=True, max_length=32)


class HouseholdStatus(models.Model):
    Incident = models.ForeignKey(Incident)
    Household = models.ForeignKey(Household)
    Status = models.CharField(blank=True, null=True, max_length=32)

    def __family_head(self):
        return self.Household.family_head

    family_head = property(__family_head)
