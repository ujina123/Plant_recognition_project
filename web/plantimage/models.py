# JngMkk
from django.db import models
from finalproject.models import AuthUser, Plants
from django.utils.translation import gettext_lazy

class PlantModel(models.Model):
    plmodelid = models.AutoField(primary_key=True, db_column="plmodelid")
    userid = models.ForeignKey(AuthUser, null=True, on_delete=models.CASCADE, db_column="userid")
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(gettext_lazy("image"), blank=True, upload_to="plantimages")
    plantid = models.ForeignKey(Plants, on_delete=models.CASCADE, null=True, db_column="plantid")
    accuracy = models.FloatField(null=True)
    outimage = models.ImageField(gettext_lazy("image"), null=True, upload_to="plant_out")

    class Meta:
        db_table = "plantmodel"