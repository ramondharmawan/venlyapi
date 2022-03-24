from django import forms
from ..models import ImageContractNft 

#ini tidak dipakai hanya referensi saja

# Create your forms here.
class DeployNftContractForm(forms.ModelForm):

    class Meta:
        model = ImageContractNft
        fields = ('image')