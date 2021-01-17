import os
import sys
import random
import pygame

pygame.init()

SIZE_WINDOW = 1200, 600
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption('BEAR')
screen = pygame.display.set_mode(SIZE_WINDOW)
font = pygame.font.Font(None, 30)
NAVY = pygame.Color('navy')
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
alpha = 255
vel = 0
life = 10
points = [0]
block = False

dirname = os.path.dirname(__file__)
images_bear = []
path = os.path.join(dirname, 'Bear')
for file_name in os.listdir(path):
    image = pygame.image.load(os.path.join(path, file_name))
    images_bear.append(image)
# print(images_bear)
images_cloud = []
path2 = os.path.join(dirname, 'Cloud')
for file_name in os.listdir(path2):
    image = pygame.image.load(os.path.join(path2, file_name))
    images_cloud.append(image)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = images_bear
        self.index = 0  # первое изображение
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(0, SIZE_WINDOW[1] // 2))

    def update(self):
        self.rect.x += 1
        if self.rect.left > SIZE_WINDOW[0]:
            self.rect.right = 0
        if self.rect.bottom < SIZE_WINDOW[1] // 1.5 + 5:
            self.rect.x += 10
        self.index += 0.1
        self.image = self.images[int(self.index % self.range)]
        # print(int(self.index % self.range))
        self.rect[2:] = self.image.get_rect()[2:]
        self.image.set_alpha(alpha)


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(dirname, 'cone.png'))
        self.size = self.image.get_width() // 2, self.image.get_height() // 2
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, SIZE_WINDOW[1] // 1.5 - 10))

    def update(self):
        self.rect.x -= 2  # random.randint(2, 3)
        if self.rect.right < 0:
            self.rect.left = SIZE_WINDOW[0] * random.randint(2, 3)
            points[0] += 1


class Text(pygame.sprite.Sprite):
    def __init__(self, text, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = text
        self.rect = self.image.get_rect(topleft=(10, y))


class Clouds(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.images = images_cloud
        self.index = 1
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.h = self.image.get_height()
        self.rect = self.image.get_rect(center=(x // 2, self.h))
        self.speed = random.randint(2, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SIZE_WINDOW[0]
            self.rect.y = random.randint(self.h, SIZE_WINDOW[1] // 3)
            self.index += 1
            if self.index >= self.range:
                self.index = 0
            self.speed = random.randint(2, 3)
        self.image = self.images[self.index]


bear = AnimatedSprite()
cloud = Clouds(SIZE_WINDOW[0])
text1 = Text(font.render(f'life: {life}', True, WHITE), 10)
text2 = Text(font.render(f'points: {points[0]}', True, WHITE), 30)
sprites = pygame.sprite.Group()
cones = pygame.sprite.Group()
for i in range(3):
    cone = Obstacles(SIZE_WINDOW[0] + i * SIZE_WINDOW[0] // 3)
    cones.add(cone)
    sprites.add(cone)
sprites.add(cloud, bear, text1, text2)  # показать
# sprites.remove(bear)  # спрятать

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit(0)
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                alpha += 25 if alpha < 250 else 5 if alpha < 255 else 0
            elif e.key == pygame.K_DOWN:
                alpha -= 25 if alpha > 5 else 5 if alpha > 0 else 0
            elif e.key == pygame.K_SPACE \
                    and bear.rect.bottom > SIZE_WINDOW[1] // 1.5 + 5 \
                    and not block:
                vel = -20

    screen.fill(NAVY)
    earth = pygame.draw.rect(
        screen, GREEN,
        (0, SIZE_WINDOW[1] // 1.5, SIZE_WINDOW[0], SIZE_WINDOW[1] // 3))

    if len(cones) < 3:
        cone = Obstacles(SIZE_WINDOW[0] * random.randint(2, 3))
        cones.add(cone)
        sprites.add(cone)
    if pygame.sprite.spritecollide(
            bear, cones, True, pygame.sprite.collide_circle_ratio(0.75)):
        if bear.rect.right < SIZE_WINDOW[0]:
            life -= 1
        if life < 1:
            block = True
    text1.image = font.render(f'life: {life}', True, WHITE)
    text2.image = font.render(f'points: {points[0]}', True, WHITE)
    # гравитация
    vel += 1
    bear.rect.y += vel
    while bear.rect.colliderect((earth[0], earth[1] + 10, earth[2], earth[3])):
        vel = 0
        bear.rect.y -= 1
    # print(earth)

    if not block:
        sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
