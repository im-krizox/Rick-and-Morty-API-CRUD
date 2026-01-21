from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Character, Location, Episode
from .api_service import DataLoader

# Create your views here.


def index(request):
    # Vista principal - Lista todos los personajes
    characters = Character.objects.all().select_related('location').prefetch_related('episode')
    
    context = {
        'characters': characters,
        'total_characters': characters.count(),
        'total_locations': Location.objects.count(),
        'total_episodes': Episode.objects.count(),
    }
    
    return render(request, 'rickmorty_app/index.html', context)


def initialize_database(request):
    # Vista para inicializar la base de datos con datos de la API
    if request.method == 'POST':
        try:
            # Cargar los personajes desde la API
            stats = DataLoader.load_characters(limit=150)
            
            messages.success(
                request,
                f'Base de datos inicializada correctamente'
                f'Se crearon {stats["created"]} personajes, '
                f'se omitieron {stats["skipped"]} (ya existían) y '
                f'hubo {stats["errors"]} errores.'
            )
        except Exception as e:
            messages.error(
                request,
                f'Error al inicializar la base de datos: {str(e)}'
            )
    
    return redirect('index')


def character_detail(request, pk):
    # Vista de detalle de un personaje
    character = get_object_or_404(
        Character.objects.select_related('location').prefetch_related('episode'),
        pk=pk
    )
    
    context = {
        'character': character,
    }
    
    return render(request, 'rickmorty_app/character_detail.html', context)


def character_create(request):
    # Vista para crear un nuevo personaje
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            name = request.POST.get('name')
            location_id = request.POST.get('location')
            image = request.FILES.get('image')
            episode_ids = request.POST.getlist('episodes')
            
            # Validar nombre
            if not name:
                messages.error(request, 'El nombre es obligatorio')
                return redirect('character_create')
            
            # Obtener o crear ubicación
            location = None
            if location_id:
                location = Location.objects.get(id=location_id)
            
            # Crear personaje
            character = Character.objects.create(
                name=name,
                location=location,
                image=image
            )
            
            # Agregar episodios
            if episode_ids:
                episodes = Episode.objects.filter(id__in=episode_ids)
                character.episode.set(episodes)
            
            messages.success(request, f'El personaje "{name}" ha sido creado correctamente')
            return redirect('character_detail', pk=character.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear el personaje: {str(e)}')
            return redirect('character_create')
    
    # GET request
    locations = Location.objects.all().order_by('name')
    episodes = Episode.objects.all().order_by('id')
    
    context = {
        'locations': locations,
        'episodes': episodes,
    }
    
    return render(request, 'rickmorty_app/character_form.html', context)


def character_edit(request, pk):
    # Vista para editar un personaje existente
    character = get_object_or_404(Character, pk=pk)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            name = request.POST.get('name')
            location_id = request.POST.get('location')
            image = request.FILES.get('image')
            episode_ids = request.POST.getlist('episodes')
            
            # Validar nombre
            if not name:
                messages.error(request, 'El nombre es obligatorio')
                return redirect('character_edit', pk=pk)
            
            # Actualizar personaje
            character.name = name
            
            # Actualizar ubicación
            if location_id:
                character.location = Location.objects.get(id=location_id)
            else:
                character.location = None
            
            # Actualizar imagen solo si se subió una nueva
            if image:
                character.image = image
            
            character.save()
            
            # Actualizar episodios
            if episode_ids:
                episodes = Episode.objects.filter(id__in=episode_ids)
                character.episode.set(episodes)
            else:
                character.episode.clear()
            
            messages.success(request, f'El personaje "{name}" ha sido actualizado correctamente')
            return redirect('character_detail', pk=character.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el personaje: {str(e)}')
            return redirect('character_edit', pk=pk)
    
    # GET request
    locations = Location.objects.all().order_by('name')
    episodes = Episode.objects.all().order_by('id')
    
    context = {
        'character': character,
        'locations': locations,
        'episodes': episodes,
        'is_edit': True,
    }
    
    return render(request, 'rickmorty_app/character_form.html', context)


def character_delete(request, pk):
    # Vista para eliminar un personaje
    character = get_object_or_404(Character, pk=pk)
    
    if request.method == 'POST':
        character_name = character.name
        character.delete()
        messages.success(request, f'El personaje "{character_name}" ha sido eliminado correctamente')
        return redirect('index')
    
    context = {
        'character': character,
    }
    
    return render(request, 'rickmorty_app/character_confirm_delete.html', context)