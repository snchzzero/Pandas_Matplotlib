from django.db import models

class ModelAction(models.Model):
    Analysis_Model = models.CharField(max_length=30, default="novalue", blank=True)
    ShowWebTab_Model = models.CharField(max_length=30, default="novalue", blank=True)
    SendDateGS_Model = models.CharField(max_length=30, default="novalue", blank=True)
    CreatePlot_Model = models.CharField(max_length=30, default="novalue", blank=True)
    ShowPlot_Model = models.CharField(max_length=30, default="novalue", blank=True)



class ModelSort(models.Model):
    sorts_1_Model = models.CharField(max_length=30, default="area")  # ASC - по возрастанию, DESC - убыванию
    ASC_DESC_1_Model = models.CharField(max_length=30, default="ASC")
    sorts_2_Model = models.CharField(max_length=30, default="cluster")
    ASC_DESC_2_Model = models.CharField(max_length=30, default="ASC")
    sorts_3_Model = models.CharField(max_length=30, default="cluster name")
    ASC_DESC_3_Model = models.CharField(max_length=30, default="ASC")
    sorts_4_Model = models.CharField(max_length=30, default="count")
    ASC_DESC_4_Model = models.CharField(max_length=30, default="DESC")
    Sort_Default_Model = models.CharField(max_length=30, default="novalue", blank=True)  # сортировка по умолчанию