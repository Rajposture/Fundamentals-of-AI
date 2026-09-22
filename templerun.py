"""
TEMPLE RUNNER — Reworked Edition
A polished single-file pygame endless runner in the "Temple Run" style:
3-lane pseudo-3D path, jump/slide/strafe, obstacle variety, coins,
power-ups, particle FX, animated torches, parallax jungle, camera shake,
combo scoring, and persistent high score.

Controls:
  LEFT / A / RIGHT / D  - change lane
  UP / W / SPACE        - jump
  DOWN / S               - slide
  R                      - restart after death
  ESC                    - quit
"""

import pygame
import random
import sys
import math
import json
import os

pygame.init()
pygame.mixer.init(buffer=512)

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temple Runner")
clock = pygame.time.Clock()

HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temple_runner_highscore.json")

HORIZON_Y = 210
GROUND_Y = HEIGHT - 70
LANE_SPACING = 190
LANES_X = [WIDTH // 2 - LANE_SPACING, WIDTH // 2, WIDTH // 2 + LANE_SPACING]

GRAVITY = 1.05
JUMP_POWER = -19
SLIDE_FRAMES = 26
LANE_SWITCH_SPEED = 0.28

# Palette — warm jungle-temple dusk
SKY_TOP = (18, 12, 38)
SKY_MID = (72, 34, 62)
SKY_BOTTOM = (168, 84, 66)
SUN_COLOR = (255, 196, 110)
STONE_DARK = (52, 40, 46)
STONE_MID = (86, 66, 58)
STONE_LIGHT = (128, 100, 78)
PATH_COLOR = (104, 80, 62)
PATH_EDGE = (58, 42, 36)
PATH_SEAM = (150, 118, 86)
VINE_GREEN = (56, 92, 48)
VINE_DARK = (34, 58, 30)
GOLD = (255, 210, 80)
GOLD_DARK = (196, 150, 44)
RED = (222, 70, 62)
EMBER = (255, 130, 40)
WHITE = (245, 245, 245)
SHADOW_COLOR = (8, 6, 12)
SKIN = (222, 178, 140)
HAIR = (58, 38, 24)
SHIRT = (200, 64, 58)
SHIRT_DARK = (160, 46, 42)
PANTS = (58, 48, 66)

font_title = pygame.font.SysFont("arial", 68, bold=True)
font_big = pygame.font.SysFont("arial", 46, bold=True)
font_med = pygame.font.SysFont("arial", 30, bold=True)
font_small = pygame.font.SysFont("arial", 20)
font_tiny = pygame.font.SysFont("arial", 16)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ease_out(t):
    return 1 - (1 - t) ** 3


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f).get("high_score", 0)
    except Exception:
        return 0


def save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump({"high_score": value}, f)
    except Exception:
        pass


# ----------------------------------------------------------------------------
# BACKGROUND LAYERS
# ----------------------------------------------------------------------------
class Star:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HORIZON_Y * 0.8)
        self.r = random.uniform(0.6, 1.8)
        self.phase = random.uniform(0, math.tau)

    def draw(self, surf, t):
        flicker = 0.6 + 0.4 * math.sin(t * 2 + self.phase)
        c = int(200 * flicker) + 55
        pygame.draw.circle(surf, (c, c, min(255, c + 20)), (int(self.x), int(self.y)), self.r)


STARS = [Star() for _ in range(70)]


