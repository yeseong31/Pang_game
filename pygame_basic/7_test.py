import pygame

# 초기화 (반드시 필요함)
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))      # 게임 화면 크기 설정

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")     # 게임 이름

# FPS
clock = pygame.time.Clock()

# 배경 이미지
background = pygame.image.load('C:/Yeseong31/Study/PROJECT/Pang_game/pygame_basic/background.png')

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load('C:/Yeseong31/Study/PROJECT/Pang_game/pygame_basic/character.png')
character_size = character.get_rect().size      # 이미지의 크기
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)    # 캐릭터 x좌표
character_y_pos = screen_height - character_height              # 캐릭터 y 좌표

# 이동할 죄표
to_x , to_y = 0, 0
# 이동 속도
character_speed = 0.6

# 적 enemy 캐릭터
enemy = pygame.image.load('C:/Yeseong31/Study/PROJECT/Pang_game/pygame_basic/enemy.png')
enemy_size = enemy.get_rect().size      # 이미지의 크기
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = (screen_width / 2) - (enemy_width / 2)    # enemy x좌표
enemy_y_pos = (screen_height / 2) - (enemy_height / 2)  # enemy y 좌표

# 폰트 정의
game_font = pygame.font.Font(None, 40)      # 폰트 객체 생성

# 총 시간
total_time = 10
# 시작 시간
start_ticks = pygame.time.get_ticks()       # 시작 tick을 받음

# 이벤트 루프
running = True      # 게임 진행 확인
while running:
    # 게임 화면의 초당 프레임 수 설정
    dt = clock.tick(75)

    print("fps: " + str(clock.get_fps()))

    for event in pygame.event.get():        # 이벤트 발생 시
        if event.type == pygame.QUIT:       # 창이 닫히면 게임 종료
            running = False

        # 키 입력이 있다면
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        # 키 입력이 끝났다면
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    # 캐릭터 이동
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 화면 밖으로 벗어나지 않도록 설정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌하였음")
        running = False

    screen.blit(background, (0, 0))     # (0, 0)부터 이미지를 복사해서 넣음
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 타이머 집어 넣기
    # 경과 시간 계산
    elapse_time = (pygame.time.get_ticks() - start_ticks) / 1000    # 경과 시간을 1000으로 나눠서 초 단위로 표시

    timer = game_font.render(str(int(total_time - elapse_time)), True, (255, 255, 255))     # 시간, True, 색상
    screen.blit(timer, (10, 10))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapse_time <= 0:
        print("타임아웃")
        running = False

    pygame.display.update()             # 화면을 다시 그리기(필수)

# 잠시 대기
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
