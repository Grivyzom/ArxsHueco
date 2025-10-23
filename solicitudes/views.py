from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Solicitud
from .forms import SolicitudForm


# 🧾 Crear una nueva solicitud (usuario)
class CrearSolicitud(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/solicitud_formulario.html'
    success_url = reverse_lazy('solicitudes:lista')

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        solicitud.estado = Solicitud.PENDIENTE
        solicitud.save()
        messages.success(self.request, 'Solicitud registrada correctamente.')
        return super().form_valid(form)


# 📋 Listado de solicitudes (administrador)
class ListarSolicitudes(ListView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_lista.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        queryset = super().get_queryset()
        for solicitud in queryset:
            solicitud.actualizar_estado_por_vigencia()
        return queryset


# 🔎 Detalle de una solicitud
class DetalleSolicitud(DetailView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_detalle.html'
    context_object_name = 'solicitud'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.actualizar_estado_por_vigencia()
        return obj


# ✏️ Actualizar solicitud (cambiar estado o editar datos)
class EditarSolicitud(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/solicitud_formulario.html'
    success_url = reverse_lazy('solicitudes:lista')

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        if solicitud.estado == Solicitud.ACEPTADA and not solicitud.fecha_aceptacion:
            solicitud.fecha_aceptacion = timezone.now()
        solicitud.save()
        messages.success(self.request, 'Solicitud actualizada correctamente.')
        return super().form_valid(form)


# 🗑️ Eliminar solicitud (con confirmación)
class EliminarSolicitud(DeleteView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_confirmar_eliminacion.html'
    success_url = reverse_lazy('solicitudes:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Solicitud eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


# 🔍 Búsqueda por RUT (vendedores)
def buscar_solicitud(request):
    resultado = None
    rut = request.GET.get('rut')
    if rut:
        resultado = Solicitud.objects.filter(rut=rut).first()
        if resultado:
            resultado.actualizar_estado_por_vigencia()
        else:
            messages.warning(request, 'No se encontró ninguna solicitud con ese RUT.')
    return render(request, 'solicitudes/solicitud_buscar.html', {'resultado': resultado})
