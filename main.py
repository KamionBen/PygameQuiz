import pygame
import time
from pygame.locals import *
from constants import *
from files import *


""" Pardonnez-moi le bordel ^^ """
version = '1.0'

jingles_txt = {'nuggets': "On passe aux NUGGETS ! ",
               'seloupoivre': "C'est le moment du SEL OU POIVRE !",
               'menus': "Tout de suite, les MENUS",
               'addition': "Et maintenant, L'ADDITION",
               'burger': "C'est l'heure du BURGER DE LA MORT !"}


class Log:
    """ Permet de faire un compte rendu système (Chargement des images et des polices)
     Un compte rendu du jeu (Qui a gagné combien de points et à quelle heure, pour pouvoir gérer les conflits)
     Il faudrait qu'il capte les erreurs de système et enregistre un log de plantage, le cas échéant """
    id = 0

    def __init__(self):
        self._ids = []
        self._time = []
        self._type = []
        self._message = []

    def append(self, n_time, n_type, message):
        if n_type == 'score':
            equipe = message[0]
            score = message[1]

            previous_id = Log.id - 1
            previous_team = self._message[previous_id][0]
            previous_time = self._time[previous_id]

            if previous_team == equipe and previous_time.tm_min == n_time.tm_min:
                self._message[previous_id][1] += score
            else:
                self._ids.append(Log.id)
                self._time.append(n_time)
                self._type.append(n_type)
                self._message.append(message)

                Log.id += 1

        else:
            self._ids.append(Log.id)
            self._time.append(n_time)
            self._type.append(n_type)
            self._message.append(message)

            Log.id += 1

    def __iter__(self):
        return iter(self._ids)

    def print(self, n_id=None):
        if n_id is None:
            for m_id in self._ids:
                self.print(m_id)
        else:
            if self._type[n_id] == 'score':
                s_type = "[SCORE]"
                s_time = "%s:%s" % (self._time[n_id].tm_hour, self._time[n_id].tm_min)
                if self._message[n_id][1] >= 0:
                    bonus = "gagne"
                else:
                    bonus = "perd"
                s_score = abs(self._message[n_id][1])

                s_message = "L'équipe %s %s %s points" % (self._message[n_id][0], bonus, s_score)
                print("%s[%s] : %s" % (s_type, s_time, s_message))

            elif self._type[n_id] == 'jingle':
                j_type = self._type[n_id].upper()
                j_time = "%s:%s" % (self._time[n_id].tm_hour, self._time[n_id].tm_min)
                j_message = jingles_txt[self._message[n_id]]
                print("[%s][%s] : %s" % (j_type, j_time, j_message))

            else:
                n_type = self._type[n_id].upper()
                n_time = "%s:%s" % (self._time[n_id].tm_hour, self._time[n_id].tm_min)
                n_message = self._message[n_id]

                print("[%s][%s] : %s" % (n_type, n_time, n_message))

    def get_colored(self, n_id):
        if self._type[n_id] == 'jeu':
            pass


pygame.init()

log = Log()


def load_image(file, alpha=False):
    try:
        img = pygame.image.load(file)
        if alpha:
            img.convert_alpha()
        else:
            img.convert()

        log.append(time.localtime(), 'system', "[REUSSITE] Fichier chargé : %s" % file)

        return img
    except Exception as e:
        print(e)
        log.append(time.localtime(), 'system', '[ECHEC] Impossible de charger %s\n%s' % (file, e))
        return False


def load_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        log.append(time.localtime(), 'system', "[REUSSITE] Fichier chargé : %s" % file)
        return sound
    except Exception as e:
        print(e)
        log.append(time.localtime(), 'system', '[ECHEC] Impossible de charger %s\n%s' % (file, e))
        return False


