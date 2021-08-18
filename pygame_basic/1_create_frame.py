import pygame

# 초기화 (반드시 필요함)
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))      # 게임 화면 크기 설정

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")     # 게임 이름

# 이벤트 루프
running = True      # 게임 진행 확인
while running:
    for event in pygame.event.get():    # 이벤트 발생 시
        if event.type == pygame.QUIT:   # 창이 닫히면
            running = False             # 게임 종료

# pygame 종료
pygame.quit()