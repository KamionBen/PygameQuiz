import os
import sys

if getattr(sys, 'frozen', False):
    HOME = sys._MEIPASS
else:
    HOME = os.path.dirname(os.path.abspath(__file__))

""" FONTS """
DIMBO_FILE = os.path.join(HOME, 'fonts/Dimbo Regular.ttf')
HS_FILE = os.path.join(HOME, 'fonts/horseshoes.ttf')
HSLMD_FILE = os.path.join(HOME, 'fonts/horseshoeslemonade.ttf')

""" IMAGES """
MAIN_IMG = os.path.join(HOME, 'images/main.jpg')
ICON_FILE = os.path.join(HOME, 'images/icon256.png')

nuggets_imgfile = os.path.join(HOME, 'images/nuggets_img.png')
seloupoivre_imgfile = os.path.join(HOME, 'images/seloupoivre_img.png')
menus_imgfile = os.path.join(HOME, 'images/menus_img.png')
addition_imgfile = os.path.join(HOME, 'images/addition_img.png')
burger_imgfile = os.path.join(HOME, 'images/burger_img.png')

""" SOUNDS """
generique_soundfile = os.path.join(HOME, 'jingles/generique_son.wav')
nuggets_soundfile = os.path.join(HOME, 'jingles/nuggets_son.wav')
seloupoivre_soundfile = os.path.join(HOME, 'jingles/seloupoivre_son.wav')
menus_soundfile = os.path.join(HOME, 'jingles/menus_son.wav')
addition_soundfile = os.path.join(HOME, 'jingles/addition_son.wav')
burger_soundfile = os.path.join(HOME, 'jingles/burger_son.wav')
