from django import forms
from PIAs.models import Profile, Organization, PIA, RiesgoInherente, Risk

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'organization')  # Mandatory fields

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('orgName', 'orgCode')  # Mandatory fields

class NewPIAForm(forms.ModelForm):
    class Meta:
        model = PIA
        fields = ('name',)



class EditRiskForm(forms.ModelForm):
    class Meta:
        model = RiesgoInherente
        fields = ('risk',)
