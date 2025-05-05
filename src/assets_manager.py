from pygame import image, mixer

_assets = {}
_sounds = {}

def load_image(name, path):
    _assets[name] = image.load(path).convert_alpha()
    
def get_image(name):
    return _assets.get(name)

def load_sound(name, path):
    _sounds[name] = mixer.Sound(path)
    
def get_sound(name):
    return _sounds.get(name)

def load_all_assets():
    load_all_sprites()
    load_all_sounds()
    
def load_all_sprites():
    load_image("ball", "assets\\sprites\\16x16 ball.png")
    load_image("hole", "assets\\sprites\\hole_24x24.png")
    load_image("home", "assets\\sprites\\home.png")
    load_image("back_arrow", "assets\\sprites\\back_arrow.png")
    load_image("white_arrow", "assets\\sprites\\white_arrow_edited.png")
    load_image("next_arrow", "assets\\sprites\\white_arrow.png")   
    load_image("undo_arrow", "assets\\sprites\\undo_arrow.png")    
    load_image("wind_arrows", "assets\\sprites\\wind_arrows_edited.png")
    load_image("tree_topground", "assets\\sprites\\plain_biome_sketch.png")
    load_image("plain_biome_background", "assets\\sprites\\plain_biome_background.png")
    load_image("plain_biome_flowers", "assets\\sprites\\plain_biome_flowers.png")
    for i in range(1, 10):
        load_image(f"blackhole{i}", f"assets\\sprites\\blackhole{i}.png")
    for i in range(1, 8):
        load_image(f"wind{i}", f"assets\\sprites\\wind_anim{i}.png")
    for i in range(1, 6):
        load_image(f"portal_exit{i}", f"assets\\sprites\\portal{i}.png")

def load_all_sounds():
    load_sound("swing", "assets\\sounds\\swing.mp3")
    load_sound("bounce", "assets\\sounds\\bounce.mp3")
    load_sound("hole", "assets\\sounds\\hole.mp3")
    load_sound("click", "assets\\sounds\\click.mp3")
    load_sound("portal", "assets\\sounds\\portal.mp3")