def draw_sky(t):
    for y in range(0, HORIZON_Y):
        f = y / HORIZON_Y
        if f < 0.55:
            tt = f / 0.55
            color = (lerp(SKY_TOP[0], SKY_MID[0], tt), lerp(SKY_TOP[1], SKY_MID[1], tt), lerp(SKY_TOP[2], SKY_MID[2], tt))
        else:
            tt = (f - 0.55) / 0.45
            color = (lerp(SKY_MID[0], SKY_BOTTOM[0], tt), lerp(SKY_MID[1], SKY_BOTTOM[1], tt), lerp(SKY_MID[2], SKY_BOTTOM[2], tt))
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    for s in STARS:
        s.draw(screen, t)

    sun_pos = (WIDTH // 2, HORIZON_Y - 6)
    glow = pygame.Surface((260, 260), pygame.SRCALPHA)
    for r in range(130, 0, -2):
        a = int(70 * (1 - r / 130) ** 2)
        pygame.draw.circle(glow, (*SUN_COLOR, a), (130, 130), r)
    screen.blit(glow, (sun_pos[0] - 130, sun_pos[1] - 130))
    pygame.draw.circle(screen, SUN_COLOR, sun_pos, 46)


def draw_distant_ruins(offset):
    base_y = HORIZON_Y
    silhouette = (36, 22, 34)
    random.seed(42)
    x = -60
    while x < WIDTH + 120:
        h = random.randint(30, 90)
        w = random.randint(50, 90)
        sway = math.sin((x + offset * 40) * 0.002) * 4
        pygame.draw.rect(screen, silhouette, (x + sway, base_y - h, w, h))
        pygame.draw.polygon(screen, silhouette, [(x + sway, base_y - h), (x + sway + w / 2, base_y - h - 22), (x + sway + w, base_y - h)])
        x += w + random.randint(40, 90)
    random.seed()


# ----------------------------------------------------------------------------
# PATH / ENVIRONMENT
# ----------------------------------------------------------------------------
class Torch:
    def __init__(self, side, i):
        self.side = side
        self.i = i
        self.flicker = random.uniform(0, 10)

    def draw(self, offset, t):
        idx = (self.i + int(offset)) % 8
        loop = ((self.i - offset) % 8) / 8
        if loop < 0.05:
            return
        y = lerp(HORIZON_Y, HEIGHT + 40, loop)
        scale = lerp(0.08, 1.15, loop)
        x = WIDTH // 2 + self.side * lerp(70, 470, loop)
        if scale < 0.05:
            return

        pole_h = 90 * scale
        pygame.draw.rect(screen, STONE_DARK, (x - 6 * scale, y - pole_h, 12 * scale, pole_h))
        flick = 0.75 + 0.25 * math.sin(t * 9 + self.flicker)
        flame_h = 26 * scale * flick
        flame_w = 14 * scale
        fx, fy = x, y - pole_h
        pygame.draw.polygon(screen, EMBER, [(fx, fy - flame_h), (fx - flame_w / 2, fy + 4 * scale), (fx + flame_w / 2, fy + 4 * scale)])
        pygame.draw.polygon(screen, GOLD, [(fx, fy - flame_h * 0.55), (fx - flame_w / 3, fy + 2 * scale), (fx + flame_w / 3, fy + 2 * scale)])

        glow = pygame.Surface((int(120 * scale) + 2, int(120 * scale) + 2), pygame.SRCALPHA)
        gr = int(60 * scale)
        if gr > 1:
            for r in range(gr, 0, -2):
                a = int(50 * flick * (1 - r / gr))
                pygame.draw.circle(glow, (*EMBER, a), (gr, gr), r)
            screen.blit(glow, (fx - gr, fy - flame_h - gr * 0.3), special_flags=pygame.BLEND_ADD)


TORCHES = [Torch(side, i) for side in (-1, 1) for i in range(8)]


def draw_pillars(offset):
    for side in (-1, 1):
        for i in range(-2, 9):
            t = ((i + offset) % 9) / 9
            if t < 0.04:
                continue
            scale = lerp(0.05, 1, t)
            y = lerp(HORIZON_Y, HEIGHT + 30, t)
            x = WIDTH // 2 + side * lerp(90, 520, t)
            w, h = 46 * scale, 300 * scale
            pygame.draw.rect(screen, STONE_MID, (x - w / 2, y - h, w, h))
            pygame.draw.rect(screen, STONE_LIGHT, (x - w / 2, y - h, w, 16 * scale))
            for band in range(1, 4):
                by = y - h + h * band / 4
                pygame.draw.line(screen, STONE_DARK, (x - w / 2, by), (x + w / 2, by), max(1, int(3 * scale)))
            if t > 0.35:
                vine_h = h * 0.5
                pygame.draw.line(screen, VINE_DARK, (x - w / 2 - 2 * scale, y - h), (x - w / 2 - 5 * scale, y - h + vine_h), max(1, int(3 * scale)))
                for vy in range(3):
                    leaf_y = y - h + vine_h * (vy + 1) / 3
                    pygame.draw.circle(screen, VINE_GREEN, (int(x - w / 2 - 6 * scale), int(leaf_y)), max(1, int(4 * scale)))


def draw_path(offset, shake):
    sx = shake[0]
    pygame.draw.rect(screen, STONE_DARK, (0, 0, WIDTH, HORIZON_Y))
    draw_distant_ruins(offset)

    left_far, right_far = WIDTH // 2 - 46 + sx, WIDTH // 2 + 46 + sx
    left_near, right_near = -140 + sx, WIDTH + 140 + sx

    pygame.draw.polygon(screen, PATH_COLOR, [
        (left_far, HORIZON_Y), (right_far, HORIZON_Y),
        (right_near, HEIGHT), (left_near, HEIGHT)
    ])

    pygame.draw.polygon(screen, STONE_DARK, [(0, 0), (left_far, HORIZON_Y), (left_near, HEIGHT), (0, HEIGHT)])
    pygame.draw.polygon(screen, STONE_DARK, [(WIDTH, 0), (right_far, HORIZON_Y), (right_near, HEIGHT), (WIDTH, HEIGHT)])

    # side edge highlight
    pygame.draw.line(screen, PATH_EDGE, (left_far, HORIZON_Y), (left_near, HEIGHT), 4)
    pygame.draw.line(screen, PATH_EDGE, (right_far, HORIZON_Y), (right_near, HEIGHT), 4)

    # stone seams across the path
    for i in range(-2, 14):
        t = ((i + offset) % 14) / 14
        if t < 0.03:
            continue
        y = lerp(HORIZON_Y, HEIGHT, t)
        w = lerp(2, 20, t)
        pygame.draw.line(screen, PATH_SEAM, (WIDTH // 2 - w * 4 + sx * t, y), (WIDTH // 2 + w * 4 + sx * t, y), max(1, int(w / 5)))

    # lane guide studs
    for lane_x in LANES_X:
        for i in range(-2, 11):
            t = ((i + offset * 1.6) % 11) / 11
            if t < 0.03:
                continue
            y = lerp(HORIZON_Y, HEIGHT, t)
            scale = lerp(0.05, 1, t)
            lx = lerp(WIDTH // 2, lane_x, t) + sx * t
            pygame.draw.line(screen, GOLD_DARK, (lx - 16 * scale, y), (lx + 16 * scale, y), max(1, int(3 * scale)))

    for torch in TORCHES:
        torch.draw(offset, pygame.time.get_ticks() / 1000)


# ----------------------------------------------------------------------------
# PARTICLES
# ----------------------------------------------------------------------------
class Particle:
    def __init__(self, x, y, color, vy_range=(-4, -1), vx_range=(-2, 2), life=30, gravity=0.15, size=None):
        self.x, self.y = x, y
        self.vx = random.uniform(*vx_range)
        self.vy = random.uniform(*vy_range)
        self.life = life
        self.max_life = life
        self.color = color
        self.gravity = gravity
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        t = self.life / self.max_life
        size = self.size if self.size else max(1, int(4 * t) + 1)
        alpha = int(255 * t)
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (size, size), size)
        surf.blit(s, (self.x - size, self.y - size))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, count=10, **kwargs):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, **kwargs))

    def dust(self, x, y):
        self.particles.append(Particle(x, y, (180, 150, 120), vy_range=(-1.5, -0.3), vx_range=(-1, 1), life=22, gravity=0.05, size=3))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ----------------------------------------------------------------------------
