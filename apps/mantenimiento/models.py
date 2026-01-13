from django.db import models
from django.conf import settings
from apps.lugar.models import Lugar
from apps.equipo.models import Equipo
from django.utils import timezone

class Ticket(models.Model):
    id_ticket = models.AutoField(primary_key=True, db_column='id_ticket')
    id_users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_users')
    id_equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_equipo')
    
    id_lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lugar')
        # Agregamos choices para el estado del ticketF
    TIPO_SOPORTE_CHOICES = [
        ('preventivo', 'Mantenimiento Preventivo'),
        ('correctivo', 'Mantenimiento Correctivo'),
        ('recarga_tinta', 'Recarga de Tinta'),
        ('tonner', 'Recarga de Tonner'),
        ('soporte_usuario', 'Soporte al Usuario'),
    ]
    tipo_soporte = models.CharField(
        max_length=50, 
        choices=TIPO_SOPORTE_CHOICES, 
        null=True, 
        blank=True
    )
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media',  # por defecto media
        db_column='prioridad'
    )
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    estado_ticket = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        db_column='estado_ticket'
    )
    descripcion = models.TextField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)
    solucion_aplicada = models.TextField(null=True, blank=True)
    observaciones_tecnicas = models.TextField(null=True, blank=True)
    insumos_utilizados = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    tiempo_estimado = models.DurationField(null=True, blank=True)
    tiempo_real = models.DurationField(null=True, blank=True)
    comentario_usuario = models.TextField(null=True, blank=True)
    CANCELACION_CHOICES = [
        ('usuario', 'Cancelado por Usuario'),
        ('tecnico', 'Cancelado por Técnico'),
    ]
    cancelado_por = models.CharField(
        max_length=20,
        choices=CANCELACION_CHOICES,
        blank=True,
        null=True,
        db_column='cancelado_por'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='modificado_por',
        db_column='modificado_por'
    )
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    class Meta:
        db_table = 'ticket'

    def __str__(self):
        return f'Ticket {self.id_ticket}'

# Tabla comentarios
class ComentarioTicket(models.Model):
    id = models.AutoField(primary_key=True)
    comentario = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        db_table = 'comentario_ticket'

    def __str__(self):
        return f'Comentario {self.id} - Ticket {self.ticket.id_ticket}'

# Tabla historial de cambios de estado
class HistorialTicket(models.Model):
    id = models.AutoField(primary_key=True)
    estado_anterior = models.CharField(max_length=50)
    estado_nuevo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='historial')

    class Meta:
        db_table = 'historial_ticket'

    def __str__(self):
        return f'Historial {self.id} - Ticket {self.ticket.id_ticket}'


class ReporteMantenimiento(models.Model):
    id_reporte = models.AutoField(primary_key=True, db_column='id_reporte')
    id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='id_ticket')
    id_equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_equipo')
    
    id_elaborado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='elaborados', db_column='id_elaborado_por')
    id_aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='aprobados', db_column='id_aprobado_por')
    id_lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lugar')
    fecha_mantenimiento = models.DateTimeField(null=True, blank=True, db_column='fecha_mantenimiento')
    descripcion = models.CharField(max_length=300, blank=True, null=True, db_column='descripcion')
    observaciones = models.CharField(max_length=300, blank=True, null=True, db_column='observaciones')
    firma_tecnico = models.CharField(max_length=100, blank=True, null=True, db_column='firma_tecnico')
    firma_responsable = models.CharField(max_length=100, blank=True, null=True, db_column='firma_responsable')
    fecha_envio = models.DateTimeField(null=True, blank=True, db_column='fecha_envio')
    fecha_aprobacion = models.DateTimeField(default=timezone.now)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, db_column='fecha_eliminacion')

    creado_por = models.CharField(max_length=50, blank=True, null=True, db_column='creado_por')
    modificado_por = models.CharField(max_length=50, blank=True, null=True, db_column='modificado_por')
    eliminado_por = models.CharField(max_length=50, blank=True, null=True, db_column='eliminado_por')


    class Meta:
        db_table = 'Reporte_Mantenimiento'

class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    id_users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_users')
    id_ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, db_column = 'id_ticket')
    id_equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True, db_column = 'id_equipo')
    id_lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, db_column = 'id_lugar')
    descripcion = models.CharField(max_length=300, blank=True, null=True, db_column='descripcion')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, db_column='fecha_eliminacion')

    creado_por = models.CharField(max_length=50, blank=True, null=True, db_column='creado_por')
    modificado_por = models.CharField(max_length=50, blank=True, null=True, db_column='modificado_por')
    eliminado_por = models.CharField(max_length=50, blank=True, null=True, db_column='eliminado_por')


    class Meta:
        db_table = 'Notificacion'
