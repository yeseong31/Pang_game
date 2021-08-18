import os
import pygame

#######################################################################################################
# 기본 초기화 (반드시 필요함)
pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))  # 게임 화면 크기 설정

# 화면 타이틀 설정
pygame.display.set_caption("PANG Game")  # 게임 이름

# FPS
clock = pygame.time.Clock()

#######################################################################################################
# 1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 배경
current_path = os.path.dirname(__file__)  # 현재 파일의 위치
image_path = os.path.join(current_path, "images")  # images 폴더 위치

background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동
character_to_x = 0
character_speed = 5

# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []
# 무기 이동 속도
weapon_speed = 10

# 공 (160, 80, 40, 20, 4개 크기에 대하여 따로 처리)
ball_images = [pygame.image.load(os.path.join(image_path, "balloon1.png")),
               pygame.image.load(os.path.join(image_path, "balloon2.png")),
               pygame.image.load(os.path.join(image_path, "balloon3.png")),
               pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 최초로 발생하는 큰 공 추가
balls = []
balls.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,  # 어떤 공(인덱스)을 쓸지
    "to_x": 3,  # 공의 x축 이동 방향
    "to_y": -6,  # 공의 y축 이동 방향
    "init_spe_y": ball_speed_y[0]  # y 최초 속도
})

# 사라질 무기, 공 정보
weapon_to_remove = -1
ball_to_remove = -1

running = True
while running:
    dt = clock.tick(75)

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키를 눌렀을 때
        if event.type == pygame.KEYDOWN:
            # 왼쪽으로 이동
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            # 오른쪽으로 이동
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            # 무기 발사
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        # 키를 뗐을 때
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정 (y 좌표만 줄어듦)
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    # 무기가 천장에 닿았을 때 무기없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 벽에 닿았을 때 공 이동 방향 변경
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] *= -1

        # 지면에 닿았을 때 공 이동 방향 변경... 그게 아니라면 속도를 줄임
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리
    # 공하고 캐릭터가 충돌
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공하고 무기가 충돌
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                # 충돌한 공과 무기 인덱스 값 저장
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                break

    # 충돌된 공과 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:  # 레이아웃 순서를 바꿈
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))

    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()  # 화면을 다시 그리기(필수)

# pygame 종료
pygame.quit()
