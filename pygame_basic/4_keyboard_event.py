import pygame

# 초기화 (반드시 필요함)
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))      # 게임 화면 크기 설정

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")     # 게임 이름

# 배경 이미지
background = pygame.image.load('C:/Yeseong31/Study/PROJECT/Pang_game/pygame_basic/background.png')

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load('C:/Yeseong31/Study/PROJECT/Pang_game/pygame_basic/character.png')
character_size = character.get_rect().size      # 이미지의 크기
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)    # 화면 정중앙 x좌표
character_y_pos = screen_height - character_height              # 화면 가장 아래 y 좌표

# 이동할 죄표
to_x , to_y = 0, 0

# 이벤트 루프
running = True      # 게임 진행 확인
while running:
    for event in pygame.event.get():        # 이벤트 발생 시
        if event.type == pygame.QUIT:       # 창이 닫히면 게임 종료
            running = False

        # 키 입력이 있다면
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= 5
            elif event.key == pygame.K_RIGHT:
                to_x += 5
            elif event.key == pygame.K_UP:
                to_y -= 5
            elif event.key == pygame.K_DOWN:
                to_y += 5

        # 키 입력이 끝났다면
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    # 캐릭터 이동
    character_x_pos += to_x
    character_y_pos += to_y

    # 화면 밖으로 벗어나지 않도록 설정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    screen.blit(background, (0, 0))     # (0, 0)부터 이미지를 복사해서 넣음
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()             # 화면을 다시 그리기(필수)

# pygame 종료
pygame.quit()
