import pygame
import random
import time
from constants_for_game import screen,left_margin,right_margin
class Character(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 1
        self.health = 100
        self.max_health= 100
        self.health_bar_length= 300
        self.displayed_health=False
        self.health_ratio = self.max_health / self.health_bar_length
        self.defense_power=random.randint(10, 15)
        self.attack_power=random.randint(15, 20)
        self.alive = True 
        self.image= pygame.image.load('character.png').convert_alpha()
        self.image_right=pygame.image.load('character_right.png').convert_alpha()
        self.flip = False
        self.direction=1
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.special_ability=random.choice([None,"extra_attack","self_heal","half_damage_ability"])
        self.ability_active=False
        self.ability_cooldown= False
        self.ability_start_time=0
        self.cooldown_start_time=0

    def activate_ability(self):
        if not self.ability_cooldown and not self.ability_active:
            self.ability_active = True
            self.ability_start_time = time.time()

    def update_ability(self):
        if self.ability_active:
            if time.time() - self.ability_start_time >= 5:
                self.ability_active = False
                self.ability_cooldown = True
                self.cooldown_start_time = time.time()

        if self.ability_cooldown:
            if time.time() - self.cooldown_start_time >= 5:
                self.ability_cooldown = False

    def draw(self,is_opponent=False):
        if self.alive:
            screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
            self.basic_health(is_opponent)

    def move(self,moving_left=False,moving_right=False):
        if not self.alive:
            return 
        dx = 0
        if moving_left:
            dx -= self.speed
            self.flip=True
            self.direction = -1
        if moving_right:
            dx += self.speed
            self.flip=False
            self.direction = 1
        self.rect.x += dx
        if self.rect.x < left_margin:
            self.rect.x = left_margin
        if self.rect.x > right_margin:
            self.rect.x = right_margin

    def move_as_opponent(self,player):
        if self.alive:
            distance = abs(self.rect.x - player.rect.x)
            if distance > 20:
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                    self.flip= False
                    self.direction = 1
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
                    self.flip=True
                    self.direction = -1 

    def get_damage(self, attack_power):
        damage = max(0,attack_power - self.defense_power)
        if self.special_ability == "half_damage_ability":
            damage = damage // 2
        self.health -= damage
        if self.special_ability == "self_heal" and self.health<30:
            self.health += 5
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.rect=pygame.Rect(0,0,0,0)
    
    def attack(self, target):
        attack_power = self.attack_power
        if self.special_ability == "extra_attack":
            attack_power = int(attack_power * 1.5)
        if pygame.sprite.collide_mask(self,target) and target != self:
            target.get_damage(attack_power)

    def basic_health(self,is_opponent=False):
        if self.alive:
            if not self.displayed_health:
                self.displayed_health = self.health

        if self.displayed_health > self.health:
            self.displayed_health -= 0.2

        if is_opponent: 
            x_position = right_margin - self.health_bar_length //2 -25
        else:
            x_position = 25

        pygame.draw.rect(screen, (0, 255, 0), (x_position, 10, self.health / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (x_position, 10, self.health_bar_length, 20), 4)

        pygame.draw.rect(screen, (204, 160, 29), (x_position + self.health / self.health_ratio, 10, 
                        (self.displayed_health - self.health) / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (x_position, 10, self.health_bar_length, 20), 4)

        if self.health < self.max_health / 2:
            pygame.draw.rect(screen, (255, 255, 0), (x_position, 10, self.health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255),(x_position, 10, self.health_bar_length, 20), 4)
        if self.health < self.max_health / 4:
            pygame.draw.rect(screen, (255, 0, 0), (x_position, 10, self.health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255), (x_position, 10, self.health_bar_length, 20), 4)
