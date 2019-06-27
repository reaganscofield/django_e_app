import os
import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractUser


def getFileNameExt(filepath):
    baseName = os.path.basename(filepath)
    name, ext = os.path.splitext(baseName)
    return name, ext

def uploadFile(instance, filename):
    new_fileName = random.randint(1,3445565632)
    ext = getFileNameExt(filename)
    finalName = '{new_fileName}{ext}'.format(new_fileName=new_fileName, ext=ext)
    return "{finalName}".format(finalName=finalName)

# Create your models here.
class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, default=None)
    price = models.FloatField(null=False, default=None)
    file = models.ImageField(upload_to=uploadFile, blank=False, null=False)

    active = models.BooleanField(null=False, default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=False, blank=True, null=True, default=None)
    deleted_at = models.DateField(auto_now_add=False, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

class AddCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(Users, on_delete="models.CASCADE")
    product_id = models.ForeignKey(Products, on_delete="models.CASCADE")
    product_name = models.CharField(max_length=100, null=False, default=None)
    product_price = models.FloatField(null=False, default=None)
    number_of_items = models.IntegerField(null=False, default=None)

    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.id
   

class Bought(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(Products, on_delete="models.CASCADE")
    customer_id = models.ForeignKey(Users, on_delete="models.CASCADE")
    payments_id = models.CharField(max_length=100)
    total_paid = models.FloatField(null=False, default=None)
    total_tax = models.FloatField(null=True, default=None)
    total_discount = models.FloatField(null=True, default=None)
    paid_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.id
    
