from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Huone, Valo
from .forms import HuoneForm
from .forms import ValoForm
from .forms import LisaaYllapitoKauttaja
from .forms import SalasanaHyvaksynta
from .forms import LisaaKauttaja

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
            messages.success(request, "Huone lisätty onnistuneesti!")
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
        messages.success(request, "Huone poistettu onnistuneesti!")
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

# Tarkista Käyttäjän tila
def is_yllapitaja(user):
    return user.is_superuser 

# Luo ylläpitäjä
@user_passes_test(is_yllapitaja)
def luo_yllapitokayttaja(request):
    if request.method == 'POST':
        form = LisaaYllapitoKauttaja(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('yllapito')  # Takaisin Ylläpito sivulle
    else:
        form = LisaaYllapitoKauttaja()
    return render(request, 'valot/LisaaYllapitoKauttaja.html', {'form': form})

# Ylläpito sivu
@user_passes_test(is_yllapitaja)
def yllapito(request):
    superusers = User.objects.filter(is_superuser=True)  # Hae Ylläpitäjät
    users = User.objects.filter(is_superuser=False) # Hae Käyttäjät

    return render(request, 'valot/yllapito.html', {'superusers': superusers, 'users': users})

@user_passes_test(is_yllapitaja)
def poista_yllapitokayttaja(request, user_id):
    # Hae Käyttäjä
    user_to_delete = get_object_or_404(User, id=user_id, is_superuser=True)

    if request.method == 'POST':
        form = SalasanaHyvaksynta(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            
            # Autentikointi
            user = authenticate(username=request.user.username, password=password)

            if user is not None:
                
                user_to_delete.delete()
                return redirect('yllapito')  
            else:
                
                form.add_error('password', 'Väärä salasana.')

    else:
        form = SalasanaHyvaksynta()

    return render(request, 'valot/poista_yllapitokayttaja.html', {'form': form, 'user_to_delete': user_to_delete})

 # Poista Käyttäjä
@user_passes_test(is_yllapitaja)
def poista_kayttaja(request, user_id):

    user_to_delete = get_object_or_404(User, id=user_id, is_superuser=False)

    user_to_delete.delete()

    return redirect('yllapito')


 # Lisää Käyttäjä
@user_passes_test(is_yllapitaja)
def lisaa_kayttaja(request):
    if request.method == 'POST':
        form = LisaaKauttaja(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return redirect('yllapito')  
    else:
        form = LisaaKauttaja()

    return render(request, 'valot/lisaa_kayttaja.html', {'form': form})