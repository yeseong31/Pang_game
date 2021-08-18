import random

import pygame
#######################################################################################################
# Quiz) 하늘에서 떨어지는 똘 피아기 게임을 만드시오
# [게임 조건]
# 1. 캐릭터는 화면 가장 아래에 위치, 좌우로만 이동 가능
# 2. 똥은 화면 가장 위에서 떨어짐. x 좌표는 매번 랜덤으로 설정
# 3. 캐릭터가 똥을 피하면 다음 똥이 다시 떨어짐
# 4. 캐릭터가 똥과 충돌하면 게임 종료
# 5. FPS는 75로 고정

#######################################################################################################
# 기본 초기화 (반드시 필요함)
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))      # 게임 화면 크기 설정

# 화면 타이틀 설정
pygame.display.set_caption("DDONG Game")     # 게임 이름

# FPS
clock = pygame.time.Clock()

#######################################################################################################
# 1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 캐릭터
character = pygame.image.load('character.png')
character_width = character.get_width()
character_height = character.get_height()
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height

# 똥
enemy = pygame.image.load('enemy.png')
enemy_width = enemy.get_width()
enemy_height = enemy.get_height()
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0

# 좌표
character_nx = 0

# 배경
background = pygame.image.load('background.png')

# 속도
character_speed = 0.6
enemy_speed = 0.6

# 폰트
font = pygame.font.Font(None, 40)

# 시간
total_time = 60
start_ticks = pygame.time.get_ticks()


running = True
while running:
    dt = clock.tick(75)

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키 입력 start
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_nx -= character_speed
            if event.key == pygame.K_RIGHT:
                character_nx += character_speed

        # 키 입력 end
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_nx = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_nx * dt
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print('충돌하였음')
        pygame.time.delay(1000)
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    elapse_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = font.render(str(int(total_time - elapse_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - elapse_time <= 0:
        print('타임아웃')
        pygame.time.delay(1000)
        running = False

    enemy_y_pos += enemy_speed * dt

    if enemy_y_pos > screen_height:
        enemy_x_pos = random.randint(0, screen_width - enemy_width)
        enemy_y_pos = 0

    pygame.display.update()     # 화면을 다시 그리기(필수)


# pygame 종료
pygame.quit()
