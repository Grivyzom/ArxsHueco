from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re

def validar_rut(value):
    """
    Valida el formato del RUT chileno (sin puntos, con guión).
    Formato esperado: 12345678-9
    """
    # Patrón: 7-8 dígitos, guión, dígito o K
    patron = r'^\d{7,8}-[\dkK]$'
    if not re.match(patron, value):
        raise ValidationError(
            'El RUT debe tener el formato 12345678-9 (sin puntos, con guión).'
        )

def validar_telefono(value):
    """
    Valida el formato del teléfono chileno.
    Acepta formatos: +56912345678 o 912345678
    """
    # Patrón: opcional +56, luego 9 dígitos
    patron = r'^(\+?56)?9\d{8}$'
    if not re.match(patron, value):
        raise ValidationError(
            'El teléfono debe tener formato válido chileno: +56912345678 o 912345678'
        )
        
class Solicitud(models.Model):

    # Posibles Estados
    PENDIENTE = 'PENDIENTE'
    ACEPTADA = 'ACEPTADA'
    RECHAZADA = 'RECHAZADA'
    EXPIRADA = 'EXPIRADA'
    
    ESTADOS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ACEPTADA, 'Aceptada'),
        (RECHAZADA, 'Rechazada'),
        (EXPIRADA, 'Expirada'),
    ]
    
    # Campos de información personal
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[validar_rut],
        help_text='Formato: 12345678-9 (sin puntos, con guión)',
        verbose_name='RUT'
    )
    
    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )
    
    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )
    
    direccion = models.CharField(
        max_length=255,
        verbose_name='Dirección'
    )
    
    telefono = models.CharField(
        max_length=15,
        validators=[validar_telefono],
        help_text='Formato: +56912345678 o 912345678',
        verbose_name='Teléfono'
    )
    
    comuna = models.CharField(
        max_length=100,
        verbose_name='Comuna'
    )
    
    # Campos de control de estado y fechas
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS_CHOICES,
        default=PENDIENTE,
        verbose_name='Estado'
    )
    
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Solicitud'
    )
    
    fecha_aceptacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Aceptación'
    )
    
    # Campos de auditoría
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación'
    )
    
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"{self.rut} - {self.nombres} {self.apellidos} ({self.get_estado_display()})"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del solicitante."""
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def esta_vigente(self):
        """
        Determina si una solicitud ACEPTADA está vigente.
        Una solicitud expira a los 30 días de su aceptación.
        Retorna True si está vigente, False si expiró o None si no aplica.
        """
        if self.estado != self.ACEPTADA or not self.fecha_aceptacion:
            return None  # No aplica para solicitudes no aceptadas
        
        fecha_expiracion = self.fecha_aceptacion + timedelta(days=30)
        return timezone.now() < fecha_expiracion
    
    @property
    def dias_restantes(self):
        """
        Calcula los días restantes de vigencia para una solicitud ACEPTADA.
        Retorna None si no aplica o el número de días (puede ser negativo si expiró).
        """
        if self.estado != self.ACEPTADA or not self.fecha_aceptacion:
            return None
        
        fecha_expiracion = self.fecha_aceptacion + timedelta(days=30)
        diferencia = fecha_expiracion - timezone.now()
        return diferencia.days
    
    def actualizar_estado_por_vigencia(self):
        """
        Actualiza el estado de la solicitud a EXPIRADA si corresponde.
        Este método debe llamarse antes de mostrar las solicitudes.
        Retorna True si se actualizó el estado, False en caso contrario.
        """
        # Solo aplica para solicitudes ACEPTADAS con fecha de aceptación
        if self.estado == self.ACEPTADA and self.fecha_aceptacion:
            if self.esta_vigente == False:  # Explícitamente False, no None
                self.estado = self.EXPIRADA
                self.save(update_fields=['estado', 'fecha_modificacion'])
                return True
        return False
    
    def aceptar_solicitud(self):
        """
        Cambia el estado a ACEPTADA y registra la fecha de aceptación.
        Solo puede aceptarse si está en estado PENDIENTE.
        """
        if self.estado == self.PENDIENTE:
            self.estado = self.ACEPTADA
            self.fecha_aceptacion = timezone.now()
            self.save()
            return True
        return False
    
    def rechazar_solicitud(self):
        """
        Cambia el estado a RECHAZADA.
        Solo puede rechazarse si está en estado PENDIENTE.
        """
        if self.estado == self.PENDIENTE:
            self.estado = self.RECHAZADA
            self.save()
            return True
        return False
    
    def clean(self):
        """
        Validaciones adicionales del modelo.
        """
        super().clean()
        
        # Validar que si el estado es ACEPTADA, debe tener fecha_aceptacion
        if self.estado == self.ACEPTADA and not self.fecha_aceptacion:
            self.fecha_aceptacion = timezone.now()
        
        # Validar que si no está ACEPTADA, no debe tener fecha_aceptacion
        if self.estado != self.ACEPTADA and self.fecha_aceptacion:
            self.fecha_aceptacion = None
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para ejecutar validaciones.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def get_badge_class(self):
        """
        Retorna la clase CSS de Bootstrap para el badge según el estado.
        Útil para los templates.
        """
        clases = {
            self.PENDIENTE: 'bg-warning text-dark',
            self.ACEPTADA: 'bg-success',
            self.RECHAZADA: 'bg-danger',
            self.EXPIRADA: 'bg-secondary',
        }
        return clases.get(self.estado, 'bg-secondary')