from django.db import models
from django import forms
import cv2 as cv
import numpy as np
import base64

# Create your models here.

class Block(models.Model):
    
    id = models.AutoField(primary_key=True)
    previous_hash = models.CharField(max_length=64)
    current_hash = models.CharField(max_length=64)
    proof = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField() 
    image_name = models.CharField(max_length=200)
    image_description = models.CharField(max_length=200, default="No description")
    average_hash = models.CharField(max_length=64)
    phash = models.CharField(max_length=64)
    dhash = models.CharField(max_length=64)
    whash = models.CharField(max_length=64)
    colorhash = models.CharField(max_length=64)
    

class BlockChain(models.Model):
    
    id = models.AutoField(primary_key=True)
    block_id = models.ForeignKey(Block, on_delete=models.CASCADE)
    
    
class BlockForm(forms.Form):
    
    image_url = forms.ImageField() 
    image_name = forms.CharField(max_length=200)
    image_description = forms.CharField(max_length=200)
    