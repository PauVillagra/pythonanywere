from django.db import models

# Creacion del modelo de base de datos
class Flores(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    valor=models.IntegerField()
    descripcion=models.TextField()
    estado=models.CharField(max_length=1)
    stock=models.IntegerField()
    imagen=models.ImageField(upload_to="media",null=False)

    def __str__(self):
        return self.name

