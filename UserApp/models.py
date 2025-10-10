from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid

# Create your models here.
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","central.com"] 
    if email.split("@")[1] not in domaine:
        raise ValidationError("Email domain is not allwoed")

name_validators = RegexValidator(
    regex=r'^[A-Za-z\s-]+$',
    message='Name must contain only letters, spaces.'
)

class User (AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True)
    first_name = models.CharField(max_length=50, validators=[name_validators])
    last_name = models.CharField(max_length=50, validators=[name_validators])
    email = models.EmailField(max_length=100,validators=[verify_email])
    affiliation = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    ROLE=[('participant','Participant'),('comitte','organizing comitee member')]
    role=models.CharField(max_length=50,choices=ROLE,default='participant')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self,*args,**kwargs): #fct pré-definie pour ajouter un utilisateur dans ce cas là
        #*args forme tuple et **kwargs forme dictionnaire
        if not self.user_id:
            new_id=generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_user_id()
            self.user_id=new_id
        super().save(*args,**kwargs)

    #submissions=models.ManyToManyField('ConferenceApp.Conference',through='Submission')
    #organizing_committees=models.ManyToManyField('ConferenceApp.Conference',through='OrganizingCommittee')

class OrganizingCommittee(models.Model):
    user=models.ForeignKey('UserApp.User',on_delete=models.CASCADE,related_name='committees')
    conference=models.ForeignKey('ConferenceApp.Conference',on_delete=models.CASCADE,related_name='committees')
    CROLE=[('chair','Chair'),('co-chair','Co-Chair'),('member','Member')]
    commitee_role=models.CharField(max_length=50,choices=CROLE)
    date_joined=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)