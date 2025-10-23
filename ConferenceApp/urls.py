from django.urls import path
from .views import *
#from . import views

urlpatterns=[
    #path("liste/",views.all_conference,name="conference_liste"),
    path("liste/",ConferenceListe.as_view(),name="conferecne_liste"),
    path("details/<int:pk>/",ConferenceDetail.as_view(),name="conference_detail"),
    path("form/",ConferenceCreate.as_view(),name="conference_add"),
    path("edit/<int:pk>/",ConferenceUpdate.as_view(),name="conference_edit"),
    path("delete/<int:pk>/",ConferenceDelete.as_view(),name="conference_delete") 
]