import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 
import cairo
import math

class DRAWING():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        drawing_width = int(self.screen_width * 0.75)
        drawing_height = int(self.screen_height * 0.8)
        
        self.main_drawing = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.secondary_drawing = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.main_drawing.pack_start(self.secondary_drawing, True, True, 0)
        self.drawing_box = Gtk.Box()
        self.drawing_box.set_name("DRAWING_BOX")
        self.drawing_box.set_size_request(drawing_width, drawing_height)
        #self.main_drawing.pack_start(self.drawing_box, True, False, 0)
        self.secondary_drawing.pack_start(self.drawing_box, True, False, 0)
        self.g_ex = None
        self.g_ey = None
        self.pix = None
        self.darea = Gtk.DrawingArea()
        self.drawing_box.pack_start(self.darea, True, True, 0)
        self.clicked = False

        self.darea.set_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)

        #self.darea.connect('motion-notify-event', self.motion_event)
        #self.darea.connect('button-press-event', self.__drawing_clicked)
        #self.darea.connect('draw', self.on_draw)
    
    def motion_event(self, w, e):
        self.g_ex = e.x
        self.g_ey = e.y
        #self.darea.queue_draw()

    def create_rectbox_clicked(self):
        self.clicked = True


    def __drawing_clicked(self, w, e):
        self.clicked = True
        self.click_ex = e.x
        self.click_ey = e.y
        #print("clicked")
        #self.darea.queue_draw()
        #self.pix = GdkPixbuf.Pixbuf.new_from_file_at_size('pikachu_meme.jpg', img_width, img_height)
        #self.pix = GdkPixbuf.Pixbuf.new_from_file('pikachu_meme.jpg')
        

    #def on_draw(self, w, cr):
    #    print("painting circle", self.clicked)
    #    if self.clicked:
    #        print("painting circle2")
            #Gdk.cairo_set_source_pixbuf(cr, self.pix, 0, 0)
    #        cr.set_source_rgb(1,1,1)
    #        cr.arc(self.click_ex, self.click_ey, 5, 0, 2*math.pi)
    #        cr.fill()
    #        cr.stroke()
        """
        if self.pix is not None:
            Gdk.cairo_set_source_pixbuf(cr, self.pix, 0, 0)
            cr.paint()
            cr.set_source_rgb(1,1,1)
            cr.arc(self.g_ex, self.g_ey, 5, 0, 2*math.pi)
            cr.fill()
            cr.stroke()
        """

    def get_drawing_area(self):
        return self.darea

    def return_drawing_box(self):
        return self.main_drawing