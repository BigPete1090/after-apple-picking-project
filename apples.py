import pygame
import random
from PIL import Image, ImageFilter, ImageEnhance
import imageio
import math
import os

pygame.init()
# loading images
bg_img = pygame.image.load("apple_orchard.jpg")
bg_width, bg_height = bg_img.get_size()
apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (120, 120))

# Setting up the screen with pygame
screen = pygame.display.set_mode((bg_width, bg_height))
clock = pygame.time.Clock()
# Making the falling apples
num_apples = 20
apples = [{"x": random.randint(50, bg_width - 50), "y": random.randint(-50, 0), "speed": random.uniform(3, 5)} for _ in range(num_apples)]

frames = []
# 10 fps for 7 seconds
max_frames = 70  

# applies the horizontal stretch
def apply_horizontal_stretch(img, frame, max_frames):
    img = img.convert("RGB")
    pixels = img.load()

    delay_start = 20
    stretch_factor = max(0, frame - delay_start) / (max_frames - delay_start) if frame > delay_start else 0
    wave_amplitude = stretch_factor * 30

    for y in range(bg_height):
        offset = int(wave_amplitude * math.sin(y / 50.0 + frame / 40.0))
        for x in range(bg_width):
            new_y = y + offset
            if 0 <= new_y < bg_height:
                pixels[x, y] = pixels[x, new_y]
    return img
# adds the changes and updates to each frame and saves it
for frame in range(max_frames):
    # Load and distort background 
    img = Image.open("apple_orchard.jpg")
    img = apply_horizontal_stretch(img, frame, max_frames)
    t = min(frame / max_frames, 1)
    blur_factor = t ** 2.2  
    blur_radius = blur_factor * 8
    # adds a slight blur, and stretches
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # increases brightness
    brightness = 1 + blur_factor * 0.3
    img = ImageEnhance.Brightness(img).enhance(brightness)
    # increases color extremeness
    if blur_factor > 0.5:
        img = ImageEnhance.Color(img).enhance(1 + (blur_factor - 0.5) * 0.3)
    #saves each frame
    img.save("temp_frame.jpg")
    bg_img = pygame.image.load("temp_frame.jpg")

    # has each apple fall some
    apple_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    for apple in apples:
        apple["y"] += apple["speed"]
        if apple["y"] > bg_height:
            apple["y"] = random.randint(-50, 0)
            apple["x"] = random.randint(50, bg_width - 50)
        apple_surface.blit(apple_img, (apple["x"], apple["y"]))
    # Save apple surface to image and apply minor blur
    pygame.image.save(apple_surface, "temp_apples.png")
    apple_pil = Image.open("temp_apples.png").filter(ImageFilter.GaussianBlur(radius=blur_radius))
    apple_pil.save("temp_apples_blurred.png")
    blurred_apples = pygame.image.load("temp_apples_blurred.png")
    # fully load screen
    screen.blit(bg_img, (0, 0))
    screen.blit(blurred_apples, (0, 0))
    pygame.display.flip()
    clock.tick(10)
    # Save frame for GIF to be turned into a gif later
    frame_path = f"frame_{frame}.jpg"
    pygame.image.save(screen, frame_path)
    frames.append(imageio.imread(frame_path))

# Save animation as GIF using each frame
try:
    imageio.mimsave("dreamy_apple_fall.gif", frames, duration=0.1)
    print("GIF successfully saved.")
except Exception as e:
    print("GIF failed to save:", e)

# this removes temporary files which it kept creating temporary images
# if it doesn't make temporary images nothing happens
for frame in range(max_frames):
    try:
        os.remove(f"frame_{frame}.jpg")
    except:
        pass
#removes extra files
os.remove("temp_frame.jpg")
os.remove("temp_apples.png")
os.remove("temp_apples_blurred.png")

pygame.quit()