# PLAYER
# ----------------------------------------------------------------------------
class Player:
    def __init__(self):
        self.lane = 1
        self.x = LANES_X[self.lane]
        self.target_x = self.x
        self.y = GROUND_Y
        self.vel_y = 0
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0
        self.run_cycle = 0
        self.lean = 0
        self.hit_flash = 0
        self.shield = 0
        self.magnet = 0
        self.invincible_flicker = 0

    def move_lane(self, direction):
        new_lane = clamp(self.lane + direction, 0, 2)
        if new_lane != self.lane:
            self.lane = new_lane
            self.target_x = LANES_X[self.lane]
            self.lean = direction * 10

    def jump(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_jumping = True
            self.vel_y = JUMP_POWER

    def slide(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = SLIDE_FRAMES

    def hit(self):
        if self.shield > 0:
            self.shield = 0
            self.hit_flash = 14
            return False
        return True

    def update(self, particles, speed_factor):
        self.x += (self.target_x - self.x) * LANE_SWITCH_SPEED
        self.lean *= 0.85
        self.run_cycle += 0.28 * (0.6 + speed_factor) if not self.is_sliding else 0.5
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.shield > 0:
            self.shield -= 1
        if self.magnet > 0:
            self.magnet -= 1

        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += GRAVITY
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
                self.vel_y = 0
                particles.burst(self.x, GROUND_Y + 30, (190, 165, 130), count=8, vy_range=(-2, -0.4), life=18)

        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False

        if not self.is_jumping and random.random() < 0.45:
            particles.dust(self.x + random.uniform(-14, 14), GROUND_Y + 28)

    def get_body_height(self):
        return 36 if self.is_sliding else 82

    def draw(self, surf):
        air_t = clamp((GROUND_Y - self.y) / 200, 0, 1)
        shadow_scale = 1.0 - air_t * 0.65
        shadow_alpha = int(140 * (1 - air_t * 0.7))
        shadow = pygame.Surface((80, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, shadow_alpha), (40 - 30 * shadow_scale, 13 - 7 * shadow_scale, 60 * shadow_scale, 14 * shadow_scale))
        surf.blit(shadow, (self.x - 40, GROUND_Y + 22))

        bob = math.sin(self.run_cycle) * (4 if not self.is_jumping else 0)
        height = self.get_body_height()
        cx = int(self.x + self.lean)
        cy = int(self.y - height / 2 - (0 if self.is_sliding else 0) + bob - (GROUND_Y - self.y))

        flicker_visible = True
        if self.shield > 0 and self.shield % 8 < 4:
            flicker_visible = True

        leg_swing = math.sin(self.run_cycle) * (16 if not self.is_sliding else 4)
        arm_swing = math.sin(self.run_cycle + math.pi) * 14

        body_color = SHIRT if self.hit_flash % 6 < 3 or self.hit_flash == 0 else RED

        if self.is_sliding:
            # low sliding pose
            pygame.draw.ellipse(surf, PANTS, (cx - 34, cy + 4, 68, 24))
            pygame.draw.ellipse(surf, body_color, (cx - 30, cy - 10, 60, 26))
            pygame.draw.circle(surf, SKIN, (cx + 30, cy - 4), 14)
            pygame.draw.circle(surf, HAIR, (cx + 30, cy - 12), 9)
            pygame.draw.line(surf, PANTS, (cx - 30, cy + 14), (cx - 46, cy + 22), 8)
            pygame.draw.line(surf, PANTS, (cx - 10, cy + 14), (cx - 26, cy + 24), 8)
        else:
            # legs
            pygame.draw.line(surf, PANTS, (cx - 9, cy + height // 2 - 6), (cx - 9 + leg_swing, cy + height // 2 + 30), 10)
            pygame.draw.line(surf, PANTS, (cx + 9, cy + height // 2 - 6), (cx + 9 - leg_swing, cy + height // 2 + 30), 10)
            # torso
            pygame.draw.ellipse(surf, SHIRT_DARK, (cx - 19, cy - height // 2 + 4, 38, height - 6))
            pygame.draw.ellipse(surf, body_color, (cx - 20, cy - height // 2, 40, height - 8))
            # arms
            pygame.draw.line(surf, SKIN, (cx - 16, cy - height // 4), (cx - 16 + arm_swing, cy + height // 4), 7)
            pygame.draw.line(surf, SKIN, (cx + 16, cy - height // 4), (cx + 16 - arm_swing, cy + height // 4), 7)
            # head
            pygame.draw.circle(surf, SKIN, (cx, cy - height // 2 - 10), 17)
            pygame.draw.circle(surf, HAIR, (cx, cy - height // 2 - 20), 13)
            pygame.draw.rect(surf, HAIR, (cx - 13, cy - height // 2 - 22, 26, 8), border_radius=4)

        if self.shield > 0 and self.shield % 8 < 6:
            ring = pygame.Surface((110, 130), pygame.SRCALPHA)
            pygame.draw.ellipse(ring, (90, 190, 255, 90), (5, 5, 100, 120), 4)
            surf.blit(ring, (cx - 55, cy - height // 2 - 30))


# ----------------------------------------------------------------------------
# OBSTACLES / COLLECTIBLES
# ----------------------------------------------------------------------------
class Entity:
    """A world object that travels from z=0.02 (far) to z=1.0+ (past camera)."""

    def __init__(self, lane, kind, z=0.02):
        self.lane = lane
        self.kind = kind
        self.z = z
        self.resolved = False
        self.bob = random.uniform(0, math.tau)

    def screen_pos(self):
        t = clamp(self.z, 0.0, 1.4)
        scale = lerp(0.05, 1.35, t)
        x = lerp(WIDTH // 2, LANES_X[self.lane], t)
        y = lerp(HORIZON_Y, HEIGHT + 40, t)
        return x, y, scale

    def update(self, speed):
        self.z += speed

    def draw(self, surf, t):
        x, y, scale = self.screen_pos()
        if scale < 0.03:
            return
        kind = self.kind

        if kind == "barrier":
            w, h = 78 * scale, 50 * scale
            pygame.draw.rect(surf, STONE_MID, (x - w / 2, y - h, w, h), border_radius=int(6 * scale))
            pygame.draw.rect(surf, STONE_DARK, (x - w / 2, y - h, w, h), max(1, int(3 * scale)), border_radius=int(6 * scale))
            for cx in (0.28, 0.72):
                pygame.draw.circle(surf, STONE_DARK, (int(x - w / 2 + w * cx), int(y - h / 2)), max(1, int(4 * scale)))

        elif kind == "gap":
            w, h = 100 * scale, 22 * scale
            pygame.draw.ellipse(surf, (4, 4, 8), (x - w / 2, y - h / 2, w, h))
            pygame.draw.ellipse(surf, (30, 18, 14), (x - w / 2, y - h / 2, w, h), max(1, int(2 * scale)))

        elif kind == "low":
            w, h = 100 * scale, 22 * scale
            wobble = math.sin(t * 4 + self.bob) * 3 * scale
            bar_y = y - 108 * scale + wobble
            pygame.draw.rect(surf, (150, 40, 40), (x - w / 2, bar_y, w, h), border_radius=int(4 * scale))
            for spike_x in range(3):
                sx = x - w / 2 + w * (spike_x + 0.5) / 3
                pygame.draw.polygon(surf, (200, 60, 50), [(sx, bar_y), (sx - 5 * scale, bar_y - 10 * scale), (sx + 5 * scale, bar_y - 10 * scale)])

        elif kind == "boulder":
            r = max(3, int(46 * scale))
            roll = t * 6
            pygame.draw.circle(surf, (70, 55, 48), (int(x), int(y - r * 0.6)), r)
            pygame.draw.circle(surf, (95, 75, 64), (int(x), int(y - r * 0.6)), r, max(1, int(3 * scale)))
            for a in range(4):
                ang = roll + a * math.pi / 2
                px = x + math.cos(ang) * r * 0.6
                py = (y - r * 0.6) + math.sin(ang) * r * 0.6
                pygame.draw.circle(surf, (50, 38, 34), (int(px), int(py)), max(1, int(5 * scale)))

        elif kind == "coin":
            bob = math.sin(t * 5 + self.bob) * 5 * scale
            r = max(2, int(15 * scale))
            cy = y - 55 * scale + bob
            squash = 0.55 + 0.45 * abs(math.sin(t * 5 + self.bob))
            pygame.draw.ellipse(surf, GOLD_DARK, (x - r, cy - r * squash, r * 2, r * 2 * squash))
            pygame.draw.ellipse(surf, GOLD, (x - r * 0.75, cy - r * squash * 0.75, r * 1.5, r * 2 * squash * 0.75))

        elif kind == "shield":
            bob = math.sin(t * 4 + self.bob) * 5 * scale
            r = max(3, int(18 * scale))
            cy = y - 55 * scale + bob
            pygame.draw.circle(surf, (90, 170, 255), (int(x), int(cy)), r)
            pygame.draw.circle(surf, (200, 230, 255), (int(x), int(cy)), r, max(1, int(3 * scale)))

        elif kind == "magnet":
            bob = math.sin(t * 4 + self.bob) * 5 * scale
            s = max(3, int(20 * scale))
            cy = y - 55 * scale + bob
            pygame.draw.arc(surf, (230, 60, 60), (x - s, cy - s, s * 2, s * 2), math.pi * 0.15, math.pi * 0.85, max(2, int(6 * scale)))
            pygame.draw.rect(surf, (200, 200, 210), (x - s, cy, max(1, int(6 * scale)), s * 0.7))
            pygame.draw.rect(surf, (200, 200, 210), (x + s - max(1, int(6 * scale)), cy, max(1, int(6 * scale)), s * 0.7))


# ----------------------------------------------------------------------------
# UI HELPERS
# ----------------------------------------------------------------------------
def draw_text_center(text, font, color, y, shadow=True, x=None):
    cx = x if x is not None else WIDTH // 2
    if shadow:
        s = font.render(text, True, (0, 0, 0))
        r = s.get_rect(center=(cx + 3, y + 3))
        screen.blit(s, r)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(cx, y))
    screen.blit(surf, rect)
    return rect


def draw_panel(rect, alpha=140, color=(10, 8, 16)):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]), border_radius=14)
    pygame.draw.rect(s, (*GOLD, 90), (0, 0, rect[2], rect[3]), 2, border_radius=14)
    screen.blit(s, (rect[0], rect[1]))


def draw_hud(score, coins, combo, speed_factor, player, high_score):
    draw_panel((16, 16, 230, 92))
    hud = font_med.render(f"{int(score):06d}", True, WHITE)
    screen.blit(hud, (32, 24))
    coin_icon_center = (46, 68)
    pygame.draw.circle(screen, GOLD_DARK, coin_icon_center, 11)
    pygame.draw.circle(screen, GOLD, coin_icon_center, 8)
    coin_txt = font_small.render(f"x {coins}", True, GOLD)
    screen.blit(coin_txt, (62, 58))

    if combo > 1:
        combo_txt = font_small.render(f"COMBO x{combo}", True, EMBER)
        screen.blit(combo_txt, (140, 58))

    hs_txt = font_tiny.render(f"BEST {int(high_score):06d}", True, (200, 190, 170))
    screen.blit(hs_txt, (32, 84))

    # speed meter
    bar_x, bar_y, bar_w, bar_h = WIDTH - 216, 24, 190, 14
    draw_panel((bar_x - 10, bar_y - 10, bar_w + 20, bar_h + 34), alpha=120)
    pygame.draw.rect(screen, (40, 30, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=7)
    pygame.draw.rect(screen, EMBER, (bar_x, bar_y, bar_w * speed_factor, bar_h), border_radius=7)
    screen.blit(font_tiny.render("SPEED", True, WHITE), (bar_x, bar_y + 18))

    # power-up icons
    icon_y = bar_y + 42
    if player.shield > 0:
        pygame.draw.circle(screen, (90, 170, 255), (bar_x + 14, icon_y), 10)
        screen.blit(font_tiny.render("SHIELD", True, (170, 210, 255)), (bar_x + 30, icon_y - 8))
    if player.magnet > 0:
        pygame.draw.circle(screen, (230, 60, 60), (bar_x + 14, icon_y + 22), 10)
        screen.blit(font_tiny.render("MAGNET", True, (255, 170, 170)), (bar_x + 30, icon_y + 14))


def draw_start_screen(t):
    pulse = 0.5 + 0.5 * math.sin(t * 2)
    draw_text_center("TEMPLE RUNNER", font_title, GOLD, HEIGHT // 2 - 90)
    draw_text_center("Press any key to run", font_med, (255, 255, 255), HEIGHT // 2 - 20)
    hint_color = (int(200 + 40 * pulse),) * 1
    draw_text_center("ARROWS / WASD to move    SPACE to jump    DOWN to slide", font_small, (220, 210, 200), HEIGHT // 2 + 30)
    draw_text_center("Grab coins, dodge ruins, chase your best score", font_tiny, (180, 165, 150), HEIGHT // 2 + 60)


def draw_game_over(score, coins, high_score, new_record):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((5, 3, 10, 190))
    screen.blit(overlay, (0, 0))
    draw_text_center("YOU FELL!", font_title, RED, HEIGHT // 2 - 110)
    if new_record:
        draw_text_center("NEW BEST SCORE!", font_small, GOLD, HEIGHT // 2 - 55)
    draw_text_center(f"Score {int(score)}   Coins {coins}", font_med, WHITE, HEIGHT // 2 - 5)
    draw_text_center(f"Best {int(high_score)}", font_small, (210, 195, 170), HEIGHT // 2 + 35)
    draw_text_center("Press R to run again", font_small, (230, 220, 205), HEIGHT // 2 + 80)


# ----------------------------------------------------------------------------
# MAIN GAME
# ----------------------------------------------------------------------------
class Game:
    def __init__(self):
        self.high_score = load_high_score()
        self.reset()

    def reset(self):
        self.player = Player()
        self.entities = []
        self.particles = ParticleSystem()
        self.score = 0.0
        self.coins = 0
        self.combo = 1
        self.combo_timer = 0
        self.speed = 0.0095
        self.max_speed = 0.030
        self.spawn_timer = 40
        self.game_over = False
        self.started = False
        self.bg_offset = 0.0
        self.shake_time = 0
        self.shake_mag = 0
        self.new_record = False
        self.recent_lanes = []

    @property
    def speed_factor(self):
        return clamp((self.speed - 0.0095) / (self.max_speed - 0.0095), 0, 1)

    def trigger_shake(self, magnitude, duration):
        self.shake_mag = magnitude
        self.shake_time = duration

    def get_shake_offset(self):
        if self.shake_time <= 0:
            return (0, 0)
        self.shake_time -= 1
        m = self.shake_mag * (self.shake_time / 20)
        return (random.uniform(-m, m), random.uniform(-m, m))

    def spawn_wave(self):
        lane = random.randint(0, 2)
        roll = random.random()
        if roll < 0.40:
            kind = random.choice(["barrier", "gap", "low", "boulder"])
            self.entities.append(Entity(lane, kind))
            # occasionally leave a safe lane clearly free; sometimes block two lanes
            if random.random() < 0.22:
                other = (lane + random.choice([1, 2])) % 3
                if other != lane:
                    self.entities.append(Entity(other, random.choice(["barrier", "low"])))
        elif roll < 0.85:
            # coin arc across one or more lanes
            arc_lane = random.randint(0, 2)
            for i in range(5):
                e = Entity(arc_lane, "coin", z=0.02 - i * 0.012)
                self.entities.append(e)
        else:
            kind = random.choice(["shield", "magnet"])
            self.entities.append(Entity(lane, kind))

    def update(self, keys_pressed_events):
        if not self.started or self.game_over:
            return

        self.bg_offset += self.speed * 34
        self.speed = min(self.max_speed, self.speed + 0.0000055)
        self.score += (1.2 + self.speed_factor * 2.2) * self.combo

        self.combo_timer -= 1
        if self.combo_timer <= 0:
            self.combo = 1

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = random.randint(30, 46) - int(self.speed_factor * 12)
            self.spawn_wave()

        self.player.update(self.particles, self.speed_factor)

        for e in self.entities[:]:
            e.update(self.speed)
            if e.z > 1.15:
                self.entities.remove(e)
                continue

            if e.kind in ("shield", "magnet", "coin") and self.player.magnet > 0:
                # magnet pulls matching-lane-ish pickups in gently by snapping lane
                if abs(e.z - 0.2) < 0.5:
                    e.lane = self.player.lane

            if 0.17 < e.z < 0.25 and e.lane == self.player.lane and not e.resolved:
                x, y, _ = e.screen_pos()
                if e.kind in ("barrier",) and not self.player.is_jumping:
                    self.resolve_hit(e)
                elif e.kind == "gap" and not self.player.is_jumping:
                    self.resolve_hit(e)
                elif e.kind == "boulder" and not self.player.is_jumping:
                    self.resolve_hit(e)
                elif e.kind == "low" and not self.player.is_sliding:
                    self.resolve_hit(e)
                elif e.kind == "coin":
                    e.resolved = True
                    self.coins += 1
                    self.combo = min(8, self.combo + 1)
                    self.combo_timer = 90
                    self.particles.burst(x, y - 50, GOLD, count=8, life=20, vy_range=(-3, -1))
                elif e.kind == "shield":
                    e.resolved = True
                    self.player.shield = 420
                    self.particles.burst(x, y - 50, (90, 170, 255), count=14, life=26)
                elif e.kind == "magnet":
                    e.resolved = True
                    self.player.magnet = 360
                    self.particles.burst(x, y - 50, (230, 60, 60), count=14, life=26)

        self.particles.update()

    def resolve_hit(self, e):
        e.resolved = True
        if self.player.hit():
            self.game_over = True
            self.trigger_shake(14, 20)
            self.particles.burst(self.player.x, self.player.y - 40, RED, count=22, life=32, vy_range=(-5, -1), vx_range=(-4, 4))
            if self.score > self.high_score:
                self.high_score = self.score
                self.new_record = True
                save_high_score(self.high_score)
        else:
            self.trigger_shake(6, 12)

    def draw(self):
        t = pygame.time.get_ticks() / 1000
        shake = self.get_shake_offset()

        draw_sky(t)
        draw_pillars(self.bg_offset)
        draw_path(self.bg_offset, shake)

        self.entities.sort(key=lambda e: e.z)
        for e in self.entities:
            e.draw(screen, t)

        self.particles.draw(screen)
        self.player.draw(screen)

        draw_hud(self.score, self.coins, self.combo, self.speed_factor, self.player, self.high_score)

        if not self.started:
            draw_start_screen(t)
        elif self.game_over:
            draw_game_over(self.score, self.coins, self.high_score, self.new_record)


def main():
    game = Game()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not game.started:
                    game.started = True
                    continue
                if game.game_over:
                    if event.key == pygame.K_r:
                        game = Game()
                    continue
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    game.player.move_lane(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.player.move_lane(1)
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                    game.player.jump()
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.player.slide()

        game.update(None)
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()