from django import forms

class RentalPriceForm(forms.Form):
    year=forms.IntegerField(label="Year")
    bhk = forms.IntegerField(label='BHK',required=True)
    size = forms.IntegerField(label='Size (in sq ft)')
    current_floor = forms.IntegerField(label='Floor')
    bathrooms=forms.IntegerField(label="Bathrooms")
    area_locality = forms.CharField(label='Area Locality')
    city = forms.CharField(label='City')
    furnished_status = forms.ChoiceField(choices=[("Furnished Status","Furnished Status"),('Furnished', 'Furnished'), ('Unfurnished', 'Unfurnished'),('Semi-Furnished', 'Semi-Furnished')], label='Furnished Status')