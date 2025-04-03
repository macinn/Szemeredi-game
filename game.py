import pygame, sys, math
from typing import List, Dict, Any, Set, Optional
from utils import has_arithmetic_progression, find_winning_progression, find_all_arithmetic_progressions
from utils import generate_random_subset_with_progression
from algorithms import registry

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
PLAYER_COLOR: tuple[int, int, int] = (0, 0, 255)
COMPUTER_COLOR: tuple[int, int, int] = (255, 0, 0)

def draw_text_with_outline(screen: pygame.Surface, text: str, font: pygame.font.Font, center: tuple[int, int],
                           text_color: tuple[int, int, int] = WHITE, outline_color: tuple[int, int, int] = BLACK) -> None:
    txt = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                pos = (center[0] + dx, center[1] + dy)
                screen.blit(outline, outline.get_rect(center=pos))
    screen.blit(txt, txt.get_rect(center=center))

def show_all_progressions_screen(screen: pygame.Surface, font: pygame.font.Font, progressions: List[List[int]]) -> None:
    clock = pygame.time.Clock()
    back_button = pygame.Rect(350, 530, 100, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
        screen.fill((40, 40, 40))
        title = font.render("All Winning APs:", True, WHITE)
        screen.blit(title, (50, 20))
        y = 60
        for prog in progressions:
            d = prog[1] - prog[0] if len(prog) >= 2 else "N/A"
            prog_text = " ".join(str(n) for n in prog) + f" ; d = {d}"
            line = font.render(prog_text, True, WHITE)
            screen.blit(line, (50, y))
            y += 30
            if y > 500:
                break
        pygame.draw.rect(screen, (200, 0, 0), back_button)
        draw_text_with_outline(screen, "Back", font, back_button.center)
        pygame.display.flip()
        clock.tick(30)

def end_game_screen(screen: pygame.Surface, font: pygame.font.Font, winner: Optional[str],
                    forced_prog: List[int], all_progs: List[List[int]], win_prog: Optional[List[int]]) -> str:
    clock = pygame.time.Clock()
    play_button = pygame.Rect(150, 500, 120, 50)
    menu_button = pygame.Rect(330, 500, 120, 50)
    show_ap_button = pygame.Rect(510, 500, 220, 50)
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
        screen.fill((30, 30, 30))
        msg = f"{winner} wins!" if winner else "Draw!"
        draw_text_with_outline(screen, msg, font, (400, 80))
        if winner and win_prog:
            d_val = win_prog[1] - win_prog[0] if len(win_prog) >= 2 else "N/A"
            prog_str = "Winning AP: " + " ".join(str(n) for n in win_prog) + f" ; d = {d_val}"
            draw_text_with_outline(screen, prog_str, font, (400, 140))
        else:
            d_val = forced_prog[1] - forced_prog[0] if len(forced_prog) >= 2 else "N/A"
            prog_str = "Forced AP: " + " ".join(str(n) for n in forced_prog) + f" ; d = {d_val}"
            draw_text_with_outline(screen, prog_str, font, (400, 140))
        pygame.draw.rect(screen, (0, 200, 0), play_button)
        draw_text_with_outline(screen, "Play Again", font, play_button.center)
        pygame.draw.rect(screen, (0, 0, 200), menu_button)
        draw_text_with_outline(screen, "Main Menu", font, menu_button.center)
        pygame.draw.rect(screen, (200, 200, 0), show_ap_button)
        draw_text_with_outline(screen, "Show All APs", font, show_ap_button.center)
        turn_info = font.render("Game Over", True, WHITE)
        screen.blit(turn_info, (10, 10))
        pygame.display.flip()
        clock.tick(30)

def run_game(settings: Dict[str, Any]) -> None:
    k: int = settings.get("k", 3)
    x: int = settings.get("x", 20)
    lower: int = settings.get("lower", 1)
    bound: int = settings.get("bound", 100)
    ai_choice: str = settings.get("algorithm", "random")
    ai_algorithm = registry.get(ai_choice.lower(), registry.get("random"))
    try:
        X, forced_prog = generate_random_subset_with_progression(k, x, lower, bound)
    except Exception as e:
        print("Error generating set:", e)
        sys.exit(1)
    all_possible: List[List[int]] = find_all_arithmetic_progressions(k, X)
    if not all_possible:
        print("No arithmetic progression of length", k, "found with the given settings.")
        sys.exit(1)
    pygame.init()
    screen_width: int = 800
    screen_height: int = 600
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Szemerédi's Game")
    clock = pygame.time.Clock()
    font: pygame.font.Font = pygame.font.Font(None, 24)
    left_margin: int = 20
    right_margin: int = 20
    top_margin: int = 80
    bottom_margin: int = 20
    cols: int = int(math.ceil(x**0.5))
    rows: int = int(math.ceil(x / cols))
    cell_width: float = (screen_width - left_margin - right_margin) / cols
    cell_height: float = (screen_height - top_margin - bottom_margin) / rows
    radius: int = int(min(cell_width, cell_height) / 2 * 0.8)
    cells: List[Dict[str, Any]] = []
    for index in range(x):
        row: int = index // cols
        col: int = index % cols
        cx: float = left_margin + col * cell_width + cell_width / 2
        cy: float = top_margin + row * cell_height + cell_height / 2
        rect: pygame.Rect = pygame.Rect(int(cx - radius), int(cy - radius), 2 * radius, 2 * radius)
        cell: Dict[str, Any] = {"value": X[index], "center": (int(cx), int(cy)), "rect": rect, "color": BLACK}
        cells.append(cell)
    player_moves: List[int] = []
    computer_moves: List[int] = []
    available_indices: Set[int] = set(range(x))
    game_over: bool = False
    winner: Optional[str] = None
    turn: str = settings.get("first", "player").lower()
    turn_count: int = 1
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
                        if has_arithmetic_progression(k, player_moves):
                            winner = "Player"
                            game_over = True
                        turn = "computer"
                        turn_count += 1
                        break
        if turn == "computer" and not game_over:
            if available_indices:
                available_numbers: List[int] = [cells[i]["value"] for i in available_indices]
                chosen_number: int = ai_algorithm(available_numbers, computer_moves, player_moves, k)
                chosen_index: Optional[int] = None
                for idx in available_indices:
                    if cells[idx]["value"] == chosen_number:
                        chosen_index = idx
                        break
                if chosen_index is None:
                    chosen_index = available_indices.pop()
                else:
                    available_indices.remove(chosen_index)
                cell = cells[chosen_index]
                cell["color"] = COMPUTER_COLOR
                computer_moves.append(cell["value"])
                if has_arithmetic_progression(k, computer_moves):
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
        turn_text: str = f"Turn: {turn.capitalize()}"
        count_text: str = f"Turn Number: {turn_count}"
        turn_surf = font.render(turn_text, True, BLACK)
        count_surf = font.render(count_text, True, BLACK)
        screen.blit(turn_surf, (10, 10))
        screen.blit(count_surf, (10, 40))
        pygame.display.flip()
        clock.tick(30)
    if winner == "Player":
        win_prog = next((ap for ap in all_possible if set(player_moves) >= set(ap)), None)
    elif winner == "Computer":
        win_prog = next((ap for ap in all_possible if set(computer_moves) >= set(ap)), None)
    else:
        win_prog = None
    if forced_prog in all_possible:
        all_possible.remove(forced_prog)
    result: str = end_game_screen(screen, font, winner, forced_prog, all_possible, win_prog)
    pygame.quit()
    if result == "play_again":
        run_game(settings)
    else:
        return
