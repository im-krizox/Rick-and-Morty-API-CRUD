from django.db import models

# Create your models here.

class Location(models.Model):
    # Modelo para las ubicaciones
    name = models.CharField(max_length=200, verbose_name="Nombre")
    dimension = models.CharField(max_length=200, blank=True, verbose_name="Dimensión",
                                help_text="Ej: Dimension C-137")
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Episode(models.Model):
    # Modelo para los episodios
    name = models.CharField(max_length=200, verbose_name="Nombre del episodio")
    air_date = models.CharField(max_length=100, verbose_name="Fecha de emisión",
                                help_text="Ej: December 2, 2013")
    
    class Meta:
        verbose_name = "Episodio"
        verbose_name_plural = "Episodios"
        ordering = ['id']
    
    def __str__(self):
        return self.name


class Character(models.Model):
    # Modelo principal para los personajes de Rick and Morty
    name = models.CharField(max_length=200, verbose_name="Nombre")
    
    # Campo de imagen
    image = models.ImageField(
        upload_to='characters/',
        blank=True,
        null=True,
        verbose_name="Imagen",
        help_text="Imagen del personaje"
    )
    
    # Relación con Location (ForeignKey - Muchos a Uno)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
        verbose_name="Ubicación"
    )
    
    # Relación ManyToMany con Episode
    episode = models.ManyToManyField(
        Episode,
        related_name='characters',
        blank=True,
        verbose_name="Episodios"
    )
    
    class Meta:
        verbose_name = "Personaje"
        verbose_name_plural = "Personajes"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def episode_count(self):
        # Retorna el número de episodios en los que aparece
        return self.episode.count()
    
    episode_count.short_description = "Número de episodios"