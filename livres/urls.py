from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('livres-disponibles/', views.livres_disponibles, name='livres_disponibles'),
    path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('livre/<int:pk>/', views.details_livre, name='details_livre'),
    path('update-livre/<int:pk>/', views.update_livre, name='update_livre'),
    path('livres-non-disponibles/', views.livres_non_disponibles, name='livres_non_disponibles'),
    path('emprunter-livre/<int:pk>/', views.emprunter_livre, name='emprunter_livre'),
    path('compteur-livres-empruntes/', views.compteur_livres_empruntes, name='compteur_livres_empruntes'),
    path('livres-trie-par-date/', views.livres_trie_par_date, name='livres_trie_par_date'),
    path('rechercher-livres/', views.rechercher_livres, name='rechercher_livres'),
    path('emprunter-livre/<int:pk>/', views.creer_emprunt, name='creer_emprunt'),
    path('moyenne-publication/', views.moyenne_publication, name='moyenne_publication'),
    path('emprunts/', views.emprunts, name='emprunts'),
    path('return_livre/<int:pk>/', views.return_livre, name='return_livre'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)