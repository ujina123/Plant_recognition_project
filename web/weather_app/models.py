from django.db import models

class Weather(models.Model):
    weatherid = models.AutoField(db_column='weatherID', primary_key=True)  # Field name made lowercase.
    areano = models.BigIntegerField(db_column='areaNo')  # Field name made lowercase.
    si = models.CharField(max_length=30)
    time = models.IntegerField()
    condi = models.CharField(max_length=30)
    isday = models.IntegerField(db_column='isDay', blank=True, null=True)  # Field name made lowercase.
    temp = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    rainratio = models.IntegerField(db_column='rainRatio', blank=True, null=True)  # Field name made lowercase.
    snowratio = models.IntegerField(db_column='snowRatio', blank=True, null=True)  # Field name made lowercase.
    uv = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
