# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

clock = pygame.time.Clock()

dt = 0
init_y = 50
init_v = 0
# This doesn't have much meaning without some kind of scale,
# But at least this will remind me of what the term is for
g = 9.8/2
t = 0
scale = 100

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))


    t = t + dt
    y = t**2 * g + t * init_v + init_y

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 25, 25), (250, y), 10)

    # Flip the display
    pygame.display.flip()

    dt = clock.tick(60) / scale
    print(t)


# Done! Time to quit.
pygame.quit()
