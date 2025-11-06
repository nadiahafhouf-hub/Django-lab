from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Conference
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import ConferenceModel
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def all_conference(req):
    conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conferences})

class ConferenceListe(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="Conference/liste.html"

class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="Conference/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model=Conference
    template_name="Conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url = reverse_lazy("conferecne_liste")#si l'ajout est fait avec succes , on redirect vers une autre page 

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model=Conference
    template_name="Conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url = reverse_lazy("conferecne_liste")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name="Conference/conference_delete.html"
    success_url = reverse_lazy("conferecne_liste")

