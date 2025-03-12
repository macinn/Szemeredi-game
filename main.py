import pygame, sys
from game import run_game
from algorithms import registry

def settings_screen():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Szemerédi's Game - Settings")
    font = pygame.font.Font(None,32)
    clock = pygame.time.Clock()
    algo_names = list(registry.keys())
    if not algo_names:
        algo_names = ["random"]
    input_boxes = {
        "k": {"rect": pygame.Rect(300,100,140,32), "text": "3"},
        "x": {"rect": pygame.Rect(300,150,140,32), "text": "20"},
        "lower": {"rect": pygame.Rect(300,200,140,32), "text": "1"},
        "bound": {"rect": pygame.Rect(300,250,140,32), "text": "100"}
    }
    algo_box = {"rect": pygame.Rect(300,300,140,32), "selected": algo_names[0], "options": algo_names, "open": False}
    first_box = {"rect": pygame.Rect(300,350,140,32), "selected": "player", "options": ["player", "computer"], "open": False}
    start_button = pygame.Rect(250,420,120,50)
    exit_button = pygame.Rect(430,420,120,50)
    active_box = None
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    error_msg = ""
    error_timer = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if algo_box["rect"].collidepoint(event.pos):
                    algo_box["open"] = not algo_box["open"]
                elif first_box["rect"].collidepoint(event.pos):
                    first_box["open"] = not first_box["open"]
                else:
                    if algo_box["open"]:
                        for i, option in enumerate(algo_box["options"]):
                            opt_rect = pygame.Rect(algo_box["rect"].x, algo_box["rect"].y+32*(i+1), algo_box["rect"].w,32)
                            if opt_rect.collidepoint(event.pos):
                                algo_box["selected"] = option
                                algo_box["open"] = False
                                break
                    if first_box["open"]:
                        for i, option in enumerate(first_box["options"]):
                            opt_rect = pygame.Rect(first_box["rect"].x, first_box["rect"].y+32*(i+1), first_box["rect"].w,32)
                            if opt_rect.collidepoint(event.pos):
                                first_box["selected"] = option
                                first_box["open"] = False
                                break
                    for key, box in input_boxes.items():
                        if box["rect"].collidepoint(event.pos):
                            active_box = key
                            break
                    else:
                        active_box = None
                if start_button.collidepoint(event.pos):
                    try:
                        k_val = int(input_boxes["k"]["text"])
                        x_val = int(input_boxes["x"]["text"])
                        lower_val = int(input_boxes["lower"]["text"])
                        bound_val = int(input_boxes["bound"]["text"])
                        if lower_val>bound_val or k_val<=0 or x_val<k_val or x_val>(bound_val-lower_val+1):
                            raise ValueError
                        running = False
                    except:
                        error_msg = "Invalid input! Resetting to default."
                        error_timer = pygame.time.get_ticks()
                        input_boxes["k"]["text"] = "3"
                        input_boxes["x"]["text"] = "20"
                        input_boxes["lower"]["text"] = "1"
                        input_boxes["bound"]["text"] = "100"
                        algo_box["selected"] = algo_box["options"][0]
                        first_box["selected"] = "player"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type==pygame.KEYDOWN and active_box is not None:
                if event.key==pygame.K_RETURN:
                    active_box = None
                elif event.key==pygame.K_BACKSPACE:
                    input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                else:
                    input_boxes[active_box]["text"] += event.unicode
        screen.fill((30,30,30))
        for key, box in input_boxes.items():
            txt_surface = font.render(box["text"], True, (255,255,255))
            width = max(140, txt_surface.get_width()+10)
            box["rect"].w = width
            color = color_active if active_box==key else color_inactive
            pygame.draw.rect(screen, color, box["rect"], 2)
            screen.blit(txt_surface, (box["rect"].x+5, box["rect"].y+5))
            label = font.render(key, True, (255,255,255))
            screen.blit(label, (box["rect"].x-150, box["rect"].y+5))
        pygame.draw.rect(screen, color_inactive, algo_box["rect"], 2)
        algo_txt = font.render(algo_box["selected"], True, (255,255,255))
        screen.blit(algo_txt, (algo_box["rect"].x+5, algo_box["rect"].y+5))
        label = font.render("algorithm", True, (255,255,255))
        screen.blit(label, (algo_box["rect"].x-150, algo_box["rect"].y+5))
        if algo_box["open"]:
            for i, option in enumerate(algo_box["options"]):
                opt_rect = pygame.Rect(algo_box["rect"].x, algo_box["rect"].y+32*(i+1), algo_box["rect"].w,32)
                pygame.draw.rect(screen, color_inactive, opt_rect,2)
                opt_txt = font.render(option, True, (255,255,255))
                screen.blit(opt_txt, (opt_rect.x+5, opt_rect.y+5))
        pygame.draw.rect(screen, color_inactive, first_box["rect"], 2)
        first_txt = font.render(first_box["selected"], True, (255,255,255))
        screen.blit(first_txt, (first_box["rect"].x+5, first_box["rect"].y+5))
        label = font.render("first", True, (255,255,255))
        screen.blit(label, (first_box["rect"].x-150, first_box["rect"].y+5))
        if first_box["open"]:
            for i, option in enumerate(first_box["options"]):
                opt_rect = pygame.Rect(first_box["rect"].x, first_box["rect"].y+32*(i+1), first_box["rect"].w,32)
                pygame.draw.rect(screen, color_inactive, opt_rect,2)
                opt_txt = font.render(option, True, (255,255,255))
                screen.blit(opt_txt, (opt_rect.x+5, opt_rect.y+5))
        pygame.draw.rect(screen, (0,200,0), start_button)
        start_text = font.render("Start Game", True, (255,255,255))
        start_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, (200,0,0), exit_button)
        exit_text = font.render("Exit Game", True, (255,255,255))
        exit_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_rect)
        if error_msg:
            err_text = font.render(error_msg, True, (255,0,0))
            screen.blit(err_text, (250,430))
            if pygame.time.get_ticks()-error_timer>3000:
                error_msg = ""
        pygame.display.flip()
        clock.tick(30)
    settings = {"k": int(input_boxes["k"]["text"]),
                "x": int(input_boxes["x"]["text"]),
                "lower": int(input_boxes["lower"]["text"]),
                "bound": int(input_boxes["bound"]["text"]),
                "algorithm": algo_box["selected"].lower(),
                "first": first_box["selected"].lower()}
    pygame.quit()
    return settings

if __name__=="__main__":
    from algorithms import registry
    while True:
        s = settings_screen()
        run_game(s)
