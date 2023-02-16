from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="pokemon_images", null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    # def __str__(self):
    #     return f'{self.lat}{self.lon}'
