import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from .menu import MENU
from .drawing import DRAWING
from .resources import ResourcesPanel

class DBBT():
    def __init__(self, window):
        self.window = window
        #self.screen = window.get_screen()
        self.screen = Gdk.Screen.get_default()
        monitor_geo = self.screen.get_monitor_geometry(0)
        #print("screen =", self.screen.get_width(), monitor_geo.width)
        self.screen_width = monitor_geo.width #self.screen.get_width()
        self.screen_height = monitor_geo.height #self.screen.get_height()
        self.window_width = self.screen_width
        self.window_height = self.screen_height

        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        self.set_menu()
        self.set_drawing()
        self.set_resources()

    def set_menu(self):
        self.dbbt_menu = MENU(self.window)
        menu_box = self.dbbt_menu.return_menu_box()
        self.main_box.pack_start(menu_box, False, False, 0)
    
    def set_drawing(self):
        spacing = int(self.screen_width * 0.01)
        self.dbbt_drawing = DRAWING(self.window)
        drawing_box = self.dbbt_drawing.return_drawing_box()
        self.darea = self.dbbt_drawing.get_drawing_area()
        self.main_box.pack_start(drawing_box, False ,False, spacing)
    
    def set_resources(self):
        self.dbbt_resources = ResourcesPanel(self.window)
        self.resources_box = self.dbbt_resources.return_resource_box()
        self.main_box.pack_start(self.resources_box, False, False, 0)
        self.dbbt_resources.wrap_drawing_area(self.darea)

        self.dbbt_menu.wrap_resources(self.dbbt_resources)
        self.dbbt_menu.wrap_drawing(self.dbbt_drawing)

    
    def return_main_dbbt_box(self):
        return self.main_box

