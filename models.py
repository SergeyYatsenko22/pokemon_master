from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="pokemon_images", null=True, blank=True)
    title_eng = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
