import pygame
import sys

pygame.init()
#screen setup
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("I Want to Be Friends!")
clock = pygame.time.Clock()
#colors
WHITE = (255, 255, 255)
BLK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

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