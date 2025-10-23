from django.urls import path
from .views import (
    ListarSolicitudes, DetalleSolicitud, CrearSolicitud,
    EditarSolicitud, EliminarSolicitud, buscar_solicitud
)

app_name = 'solicitudes'

urlpatterns = [
    path('', ListarSolicitudes.as_view(), name='lista'),
    path('nueva/', CrearSolicitud.as_view(), name='crear'),
    path('<int:pk>/', DetalleSolicitud.as_view(), name='detalle'),
    path('<int:pk>/editar/', EditarSolicitud.as_view(), name='editar'),
    path('<int:pk>/eliminar/', EliminarSolicitud.as_view(), name='eliminar'),
    path('buscar/', buscar_solicitud, name='buscar'),
]
