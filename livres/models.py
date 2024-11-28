from django.db import models
from datetime import date

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    date_publication = models.DateField()
    disponible = models.BooleanField(default=True)
    emprunt_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='livres/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # If "livre" is in the title, set disponible to False
        if "livre" in self.titre.lower():
            self.disponible = False
        super().save(*args, **kwargs)


class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    nom_emprunteur = models.CharField(max_length=100)
    date_emprunt = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)
    emprunt_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Ensure emprunt_count is correctly updated
        if self.return_date:
            self.livre.emprunt_count += 1
        super().save(*args, **kwargs)
