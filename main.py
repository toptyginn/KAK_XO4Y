# Это сделал Арсений
import os
import sys

import pygame
import requests


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


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f'http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}'
    else:
        map_request = f'http://static-maps.yandex.ru/1.x/?l={map_type}'
    if add_params:
        map_request += '&' + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка запроса")
        print(map_request)
        print('Http статус:', response.status_code, '(', response.reason, ')')
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except Exception as e:
        print(f'ERROR: {e}')



spn = 40
coords = get_address_coords('Австралия').split()
ll_spn = f'll={coords[0]},{coords[1]}&spn={spn},{spn}'
show_map(ll_spn, 'map')
map_file = 'map.png'


def main():
    global spn, ll_spn
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
                show_map(ll_spn, 'map')
    pygame.quit()

    os.remove('map.png')


if __name__ == '__main__':
    main()
