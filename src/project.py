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