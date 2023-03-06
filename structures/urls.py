from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from structures import views

urlpatterns = [
    path('<str:source>/<str:identifier>/models/<int:model>/chains/<str:chain>', views.StructureFile.as_view()),
    path('<str:source>/<str:identifier>/models/<int:model>', views.StructureFile.as_view()),
    path('<str:source>/<str:identifier>/chains/<str:chain>', views.StructureFile.as_view()),
    path('<str:source>/<str:identifier>/', views.StructureFile.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
