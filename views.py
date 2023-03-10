import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)



    for pokemon in Pokemon.objects.all():
        for pokemon_entity in PokemonEntity.objects.filter(pokemon__title=pokemon.title):
            if timezone.localtime(pokemon_entity.disappeared_at) >= timezone.localtime() and \
                    timezone.localtime(pokemon_entity.appeared_at) <= timezone.localtime():
                if pokemon.image:
                    add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(pokemon.image.url)
                )
                else:
                    add_pokemon(
                        folium_map, pokemon_entity.lat,
                        pokemon_entity.lon,
                        request.build_absolute_uri(pokemon.image.name)
                    )


    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        # pokemons_on_page.append({
        #     'pokemon_id': pokemon.id,
        #     'img_url': request.build_absolute_uri(pokemon.image.url),
        #     'title_ru': pokemon.title,
        # })

        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.url,
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.name,
                'title_ru': pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemons = dict()

    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
        pokemons["pokemon_id"] = pokemon.id
        pokemons["title_ru"] = pokemon.title
        pokemons["img_url"] = request.build_absolute_uri(pokemon.image.url)
        pokemons["title_en"] = pokemon.title_eng
        pokemons["title_jp"] = pokemon.title_jp
        pokemons["description"] = pokemon.description
        if pokemon.previous_evolution:
            pokemons["previous_evolution"] = dict()
            pokemons["previous_evolution"]["title_ru"] = pokemon.previous_evolution.title
            pokemons["previous_evolution"]["pokemon_id"] = pokemon.previous_evolution.id
            pokemons["previous_evolution"]["img_url"] = pokemon.previous_evolution.image.url


        for next_pokemon in pokemon.next_evolutions.all():
            pokemons["next_evolution"] = dict()
            pokemons["next_evolution"]["title_ru"] = next_pokemon.title
            pokemons["next_evolution"]["pokemon_id"] = next_pokemon.id
            pokemons["next_evolution"]["img_url"] = next_pokemon.image.url

    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>?????????? ?????????????? ???? ????????????</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon__title=pokemon.title):
        if timezone.localtime(pokemon_entity.disappeared_at) >= timezone.localtime() and \
                timezone.localtime(pokemon_entity.appeared_at) <= timezone.localtime():
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.image.url)
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons
    })
