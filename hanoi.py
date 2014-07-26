"""
 Famous game in graphic mode
"""

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout


# constants
NB_MAST = 3
NB_DISCS_DEFAULT =  7
DISC_HEIGHT = .1
DISC_MINIMUM_WIDTH = 0.2
DISC_GROTH = .01
MAST_HEIGHT = 1
MAST_WIDTH = .02
MAST_INITIAL_POS = .15
MAST_GROTH_X = .35
MAST_POS_Y  = 0

#Builder.load_file('gameboard.kv') # charge le fichier kv

class Disc(Button):
    ''' Disc object '''
    def __init__(self, **kwargs):
        ''' Create and Init a disc, the size is calculated giving the number of the disc : disc_number'''
        super(Disc, self).__init__(**kwargs)
        if 'disc_number' in kwargs:
            self.disc_number = kwargs['disc_number']
            self.size_hint = (DISC_MINIMUM_WIDTH + self.disc_number * DISC_GROTH, DISC_HEIGHT)


class Mast(Button):
    '''
       Mast object
    '''
    def other_tower_source(self, n):
        for i in range(3):
            if i == n:
                continue
            if len(self.parent.towers[i]) != 0:
                if self.parent.towers[i][0].state == 'down':
                    return True, i
            return False, n


    def __init__(self, **kwargs):
        ''' Create and Init a mast, the size and the position is calculated giving the number of the mast : mast_number '''
        super(Mast, self).__init__(**kwargs)

        if 'mast_number' in kwargs:
            self.mast_number = kwargs['mast_number']
            self.pos_hint={'center_x': MAST_INITIAL_POS + self.mast_number * MAST_GROTH_X, 'y': MAST_POS_Y}
            self.size_hint=(MAST_WIDTH, MAST_HEIGHT)
            self.list_disc = []
            self.selected = False


    def on_touch_down(self, touch):
        ''' If no mast is selected and mast not empty of disc then we select the mast and the upper disc '''
        if self.collide_point(*touch.pos): # if touch concern this mast
            no_mast_selected = True
            for i in range(NB_MAST):
                if self.parent.mast_list[i].selected:
                    no_mast_selected = False
            if no_mast_selected:
                if len(self.list_disc) != 0:
                    Select_ok = False
                    for mast in self.parent.mast_list:
                        if self == mast:
                            continue
                        if len(mast.list_disc) == 0:
                            Select_ok = True
                            break
                        elif self.list_disc[0].disc_number < mast.list_disc[0].disc_number:
                            Select_ok = True
                            break                            

                    if Select_ok:
                        self.selected = True
                        self.list_disc[0].state = 'down'
            else:
                 for mast in self.parent.mast_list:
                     if self == mast:
                         continue
                     if mast.selected:
                         if (len(self.list_disc) == 0)  or (self.list_disc[0].disc_number > mast.list_disc[0].disc_number):
                             mast.selected = False
                             w = mast.list_disc.pop(0)
                             #self.selected = True
                             w.state = 'normal'
                             self.list_disc.insert(0, w)
                             l = len(self.list_disc)
                             w.pos_hint = {'center_x':MAST_INITIAL_POS + MAST_GROTH_X * self.mast_number, 'y':(l-1) * DISC_HEIGHT}


            return super(Button, self).on_touch_down(touch)



class GameBoard(RelativeLayout):
    ring_number = NumericProperty
    def init_towers(self, n):
        ''' Init board '''

        for i in range(3):
            btn = Mast(mast_number=i)
            self.mast_list.append(btn)
            #  btn.bind(pressed=self.btn_pressed)
            self.add_widget(btn)

        for i in range( n):
            btn = Disc(disc_number=i, text=str(i+1))
            #self.towers[0].append(btn)

            btn.pos_hint = {'center_x':MAST_INITIAL_POS, 'y':(n-i-1) * .1}
            self.mast_list[0].list_disc.append(btn)
            self.add_widget(btn)
            #print("position y:", (n-i) * .1)



    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)

        if 'ring_number' in kwargs:
            self.ring_number = kwargs['ring_number']
        else:
            self.ring_number = 7

        self.mast_list = []


        self.init_towers(self.ring_number)

    def show_towers(self):
        pass

    ## def btn_pressed(self, instance, pos):
    ##     print(len(self.towers[0]))


class ButtonNotQuiet(Button):
    def on_say_to_run(self, x, y):
        pass



class ScreenColor(Screen):
    pass

class ScreenMenu(Screen):
    pass

class ScreenGame(Screen):
    pass

class ScreenLoad(Screen):
    pass

class Hanoi(ScreenManager):
    selected_color = ListProperty([1, 0, 0, 1])

class HanoiApp(App):
    def build(self):
        return Hanoi()


if __name__ == '__main__':
    HanoiApp().run()
