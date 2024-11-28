from django.shortcuts import render, get_object_or_404, redirect
from .models import Livre
from .forms import LivreForm  
from .models import Emprunt
from datetime import date
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from datetime import datetime
from django.db import connection
from django.db.models import Count

def return_livre(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    livre = emprunt.livre

    # Mark the book as available again
    livre.disponible = True
    livre.save()

    # Set the return date
    emprunt.return_date = date.today()
    emprunt.save()

    # Increment the emprunt count for the book
    livre.emprunt_count += 1
    livre.save()

    return redirect('livres_disponibles')

def emprunts(request):
    emprunts = Emprunt.objects.filter(return_date__isnull=True)  # Only show books that have not been returned
    return render(request, 'livres/emprunts.html', {'emprunts': emprunts})

def moyenne_publication(request):
    # Custom query to calculate average date using UNIX timestamps
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT AVG(strftime('%s', date_publication))
            FROM livres_livre
        """)
        result = cursor.fetchone()

    if result and result[0]:
        # Convert the timestamp back to a date
        average_timestamp = int(result[0])
        average_date = datetime.utcfromtimestamp(average_timestamp).strftime('%Y-%m-%d')
    else:
        average_date = None
    
    return render(request, 'livres/moyenne_publication.html', {'average_date': average_date})
def creer_emprunt(request, pk):
    # Fetch the book by ID
    livre = get_object_or_404(Livre, pk=pk)

    # Check if the book is available
    if not livre.disponible:
        return render(request, 'livres/erreur_emprunt.html', {'message': "Ce livre n'est pas disponible."})

    if request.method == 'POST':
        # Get the borrower's name from the form
        nom_emprunteur = request.POST.get('nom_emprunteur')
        if nom_emprunteur:
            # Create a new Emprunt
            Emprunt.objects.create(livre=livre, nom_emprunteur=nom_emprunteur, date_emprunt=date.today())
            # Mark the book as unavailable
            livre.disponible = False
            livre.save()
            return redirect('livres_disponibles')  # Redirect to the list of available books

    return render(request, 'livres/creer_emprunt.html', {'livre': livre})

def rechercher_livres(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        livres = Livre.objects.filter(titre__icontains=query)  # Case-insensitive partial match
    else:
        livres = Livre.objects.all()  # Display all books if no query
    return render(request, 'livres/rechercher_livres.html', {'livres': livres, 'query': query})

def livres_trie_par_date(request):
    order = request.GET.get('order', 'desc')  # Default to 'desc'
    if order == 'asc':
        livres = Livre.objects.all().order_by('date_publication')  # Ascending order
    else:
        livres = Livre.objects.all().order_by('-date_publication')  # Descending order
    return render(request, 'livres/livres_trie_par_date.html', {'livres': livres, 'order': order})

# def livres_trie_par_date(request):
#     livres = Livre.objects.all().order_by('-date_publication')
#     return render(request, 'livres/livres_trie_par_date.html', {'livres': livres})

def compteur_livres_empruntes(request):
    compteur = Emprunt.objects.count()
    return render(request, 'livres/compteur_livres_empruntes.html', {'compteur': compteur})

@receiver(pre_save, sender=Livre)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Livre.objects.get(pk=instance.pk).image
        except Livre.DoesNotExist:
            return
        new_image = instance.image
        if old_image and old_image != new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

# def livres_disponibles(request):
#     all_livres = Livre.objects.all()  
#     livres = [livre for livre in all_livres if livre.disponible]  
#     return render(request, 'livres/livres_disponibles.html', {'livres': livres})

# def livres_disponibles(request):
#     livres = Livre.objects.exclude(disponible=False)  
#     return render(request, 'livres/livres_disponibles.html', {'livres': livres})

# def livres_disponibles(request):
#     livres = Livre.objects.raw("SELECT * FROM livres_livre WHERE disponible = 1")
#     return render(request, 'livres/livres_disponibles.html', {'livres': livres})

# def livres_disponibles(request):
#     # Get all available books with their emprunt_count
#     livres = Livre.objects.annotate(emprunt_total=Count('emprunt'))
#     return render(request, 'livres/livres_disponibles.html', {'livres': livres})

def livres_disponibles(request):
    # Start with the base queryset
    livres = Livre.objects.annotate(emprunt_total=Count('emprunt'))
    
    # Filter by auteur if provided
    auteur = request.GET.get('auteur', None)
    if auteur:
        livres = livres.filter(auteur__icontains=auteur)  # Case-insensitive search for auteur

    # Filter by disponibilité (True or False) if provided
    disponible = request.GET.get('disponible', None)
    if disponible is not None:
        livres = livres.filter(disponible=disponible.lower() == 'true')  # Convert to boolean (True/False)

    return render(request, 'livres/livres_disponibles.html', {'livres': livres})


def details_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    return render(request, 'livres/details_livre.html', {'livre': livre})

def update_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('details_livre', pk=livre.pk)
    else:
        form = LivreForm(instance=livre)
    return render(request, 'livres/update_livre.html', {'form': form, 'livre': livre})


def livres_non_disponibles(request):
    livres = Livre.objects.filter(disponible=False)
    return render(request, 'livres/livres_non_disponibles.html', {'livres': livres})

def emprunter_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if livre.disponible:
        if request.method == 'POST':
            nom_emprunteur = request.POST.get('nom_emprunteur')
            Emprunt.objects.create(livre=livre, nom_emprunteur=nom_emprunteur, date_emprunt=date.today())
            livre.disponible = False
            livre.save()
            return redirect('livres_disponibles')
    return render(request, 'livres/emprunter_livre.html', {'livre': livre})

def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('livres_disponibles')
    else:
        form = LivreForm()
    return render(request, 'livres/ajouter_livre.html', {'form': form})
