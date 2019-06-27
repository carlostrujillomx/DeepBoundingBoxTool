import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 
import cairo
import math

class DRAWING():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height
        
        self.drawing_width = int(self.screen_width * 0.75)
        self.drawing_height = int(self.screen_height * 0.8)
        
        self.main_drawing = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.secondary_drawing = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.main_drawing.pack_start(self.secondary_drawing, True, True, 0)
        self.drawing_box = Gtk.Box()
        self.drawing_box.set_name("DRAWING_BOX")
        self.drawing_box.set_size_request(self.drawing_width, self.drawing_height)
        self.secondary_drawing.pack_start(self.drawing_box, True, False, 0)
        self.g_ex = None
        self.g_ey = None
        self.pix = None
        self.darea = Gtk.DrawingArea()
        self.darea.set_size_request(self.drawing_width, self.drawing_height)
        self.drawing_box.pack_start(self.darea, False, False, 0)
        self.clicked = False

        
    def get_drawing_area(self):
        return self.darea

    def get_drawing_size(self):
        return self.drawing_width, self.drawing_height
        
    def return_drawing_box(self):
        return self.main_drawing