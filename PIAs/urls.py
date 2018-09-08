from django.urls import path, include

from .views import PIAsView, PIAView, PIAsDetailedView, ProjectsView,\
    createPIAView, createRIView, updateRIView,download,createProjectView, GeneratePdf2, deleteRIView, download_catalog

urlpatterns = [
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/new_project', createProjectView.as_view(), name='newProject'),
    path('projects/<pk>', PIAsView.as_view(), name='project'),
    path('projects/<project_pk>/new_pia', createPIAView.as_view(), name='newPIA'),
    path('projects/<project_pk>/<pk>', PIAView.as_view(), name='pia'),
    path('projects/<project_pk>/<pk>/add_risk', createRIView.as_view(), name='addRisk'),
    path('projects/<project_pk>/<pk>/download', download, name='download'),
    path('projects/<project_pk>/<pk>/download_catalog', download_catalog, name='download_cat'),
    path('projects/<project_pk>/<pk>/pdf2', GeneratePdf2.as_view(), name='report'),
    path('projects/<project_pk>/<pia_pk>/<pk>', updateRIView.as_view(), name='editRisk'),
    path('projects/<project_pk>/<pia_pk>/<pk>/delete', deleteRIView, name='deleteRisk'),
    path('projects/<project_pk>/<pia_pk>/', download,name='download'),
    path('projects/PIAs/(?P<pk>\d+)/', PIAsDetailedView.as_view(), name='pia_detail'),
]