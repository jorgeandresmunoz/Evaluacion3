from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .models import Sala, Reserva
from .forms import ReservaForm

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, "main.html", {"salas": salas})

def detalle_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    reserva_activa = sala.reservas.order_by('-id').first()
    if reserva_activa and reserva_activa.fecha_hora_termino <= timezone.now():
        sala.disponible = True
        sala.save()
    context = {
        "sala": sala,
        "reserva": reserva_activa,
        "form": ReservaForm()
    }
    return render(request, "detalle_sala.html", context)

def reservar_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    if not sala.disponible:
        return redirect("detalle_sala", sala_id=sala.id)
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.save()
            return redirect("detalle_sala", sala_id=sala.id)
    return redirect("detalle_sala", sala_id=sala.id)

@login_required
def admin_salas(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No autorizado")
    salas = Sala.objects.all()
    return render(request, "admin_salas.html", {"salas": salas})

@login_required
def crear_sala(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No autorizado")
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        capacidad = request.POST.get("capacidad")
        Sala.objects.create(nombre=nombre, capacidad_maxima=capacidad)
        return redirect("admin_salas")
    return redirect("admin_salas")

@login_required
def editar_sala(request, sala_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("No autorizado")
    sala = get_object_or_404(Sala, id=sala_id)
    if request.method == "POST":
        sala.nombre = request.POST.get("nombre")
        sala.capacidad_maxima = request.POST.get("capacidad")
        sala.disponible = request.POST.get("disponible") == "on"
        sala.save()
        return redirect("admin_salas")
    salas = Sala.objects.all()
    return render(request, "admin_salas.html", {"editar": sala, "salas": salas})

@login_required
def eliminar_sala(request, sala_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("No autorizado")
    sala = get_object_or_404(Sala, id=sala_id)
    sala.delete()
    return redirect("admin_salas")

def cerrar_sesion(request):
    logout(request)
    return redirect('lista_salas')
