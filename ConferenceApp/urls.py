from django.urls import path
from .views import *
#from . import views

urlpatterns = [
    # Conferences
    path("conference/liste/", ConferenceListe.as_view(), name="conferecne_liste"),
    path("conference/details/<int:pk>/", ConferenceDetail.as_view(), name="conference_detail"),
    path("conference/form/", ConferenceCreate.as_view(), name="conference_add"),
    path("conference/edit/<int:pk>/", ConferenceUpdate.as_view(), name="conference_edit"),
    path("conference/delete/<int:pk>/", ConferenceDelete.as_view(), name="conference_delete"),

    # Submissions
    path("submission/liste/", SubmissionListView.as_view(), name="submission_liste"),
    path("submission/details/<str:pk>/", SubmissionDetailView.as_view(), name="submission_detail"),
    #path("submission/form/", SubmissionCreateView.as_view(), name="submission_add"),
    path("submission/form/<int:conference_id>/", SubmissionCreateView.as_view(), name="submission_add"),
    path("submission/edit/<str:pk>/", SubmissionUpdateView.as_view(), name="submission_edit"),
]
