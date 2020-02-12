from rest_framework import serializers
from .models import *

class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header       
        fields = ('id', 'CFRequestId', 'RequestDate', 'CFApiUserId', 'CFApiPassword', 'IsTestLead')

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = ('id', 'AnnualRevenue', 'MonthlyAverageBankBalance', 'MonthlyAverageCreditCardVolume')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAddress
        fields = ('id', 'Address1', 'Address2', 'City', 'State', 'Zip')

class BusinessSerializer(serializers.ModelSerializer):
    SelfReportedCashFlow = CashFlowSerializer()
    Address = AddressSerializer()

    class Meta:
        model = ApplicationBusiness
        fields = ('id', 'Name', 'SelfReportedCashFlow', 'Address', 'TaxID', 'Phone', 'NAICS', 'HasBeenProfitable', 'HasBankruptedInLast7Years', 'InceptionDate')

    def create(self, validated_data):
        cash_data = validated_data.pop('SelfReportedCashFlow')
        address_data = validated_data.pop('Address')

        SelfReportedCashFlow = CashFlowSerializer.create(CashFlowSerializer(), validated_data=cash_data)
        Address = AddressSerializer.create(AddressSerializer(), validated_data=address_data)

        business, created = ApplicationBusiness.objects.update_or_create(
                                Name=validated_data.pop('Name'), SelfReportedCashFlow=SelfReportedCashFlow,
                                Address=Address, TaxID=validated_data.pop('TaxID'), Phone=validated_data.pop('Phone'), 
                                NAICS=validated_data.pop('NAICS'), HasBeenProfitable=validated_data.pop('HasBeenProfitable'),
                                HasBankruptedInLast7Years=validated_data.pop('HasBankruptedInLast7Years'),
                                InceptionDate=validated_data.pop('InceptionDate'))

        return business

class OwnerSerializer(serializers.ModelSerializer):
    # HomeAddress = AddressSerializer()

    class Meta:
        model = BusinessOwner
        fields = ('id', 'Name', 'FirstName', 'LastName', 'Email', 
                    #'HomeAddress',
                    'DateOfBirth', 'HomePhone', 'SSN', 'PercentageOfOwnership')

    def create(self, validated_data):
        address_data = validated_data.pop('HomeAddress')

        # HomeAddress = AddressSerializer.create(AddressSerializer(), validated_data=address_data)

        owner, created = BusinessOwner.objects.update_or_create(
                        Name=validated_data.pop('Name'), FirstName=validated_data.pop('FirstName'),
                        LastName=validated_data.pop('LastName'), Email=validated_data.pop('Email'),
                        # HomeAddress=HomeAddress,
                        DateOfBirth=validated_data.pop('DateOfBirth'), HomePhone=validated_data.pop('HomePhone'),
                        SSN=validated_data.pop('SSN'), PercentageOfOwnership=validated_data.pop('PercentageOfOwnership'))

        return owner
        

class ApplicationSerializer(serializers.ModelSerializer):
    RequestHeader = HeaderSerializer()
    Business = BusinessSerializer()
    Owners = OwnerSerializer(many=True)

    class Meta:
        model = Application
        fields = ('RequestHeader', 'Business', 'Owners')

    def create(self, validated_data):
            header_data = validated_data.pop('RequestHeader')
            business_data = validated_data.pop('Business')
            owners_data = validated_data.pop('Owners')

            RequestHeader = HeaderSerializer.create(HeaderSerializer(), validated_data=header_data)
            Business = BusinessSerializer.create(BusinessSerializer(), validated_data=business_data)

            application, created = Application.objects.update_or_create(RequestHeader=RequestHeader, Business=Business)

            for owner_data in owners_data:
                BusinessOwner.objects.create(application=application, **owner_data)

            return application
        
