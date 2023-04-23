import pygame

pygame.init()

width=960
height=720
screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("Maze")

maze_pattern=[
    [1,1,1,1,2,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,1,1,0,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1],
    [1,1,1,3,1,1,1,1,1],

]
maze_width=len(maze_pattern[0])
maze_height=len(maze_pattern)
maze_pos=[0,0]
maze_offset=[0,0]
cell_size=50

start_pos=[0,0]
final_pos=[0,0]
for y,row in enumerate(maze_pattern):
    if 2 in row:
        start_pos=[row.index(2),y]
    elif 3 in row:
        final_pos=[row.index(3),y]
player_pos=[start_pos[0],start_pos[1]]
player_block=False
player_texture=pygame.image.load("character.png")
player_texture=pygame.transform.scale(player_texture, (cell_size,cell_size))

clock = pygame.time.Clock()
elapsed_time = 0
timer_time=10
timer_time_curr=timer_time #sec
timer_pos=[0,0]
timer_start=False
record=timer_time
tick_counter=0

font = pygame.font.SysFont(None, 0)
timer_text = font.render(f'{timer_time_curr}', True, (255, 0, 255))

running=True
while running:
    w, h = pygame.display.get_surface().get_size()
    font = pygame.font.SysFont(None, (w+h)//20)
    if timer_start:
        timer_text = font.render(f'{timer_time_curr}', True, (255, 0, 255))
        timer_pos = [w // 2 - timer_text.get_width() // 2, timer_text.get_height()]
        if timer_time_curr==0:
            timer_text = font.render(f'FAILED. Try again', True, (255, 0, 255))
            timer_pos = [w // 2 - timer_text.get_width() // 2, timer_text.get_height()]
            timer_start=0
        if pygame.time.get_ticks()-tick_counter>1000:
            timer_time_curr-=1
            tick_counter=pygame.time.get_ticks()
    if w>h:
        cell_size=int(h/maze_height)
        maze_pos=[w//2-maze_width*cell_size//2,0]
    else:
        cell_size=int(w/maze_width)
        maze_pos=[0,h // 2 - maze_height * cell_size//2]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_q:
                running=False
            elif event.key==pygame.K_w and player_pos[1] > 0 and maze_pattern[player_pos[1]-1][player_pos[0]]!=1 and not player_block:
                player_pos[1]-=1
                timer_start=True
            elif event.key==pygame.K_s and player_pos[1] < maze_height-1 and maze_pattern[player_pos[1]+1][player_pos[0]]!=1 and not player_block:
                player_pos[1]+=1
                timer_start = True
            elif event.key==pygame.K_d and player_pos[0] < maze_width-1 and maze_pattern[player_pos[1]][player_pos[0]+1]!=1 and not player_block:
                player_pos[0]+=1
                timer_start = True
            elif event.key==pygame.K_a and player_pos[0] > 0 and maze_pattern[player_pos[1]][player_pos[0]-1]!=1 and not player_block:
                player_pos[0]-=1
                timer_start = True
            elif event.key==pygame.K_SPACE:
                timer_start=True
                player_block=False
                timer_time_curr=timer_time
    if player_pos==final_pos:
        player_pos=[start_pos[0],start_pos[1]]
        elapsed_time=timer_time-timer_time_curr
        timer_start = 0
        player_block=True
        if elapsed_time<record:
            record=elapsed_time
            timer_text = font.render(f'NEW RECORD-{record}.SPACE to try again', True, (255, 0, 255))
            timer_pos = [w // 2 - timer_text.get_width() // 2, timer_text.get_height()]


    screen.fill((0, 255, 255))

    for y, row in enumerate(maze_pattern):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((x * cell_size)+maze_pos[0], (y * cell_size)+maze_pos[1], cell_size, cell_size))
    #pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((player_pos[0] * cell_size)+maze_pos[0], (player_pos[1] * cell_size)+maze_pos[1], cell_size, cell_size))
    screen.blit(player_texture, ((player_pos[0] * cell_size)+maze_pos[0],(player_pos[1] * cell_size)+maze_pos[1]))
    screen.blit(timer_text, timer_pos)

    pygame.display.flip()

    clock.tick(60)