import pygame
import time

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
dt = 0
info = pygame.display.Info()  # Get the screen dimensions
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
target_velocity = pygame.Vector2(0, 0)

# player parametrs
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_velocity = pygame.Vector2(0, 0)

# player_speed = 200
# acceleration = 1000
# deceleration = 1500
# rotation_speed = 10
player_speed_left = 0
player_speed_right = 0
transform_speed_left = 0
transform_speed_right = 0
is_running_right = False
is_running_left = False

start_run_left = 0
start_run_right = 0
runleft = False
runright = False
slowrun_left = 200
slowrun_right = 200
control_slowrun_left = 50
control_slowrun_right = 50

player_radius = 40
playervy = 0  # Vertical velocity
gravity = 1500  # Gravity force
frictionwall = False
jumpforce = -800  # Initial velocity when jumping
wallJumpforce = -400
jumpleft_wallforce_transform = 1500
jumpright_wallforce_transform = 1500
controljump = 0
fallbeatingforce = 1000
walljump_left = 0
walljump_right = 0
speedleft = 1000
speedright = 1000
speed = 0
jump = 0
touchedTheWallRight = False
touchedTheWallLeft = False
touchedTheWall = False
fallforce = 1000
friction = 1

current_time = None
# finishtimeA = 0
start_timeA = 0  # Tracks time of the first click
reset_intervalA = 0.3  # Maximum time interval for double click (in seconds)
doublepressA = 0  # 0: no click, 1: first click detected
start_timeD = 0
reset_intervalD = 0.3
doublepressD = 0

is_dashing_left = False
is_dashing_right = False
dash_start_time = None
dash_duration = 0.2
dash_speed = 1000
dash_change = 0

slide_speed = 50
walljumpLeft = False
walljumpRight = False
walljump_start_time_left = None
walljump_start_time_right = None
walljump_duration = 0.5
horizontalcontrol_left = 0
horizontalcontrol_right = 0
transform_left = 0
transform_right = 0
transformed = 0

# Variables to track the key presses

running = True

ground_level = screen.get_height() - player_radius  # Ground position (bottom of the screen)


def smoothx_start(transform_speed, speed, changing):
    if not transform_speed >= speed:
        transform_speed += changing
    else:
        transform_speed = speed
    return transform_speed


def smoothx_finish(transform_speed, changing):
    if not transform_speed <= 0:
        transform_speed -= changing
    else:
        transform_speed = 0
    return transform_speed


