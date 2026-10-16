import random
import pygame
from game.block import Block


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)
        self.debris = []

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def reset(self):
        self.score = 0
        self.game_over = False
        self.perfect_streak = 0
        self.perfect_message_timer = 0

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60
        base_block = Block(
            base_x, base_y, self.base_width,
            self.block_height, self.get_color(0), speed=0
        )
        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]
        next_y = top_block.y - self.block_height - 4
        speed = min(10.0, 4.5 + (len(self.stack) * 0.35))
        color = self.get_color(len(self.stack))

        start_x = 25 if random.choice([True, False]) else self.width - 25 - top_block.width
        self.active_block = Block(start_x, next_y, top_block.width, self.block_height, color, speed=speed)

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)
        right = min(act.x + act.width, top_block.x + top_block.width)
        overlap = right - left

        if overlap <= 0:
            self.game_over = True
            self.perfect_streak = 0
            return

        perfect_tolerance = 5
        is_perfect = abs(act.x - top_block.x) <= perfect_tolerance

        if is_perfect:
            new_x = top_block.x
            new_width = top_block.width
            self.perfect_streak += 1
            self.score += 5
            self.perfect_message_timer = 60
        else:
            new_x = left
            new_width = overlap
            self.perfect_streak = 0

            if act.x < top_block.x:
                debris_width = top_block.x - act.x
                debris_x = act.x
            else:
                debris_width = (act.x + act.width) - (top_block.x + top_block.width)
                debris_x = top_block.x + top_block.width

            if debris_width > 0:
                self.debris.append({
                    "x": debris_x,
                    "y": act.y,
                    "width": debris_width,
                    "height": self.block_height,
                    "vx": -3 if act.x < top_block.x else 3,
                    "vy": -2,
                    "color": act.color
                })

        new_block = Block(
            new_x,
            act.y,
            new_width,
            self.block_height,
            act.color,
            speed=0
        )

        self.stack.append(new_block)
        self.score += 1

        if self.perfect_streak > 0 and self.perfect_streak % 3 == 0:
            restored_width = min(new_block.width + 10, self.base_width)
            new_block.x -= (restored_width - new_block.width) / 2
            new_block.width = restored_width

        if new_block.y < 180:
            shift_amount = self.block_height + 4
            for block in self.stack:
                block.y += shift_amount

        self.spawn_active_block()

    def handle_event(self, event):
        if self.game_over:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.reset()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)

        if self.perfect_message_timer > 0:
            self.perfect_message_timer -= 1

        for piece in self.debris:
            piece["x"] += piece["vx"]
            piece["y"] += piece["vy"]
            piece["vy"] += 0.25

        self.debris = [
            piece for piece in self.debris
            if piece["y"] < self.height
        ]
    def get_background_color(self):
        height = len(self.stack) - 1

        if height < 5:
            return (24, 27, 36)
        elif height < 10:
            return (35, 45, 75)
        elif height < 15:
            return (75, 45, 85)
        elif height < 20:
            return (120, 55, 70)
        else:
            return (15, 15, 35)
    def render(self, screen):
        screen.fill(self.get_background_color())

        title_surf = self.font_title.render("Skyscraper Stack", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        score_surf = self.font_hud.render(f"Height: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))
        if self.perfect_message_timer > 0:
            perfect_surf = self.font_hud.render(
                "PERFECT! +5",
                True,
                (80, 255, 120)
            )
            screen.blit(
                perfect_surf,
                (self.width // 2 - perfect_surf.get_width() // 2, 90)
            )
        
        for piece in self.debris:
            pygame.draw.rect(
                screen,
                piece["color"],
                (
                    int(piece["x"]),
                    int(piece["y"]),
                    max(1, int(piece["width"])),
                    piece["height"]
                )
            )
        for b in self.stack:
            b.render(screen)

        if not self.game_over:
            self.active_block.render(screen)

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("TOWER COLLAPSED!", True, (240, 75, 75))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_hud.render(f"Final Height: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_hud.render("Press [Space] or [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
