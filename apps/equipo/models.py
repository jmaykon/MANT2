from django.db import models
from apps.lugar.models import Lugar
from django.conf import settings
from django.utils import timezone

class Equipo(models.Model):
    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("MANTENIMIENTO", "Mantenimiento"),
        ("INACTIVO", "Inactivo"),
    ]
    id_equipo = models.AutoField(primary_key=True, db_column='id_equipo')
    tipo = models.CharField(max_length=50, db_column='tipo')
    aec = models.CharField(max_length=50, db_column='aec')
    marca = models.CharField(max_length=50, blank=True, null=True, db_column='marca')
    modelo = models.CharField(max_length=50, blank=True, null=True, db_column='modelo')
    so = models.CharField(max_length=50, blank=True, null=True, db_column='so')
    procesador = models.CharField(max_length=50, blank=True, null=True, db_column='procesador')
    tipo_ram = models.CharField(max_length=50, blank=True, null=True, db_column='tipo_ram')
    ram = models.CharField(max_length=50, blank=True, null=True, db_column='ram')
    tipo_disco = models.CharField(max_length=50, blank=True, null=True, db_column='tipo_disco')
    disco = models.CharField(max_length=50, blank=True, null=True, db_column='disco')
    estado_disco = models.CharField(max_length=300, blank=True, null=True, db_column='estado_disco')
    estado_equipo = models.CharField(
        max_length=50,
        choices=ESTADOS, 
        default="ACTIVO",
        db_column='estado_equipo'
    )
    serial = models.CharField(max_length=50, unique=True, db_column='serial')
    observaciones = models.CharField(max_length=300, blank=True, null=True, db_column='observaciones')
    ip = models.CharField(max_length=45, blank=True, null=True, db_column='ip')
    
    
    id_lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lugar')
    id_users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_users')
    ip_maquina = models.CharField(max_length=45, blank=True, null=True, db_column='ip_maquina')
    
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, db_column='fecha_eliminacion')

    creado_por = models.CharField(max_length=50, blank=True, null=True, db_column='creado_por')
    modificado_por = models.CharField(max_length=50, blank=True, null=True, db_column='modificado_por')
    eliminado_por = models.CharField(max_length=50, blank=True, null=True, db_column='eliminado_por')

    class Meta:
        db_table = 'Equipo'

    def __str__(self):
        return f"{self.tipo} - {self.serial}"

class Componente(models.Model):
    id_componente = models.AutoField(primary_key=True, db_column='id_componente')
    tipo = models.CharField(max_length=50, db_column='tipo')
    aec = models.CharField(max_length=50, db_column='aec')
    marca = models.CharField(max_length=50, blank=True, null=True, db_column='marca')
    modelo = models.CharField(max_length=50, blank=True, null=True, db_column='modelo')
    serial = models.CharField(max_length=50, unique=True, db_column='serial')
    estado = models.CharField(max_length=20, default='Activo', db_column='estado')
    observaciones = models.CharField(max_length=300, blank=True, null=True, db_column='observaciones')
    
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo')
    id_users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_users')
    id_lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lugar')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, db_column='fecha_eliminacion')

    creado_por = models.CharField(max_length=50, blank=True, null=True, db_column='creado_por')
    modificado_por = models.CharField(max_length=50, blank=True, null=True, db_column='modificado_por')
    eliminado_por = models.CharField(max_length=50, blank=True, null=True, db_column='eliminado_por')
    
    
    class Meta:
        db_table = 'Componente'

    def __str__(self):
        return f"{self.tipo} - {self.serial}"
