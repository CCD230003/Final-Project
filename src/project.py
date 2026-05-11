import pygame
import sys

pygame.init()
# screen setup
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("I Want to Be Friends!")
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# fonts
font_small = pygame.font.Font(None, 36)
font_text = pygame.font.Font(None, 28)

# dialogue box settings
dialogue_box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 120)
dialogue_padding = 10

class VisualNovel():

    def __init__(self):
        self.script = [{"char": "Finn", "text": "He's so cool..."},
                       {"char": "Finn", "text": "I should talk to him. Like, now. Like, right now."},
                       {"char": "Tito", "text": "Can I help you?"},
                       {"char": "Finn", "text": "Huh?", "choices": [("Huh?", 5), ("Me?", 6)]},

                       ]
        self.current_line = 0
        self.display_text = ""
        self.text_idx = 0
        self.text_speed = 30
        self.last_update = pygame.time.get_ticks()
        self.done_typing = False
        self.showing_choices = False
        self.choices_rects = []
        self.ending = False

    def reset(self):
        self.current_line = 0
        self.display_text = ""
        self.text_idx = 0
        self.done_typing = False
        self.showing_choices = False
        self.ending = False
        self.start_typing()

    def start_typing(self):
        line = self.script[self.current_line]
        self.display_text = ""
        self.text_idx = 0
        self.done_typing = False
        self.last_update = pygame.time.get_ticks()
        self.showing_choices = False
    
    def update_text(self):
        if not self.done_typing and not self.showing_choices:
            current_time = pygame.time.get_ticks
            if current_time - self.last_update >= self.text_speed:
                line = self.script[self.current_line]
                if self.text_idx < len(line["text"]):
                    self.display_text += line["text"][self.text_idx]
                    self.text_idx += 1
                    self.last_update = current_time
                else:
                    self.done_typing = True
                    if "choices" in line and not self.ending:
                        self.showing_choices = True
                        self.create_choice_buttons()

    def create_choice_buttons(self):
        self.choices_rects = []
        line = self.script[self.current_line]
        start_y = SCREEN_HEIGHT - 130

        for i, (choice_txt, _) in enumerate(line["choices"]):
            btn_rect = pygame.Rect(70, start_y + i * 40, SCREEN_WIDTH - 140, 35)
        self.choices_rects.append((btn_rect, choice_txt, i))
    
    def handle_choice_click(self, pos):
        if not self.showing_choices:
            return False
        for rect, choice_txt, idx in self.choices_rects:
            if rect.collidepoint(pos):
                line = self.script[self.current_line]
                _, next_line = line["choices"][idx]
                self.current_line = next_line
                self.start_typing()
                return True
        return False
    
    def advance(self):
        if self.showing_choices:
            return
        if not self.done_typing:
            line = self.script[self.current_line]
            self.display_text = line["text"]
            self.done_typing = True
            if "choices" in line and not self.ending:
                self.showing_choices = True
                self.create_choice_buttons()
        else:
            self.current_line += 1
            if self.current_line >= len(self.script):
                self.ending = True
            self.start_typing
    
    def draw(self, screen):
        for i in range(SCREEN_HEIGHT):
            color_value = 20 + i // 3
            pygame.draw.line(screen, (color_value, color_value, color_value), (0, i), (SCREEN_WIDTH, i))

        line = self.script[self.current_line]
        if not self.ending:
            name_surface = font_small.render(line["char"], True, LIGHT_GRAY)
            name_rect = name_surface.get_rect()
            name_rect.topleft = (dialogue_box_rect.x + dialogue_padding, dialogue_box_rect.y - 30)
            screen.blit(name_surface, name_rect)

        pygame.draw.rect(screen, DARK_GRAY, dialogue_box_rect)
        pygame.draw.rect(screen, LIGHT_GRAY, dialogue_box_rect, 2)
        if not self.ending:
            words = self.display_text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if font_text.size(test_line)[0] < dialogue_box_rect.width - 20:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
                    lines.append(current_line)
                    y_offset = 0
            for line_text in lines:
                text_surface = font_text.render(line_text, True, WHITE)
                screen.blit(text_surface, (dialogue_box_rect.x + dialogue_padding, dialogue_box_rect.y + dialogue_padding + y_offset))
                y_offset = 30
        if self.showing_choices:
            for rect, choice_text, _ in self.choices_rects:
                pygame.draw.rect(screen, (80, 80, 100), rect)
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 2)
                text_surface = font_small.render(choice_text, True, WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
        if not self.showing_choices and not self.ending:
            hint = font_small.render("Click anywhere to continue.", True, LIGHT_GRAY)
            hint_rect = hint.get_rect()
            hint_rect.bottomright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)
            screen.blit(hint, hint_rect)
        elif self.ending:
            restart_text = font_small.render("Click to restart.", True, LIGHT_GRAY)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
            screen.blit(restart_text, restart_rect)


def main():
    vn = VisualNovel()
    vn.start_typing()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if vn.ending:
                    vn = VisualNovel()
                    vn.start_typing()
                elif vn.showing_choices:
                    vn.handle_choice_click(event.pos)
                else:
                    vn.advance()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if vn.ending:
                        vn = VisualNovel()
                        vn.start_typing()
                    elif not vn.showing_choices:
                        vn.advance()
        vn.update_text()
        vn.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()