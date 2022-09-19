from django.forms import ModelForm
from .models import ModelAction

class Form_Action(ModelForm):
    class Meta:
        model = ModelAction
        fields = ['Analysis_Model', 'ShowWebTab_Model', 'SendDateGS_Model', 'CreatePlot_Model', 'ShowPlot_Model']