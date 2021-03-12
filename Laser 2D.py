import pygame
import random
WIDTH = 800
HEIGHT= 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

#Configuración ventana

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shooter manija")
clock = pygame.time.Clock()

#Crear Jugador

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Archivos/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.life = 100
	
	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x 

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot (self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullet_List.add(bullet)
		laser_sound.play()

#Crear Obstaculos (Meteoros/enemigos)
class Meteoros(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteoro_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width) 
		self.rect.y = random.randrange(-140, -110) 
		self.speedy = random.randrange(1,10) 
		self.speedx = random.randrange(-5,5)
		
	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH +40:
			self.rect.x = random.randrange(WIDTH - self.rect.width) 
			self.rect.y = random.randrange(-100, -40) 
			self.speedy = random.randrange(1,10) 


#Dibujar Score

def draw_text(surface, txt, size, x, y):
	font = pygame.font.SysFont("serif", size)
	txt_surface = font.render(txt, True, WHITE)
	txt_rect = txt_surface.get_rect()
	txt_rect.midtop = (x, y)
	surface.blit(txt_surface, txt_rect)

#Dibujar barra de vida

def drawLife(surface,x,y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x,y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

#Programacion balas

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		super().__init__()
		self.image = pygame.image.load("Archivos/laser1.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y 
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

#Programar animacion de explosion

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center):
			super().__init__()
			self.image = explosionAnim[0]
			self.rect = self.image.get_rect()
			self.rect.center = center
			self.frame = 0
			self.lastUpdate = pygame.time.get_ticks()
			self.frameRate = 50 #Velocity of explosion

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.lastUpdate > self.frameRate:
			self.lastUpdate = now
			self.frame += 1 
			if self.frame == len(explosionAnim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosionAnim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def show_go_screen():
		screen.blit(background, [0,0] )
		draw_text(screen, "Shooter Manija", 65, WIDTH // 2, HEIGHT // 4)
		draw_text(screen, "Buen juego!", 27, WIDTH // 2, HEIGHT // 2)
		draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
		pygame.display.flip()
		waiting = True
		while waiting:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYUP:
					waiting = False







#Lista vacia
meteoro_images = []
meteoro_list = ["Archivos/meteorGrey_big1.png",
				"Archivos/meteorGrey_big2.png",
				"Archivos/meteorGrey_big3.png",
				"Archivos/meteorGrey_big4.png",
				"Archivos/meteorGrey_med1.png",
				"Archivos/meteorGrey_med2.png",
				"Archivos/meteorGrey_small1.png",
				"Archivos/meteorGrey_small2.png",
				"Archivos/meteorGrey_tiny1.png",
				"Archivos/meteorGrey_tiny2.png"]

for img in meteoro_list:
	meteoro_images.append(pygame.image.load(img).convert())


#Cargar Imagen de fondo

background = pygame.image.load("Archivos/blueSpacial.png").convert()

#Crear animacion con carga de imagenes

explosionAnim = []
for i in range (9):
	file = "Archivos/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	imgScale= pygame.transform.scale(img, (70,70))
	explosionAnim.append(imgScale)

#cargar Sonidos

laser_sound = pygame.mixer.Sound("Archivos/laser5.ogg")
explosion_sound = pygame.mixer.Sound("Archivos/explosion.wav")
pygame.mixer.music.load("Archivos/music.ogg")
pygame.mixer.music.set_volume(0.2)

#Almacenamiento del jugador/enemigo




pygame.mixer.music.play(loops=-1)

#Crear Game Over
gameOver = True
running = True 
while running:
	if gameOver:
		show_go_screen()
		gameOver = False

		all_sprites = pygame.sprite.Group()
		meteor_List = pygame.sprite.Group()
		bullet_List = pygame.sprite.Group()

		player = Player() 
		all_sprites.add(player)
		for i in range(8):
			meteor = Meteoros()
			all_sprites.add(meteor)
			meteor_List.add(meteor)
		score = 0

	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.shoot()



#Crear Colisiones


#Colisiones - meteoro - laser

	hits = pygame.sprite.groupcollide(meteor_List, bullet_List, True, True)
	for hit in hits:
		score += 15
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteoros()
		all_sprites.add(meteor)
		meteor_List.add(meteor)
# Colisione player - meteoros

	hits = pygame.sprite.spritecollide(player,meteor_List, True)
	for hit in hits:
		player.life -= 25
		meteor = Meteoros()
		all_sprites.add(meteor)
		meteor_List.add(meteor)
		if player.life <= 0:
			gameOver = True


	all_sprites.update()
	screen.blit(background, [0,0])

	all_sprites.draw(screen)


	#Marcador 
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	#Escudos
	drawLife(screen,5,5,player.life)
	
	pygame.display.flip()
pygame.quit()
