# JngMkk
from django.db import models
from finalproject.models import AuthUser
from django.utils.translation import gettext_lazy

class Plantdisease(models.Model):
    diseaseid = models.CharField(db_column='diseaseId', primary_key=True, max_length=3)  # Field name made lowercase.
    diseasename = models.CharField(db_column='diseaseName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    englishname = models.CharField(db_column='englishName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    symptom = models.TextField(blank=True, null=True)
    environment = models.TextField(blank=True, null=True)
    precaution = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plantdisease'

class DiseaseModel(models.Model):
    dsmodelid = models.AutoField(primary_key=True, db_column="dsmodelid")
    userid = models.ForeignKey(AuthUser, null=True, on_delete=models.CASCADE, db_column="userid")
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(gettext_lazy("image"), blank=True, upload_to="diseaseimages")
    diseaseid = models.CharField(max_length=3, null=True, db_column="diseaseid")
    accuracy = models.FloatField(null=True)
    outimage = models.ImageField(gettext_lazy("image"), null=True, upload_to="disease_out")

    class Meta:
        db_table = "diseasemodel"