class PQFont:
    def __init__(self, font_file):
        self.f_file = font_file
        self._f_dict = {}

    def render(self, text, size, n_color):
        if size not in self._f_dict.keys():
            self._f_dict[size] = pygame.font.Font(self.f_file, size)

        return self._f_dict[size].render(text, 1, n_color)


""" Initialisation des polices """
dimbo = PQFont(DIMBO_FILE)
horseshoelemonade = PQFont(HSLMD_FILE)

""" Init fin """

""" Initialisation des sons """

generique_sound = load_sound(generique_soundfile)
nuggets_sound = load_sound(nuggets_soundfile)
seloupoivre_sound = load_sound(seloupoivre_soundfile)
menus_sound = load_sound(menus_soundfile)
addition_sound = load_sound(addition_soundfile)
burger_sound = load_sound(burger_soundfile)


class Settings:
    def __init__(self):
        """" Paramètres (Prévoir de les enregistrer dans un fichier) """
        if pygame.display.Info().current_w < 1920:
            self.resolution = (1280, 720)
        else:
            self.resolution = (1920, 1080)

        self.sound = True
        self.nb_team = 2

        self.joystick = "Namtai Buzz"
        self.but_ketchup = 0
        self.but_mayo = 5
        self.but_wasabi = 10
        self.but_blanche = 15

    def set_nb_team(self, new_nb_team):
        """ Change the number of teams """
        self.nb_team = new_nb_team


class MainMenu:
    def __init__(self, stg=Settings()):
        """ Classe pour afficher le menu principal """
        self.screen = None

        self.played = False

        self.main_img = load_image(MAIN_IMG)

        self.stg = stg  # Settings
        self.buttons = {}
        self.update()

    def update(self):
        """ Mets à jour self.screen, pas besoin de le faire tout le temps """
        self.screen = pygame.Surface(self.stg.resolution)
        self.screen.fill(BLACK)

        if self.main_img is not False:
            n_main_img = pygame.transform.scale(self.main_img, self.stg.resolution)
            self.screen.blit(n_main_img, (0, 0))

        v_size = 18
        txt_size = 50
        width = 300
        height = 50
        start_y = 500
        y_offset = 60

        if self.stg.resolution[0] == 1920:
            v_size = 28
            txt_size = 76
            width = 450
            height = 75
            start_y = 650
            y_offset = 90

        version_txt = dimbo.render("Version %s" % version, v_size, WHITE)
        self.screen.blit(version_txt, (self.stg.resolution[0] / 2 - version_txt.get_rect().width / 2, 5))

        commencer_txt = dimbo.render("Commencer", txt_size, WHITE)
        param_txt = dimbo.render("Paramètres", txt_size, WHITE)
        quitter_txt = dimbo.render("Quitter", txt_size, WHITE)

        center = self.stg.resolution[0] / 2

        commencer_rect = pygame.rect.Rect(center - width / 2, start_y + 5, width, height)
        param_rect = pygame.rect.Rect(center - width / 2, start_y + y_offset + 5, width, height)
        quitter_rect = pygame.rect.Rect(center - width / 2, start_y + y_offset * 2 + 5, width, height)

        self.buttons['commencer'] = commencer_rect
        self.buttons['param'] = param_rect
        self.buttons['quitter'] = quitter_rect

        self.screen.blit(commencer_txt, (center - commencer_txt.get_rect().width / 2, start_y))
        self.screen.blit(param_txt, (center - param_txt.get_rect().width / 2, start_y + y_offset))
        self.screen.blit(quitter_txt, (center - quitter_txt.get_rect().width / 2, start_y + y_offset * 2))

    def display(self, window):
        """ Affiche self.screen et joue le générique de début si le son est activé dans les paramètres """
        window.blit(self.screen, (0, 0))
        if self.played is False and self.stg.sound and generique_sound is not False:
            self.played = True
            generique_sound.play()


