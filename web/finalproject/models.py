from django.db import models

class Plants(models.Model):
    plantid = models.AutoField(db_column='plantID', primary_key=True)  # Field name made lowercase.
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

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class Plantmanage(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, on_delete=models.CASCADE, db_column="username")
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE, db_column="plant")
    nickname = models.CharField(max_length=50)
    meetdate = models.DateField()
    waterdate = models.DateField()

    class Meta:
        db_table = "plantmanage"

    def str(self):
        return str(
            {
                "username": self.username,
                "plantid": self.plantid,
                "nickname": self.nickname,
                "meetdate": self.meetdate,
                "waterdate": self.waterdate
            }
        )