from django.db import models

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