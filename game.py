import pygame, sys, math
from utils import has_arithmetic_progression, find_winning_progression, find_all_arithmetic_progressions, generate_random_subset_with_progression
from algorithms import registry

BLACK = (0,0,0)
WHITE = (255,255,255)
PLAYER_COLOR = (0,0,255)
COMPUTER_COLOR = (255,0,0)

def draw_text_with_outline(screen, text, font, center, text_color=WHITE, outline_color=BLACK):
    txt = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx or dy:
                pos = (center[0]+dx, center[1]+dy)
                screen.blit(outline, outline.get_rect(center=pos))
    screen.blit(txt, txt.get_rect(center=center))

def show_all_progressions_screen(screen, font, progressions):
    clock = pygame.time.Clock()
    back_button = pygame.Rect(350,530,100,40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
        screen.fill((40,40,40))
        title = font.render("All Winning APs:", True, WHITE)
        screen.blit(title, (50,20))
        y = 60
        for prog in progressions:
            if len(prog) >= 2:
                d = prog[1] - prog[0]
            else:
                d = "N/A"
            prog_text = " ".join(str(n) for n in prog) + f" ; d = {d}"
            line = font.render(prog_text, True, WHITE)
            screen.blit(line, (50,y))
            y += 30
            if y > 500:
                break
        pygame.draw.rect(screen, (200,0,0), back_button)
        draw_text_with_outline(screen, "Back", font, back_button.center)
        pygame.display.flip()
        clock.tick(30)

def end_game_screen(screen, font, winner, forced_prog, all_progs, win_prog):
    clock = pygame.time.Clock()
    play_button = pygame.Rect(150,500,120,50)
    menu_button = pygame.Rect(330,500,120,50)
    show_ap_button = pygame.Rect(510,500,220,50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play_again"
                if menu_button.collidepoint(event.pos):
                    return "main_menu"
                if show_ap_button.collidepoint(event.pos):
                    show_all_progressions_screen(screen, font, all_progs)
        screen.fill((30,30,30))
        msg = f"{winner} wins!" if winner else "Draw!"
        draw_text_with_outline(screen, msg, font, (400,80))
        if winner and win_prog:
            if len(win_prog) >= 2:
                d_val = win_prog[1] - win_prog[0]
            else:
                d_val = "N/A"
            prog_str = "Winning AP: " + " ".join(str(n) for n in win_prog) + f" ; d = {d_val}"
            draw_text_with_outline(screen, prog_str, font, (400,140))
        else:
            prog_str = "Forced AP: " + " ".join(str(n) for n in forced_prog)
            if len(forced_prog) >= 2:
                d_val = forced_prog[1]-forced_prog[0]
            else:
                d_val = "N/A"
            prog_str += f" ; d = {d_val}"
            draw_text_with_outline(screen, prog_str, font, (400,140))
        pygame.draw.rect(screen, (0,200,0), play_button)
        draw_text_with_outline(screen, "Play Again", font, play_button.center)
        pygame.draw.rect(screen, (0,0,200), menu_button)
        draw_text_with_outline(screen, "Main Menu", font, menu_button.center)
        pygame.draw.rect(screen, (200,200,0), show_ap_button)
        draw_text_with_outline(screen, "Show All APs", font, show_ap_button.center)
        turn_info = font.render("Game Over", True, WHITE)
        screen.blit(turn_info, (10,10))
        pygame.display.flip()
        clock.tick(30)

def run_game(settings):
    k = settings.get("k",3)
    x = settings.get("x",20)
    lower = settings.get("lower",1)
    bound = settings.get("bound",100)
    ai_choice = settings.get("algorithm","random")
    ai_algorithm = registry.get(ai_choice, registry.get("random"))
    try:
        X, forced_prog = generate_random_subset_with_progression(k, x, lower, bound)
    except Exception as e:
        print("Error generating set:", e)
        sys.exit(1)
    # Check that at least one AP is possible in X.
    all_possible = find_all_arithmetic_progressions(k, X)
    if not all_possible:
        print("No arithmetic progression of length", k, "found with the given settings.")
        sys.exit(1)
    pygame.init()
    screen_width, screen_height = 800,600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Szemerédi's Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,24)
    left_margin = 20
    right_margin = 20
    top_margin = 80
    bottom_margin = 20
    cols = int(math.ceil(x**0.5))
    rows = int(math.ceil(x/cols))
    cell_width = (screen_width - left_margin - right_margin) / cols
    cell_height = (screen_height - top_margin - bottom_margin) / rows
    radius = int(min(cell_width, cell_height) / 2 * 0.8)
    cells = []
    for index in range(x):
        row = index // cols
        col = index % cols
        cx = left_margin + col * cell_width + cell_width / 2
        cy = top_margin + row * cell_height + cell_height / 2
        rect = pygame.Rect(cx-radius, cy-radius, 2*radius, 2*radius)
        cell = {"value": X[index], "center": (int(cx), int(cy)), "rect": rect, "color": BLACK}
        cells.append(cell)
    player_moves = []
    computer_moves = []
    available_indices = set(range(x))
    game_over = False
    winner = None
    turn = settings.get("first", "player").lower()
    turn_count = 1
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if turn == "player" and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in available_indices.copy():
                    cell = cells[i]
                    if cell["rect"].collidepoint(pos):
                        cell["color"] = PLAYER_COLOR
                        player_moves.append(cell["value"])
                        available_indices.remove(i)
                        if len(player_moves) > k:
                            game_over = True
                            winner = None
                        elif len(player_moves) == k and set(player_moves) == set(forced_prog):
                            winner = "Player"
                            game_over = True
                        turn = "computer"
                        turn_count += 1
                        break
        if turn == "computer" and not game_over:
            if available_indices:
                available_list = list(available_indices)
                chosen_index = ai_algorithm(available_list)
                cell = cells[chosen_index]
                cell["color"] = COMPUTER_COLOR
                computer_moves.append(cell["value"])
                available_indices.remove(chosen_index)
                if len(computer_moves) > k:
                    game_over = True
                    winner = None
                elif len(computer_moves) == k and set(computer_moves) == set(forced_prog):
                    winner = "Computer"
                    game_over = True
                turn = "player"
                turn_count += 1
            else:
                game_over = True
                winner = None
        if not available_indices:
            game_over = True
            if winner is None:
                winner = None
        screen.fill(WHITE)
        for cell in cells:
            pygame.draw.circle(screen, cell["color"], cell["center"], radius)
            pygame.draw.circle(screen, BLACK, cell["center"], radius, 2)
            draw_text_with_outline(screen, str(cell["value"]), font, cell["center"])
        turn_text = f"Turn: {turn.capitalize()}"
        count_text = f"Turn Number: {turn_count}"
        turn_surf = font.render(turn_text, True, BLACK)
        count_surf = font.render(count_text, True, BLACK)
        screen.blit(turn_surf, (10,10))
        screen.blit(count_surf, (10,40))
        pygame.display.flip()
        clock.tick(30)
    if winner == "Player":
        win_moves = player_moves
    else:
        win_moves = computer_moves
    win_prog = find_winning_progression(k, win_moves)
    all_progs = find_all_arithmetic_progressions(k, X)
    if forced_prog in all_progs:
        all_progs.remove(forced_prog)
    result = end_game_screen(screen, font, winner, forced_prog, all_progs, win_prog)
    pygame.quit()
    if result == "play_again":
        run_game(settings)
    else:
        return
