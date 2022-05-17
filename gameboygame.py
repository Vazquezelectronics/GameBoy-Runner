import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()
		player_walk_2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (180,0))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('/home/emmanuel/Documents/python files/gameboy game/audio/SFX_Jump_06.wav')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 500:
			self.rect.bottom = 500

	def animation_state(self):
		if self.rect.bottom < 500: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'one':
			one_1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/one.png').convert_alpha()
			one_2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/one.png').convert_alpha()
			self.frames = [one_1,one_2]
			y_pos = 410
		else:
			zero_1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/zero.png').convert_alpha()
			zero_2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/zero.png').convert_alpha()
			self.frames = [zero_1,zero_2]
			y_pos  = 500

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,('Blue'))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 6

			if obstacle_rect.bottom == 500: screen.blit(zero_surf,obstacle_rect)
			else: screen.blit(one_surf,obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]

		return obstacle_list
	else: return []

def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

def player_animation():
	global player_surf, player_index

	if player_rect.bottom < 300:
		player_surf = player_jump
	else:
		player_index += 0.1
		if player_index >= len(player_walk):player_index = 0
		player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((738,1197))
pygame.display.set_caption('Gameboy runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('/home/emmanuel/Documents/python files/gameboy game/fonts/PublicPixel.ttf', 20)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('/home/emmanuel/Documents/python files/gameboy game/audio/newbattle.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/gameboynew1.png').convert()

# Zero
zero_frame_1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/zero.png').convert_alpha()
zero_frame_2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/zero.png').convert_alpha()
zero_frames = [zero_frame_1, zero_frame_2]
zero_frame_index = 0
zero_surf = zero_frames[zero_frame_index]

# One
one_frame1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/one.png').convert_alpha()
one_frame2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/enemys/one.png').convert_alpha()
one_frames = [one_frame1, one_frame2]
one_frame_index = 0
one_surf = one_frames[one_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()
player_walk_2 = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (100,500))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/player/gameboy _player.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (360,250))
menuback = pygame.image.load('/home/emmanuel/Documents/python files/gameboy game/graphics/gameboy.png').convert_alpha()

game_name = test_font.render('Gameboy Runner',False,('Blue'))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,('Blue'))
game_message_rect = game_message.get_rect(center = (380,300))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,800)

zero_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(zero_animation_timer,500)

one_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(one_animation_timer,300)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
					player_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 1000)

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['one','zero','zero','zero'])))
				
			if event.type == zero_animation_timer:
				if zero_frame_index == 0: zero_frame_index = 1
				else: zero_frame_index = 0
				zero_surf = zero_frames[zero_frame_index] 

			if event.type == one_animation_timer:
				if one_frame_index == 0: one_frame_index = 1
				else: one_frame_index = 0
				one_surf = one_frames[one_frame_index] 


	if game_active:
		screen.blit(sky_surface,(0,0))
		
		score = display_score()
		
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		# Obstacle movement 
		# obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# collision 
		game_active = collision_sprite()
		# game_active = collisions(player_rect,obstacle_rect_list)
		
	else:
		
		screen.blit(menuback,[0,0])
		screen.blit(player_stand,player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)
		player_gravity = 0

		score_message = test_font.render(f'Your score: {score}',False,('Blue'))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)