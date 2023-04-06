from django.views.generic import TemplateView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from structures import views

urlpatterns = [
    path('<str:source>/<str:identifier>/models/<int:model>/chains/<str:chain>', views.StructureFileView.as_view()),
    path('<str:source>/<str:identifier>/models/<int:model>', views.StructureFileView.as_view()),
    path('<str:source>/<str:identifier>/chains/<str:chain>', views.StructureFileView.as_view()),
    path('<str:source>/<str:identifier>/', views.StructureFileView.as_view()),
    # Provide SwaggerUI for schema
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    # Provide schema for endpoint
    path('', get_schema_view(
        title="Structures WS",
        description="Web server for retrieval of MMCIF structures according to issued identifier abd database. "
                    "Extracts model and/or chain from structure file.",
        version="0.0.1",
    ), name='openapi-schema'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
