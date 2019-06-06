import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 


class MENU():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        menu_width = int(self.screen_width * 0.065)
        self.menu_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu_box.set_size_request(menu_width, 0)
        self.menu_box.set_name('MENU_BOX')


    def return_menu_box(self):
        return self.menu_box