class SettingsMenu:
    def __init__(self, settings):
        """ Class pour afficher et modifier les paramètres """
        self.stg = settings
        self.selected_res = self.stg.resolution[1]
        self.selected_sound = self.stg.sound

        self.screen = pygame.Surface(self.stg.resolution)
        self.buttons = dict

        self.update()

    def change_resolution(self, new_resolution):
        self.selected_res = int(new_resolution)
        self.update()

    def toggle_sound(self, new_sound):
        if new_sound == "sound_on":
            self.selected_sound = True
        elif new_sound == "sound_off":
            self.selected_sound = False
        self.update()

    def apply_changes(self):
        if self.selected_res == 720:
            self.stg.resolution = (1280, 720)
        elif self.selected_res == 1080:
            self.stg.resolution = (1920, 1080)

        self.stg.sound = self.selected_sound
        if self.selected_sound is False:
            pygame.mixer.stop()

        self.update()

    def update(self):
        """ Mets à jour l'écran (désolé c'est le bordel ici) """
        self.screen.fill(BLACK)

        self.buttons = {}

        medium_color = WHITE
        high_color = WHITE

        if self.selected_res == 720:
            medium_color = MAYO
            high_color = nGREY[40]
        elif self.selected_res == 1080:
            medium_color = nGREY[40]
            high_color = KETCHUP

        txt_size = 40
        y_start = 40
        y_offset = 50
        bottom = 70
        x_center = self.stg.resolution[0] / 2

        if self.stg.resolution[0] == 1920:
            txt_size = 60
            y_start = 60
            y_offset = 75
            bottom = 180

        txt_res = dimbo.render("Resolution", txt_size, WHITE)
        medium_res = dimbo.render("1280 x 720", txt_size, medium_color)
        high_res = dimbo.render("1920 x 1080", txt_size, high_color)

        self.screen.blit(txt_res, (x_center - txt_res.get_rect().width / 2, y_start))

        medium_rect = (x_center - medium_res.get_rect().width / 2,
                       y_start + y_offset,
                       medium_res.get_rect().width,
                       medium_res.get_rect().height)
        high_rect = (x_center - high_res.get_rect().width / 2,
                     y_start + y_offset * 2,
                     high_res.get_rect().width,
                     high_res.get_rect().height)

        self.screen.blit(medium_res, (medium_rect[0], medium_rect[1]))
        self.screen.blit(high_res, (high_rect[0], high_rect[1]))

        self.buttons["720"] = pygame.rect.Rect(medium_rect)
        self.buttons["1080"] = pygame.rect.Rect(high_rect)

        son_txt = dimbo.render("Son", txt_size, WHITE)
        self.screen.blit(son_txt, (x_center - son_txt.get_rect().width / 2, y_start + y_offset * 4))
        if self.selected_sound:
            on_color = MAYO
            off_color = nGREY[40]
        else:
            on_color = nGREY[40]
            off_color = KETCHUP

        on_txt = dimbo.render("ON", txt_size, on_color)
        off_txt = dimbo.render("OFF", txt_size, off_color)

        on_rect = (x_center - on_txt.get_rect().width - 5,
                   y_start + y_offset * 5,
                   on_txt.get_rect().width,
                   on_txt.get_rect().height)
        off_rect = (x_center + 5,
                    y_start + y_offset * 5,
                    off_txt.get_rect().width,
                    off_txt.get_rect().height)

        self.buttons["sound_on"] = pygame.rect.Rect(on_rect)
        self.buttons["sound_off"] = pygame.rect.Rect(off_rect)

        self.screen.blit(on_txt, (on_rect[0], on_rect[1]))
        self.screen.blit(off_txt, (off_rect[0], off_rect[1]))

        appliquer_txt = dimbo.render("Appliquer", txt_size, MAYO)
        annuler_txt = dimbo.render("Annuler", txt_size, KETCHUP)

        app_rect = (x_center - appliquer_txt.get_rect().width - 20,
                    self.stg.resolution[1] - bottom,
                    appliquer_txt.get_rect().width,
                    appliquer_txt.get_rect().height)
        ann_rect = (x_center + 20,
                    self.stg.resolution[1] - bottom,
                    annuler_txt.get_rect().width,
                    annuler_txt.get_rect().height)

        self.buttons["appliquer"] = pygame.rect.Rect(app_rect)
        self.buttons["annuler"] = pygame.rect.Rect(ann_rect)

        self.screen.blit(appliquer_txt, (app_rect[0], app_rect[1]))
        self.screen.blit(annuler_txt, (ann_rect[0], ann_rect[1]))

    def display(self, window):
        window.blit(self.screen, (0, 0))


