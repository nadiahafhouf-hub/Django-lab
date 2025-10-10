from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date
import random, string

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    
    # Room : uniquement lettres et chiffres
    room = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\s]+$',
                message="Le nom de la salle ne doit contenir que des lettres et des chiffres."
            )
        ]
    )

    session_day = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Lien avec la conférence
    conference = models.ForeignKey(
        'ConferenceApp.Conference',
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    def clean(self):
        errors = {}

        # Vérifier que la date de la session est dans l'intervalle de la conférence
        if self.session_day and self.conference:
            if self.session_day < self.conference.start_date or self.session_day > self.conference.end_date:
                errors['session_day'] = "La date de la session doit être comprise entre la date de début et la date de fin de la conférence."

        # Vérifier que l'heure de fin est après l'heure de début
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                errors['end_time'] = "L'heure de fin doit être après l'heure de début."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.title} ({self.session_day})"


