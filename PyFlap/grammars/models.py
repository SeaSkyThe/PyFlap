from turtle import right
from django.db import models

# Create your models here.
class Grammar(models.Model):
    name = models.CharField(max_length=30, default="grammar")

class Rule(models.Model):
    grammar = models.ForeignKey(Grammar, models.CASCADE, related_name="rules")
    left_side = models.CharField(max_length=30)
    right_side = models.CharField(max_length=30)


