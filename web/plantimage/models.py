import os
from re import M
from django.db import models
from finalproject.models import AuthUser
from django.utils.translation import gettext_lazy

class ImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, null=True, on_delete=models.CASCADE, db_column="username")
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(gettext_lazy("image"), upload_to="images")
    name = models.CharField(max_length=50, null=True)
    accuracy = models.FloatField(null=True)

    class Meta:
        db_table = "plantmodel"