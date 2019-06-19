import os
import random
from django.db import models


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
class Users(models.Model):
    pass
    

class Products(models.Model):
    # id to be uuid
    name = models.CharField(max_length=100, null=False, default=None)
    price = models.FloatField(null=False, default=None)
    file = models.ImageField(upload_to=uploadFile, blank=False, null=False)

    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name

class AddCard(models.Models):
    # id to be uuid
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
   

class Bought(models.Models):
    # id to be uuid
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
    
