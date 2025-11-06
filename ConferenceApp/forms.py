from django import forms
from .models import Conference



class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']
        labels={
            'name':"Nom de la conférence",
            'theme':"Thématique",
            'description':"Description",
            'location':"Location",
            'start_date':"Date de début de conférence",
            'end_date':"Date de fin de conférence",
        }
        widgets ={
            'name': forms.TextInput(
                attrs={
                    'placeholder':"Enter le nom de la conférence"
                }
            ),
            'start_date': forms.DateInput(
                attrs= {
                    'type':'date',
                    'placeholder':"Date de début de conférence"
                }),
            'end_date': forms.DateInput(
                attrs= {
                    'type':'date',
                    'placeholder':"Date de fin de conférence"
                }
            ),

        }

    