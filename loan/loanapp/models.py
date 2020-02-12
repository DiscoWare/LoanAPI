from django.db import models

class Header(models.Model):
    CFRequestId = models.IntegerField()
    RequestDate = models.CharField(max_length = 50)
    CFApiUserId = models.IntegerField(blank=True, null=True)
    CFApiPassword = models.CharField(max_length = 50, blank=True, null=True)
    IsTestLead = models.BooleanField()

    def __str__(self):
        return str(self.CFRequestId)

class CashFlow(models.Model):
    AnnualRevenue = models.FloatField()
    MonthlyAverageBankBalance = models.FloatField()
    MonthlyAverageCreditCardVolume = models.FloatField()

    def __str__(self):
        return str(self.AnnualRevenue)

class BusinessAddress(models.Model):
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100, null=True)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zip = models.IntegerField()

    def __str__(self):
        return self.Address1

class ApplicationBusiness(models.Model):
    SelfReportedCashFlow = models.OneToOneField(CashFlow, on_delete=models.CASCADE)
    Address = models.OneToOneField(BusinessAddress, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    TaxID = models.IntegerField()
    Phone = models.IntegerField()
    NAICS = models.IntegerField()
    HasBeenProfitable = models.BooleanField()
    HasBankruptedInLast7Years = models.BooleanField()
    InceptionDate = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.Name)


class Application(models.Model):
    RequestHeader = models.OneToOneField(Header, on_delete=models.CASCADE)
    Business = models.OneToOneField(ApplicationBusiness, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.CFRequestId)

class BusinessOwner(models.Model):
    Name = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    # HomeAddress = models.OneToOneField(BusinessAddress, on_delete=models.CASCADE)
    DateOfBirth = models.CharField(max_length=100)
    HomePhone = models.IntegerField()
    SSN = models.IntegerField()
    PercentageOfOwnership = models.FloatField()
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='Owners')

    def __str__(self):
        return self.Name

