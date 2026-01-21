# Servicio para consumir la API de Rick and Morty

import requests
from django.core.files.base import ContentFile
from .models import Character, Location, Episode


class RickAndMortyAPI:
    # Clase para interactuar con la API de Rick and Morty
    BASE_URL = "https://rickandmortyapi.com/api"
    
    @staticmethod
    def get_all_characters(limit=None):
        """
        Obtiene todos los personajes de la API (con paginación)
        
        Args:
            limit (int): Número máximo de personajes a obtener. 
                        Si es None, obtiene todos los disponibles.
        
        Returns:
            list: Lista de diccionarios con los datos de los personajes
        """
        characters = []
        url = f"{RickAndMortyAPI.BASE_URL}/character"
        
        while url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                # Agregar los personajes de la página actual
                characters.extend(data['results'])
                
                # Verificar si hemos alcanzado el límite
                if limit and len(characters) >= limit:
                    return characters[:limit]
                
                # Obtener la URL de la siguiente página
                url = data['info']['next']
                
                print(f"Se han obtenido {len(characters)} personajes")
                
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener personajes: {e}")
                break
        
        return characters
    
    @staticmethod
    def get_character_by_id(character_id):
        """
        Obtiene un personaje específico por su ID
        
        Args:
            character_id (int): ID del personaje
        
        Returns:
            dict: Datos del personaje o None si hay error
        """
        try:
            url = f"{RickAndMortyAPI.BASE_URL}/character/{character_id}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el personaje {character_id}: {e}")
            return None
    
    @staticmethod
    def get_location_by_url(location_url):
        """
        Obtiene una ubicación por su URL
        
        Args:
            location_url (str): URL de la ubicación
        
        Returns:
            dict: Datos de la ubicación o None si hay error
        """
        if not location_url:
            return None
        
        try:
            response = requests.get(location_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la ubicación: {e}")
            return None
    
    @staticmethod
    def get_episode_by_url(episode_url):
        """
        Obtiene un episodio por su URL
        
        Args:
            episode_url (str): URL del episodio
        
        Returns:
            dict: Datos del episodio o None si hay error
        """
        if not episode_url:
            return None
        
        try:
            response = requests.get(episode_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el episodio: {e}")
            return None
    
    @staticmethod
    def download_image(image_url):
        """
        Descarga una imagen desde una URL
        
        Args:
            image_url (str): URL de la imagen
        
        Returns:
            ContentFile: Archivo de imagen o None si hay error
        """
        if not image_url:
            return None
        
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Obtener el nombre del archivo desde la URL
            image_name = image_url.split('/')[-1]
            
            # Crear un ContentFile (compatible con ImageField de Django)
            return ContentFile(response.content, name=image_name)
        
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen {image_url}: {e}")
            return None


class DataLoader:
    """
    Clase para cargar datos de la API a la base de datos local
    """
    
    @staticmethod
    def get_or_create_location(location_data):
        """
        Obtiene o crea una ubicación en la base de datos
        
        Args:
            location_data (dict): Datos de la ubicación desde la API
        
        Returns:
            Location: Instancia de Location o None
        """
        if not location_data:
            return None
        
        location, created = Location.objects.get_or_create(
            name=location_data.get('name', 'Unknown'),
            defaults={
                'dimension': location_data.get('dimension', '')
            }
        )
        
        if created:
            print(f"Ubicación {location.name} creada")
        
        return location
    
    @staticmethod
    def get_or_create_episode(episode_data):
        """
        Obtiene o crea un episodio en la base de datos
        
        Args:
            episode_data (dict): Datos del episodio desde la API
        
        Returns:
            Episode: Instancia de Episode o None
        """
        if not episode_data:
            return None
        
        episode, created = Episode.objects.get_or_create(
            name=episode_data.get('name', 'Unknown'),
            defaults={
                'air_date': episode_data.get('air_date', '')
            }
        )
        
        if created:
            print(f"Episodio {episode.name} creado")
        
        return episode
    
    @staticmethod
    def load_characters(limit=150):
        """
        Carga personajes desde la API a la base de datos
        
        Args:
            limit (int): Número de personajes a cargar (por defecto 150)
        
        Returns:
            dict: Estadísticas de la carga
        """
        print(f"\n{'='*60}")
        print(f"INICIANDO CARGA DE {limit} PERSONAJES DESDE LA API")
        print(f"{'='*60}\n")
        
        # Obtener personajes de la API
        api_characters = RickAndMortyAPI.get_all_characters(limit=limit)
        
        stats = {
            'total': len(api_characters),
            'created': 0,
            'skipped': 0,
            'errors': 0
        }
        
        for idx, char_data in enumerate(api_characters, 1):
            try:
                print(f"\n[{idx}/{len(api_characters)}] Procesando: {char_data['name']}")
                
                # Verificar si el personaje ya existe
                if Character.objects.filter(name=char_data['name']).exists():
                    print(f"  ⊘ Personaje ya existe, omitiendo...")
                    stats['skipped'] += 1
                    continue
                
                # Procesar ubicación
                location = None
                if char_data.get('location'):
                    location_data = RickAndMortyAPI.get_location_by_url(
                        char_data['location']['url']
                    )
                    location = DataLoader.get_or_create_location(location_data)
                
                # Crear el personaje
                character = Character.objects.create(
                    name=char_data['name'],
                    location=location
                )
                
                # Descargar y guardar la imagen
                if char_data.get('image'):
                    image_file = RickAndMortyAPI.download_image(char_data['image'])
                    if image_file:
                        character.image.save(
                            f"{char_data['id']}.jpeg",
                            image_file,
                            save=True
                        )
                        print(f"Imagen descargada")
                
                # Procesar episodios
                episode_count = 0
                for episode_url in char_data.get('episode', []):
                    episode_data = RickAndMortyAPI.get_episode_by_url(episode_url)
                    episode = DataLoader.get_or_create_episode(episode_data)
                    if episode:
                        character.episode.add(episode)
                        episode_count += 1
                
                print(f"Personaje {char_data['name']} creado con {episode_count} episodios")
                stats['created'] += 1
                
            except Exception as e:
                print(f"Error al procesar el personaje: {e}")
                stats['errors'] += 1
        
        print(f"\n{'='*60}")
        print(f"Carga de personajes completada")
        print(f"{'='*60}")
        print(f"Total de personajes procesados: {stats['total']}")
        print(f"Personajes creados: {stats['created']}")
        print(f"Personajes omitidos (ya existían): {stats['skipped']}")
        print(f"Errores en la carga: {stats['errors']}")
        print(f"{'='*60}\n")
        
        return stats


# Función de prueba rápida
def test_api_connection():
    """
    Función para probar la conexión con la API
    """
    print("\n" + "="*60)
    print("Probando conexión con la API de Rick and Morty")
    print("="*60 + "\n")
    
    # Test 1: Obtener un personaje
    print("Test 1: Obteniendo personaje con ID 1...")
    character = RickAndMortyAPI.get_character_by_id(1)
    if character:
        print(f"Personaje {character['name']} obtenido")
        print(f"  - Estado: {character['status']}")
        print(f"  - Especie: {character['species']}")
        print(f"  - Ubicación: {character['location']['name']}")
    else:
        print("Error al obtener el personaje")
    
    # Test 2: Obtener primeros 5 personajes
    print("\nTest 2: Obteniendo primeros 5 personajes...")
    characters = RickAndMortyAPI.get_all_characters(limit=5)
    print(f"Se han obtenido {len(characters)} personajes:")
    for char in characters:
        print(f"  - {char['name']}")
    
    print("\n" + "="*60)
    print("Prueba de conexión con la API de Rick and Morty completada")
    print("="*60 + "\n")