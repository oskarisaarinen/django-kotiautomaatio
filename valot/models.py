from django.db import models
from django.contrib.auth.models import User

class Huone(models.Model):
    nimi = models.CharField(max_length=100)
    käyttäjä = models.ForeignKey(User, on_delete=models.CASCADE, related_name="huoneet")

    def __str__(self):
        return self.nimi

class Valo(models.Model):
    nimi = models.CharField(max_length=100)
    tila = models.BooleanField(default=False)  # True = päällä, False = pois
    huone = models.ForeignKey(Huone, on_delete=models.CASCADE, related_name="valot")

    def __str__(self):
        return f"{self.nimi} ({'Päällä' if self.tila else 'Pois'})"

class Tilaus(models.Model):
    valo = models.ForeignKey(Valo, on_delete=models.CASCADE)
    aika = models.DateTimeField(auto_now_add=True)
    toiminto = models.CharField(max_length=10, choices=[('ON', 'Päällä'), ('OFF', 'Pois')])

    def __str__(self):
        return f"Tilaus: {self.valo.nimi} -> {self.toiminto}"