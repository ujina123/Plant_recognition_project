from django.db import models


class Plants(models.Model):
    plantid = models.AutoField(db_column='plantId', primary_key=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    botanynm = models.CharField(db_column='botanyNm', max_length=255)  # Field name made lowercase.
    info = models.TextField()
    watercycle = models.CharField(db_column='waterCycle', max_length=255)  # Field name made lowercase.
    waterinfo = models.CharField(db_column='waterInfo', max_length=255)  # Field name made lowercase.
    waterexp = models.CharField(db_column='waterExp', max_length=255)  # Field name made lowercase.
    waterexpinfo = models.TextField(db_column='waterExpInfo')  # Field name made lowercase.
    light = models.CharField(max_length=255)
    lightinfo = models.CharField(db_column='lightInfo', max_length=255)  # Field name made lowercase.
    lightexp = models.CharField(db_column='lightExp', max_length=255)  # Field name made lowercase.
    lightexpinfo = models.TextField(db_column='lightExpInfo')  # Field name made lowercase.
    humidity = models.CharField(max_length=255)
    humidinfo = models.CharField(db_column='humidInfo', max_length=255)  # Field name made lowercase.
    humidexp = models.CharField(db_column='humidExp', max_length=255)  # Field name made lowercase.
    humidexpinfo = models.TextField(db_column='humidExpInfo')  # Field name made lowercase.
    tempexp = models.CharField(db_column='tempExp', max_length=255)  # Field name made lowercase.
    tempexpinfo = models.TextField(db_column='tempExpInfo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'plants'