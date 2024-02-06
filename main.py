# Это сделал Арсений
import os
import pygame
import requests


def open_map(spn):
    coords = get_address_coords('Австралия').split()
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={spn},0.002&l=map"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_address_coords(address):
    API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
    geocoord_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
    response = requests.get(geocoord_request)
    json_response = response.json()
    features = json_response['response']['GeoObjectCollection']['featureMember']
    toponym = features[0]['GeoObject']
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_coodrinates = \
    toponym['Point']['pos']
    return toponym_coodrinates


spn = 40
coords = get_address_coords('Австралия').split()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={spn},0.002&l=map"
response = requests.get(map_request)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
while running:
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            os.remove(map_file)
            if event.key == pygame.K_PAGEUP:
                if spn + 20 != 200:
                    spn += 20
            if event.key == pygame.K_PAGEDOWN:
                if spn - 20 != 0:
                    spn -= 20
            open_map(spn)
pygame.quit()

os.remove(map_file)
