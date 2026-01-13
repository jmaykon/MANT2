from django.db import models
from django.utils import timezone
class Lugar(models.Model):
    id_lugar = models.AutoField(primary_key=True, db_column='id_lugar')
    nombre = models.CharField(max_length=100, db_column='nombre')
    direccion = models.CharField(max_length=200, blank=True, null=True, db_column='direccion')
    area = models.CharField(max_length=100, blank=True, null=True, db_column='area')
    ciudad = models.CharField(max_length=50, blank=True, null=True, db_column='ciudad')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, db_column='fecha_eliminacion')

    creado_por = models.CharField(max_length=50, blank=True, null=True, db_column='creado_por')
    modificado_por = models.CharField(max_length=50, blank=True, null=True, db_column='modificado_por')
    eliminado_por = models.CharField(max_length=50, blank=True, null=True, db_column='eliminado_por')
    
    class Meta:
        db_table = 'Lugar'

    def __str__(self):
        return self.nombre
