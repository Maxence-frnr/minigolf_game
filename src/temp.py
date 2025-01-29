import pygame as py

py.init()

screen = py.display.set_mode((400, 400))
clock = py.time.Clock()

img = py.image.load("assets\\sprites\\test_arrow.png").convert_alpha()

def rotate_img(img, angle):
    w, h = img.get_size()
    box = [py.math.Vector2(p) for p in [(0,0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (200 + min_box[0], 200 - max_box[1])
    rotated_image = py.transform.rotate(img, angle)
    return rotated_image, origin

running = True
angle = 0
while running:
    clock.tick(50)
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
    angle += 1
    if angle == 360:
        angle = 0
    screen.fill((255, 255, 255))
    temp_img, origin = rotate_img(img, angle)
    screen.blit(temp_img, origin)
    py.draw.circle(screen, "red", (200, 200), 3, 3)
    py.display.update()
py.quit()
#TODO: Cry