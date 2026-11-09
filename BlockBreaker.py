
import pygame
import random
import math
from array import array

pygame.init()

# Mengatur ukuran layar
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Neon Space")

clock = pygame.time.Clock()
FPS = 60

# Daftar warna
BLACK = (8, 10, 30)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 70)
GREEN = (60, 230, 150)
BLUE = (70, 160, 255)
PINK = (255, 100, 180)
PURPLE = (180, 110, 255)
CYAN = (50, 230, 255)

# Ketahanan setiap warna balok
BLOCK_HEALTH = {
    YELLOW: 200,
    GREEN: 100,
    BLUE: 300,
    PINK: 100,
    PURPLE: 200
}

font = pygame.font.Font("freesansbold.ttf", 18)
bigFont = pygame.font.Font("freesansbold.ttf", 35)

# Membuat bintang pada background
stars = []

for i in range(70):
    stars.append((
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ))


# MEMBUAT SUARA SECARA OTOMATIS

SOUND_ENABLED = True

try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1)
except pygame.error:
    SOUND_ENABLED = False


def tone_samples(frequency, duration, volume=0.3):
    sample_rate = 44100
    total = int(sample_rate * duration)
    samples = array("h")

    for i in range(total):
        t = i / sample_rate
        fade = min(1, i / 500, (total - i) / 1000)
        value = math.sin(2 * math.pi * frequency * t)
        samples.append(int(32767 * volume * fade * value))

    return samples


def make_sound(frequency, duration, volume=0.3):
    if not SOUND_ENABLED:
        return None

    samples = tone_samples(frequency, duration, volume)
    return pygame.mixer.Sound(buffer=samples.tobytes())


def play_sound(sound):
    if SOUND_ENABLED and sound is not None:
        sound.play()


# Soundboard
soundStart = make_sound(600, 0.25)
soundPaddle = make_sound(400, 0.10)
soundBlock = make_sound(700, 0.10)
soundBreak = make_sound(1000, 0.20)
soundLose = make_sound(180, 0.40)
soundWin = make_sound(900, 0.50)


# Membuat musik synth
def create_music():
    if not SOUND_ENABLED:
        return None

    notes = [220, 261, 329, 392, 329, 261, 293, 349]
    music = array("h")

    for note in notes:
        music.extend(tone_samples(note, 0.18, 0.10))
        music.extend(array("h", [0] * 3000))

    return pygame.mixer.Sound(buffer=music.tobytes())


backgroundMusic = create_music()


# Fungsi untuk menampilkan teks
def draw_text(text, fontType, color, y):
    image = fontType.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    screen.blit(image, rect)


# Menampilkan background
def draw_background():
    screen.fill(BLACK)

    for x, y, size in stars:
        pygame.draw.circle(screen, WHITE, (x, y), size)


# Halaman awal
def start_screen():
    while True:
        draw_background()

        draw_text("BLOCK BREAKER", bigFont, CYAN, 160)
        draw_text("NEON SPACE EDITION", font, PURPLE, 205)
        draw_text("Press SPACE to Start", font, WHITE, 300)
        draw_text("Use LEFT and RIGHT arrows", font, YELLOW, 340)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_sound(soundStart)

                    if SOUND_ENABLED:
                        backgroundMusic.play(-1)

                    return True

        pygame.display.update()
        clock.tick(FPS)


# Halaman menang dan kalah
def end_screen(title, color):
    if SOUND_ENABLED:
        backgroundMusic.stop()

    if title == "YOU WIN!":
        play_sound(soundWin)
    else:
        play_sound(soundLose)

    while True:
        draw_background()

        draw_text(title, bigFont, color, 190)
        draw_text("Press R to Play Again", font, WHITE, 270)
        draw_text("Press ESC to Exit", font, YELLOW, 310)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    play_sound(soundStart)

                    if SOUND_ENABLED:
                        backgroundMusic.play(-1)

                    return True

                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()
        clock.tick(FPS)