class Score:
    def __init__(self, settings):
        """ Affiche le score
        Ne permet pas encore plus que deux équipes """
        self.stg = settings

        self.score_ketchup = 0
        self.score_mayo = 0

        self.screen = pygame.Surface(self.stg.resolution)
        self.timer = None

        self.jingles_screen = None
        self.jingles_flag = False
        self.jingle = False
        self.jingle_played = False
        self.current_jingle = None

        self.nuggets_flag = False
        self.seloupoivre_flag = False
        self.menus_flag = False
        self.addition_flag = False
        self.burger_flag = False

        self.buttons = {}
        self.jingles_buttons = {}
        self.j_buttons_created = False

        self.jingles_update()

        self.played = False
        self.update()

    def display_jingle(self, surface, jingle):
        if self.timer is None:
            self.timer = time.time()

            log.append(time.localtime(), 'jingle', jingle)

        if jingle == "nuggets":
            if self.jingle_played is False and self.stg.sound and nuggets_sound is not False:
                nuggets_sound.play()
                self.jingle_played = True
            surface.blit(nuggets_img, (0, 0))

        if jingle == 'seloupoivre':
            if self.jingle_played is False and self.stg.sound and seloupoivre_sound is not False:
                seloupoivre_sound.play()
                self.jingle_played = True
            surface.blit(seloupoivre_img, (0, 0))

        if jingle == 'menus':
            if self.jingle_played is False and self.stg.sound and menus_sound is not False:
                menus_sound.play()
            surface.blit(menus_img, (0, 0))

        if jingle == 'addition':
            if self.jingle_played is False and self.stg.sound and addition_sound is not False:
                addition_sound.play()
            surface.blit(addition_img, (0, 0))

        if jingle == 'burger':
            if self.jingle_played is False and self.stg.sound and burger_sound is not False:
                burger_sound.play()
            surface.blit(burger_img, (0, 0))

        if time.time() - self.timer > 5:
            self.jingle = False
            self.current_jingle = None
            self.timer = None
            self.jingles_flag = False
            self.jingle_played = False

    def handle_event(self, evt):
        if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
            for func, rect in self.buttons.items():
                if rect.collidepoint(evt.pos):
                    if func == 'jingles':
                        self.jingles_flag = True

        if self.jingles_flag:
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for func, rect in self.jingles_buttons.items():
                    if rect.collidepoint(evt.pos):
                        if func == 'nuggets':
                            self.nuggets_flag = True
                        if func == 'seloupoivre':
                            self.seloupoivre_flag = True
                        if func == 'menus':
                            self.menus_flag = True
                        if func == 'addition':
                            self.addition_flag = True
                        if func == 'burger':
                            self.burger_flag = True
                        if func == 'annuler':
                            self.jingles_flag = False

            if evt.type == MOUSEBUTTONUP and evt.button == 1:
                for func, rect in self.jingles_buttons.items():
                    if rect.collidepoint(evt.pos):
                        if func in ['nuggets', 'seloupoivre', 'menus', 'addition', 'burger']:
                            self.jingle = True
                            self.current_jingle = func

                self.reset_jingles_flags()
            self.jingles_update()

    def change_score(self, team, nb):
        if team == 'ketchup':
            self.score_ketchup += nb
            log.append(time.localtime(), 'score', ['ketchup', nb])
            if self.score_ketchup < 0:
                self.score_ketchup = 0
            if self.score_ketchup > 25:
                self.score_ketchup = 25

        elif team == 'mayo':
            self.score_mayo += nb
            log.append(time.localtime(), 'score', ['mayo', nb])
            if self.score_mayo < 0:
                self.score_mayo = 0
            if self.score_mayo > 25:
                self.score_mayo = 25

    def reset_jingles_flags(self):
        self.nuggets_flag = False
        self.seloupoivre_flag = False
        self.menus_flag = False
        self.addition_flag = False
        self.burger_flag = False

    def jingles_update(self):
        self.jingles_screen = pygame.Surface(self.stg.resolution)

        # Background ne marche pas
        background = pygame.Surface(self.stg.resolution)
        background.fill(BLACK)
        background.set_alpha(64)
        self.jingles_screen.blit(background, (0, 0))

        center_x = self.stg.resolution[0] / 2

        start_y = 60
        offset_y = 70
        text_size = 60
        text_size_small = 50

        if self.stg.resolution[0] == 1920:
            start_y = 140
            offset_y = 100
            text_size = 80
            text_size_small = 60

        jingle_txt = dimbo.render("Lancer un jingle", text_size_small, WHITE)
        self.jingles_screen.blit(jingle_txt, (center_x - jingle_txt.get_rect().width / 2, start_y))

        """ NUGGETS """
        nuggets_color = BQ_BLUE
        if self.nuggets_flag:
            nuggets_color = WASABI
        nuggets_txt = horseshoelemonade.render("Nuggets", text_size, nuggets_color)
        nuggets_rect = (center_x - nuggets_txt.get_rect().width / 2, start_y + offset_y,
                        nuggets_txt.get_rect().width, nuggets_txt.get_rect().height)
        self.jingles_screen.blit(nuggets_txt, (nuggets_rect[0], nuggets_rect[1]))

        """ SEL OU POIVRE """
        seloupoivre_color = BQ_BLUE
        if self.seloupoivre_flag:
            seloupoivre_color = WASABI
        seloupoivre_txt = horseshoelemonade.render("Sel ou Poivre", text_size, seloupoivre_color)
        seloupoivre_rect = (center_x - seloupoivre_txt.get_rect().width / 2, start_y + offset_y * 2,
                            seloupoivre_txt.get_rect().width, seloupoivre_txt.get_rect().height)
        self.jingles_screen.blit(seloupoivre_txt, (seloupoivre_rect[0], seloupoivre_rect[1]))

        """ MENUS """
        menus_color = BQ_BLUE
        if self.menus_flag:
            menus_color = WASABI
        menus_txt = horseshoelemonade.render("Menus", text_size, menus_color)
        menus_rect = (center_x - menus_txt.get_rect().width / 2, start_y + offset_y * 3,
                      menus_txt.get_rect().width, menus_txt.get_rect().height)
        self.jingles_screen.blit(menus_txt, (menus_rect[0], menus_rect[1]))

        """ L'ADDITION """
        addition_color = BQ_BLUE
        if self.addition_flag:
            addition_color = WASABI
        addition_txt = horseshoelemonade.render("L'addition", text_size, addition_color)
        addition_rect = (center_x - addition_txt.get_rect().width / 2, start_y + offset_y * 4,
                         addition_txt.get_rect().width, addition_txt.get_rect().height)
        self.jingles_screen.blit(addition_txt, (addition_rect[0], addition_rect[1]))

        """ LE BURGER DE LA MORT """
        burger_color = BQ_BLUE
        if self.burger_flag:
            burger_color = WASABI
        burger_txt = horseshoelemonade.render("Le Burger de la mort", text_size, burger_color)
        burger_rect = (center_x - burger_txt.get_rect().width / 2, start_y + offset_y * 5,
                       burger_txt.get_rect().width, burger_txt.get_rect().height)
        self.jingles_screen.blit(burger_txt, (burger_rect[0], burger_rect[1]))

        """ ANNULER """
        annuler_txt = dimbo.render("Annuler", text_size_small, WHITE)
        annuler_rect = (center_x - annuler_txt.get_rect().width / 2, start_y + offset_y * 7,
                        annuler_txt.get_rect().width, annuler_txt.get_rect().height)
        self.jingles_screen.blit(annuler_txt, (annuler_rect[0], annuler_rect[1]))

        """ BUTTONS """
        if self.j_buttons_created is False:
            self.jingles_buttons['nuggets'] = pygame.rect.Rect(nuggets_rect)
            self.jingles_buttons['seloupoivre'] = pygame.rect.Rect(seloupoivre_rect)
            self.jingles_buttons['menus'] = pygame.rect.Rect(menus_rect)
            self.jingles_buttons['addition'] = pygame.rect.Rect(addition_rect)
            self.jingles_buttons['burger'] = pygame.rect.Rect(burger_rect)
            self.jingles_buttons['annuler'] = pygame.rect.Rect(annuler_rect)

            self.j_buttons_created = True

    def update(self):
        self.screen.fill(BLACK)

        if self.score_ketchup < 10:
            txt_k = "0%s" % self.score_ketchup
        else:
            txt_k = str(self.score_ketchup)

        if self.score_mayo < 10:
            txt_m = "0%s" % self.score_mayo
        else:
            txt_m = str(self.score_mayo)

        size = 340
        if self.stg.resolution[0] == 1920:
            size = 500

        center_x = self.stg.resolution[0] / 2
        center_y = self.stg.resolution[1] / 2

        txt_s_k = horseshoelemonade.render(txt_k, size, KETCHUP)
        txt_s_m = horseshoelemonade.render(txt_m, size, MAYO)

        rect_s_k = txt_s_k.get_rect()
        rect_s_m = txt_s_m.get_rect()

        self.buttons = {}

        button_s_k = pygame.rect.Rect(center_x / 2 - rect_s_k.width / 2, center_y - rect_s_k.height / 2,
                                      rect_s_k.width, rect_s_k.height)
        button_s_m = pygame.rect.Rect(center_x * 1.5 - rect_s_m.width / 2, center_y - rect_s_m.height / 2,
                                      rect_s_m.width, rect_s_m.height)

        self.buttons['ketchup'] = button_s_k
        self.buttons['mayo'] = button_s_m

        self.screen.blit(txt_s_k, (center_x / 2 - rect_s_k[2] / 2, center_y - rect_s_k.height / 2))
        self.screen.blit(txt_s_m, (center_x * 1.5 - rect_s_m[2] / 2, center_y - rect_s_m.height / 2))

        bottom = 20
        txt_size = 30
        if self.stg.resolution[0] == 1920:
            bottom = 80
            txt_size = 40

        retour_txt = dimbo.render("Retour", txt_size, WHITE)
        retour_button = (self.stg.resolution[0] - retour_txt.get_rect().width - bottom,
                         self.stg.resolution[1] - retour_txt.get_rect().height - bottom,
                         retour_txt.get_rect().width,
                         retour_txt.get_rect().height)
        self.screen.blit(retour_txt, (retour_button[0], retour_button[1]))
        self.buttons['retour'] = pygame.rect.Rect(retour_button)

        jingle_txt = dimbo.render("Jingles", txt_size, WHITE)
        jingle_rect = (self.stg.resolution[0] - jingle_txt.get_rect().width - bottom - 100,
                       self.stg.resolution[1] - jingle_txt.get_rect().height - bottom,
                       jingle_txt.get_rect().width,
                       jingle_txt.get_rect().height)
        self.screen.blit(jingle_txt, (jingle_rect[0], jingle_rect[1]))
        self.buttons['jingles'] = pygame.rect.Rect(jingle_rect)

    def display(self, window):
        window.blit(self.screen, (0, 0))
        if self.jingles_flag:
            window.blit(self.jingles_screen, (0, 0))

        if self.jingle:
            self.display_jingle(window, self.current_jingle)


