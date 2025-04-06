import pygame
import sys
import logic_2048 as logic

SIZE=logic.SIZE
TILE_SIZE=100
MARGIN=10
TOP_MARGIN=100

WINDOW_WIDTH=SIZE*TILE_SIZE+(SIZE+1)*MARGIN
WINDOW_HEIGHT=SIZE*TILE_SIZE+(SIZE+1)*MARGIN+TOP_MARGIN

BG_COLOR=(187,173,160)
TEXT_COLOR=(119,110,101)
SCORE_COLOR=(249,246,242)
BUTTON_BG=(119,110,101)
BUTTON_TEXT=(255,255,255)

TILE_COLORS={
    0:(205,193,180),
    2:(238,228,218),
    4:(237,224,200),
    8:(242,177,121),
    16:(245,149,99),
    32:(246,124,95),
    64:(246,94,59),
    128:(237,207,114),
    256:(237,204,97),
    512:(237,200,80),
    1024:(237,197,63),
    2048:(237,194,46),
}

def draw_board(screen, board, score, font, ai_enabled):
    screen.fill(BG_COLOR)

    title_font=pygame.font.SysFont(None,60)
    title_surf=title_font.render("2048",True,TEXT_COLOR)
    screen.blit(title_surf,(MARGIN,MARGIN))

    score_text=f"Skóre: {score}"
    score_surf=font.render(score_text,True,SCORE_COLOR)
    screen.blit(score_surf,(MARGIN,60))

    ai_button_rect=pygame.Rect(WINDOW_WIDTH-130,10,120,40)
    pygame.draw.rect(screen,BUTTON_BG,ai_button_rect,border_radius=5)
    ai_status_text="AI: ON" if ai_enabled else "AI: OFF"
    ai_surf=font.render(ai_status_text,True,BUTTON_TEXT)
    ai_text_rect=ai_surf.get_rect(center=ai_button_rect.center)
    screen.blit(ai_surf,ai_text_rect)

    stats_button_rect=pygame.Rect(WINDOW_WIDTH-130,60,120,40)
    pygame.draw.rect(screen,BUTTON_BG,stats_button_rect,border_radius=5)
    stats_surf=font.render("Stats",True,BUTTON_TEXT)
    stats_text_rect=stats_surf.get_rect(center=stats_button_rect.center)
    screen.blit(stats_surf,stats_text_rect)

    for r in range(SIZE):
        for c in range(SIZE):
            value=board[r][c]
            color=TILE_COLORS[value] if value in TILE_COLORS else TILE_COLORS[2048]
            x=c*TILE_SIZE+(c+1)*MARGIN
            y=r*TILE_SIZE+(r+1)*MARGIN+TOP_MARGIN
            rect=pygame.Rect(x,y,TILE_SIZE,TILE_SIZE)
            pygame.draw.rect(screen,color,rect,border_radius=5)

            if value!=0:
                text_surf=font.render(str(value),True,TEXT_COLOR)
                text_rect=text_surf.get_rect(center=rect.center)
                screen.blit(text_surf,text_rect)

    return ai_button_rect, stats_button_rect

def get_max_tile(board):
    return max(max(row) for row in board)

def game_over(screen, board, score, moves, moves_by_direction, font, ai_enabled):
    # Check if the player won (reached 2048)
    max_tile = get_max_tile(board)
    won = max_tile >= logic.WIN_TILE
    
    # Display game over screen
    draw_board(screen, board, score, font, ai_enabled)
    pygame.display.flip()
    
    print("Konec hry! Skóre =", score)
    
    # Save statistics
    logic.add_stat(score, moves, max_tile, moves_by_direction, won)
    logic.print_stats()
    
    pygame.time.wait(3000)

def main():
    pygame.init()
    screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - (UP,LEFT,RIGHT) Nudging Logic")

    font=pygame.font.SysFont(None,40)
    clock=pygame.time.Clock()

    board=logic.init_board()
    score=0
    moves=0
    
    # Track moves by direction
    moves_by_direction = {"up": 0, "down": 0, "left": 0, "right": 0}

    ai_enabled=False
    ai_move_delay=2
    ai_frame_counter=0

    running=True
    while running:
        clock.tick(60)
        ai_frame_counter+=1

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                # Save stats on exit
                if moves > 0:
                    game_over(screen, board, score, moves, moves_by_direction, font, ai_enabled)
                running=False

            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=event.pos
                ai_button_rect,stats_button_rect=draw_board(screen,board,score,font,ai_enabled)
                pygame.display.flip()

                if ai_button_rect.collidepoint(mouse_pos):
                    ai_enabled=not ai_enabled
                elif stats_button_rect.collidepoint(mouse_pos):
                    logic.print_stats()

            elif event.type==pygame.KEYDOWN and not ai_enabled:
                moved=False
                if event.key in (pygame.K_UP,pygame.K_w):
                    nb,ch,score=logic.move_up(board,score)
                    if ch:
                        board=nb
                        moved=True
                        moves_by_direction["up"] += 1
                elif event.key in (pygame.K_DOWN,pygame.K_s):
                    nb,ch,score=logic.move_down(board,score)
                    if ch:
                        board=nb
                        moved=True
                        moves_by_direction["down"] += 1
                elif event.key in (pygame.K_LEFT,pygame.K_a):
                    nb,ch,score=logic.move_left(board,score)
                    if ch:
                        board=nb
                        moved=True
                        moves_by_direction["left"] += 1
                elif event.key in (pygame.K_RIGHT,pygame.K_d):
                    nb,ch,score=logic.move_right(board,score)
                    if ch:
                        board=nb
                        moved=True
                        moves_by_direction["right"] += 1

                if moved:
                    moves+=1
                    logic.spawn_new_tile(board)
                    if not logic.can_move(board):
                        game_over(screen, board, score, moves, moves_by_direction, font, ai_enabled)
                        running=False
                        break
                        
        if ai_enabled and ai_frame_counter>=ai_move_delay:
            ai_frame_counter=0
            new_b,changed,new_score=logic.ai_move(board,score)
            if changed:
                # Try to figure out what direction AI moved 
                # by comparing to potential moves
                old_score = score
                test_up, ch_up, score_up = logic.move_up(board.copy(), score)
                test_down, ch_down, score_down = logic.move_down(board.copy(), score)
                test_left, ch_left, score_left = logic.move_left(board.copy(), score)
                test_right, ch_right, score_right = logic.move_right(board.copy(), score)
                
                # Check which direction the AI moved
                if ch_up and new_b == test_up:
                    moves_by_direction["up"] += 1
                elif ch_down and new_b == test_down:
                    moves_by_direction["down"] += 1
                elif ch_left and new_b == test_left:
                    moves_by_direction["left"] += 1
                elif ch_right and new_b == test_right:
                    moves_by_direction["right"] += 1
                    
                moves+=1
                board=new_b
                score=new_score
                logic.spawn_new_tile(board)
                if not logic.can_move(board):
                    game_over(screen, board, score, moves, moves_by_direction, font, ai_enabled)
                    running=False

        ai_button_rect,stats_button_rect=draw_board(screen,board,score,font,ai_enabled)
        pygame.display.flip()

    sys.exit()

if __name__=="__main__":
    main()