while running:
    current_time = time.time()

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # Correct event handling
            if event.key == pygame.K_a:  # Detect 'A' key press
                if doublepressA == 0:  # First press
                    start_timeA = current_time
                    doublepressA = 1
                elif doublepressA == 1 and current_time - start_timeA <= reset_intervalA:  # Second press within interval
                    dash_start_time = time.time()
                    is_dashing_left = True
                    dash_speed = 3000
                    dash_change = 100
                    doublepressA = 0  # Reset state after detection
            elif event.key == pygame.K_d:
                doublepressA = 0

            if event.key == pygame.K_d:  # Detect 'D' key press
                if doublepressD == 0:  # First press
                    start_timeD = current_time
                    doublepressD = 1
                elif doublepressD == 1 and current_time - start_timeD <= reset_intervalD:  # Second press within interval
                    dash_start_time = time.time()
                    is_dashing_right = True
                    dash_speed = 3000
                    dash_change = 100
                    doublepressD = 0  # Reset state after detection
            elif event.key == pygame.K_a:
                doublepressD = 0

    if doublepressA == 1 and current_time - start_timeA > reset_intervalA:
        doublepressA = 0  # Reset after time interval

    if doublepressD == 1 and current_time - start_timeD > reset_intervalD:
        doublepressD = 0  # Reset after time interval

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "dark red", player_pos, player_radius)

    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_a]:
        is_running_right = True
        player_pos.x -= (speedleft + speed) * dt
        if speedleft < 800:
            speedleft += 10
    else:
        is_running_right = False
        speedleft = 600
    if keys[pygame.K_d]:
        is_running_left = True
        player_pos.x += (speedright + speed) * dt
        if speedright < 800:
            speedright += 10
    else:
        is_running_left = False
        speedright = 600

    if touchedTheWall == False:
        if (keys[pygame.K_a] or keys[pygame.K_d]):
            if speed < 600:
                speed += 1
        else:
            speed = 0
    else:
        speed = 0

    # if is_running_right:
    #     # if not transform_speed_right >= player_speed_right:
    #     #     transform_speed_right += 300
    #     # else:
    #     #     transform_speed_right = player_speed_right
    #     transform_speed_right = smoothx_start(transform_speed_right, player_speed_right, slowrun_right)
    # else:
    #     # if not transform_speed_right <= 0:
    #     #     transform_speed_right -= 300
    #     # else:
    #     #     transform_speed_right = 0
    #     transform_speed_right = smoothx_finish(transform_speed_right, slowrun_right)

    # if is_running_left:
    #     # if not transform_speed_left >= player_speed_left:
    #     #     transform_speed_left += 300
    #     # else:
    #     #     transform_speed_left = player_speed_left
    #     transform_speed_left = smoothx_start(transform_speed_left, player_speed_left, slowrun_left)

    # else:
    #     # if not transform_speed_left <= 0:
    #     #     transform_speed_left -= 300
    #     # else:
    #     #     transform_speed_left = 0
    #     transform_speed_left = smoothx_finish(transform_speed_left, slowrun_left)
    # player_pos.x += (transform_speed_left - transform_speed_right) * dt

    # if keys[pygame.K_a]:
    #     if not start_run_left > 2:
    #         start_run_left += 1
    #     player_pos.x -= (speedleft + speed) * dt
    #     if speedleft < 700:
    #         speedleft+=7
    # else:
    #     start_run_left = 0
    #     speedleft = 400
    # if keys[pygame.K_d]:
    #     if not start_run_right > 2:
    #         start_run_right += 1
    #     player_pos.x = (speedright + speed) * dt
    #     if speedright < 700:
    #         speedright+=7
    # else:
    #     start_run_right = 0
    #     speedright = 400

    # if touchedTheWall == False:
    #     if(keys[pygame.K_a] or keys[pygame.K_d]):
    #         if speed < 700:
    #             speed+=1
    #     else:
    #         speed = 0
    # else:
    #     speed = 0

    # if start_run_left == 1:
    #     runleft = True
    # if start_run_right == 1:
    #     runright = True

    # if runleft:
    #     slowrun_left -= 50
    #     player_pos.x += slowrun_left * dt
    #     if slowrun_left <= 0:
    #         slowrun_left = 300
    #         control_slowrun_left = 50
    #         runleft = False
    # if runright:
    #     slowrun_right -= control_slowrun_right
    #     player_pos.x -= slowrun_right * dt
    #     if slowrun_right <= 0:
    #         slowrun_right = 300
    #         control_slowrun_right = 50
    #         runright = False

    # if keys[pygame.K_a]:
    #     if player_velocity.x > 0:  # Если двигались вправо, а теперь влево
    #         player_velocity.x -= deceleration * dt
    #     target_velocity = -(speedleft + speed)
    #     player_velocity.x = max(player_velocity.x - acceleration * dt, target_velocity)
    # elif keys[pygame.K_d]:
    #     if player_velocity.x < 0:  # Если двигались влево, а теперь вправо
    #         player_velocity.x += deceleration * dt
    #     target_velocity = (speedright + speed)
    #     player_velocity.x = min(player_velocity.x + acceleration * dt, target_velocity)
    # else:
    #     # Замедление до полной остановки
    #     if player_velocity.x > 0:
    #         player_velocity.x = max(player_velocity.x - deceleration * dt, 0)
    #     elif player_velocity.x < 0:
    #         player_velocity.x = min(player_velocity.x + deceleration * dt, 0)
    # player_pos.x += player_velocity.x * dt

    # if keys[pygame.K_a]:
    #     target_velocity.x = -(speedleft + speed)
    #     if speedleft < 700:
    #         speedleft+=7
    # else:
    #     speedleft = 400
    # if keys[pygame.K_d]:
    #     target_velocity.x = (speedright + speed)
    #     if speedright < 700:
    #         speedright+=7
    # else:
    #     speedright = 400

    # if touchedTheWall == False:
    #     if(keys[pygame.K_a] or keys[pygame.K_d]):
    #         if speed < 700:
    #             speed+=1
    #     else:
    #         speed = 0
    # else:
    #     speed = 0

    # if not transform_left >= horizontalcontrol_left:
    #     transform_left += 5%horizontalcontrol_left
    # else:
    #     transform_left = horizontalcontrol_left

    # if not transform_right >= horizontalcontrol_right:
    #     transform_right += 5%horizontalcontrol_right
    # else:
    #     transform_right = horizontalcontrol_right

    # transformed = (transform_left - transform_right)

    # player_pos.x += transformed *dt

    if is_dashing_left and not is_dashing_right:
        dash_speed = smoothx_finish(dash_speed, dash_change)
        # Perform dash for a set time
        if current_time - dash_start_time < dash_duration:
            player_pos.x -= dash_speed * dt
        else:
            is_dashing_left = False

    if is_dashing_right and not is_dashing_left:
        dash_speed = smoothx_finish(dash_speed, dash_change)
        if current_time - dash_start_time < dash_duration:
            player_pos.x += dash_speed * dt
        else:
            is_dashing_right = False

    # Jumping mechanics
    # if not frictionwall:
    # if controljump < 10:
    #     if keys[pygame.K_SPACE]:
    #         if jump == 2:
    #             playervy = jumpforce
    #             controljump += 1
    #         elif jump == 1:
    #             playervy = jumpforce
    #             jump = 0
    # elif controljump > 1 and not controljump >= 10:
    #     jump = 1
    #     if not keys[pygame.K_SPACE]:
    #         controljump = 0

    if touchedTheWall:
        if playervy:
            if touchedTheWallRight and keys[pygame.K_a]:
                playervy = min(playervy + gravity, slide_speed)
                if keys[pygame.K_w]:
                    player_pos.y -= 300 * dt
                if keys[pygame.K_SPACE]:
                    walljumpLeft = True
                    playervy = wallJumpforce
                    walljump_start_time_left = time.time()
            if touchedTheWallLeft and keys[pygame.K_d]:
                playervy = min(playervy + gravity, slide_speed)
                if keys[pygame.K_w]:
                    player_pos.y -= 300 * dt
                if keys[pygame.K_SPACE]:
                    walljumpRight = True
                    playervy = wallJumpforce
                    walljump_start_time_right = time.time()

    if walljumpLeft:
        touchedTheWallLeft = True
        touchedTheWallRight = True
        if current_time - walljump_start_time_left < walljump_duration:
            speedleft = 100
            speedright = 100
            jumpleft_wallforce_transform = smoothx_finish(jumpleft_wallforce_transform, 30)
            player_pos.x += jumpleft_wallforce_transform * dt
        else:
            jumpleft_wallforce_transform = 1500
            speedleft = 1000
            speedright = 1000
            walljumpLeft = False
    if walljumpRight:
        touchedTheWallRight = True
        touchedTheWallLeft = True
        if current_time - walljump_start_time_right < walljump_duration:
            speedleft = 100
            speedright = 100
            jumpright_wallforce_transform = smoothx_finish(jumpright_wallforce_transform, 30)
            player_pos.x -= jumpright_wallforce_transform * dt
        else:
            jumpright_wallforce_transform = 1500
            speedleft = 1000
            speedright = 1000
            walljumpRight = False

    if not touchedTheWallLeft and not touchedTheWallRight:
        if not touchedTheWall:
            if keys[pygame.K_SPACE]:
                if jump == 3 or jump == 2:
                    jump = 2
                    controljump += 1
                    if controljump < 20:
                        playervy = jumpforce
                elif jump == 1:
                    playervy = jumpforce
                    jump = 0
            elif jump == 2:
                jump = 1

    if keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL]:
        playervy = fallforce

    if keys[pygame.K_LSHIFT] or keys[pygame.K_RETURN]:
        playervy = min(playervy + gravity, slide_speed)

    # else:  # Wall sliding
    #     playervy += gravity * dt  # Continue applying gravity while sliding down
    #     # if keys[pygame.K_SPACE]:  # Jump off the wall
    #     #     playervy = walljumpforce  # Give an upward force
    #     #     frictionwall = False  # Reset wall friction
    #     # else:
    #     #     playervy = 0  # Reset vertical velocity to allow sliding down

    # Apply gravity to the player's vertical velocity

    playervy += gravity * dt
    player_pos.y += playervy * dt

    # Check if the player is on the ground
    if player_pos.y >= ground_level:
        player_pos.y = ground_level  # Snap the player to the ground
        playervy = 0  # Stop any downward movement,
        jump = 3  # Allow jumping again
        controljump = 0

    # Boundary check to prevent the player from going off-screen
    if player_pos.x - player_radius < 0:  # Left boundary
        player_pos.x = player_radius
        if player_pos.y <= 650:
            touchedTheWall = True
    elif player_pos.x + player_radius > screen.get_width():  # Right boundary
        player_pos.x = screen.get_width() - player_radius
        if player_pos.y <= 650:
            touchedTheWall = True
    else:
        touchedTheWall = False
    if player_pos.y > 650:
        touchedTheWall = False

    if player_pos.x - player_radius < 20:
        touchedTheWallRight = True
        jump = 1
    else:
        touchedTheWallRight = False
    if player_pos.x + player_radius > screen.get_width() - 20:
        touchedTheWallLeft = True
        jump = 1
    else:
        touchedTheWallLeft = False

    if player_pos.y - player_radius < 0:
        player_pos.y = player_radius

    # Check for wall sliding
    # if player_pos.y <= 480:  # Check for height threshold for wall sliding
    if player_pos.x - player_radius < 10:
        if keys[pygame.K_a]:
            frictionwall = True
    elif player_pos.x + player_radius > screen.get_width() - 10:
        if keys[pygame.K_d]:
            frictionwall = True
    else:
        frictionwall = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(120) / 1000

pygame.quit()
