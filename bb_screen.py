import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 
import cairo
import math

import cv2


class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Screen_BB2():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.window_width = self.screen_width
        self.window_height = self.screen_height


        window.resize(self.screen_width, self.screen_height)

        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.set_menu()
        self.set_drawing_box()

    def window_change(self, window):
        self.window_width = window.get_allocation().width
        self.window_height = window.get_allocation().height
    
    def set_menu(self):
        self.menu = Menu(self.window)
        menu_box = self.menu.return_menu_box()
        self.main_box.pack_start(menu_box, False, False, 0)

    def set_drawing_box(self):
        spacing = int(self.screen_width * 0.01)
        self.drawing = Drawing(self.window)
        drawing_box = self.drawing.return_drawing_box()
        self.main_box.pack_start(drawing_box, False, False, spacing)

    def return_main_box(self):
        return self.main_box

class Menu():
    def __init__(self, window):
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        menu_width = (self.screen_width*0.065)
        self.menu_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu_box.set_size_request(menu_width, 0)
        self.menu_box.set_name('MENU_BOX')


    def return_menu_box(self):
        return self.menu_box
    

class Drawing():
    def __init__(self, window):
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        drawing_width = int(self.screen_width * 0.75)
        drawing_height = int(self.screen_height * 0.8)
        
        self.main_drawing = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.drawing_box = Gtk.Box()
        self.drawing_box.set_name("DRAWING_BOX")
        self.drawing_box.set_size_request(drawing_width, drawing_height)
        self.main_drawing.pack_start(self.drawing_box, True, False, 0)

        self.g_ex = None
        self.g_ey = None
        self.pix = None
        self.darea = Gtk.DrawingArea()
        self.drawing_box.pack_start(self.darea, True, True, 0)

        self.darea.set_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)

        self.darea.connect('motion-notify-event', self.motion_event)
        self.darea.connect('button-press-event', self.drawing_clicked)
        self.darea.connect('draw', self.on_draw)
    
    def motion_event(self, w, e):
        self.g_ex = e.x
        self.g_ey = e.y
        self.darea.queue_draw()

    def drawing_clicked(self, w, e):
        print('clicked position:', e.x, e.y)
        img_width = int(self.screen_width * 0.8)
        img_height = int(self.screen_height * 0.8)

        #self.pix = GdkPixbuf.Pixbuf.new_from_file_at_size('pikachu_meme.jpg', img_width, img_height)
        self.pix = GdkPixbuf.Pixbuf.new_from_file('pikachu_meme.jpg')
        

    def on_draw(self, w, cr):
        if self.pix is not None:
            Gdk.cairo_set_source_pixbuf(cr, self.pix, 0, 0)
            cr.paint()
            cr.set_source_rgb(1,1,1)
            cr.arc(self.g_ex, self.g_ey, 5, 0, 2*math.pi)
            cr.fill()
            cr.stroke()

    def return_drawing_box(self):
        return self.main_drawing












class Screen_BB():
    def __init__(self, window):
        self.first_pressed = False
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        window.resize(self.screen_width, self.screen_height)
        window.connect('check-resize', self.changed)
        
        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.main_box.set_name("MAIN_BOX")
        
        self.coords = []
        self.pix = GdkPixbuf.Pixbuf.new_from_file_at_size('pikachu_meme.jpg', self.screen_width, self.screen_height)
        self.drawing_area_box()

    def changed(self, window):
        self.screen_width = window.get_allocation().width
        self.screen_height = window.get_allocation().height
        
    def options_box(self):
        pass
    
    def drawing_area_box(self):
        self.darea = Gtk.DrawingArea()
        self.main_box.pack_start(self.darea, True, True, 0)
        
        self.darea.set_events(Gdk.EventMask.POINTER_MOTION_MASK|Gdk.EventMask.BUTTON_PRESS_MASK)
        self.darea.connect('motion-notify-event', self.motion_event)
        self.darea.connect('button-press-event', self.on_button_press) 
        self.darea.connect('draw', self.on_draw)

        
        

    def on_button_press(self, w, e):
        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == MouseButtons.LEFT_BUTTON:
            self.coords.append([e.x, e.y])
            self.darea.queue_draw()

    def motion_event(self, w, e):
        #print('position:', e.x, e.y)
        pass

    def on_draw(self, wid, cr):
        #cr.set_source_rgb(0,0,0)
        
        #cr = cairo.Context(im)
        if not self.first_pressed:
            im = cairo.ImageSurface.create_from_png('proyecto.png')
            cr.set_source_surface(im, 0,0)
            cr.paint()
            
        #print('first:', self.first_pressed)
        #Gdk.cairo_set_source_pixbuf(cr, self.pix, 0, 0)
        #Gdk.cairo_surface_create_from_pixbuf(cr, self.pix, 0, 0)
        #cr.cairo_surface_create_from_pixbuf(self.pix, 1)
        self.first_pressed = True   
        #cr.paint()
        #cr.set_surface(self.pix, 0, 0)
        #cairo.set_source_pixbuf(cr, self.pix, 0, 0)
        
        #cr.set_source_pixbuf(self.pix, 0, 0)
        #cr.paint()
        #cr.set_line_width(1)
        #for x,y in self.coords:
            #print('coords:', x, y)
        #    cr.arc(x,y, 5, 0, 2*math.pi)
        #    cr.fill()
        #    cr.stroke()
        

    def net_and_data_box(self):
        pass

    def return_main_box(self):
        return self.main_box




