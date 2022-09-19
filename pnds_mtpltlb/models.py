from django.db import models

class ModelAction(models.Model):
    Analysis_Model = models.CharField(max_length=30, default="novalue", blank=True)
    ShowWebTab_Model = models.CharField(max_length=30, default="novalue", blank=True)
    SendDateGS_Model = models.CharField(max_length=30, default="novalue", blank=True)
    CreatePlot_Model = models.CharField(max_length=30, default="novalue", blank=True)
    ShowPlot_Model = models.CharField(max_length=30, default="novalue", blank=True)
