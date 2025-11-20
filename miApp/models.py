from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_maxima = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    fecha_hora_inicio = models.DateTimeField(default=timezone.now)
    fecha_hora_termino = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.fecha_hora_termino:
            self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)
        self.sala.disponible = False
        self.sala.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.sala.nombre} - {self.rut}"
