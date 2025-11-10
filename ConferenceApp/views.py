from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Conference, Submission
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import ConferenceModel, SubmissionForm
from django.contrib.auth.mixins import UserPassesTestMixin
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

class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    context_object_name = "submissions"
    template_name = "submissions/submissionListe.html"

    def get_queryset(self):
        # Afficher seulement les soumissions de l'utilisateur connecté
        return Submission.objects.filter(user_id=self.request.user).order_by("-submission_date")


# 2. Détail d'une soumission
class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    context_object_name = "submission"
    template_name = "submissions/submissionDetail.html"


#  3. Ajouter une soumission
class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"
    success_url = reverse_lazy("submission_liste")

    def get_initial(self):
        initial = super().get_initial()
        conference_id = self.kwargs.get("conference_id")
        if conference_id:
            initial["conference_id"] = conference_id
        return initial

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)



#  4. Modifier une soumission
class SubmissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"
    success_url = reverse_lazy("submission_liste")

    def test_func(self):
        submission = self.get_object()
        # Seul l'auteur peut modifier sa soumission
        # et uniquement si elle n’est ni acceptée ni rejetée
        return (
            submission.user_id == self.request.user
            and submission.status not in ["accepted", "rejected"]
        )