# CLASS STRIKER
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(
            posx, posy, width, height
        )

    def display(self):
        pygame.draw.rect(
            screen, self.color, self.strikerRect,
            border_radius=8
        )

    def update(self, xFac):
        self.posx += self.speed * xFac

        if self.posx <= 0:
            self.posx = 0

        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy,
            self.width, self.height
        )

    def getRect(self):
        return self.strikerRect


# CLASS BLOCK
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.color = color

        self.health = BLOCK_HEALTH[color]
        self.damage = 100

        self.blockRect = pygame.Rect(
            posx, posy, width, height
        )

    def display(self):
        if self.health > 0:
            pygame.draw.rect(
                screen, self.color,
                self.blockRect, border_radius=5
            )

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


# CLASS BALL
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color

        self.xFac = 1
        self.yFac = -1

    def display(self):
        pygame.draw.circle(
            screen, self.color,
            (int(self.posx), int(self.posy)),
            self.radius
        )

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        if self.posx - self.radius <= 0:
            self.xFac = 1

        elif self.posx + self.radius >= WIDTH:
            self.xFac = -1

        if self.posy - self.radius <= 0:
            self.yFac = 1

        if self.posy - self.radius >= HEIGHT:
            return True

        return False

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 70
        self.xFac = random.choice([-1, 1])
        self.yFac = -1

    def hit(self):
        self.yFac *= -1

    def getRect(self):
        return pygame.Rect(
            self.posx - self.radius,
            self.posy - self.radius,
            self.radius * 2,
            self.radius * 2
        )


# FUNGSI TAMBAHAN

def collisionChecker(rect, ball):
    return rect.colliderect(ball)


def populateBlocks():
    listOfBlocks = []

    blockWidth = 45
    blockHeight = 18
    horizontalGap = 10
    verticalGap = 12

    for i in range(10, WIDTH - blockWidth, blockWidth + horizontalGap):
        for j in range(45, 180, blockHeight + verticalGap):
            color = random.choice(list(BLOCK_HEALTH.keys()))

            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, color)
            )

    return listOfBlocks


# FUNGSI UTAMA
def main():
    running = True

    lives = 3
    score = 0

    striker = Striker(
        WIDTH // 2 - 50, HEIGHT - 40,
        100, 15, 8, CYAN
    )

    ball = Ball(
        WIDTH // 2, HEIGHT - 70,
        8, 5, WHITE
    )

    strikerXFac = 0
    listOfBlocks = populateBlocks()

    if not start_screen():
        return

    while running:
        draw_background()

        # Menampilkan skor dan nyawa
        scoreText = font.render(
            "Score: " + str(score), True, WHITE
        )

        livesText = font.render(
            "Lives: " + str(lives), True, YELLOW
        )

        screen.blit(scoreText, (15, HEIGHT - 30))
        screen.blit(livesText, (WIDTH - 110, HEIGHT - 30))

        # Membaca input keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1

                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    strikerXFac = 0

        # Tabrakan bola dengan papan
        if collisionChecker(striker.getRect(), ball.getRect()):
            if ball.yFac > 0:
                ball.yFac = -1
                play_sound(soundPaddle)

        # Tabrakan bola dengan balok
        for block in listOfBlocks:
            if collisionChecker(block.getRect(), ball.getRect()):
                ball.hit()
                block.hit()

                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5
                    play_sound(soundBreak)
                else:
                    play_sound(soundBlock)

                break

        # Memperbarui posisi objek
        striker.update(strikerXFac)

        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            play_sound(soundLose)

        # Memeriksa kemenangan
        if not listOfBlocks:
            if not end_screen("YOU WIN!", GREEN):
                running = False
                break

            lives = 3
            score = 0
            listOfBlocks = populateBlocks()
            ball.reset()

        # Memeriksa kekalahan
        if lives <= 0:
            if not end_screen("GAME OVER", PINK):
                running = False
                break

            lives = 3
            score = 0
            listOfBlocks = populateBlocks()
            ball.reset()

        # Menampilkan objek permainan
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)

    if SOUND_ENABLED:
        backgroundMusic.stop()


if __name__ == "__main__":
    main()
    pygame.quit()
