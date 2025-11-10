from django import forms
from .models import Conference, Submission



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

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["title", "abstract", "keywords", "papier", "conference_id", "user_id"]
        widgets = {
            "abstract": forms.Textarea(attrs={"rows": 4}),
            "keywords": forms.Textarea(attrs={"rows": 2}),
            "user_id": forms.HiddenInput(),  # cache le champ user_id
        }
