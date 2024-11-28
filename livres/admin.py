from django.contrib import admin
from .models import Livre, Emprunt

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'disponible')
    search_fields = ('titre', 'auteur')
    list_filter = ('disponible', 'date_publication')


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('livre', 'nom_emprunteur', 'date_emprunt')
    search_fields = ('livre__titre', 'nom_emprunteur')
    list_filter = ('date_emprunt',)
