from django.test import TestCase
from .models import Livre

# Create your tests here.

class LivreTestCase(TestCase):
    def setUp(self):
        Livre.objects.create(titre = "Django Unchained", auteur = "Tarantino", date_publication= "2012-01-01")

    def test_list_livres(self):
        response = self.client.get('/livres-disponibles/')
        self.assertEqual(response.status_code, 200)

    def test_ajouter_livre(self):
        response = self.client.post('/ajouter-livre/', {'titre': 'Nouveau Livre', 'auteur': 'Auteur',
                                                  'date_publication':'2024-11-01', 'disponible': True})
        self.assertEqual(Livre.objects.count(), 2)
