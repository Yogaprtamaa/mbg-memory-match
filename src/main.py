import pygame
from src.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_TITLE
from src.managers.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    scene_manager = SceneManager()
    scene_manager.set_scene(MenuScene(scene_manager))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)

        scene_manager.update()
        scene_manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
