from django.forms import ModelForm
from .models import ModelAction, ModelSort

class Form_Action(ModelForm):
    class Meta:
        model = ModelAction
        fields = ['Analysis_Model', 'ShowWebTab_Model', 'SendDateGS_Model', 'CreatePlot_Model', 'ShowPlot_Model']

class Form_Sort(ModelForm):
    class Meta:
        model = ModelSort
        fields = ['sorts_1_Model', 'ASC_DESC_1_Model', 'sorts_2_Model', 'ASC_DESC_2_Model', 'sorts_3_Model',
                  'ASC_DESC_3_Model', 'sorts_4_Model', 'ASC_DESC_4_Model']