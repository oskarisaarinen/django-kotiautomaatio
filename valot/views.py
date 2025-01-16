from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Huone, Valo
from .forms import HuoneForm
from .forms import ValoForm

# Kirjautuminen
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('huoneet_lista')  # Ohjaa huoneiden listaukseen
        else:
            return render(request, 'valot/login.html', {'error': 'Virheellinen käyttäjätunnus tai salasana.'})
    return render(request, 'valot/login.html')

# Uloskirjautuminen
def custom_logout(request):
    logout(request)
    return redirect('login')  # Ohjaa kirjautumissivulle uloskirjautumisen jälkeen

# Huoneiden listaaminen
@login_required
def huoneet_lista(request):
    huoneet = Huone.objects.all()
    return render(request, 'valot/huoneet_lista.html', {'huoneet': huoneet})

# Valojen hallinta huoneessa
@login_required
def valojen_hallinta(request, huone_id):
    huone = get_object_or_404(Huone, id=huone_id)
    valot = huone.valot.all()
    return render(request, 'valot/valojen_hallinta.html', {'huone': huone, 'valot': valot})

# Valon tilan muuttaminen
@login_required
def muuta_valon_tila(request, valo_id):
    valo = get_object_or_404(Valo, id=valo_id)
    valo.tila = not valo.tila  # Vaihda tila (True ↔ False)
    valo.save()
    return redirect('valojen_hallinta', huone_id=valo.huone.id)

# Huoneen lisääminen
@login_required
def lisaa_huone(request):
    if request.method == 'POST':
        form = HuoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('huoneet_lista')
    else:
        form = HuoneForm()
    return render(request, 'valot/lisaa_huone.html', {'form': form})

# Huoneen poistaminen
@login_required
def poista_huone(request, huone_id):
    huone = get_object_or_404(Huone, id=huone_id)
    if request.method == 'POST':
        huone.delete()
        return redirect('huoneet_lista')
    return render(request, 'valot/poista_huone.html', {'huone': huone})

@login_required
def lisaa_valo(request):
    if request.method == 'POST':
        form = ValoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('huoneet_lista')  # Ohjaa takaisin huoneisiin
    else:
        form = ValoForm()
    return render(request, 'valot/lisaa_valo.html', {'form': form})

# Valojen poistaminen
@login_required
def poista_valo(request, valo_id):
    valo = get_object_or_404(Valo, id=valo_id)
    if request.method == 'POST':
        valo.delete()
        return redirect('huoneet_lista')  # Ohjaa takaisin huoneisiin
    return render(request, 'valot/poista_valo.html', {'valo': valo})
