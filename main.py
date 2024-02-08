import os
import pygame
import requests


def open_map(spn):
    coords = get_address_coords(coord).split()
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={spn},0.002&{marcs}&l=map"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def print_text(size, toprint, col, rect):
    font = pygame.font.SysFont('sistem', size)
    text = font.render(toprint, True, col)
    screen.blit(text, rect)


def get_address_coords(address):
    API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
    geocoord_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
    response = requests.get(geocoord_request)
    json_response = response.json()
    if 'error' not in json_response:
        features = json_response['response']['GeoObjectCollection']['featureMember']
        toponym = features[0]['GeoObject']
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = \
        toponym['Point']['pos']
        return toponym_coodrinates
    return 'error'


coord = 'Австралия'
spn = 40
coords = get_address_coords(coord).split()
marcs = f'pt={coords[0]},{coords[1]},pm2wtl'
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={spn},0.002&{marcs}&l=map"
response = requests.get(map_request)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 500))
cl = pygame.time.Clock()
toprint = False
s = ''
running = True
while running:
    screen.blit(pygame.image.load(map_file), (0, 50))
    print_text(40, 'Поиск:', 'white', (0, 10))
    pygame.draw.rect(screen, 'white', ((100, 10), (400, 30)))
    pygame.draw.rect(screen, 'green', ((510, 10), (80, 30)))
    print_text(30,  s, 'black', (110, 20))
    print_text(40, 'Найти', 'white', (510, 10))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if spn + 10 != 180:
                    spn += 10
                    os.remove(map_file)
                    open_map(spn)
            if event.key == pygame.K_PAGEDOWN:
                if spn - 10 != 0:
                    spn -= 10
                    os.remove(map_file)
                    open_map(spn)
            if toprint:
                if event.dict['unicode'] == '\x08':
                    s = s[:-1]
                else:
                    s += event.dict['unicode']

        elif event.type == pygame.MOUSEBUTTONUP:
            toprint = False
            if 100 < event.pos[0] < 500 and 10 < event.pos[1] < 40:
                toprint = True
            elif 510 < event.pos[0] < 590 and 10 < event.pos[1] < 40:
                if get_address_coords(s) != 'error':
                    spn = 40
                    coord = s
                    coords = get_address_coords(coord).split()
                    marcs += f'~{coords[0]},{coords[1]},pm2wtl'
                    open_map(spn)

pygame.quit()


os.remove(map_file)