class PygameQuiz:
    def __init__(self):
        """ Main class, gère tous les écrans, et capte les évènements """
        self.stg = Settings()
        self.window = pygame.display.set_mode(self.stg.resolution)
        icon = pygame.image.load(ICON_FILE).convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Pygame Quiz")

        self.continuer = True

        self.mainmenu = MainMenu(self.stg)
        self.mainmenu_flag = True

        self.settings = None
        self.settings_flag = False

        self.score = None
        self.score_flag = False

        self.loading = None
        self.loading_flag = False

    def main_menu(self):
        self.window = pygame.display.set_mode(self.stg.resolution)

        self.mainmenu.update()
        self.mainmenu_flag = True

        self.settings = None
        self.settings_flag = False

        self.score = None
        self.score_flag = False

        self.loading = None
        self.loading_flag = False

    def start_game(self):
        self.score = Score(self.stg)
        self.score_flag = True

        self.mainmenu_flag = False

    def menu_param(self):
        self.settings = SettingsMenu(self.stg)
        self.settings_flag = True

        self.mainmenu_flag = False

    def handle_event(self, evt):
        if evt.type == KEYDOWN and evt.key == K_SPACE:
            pygame.mixer.stop()

        if self.mainmenu_flag:
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for func, rect in self.mainmenu.buttons.items():
                    if rect.collidepoint(evt.pos):
                        if func == "commencer":
                            self.start_game()
                        if func == "param":
                            self.menu_param()
                        if func == "quitter":
                            self.continuer = False

        if self.score_flag:
            self.score.handle_event(evt)
            if evt.type == MOUSEBUTTONDOWN:
                for func, rect in self.score.buttons.items():
                    if rect.collidepoint(evt.pos):
                        if func == 'retour':
                            self.main_menu()
                        else:
                            if evt.button == 1:
                                self.score.change_score(func, 1)
                            elif evt.button == 3:
                                self.score.change_score(func, -1)
                            self.score.update()

        if self.settings_flag:
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for func, rect in self.settings.buttons.items():
                    if rect.collidepoint(evt.pos):
                        if func == "720" or func == "1080":
                            self.settings.change_resolution(func)
                        if func == "sound_on" or func == "sound_off":
                            self.settings.toggle_sound(func)
                        if func == "appliquer":
                            self.settings.apply_changes()
                            self.main_menu()
                        if func == "annuler":
                            self.main_menu()

    def display(self):
        if self.mainmenu_flag:
            self.mainmenu.display(self.window)
        if self.score_flag:
            self.score.display(self.window)
        if self.settings_flag:
            self.settings.display(self.window)


pq = PygameQuiz()

""" Chargement des images """
nuggets_img = load_image(nuggets_imgfile)
seloupoivre_img = load_image(seloupoivre_imgfile)
menus_img = load_image(menus_imgfile)
addition_img = load_image(addition_imgfile)
burger_img = load_image(burger_imgfile)

if pq.stg.resolution[0] == 1280:
    nuggets_img = pygame.transform.scale(nuggets_img, pq.stg.resolution)
    seloupoivre_img = pygame.transform.scale(seloupoivre_img, pq.stg.resolution)
    menus_img = pygame.transform.scale(menus_img, pq.stg.resolution)
    addition_img = pygame.transform.scale(addition_img, pq.stg.resolution)
    burger_img = pygame.transform.scale(burger_img, pq.stg.resolution)

continuer = True
while continuer:

    continuer = pq.continuer
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

        pq.handle_event(event)

    pq.display()
    pygame.display.flip()

pygame.quit()
