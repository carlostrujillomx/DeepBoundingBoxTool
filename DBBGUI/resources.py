import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
import cairo

from os import listdir
import cv2
import math
from copy import deepcopy


class ResourcesPanel():
    def __init__(self, window):
        self.window = window
        #self.screen = Gdk.Screen.get_default()
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width #self.screen.get_width()
        self.screen_height = monitor_geo.height #self.screen.get_height()
        
        box_width = int(self.screen_width*0.178)
        self.resource_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.resource_box.set_name("MENU_BOX")
        self.resource_box.set_size_request(box_width, 0)
        
        self.current_pix = None
        self.clicked = False
        self.clicks_qty = 0
        self.click_ex = 0
        self.click_ey = 0
        self.motion_ex = 0
        self.motion_ey = 0
        self.rectangles = []
        self.current_rectangle = []

        self.set_label()
        self.set_net_box()
        self.set_files_loaded()
        self.add_remove_label()
        self.set_label_classes()
        self.set_resources()

    def set_label(self):
        label_box = Gtk.Box()
        label = Gtk.Label("Deep Learning Model")
        label_box.pack_start(label, True, False, 0)
        self.resource_box.pack_start(label_box, False, False, 0)

    def set_net_box(self):
        spacing = int(self.screen_height * 0.01)
        label_spacing = int(self.screen_width * 0.005)
        net_box = Gtk.Box()
        net_label = Gtk.Label("Model Path:")
        net_button = Gtk.Button("Select Path")

        net_box.pack_start(net_label, False, False, label_spacing)
        net_box.pack_start(net_button, True, False, 0)

        self.resource_box.pack_start(net_box, False, False, spacing)

    def set_files_loaded(self):
        spacing = int(self.screen_height * 0.01)
        scroll_height = int(self.screen_height * 0.1)

        scroll_window = Gtk.ScrolledWindow(None, None)
        scroll_window.set_name("NETSCROLLWINDOW")
        scroll_window.set_size_request(0, scroll_height)
        scroll_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.resource_box.pack_start(scroll_window, False, False, spacing)

        listmodel = Gtk.ListStore(str)
        view = Gtk.TreeView(model = listmodel)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Files loaded", renderer_text, text=0)
        view.append_column(columntext)


        scroll_window.add(view)

    def add_remove_label(self):
        box_width = int(self.screen_width*0.178)
        entryt_width = int(box_width*0.55)

        box = Gtk.Box()
        label_entry = Gtk.Entry()
        label_entry.set_text("Label")
        label_entry.set_size_request(entryt_width, 0)
        box.pack_start(label_entry, False, False, 0)

        add_button = Gtk.Button('Add')
        remove_button = Gtk.Button('Remove')

        box.pack_start(add_button, False, False, 0)
        box.pack_start(remove_button, False, False, 0)
        self.resource_box.pack_start(box, False, False ,0)

    def set_label_classes(self):
        box_height = int(self.screen_height * 0.3)
        box_width = int(self.screen_width*0.178)

        vbox = Gtk.Box()
        vbox.set_size_request(0, box_height)
        self.resource_box.pack_start(vbox, False, False, 0)
        
        scw_width = int(box_width/3)
        scw1 = Gtk.ScrolledWindow(None, None)
        scw1.set_name("NETSCROLLWINDOW")
        scw1.set_size_request(scw_width, box_height)
        scw1.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        listmodel = Gtk.ListStore(str)
        view = Gtk.TreeView(model = listmodel)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Image labels", renderer_text, text=0)
        view.append_column(columntext)
        
        scw1.add(view)
        vbox.pack_start(scw1, False, False, 0)

        
        scw2 = Gtk.ScrolledWindow(None, None)
        scw2.set_name("NETSCROLLWINDOW")
        scw2.set_size_request(scw_width, box_height)
        scw2.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        listmodel2 = Gtk.ListStore(str)
        view2 = Gtk.TreeView(model = listmodel2)
        view2.set_name("NETVIEW")
        renderer_text2 = Gtk.CellRendererText()
        columntext2 = Gtk.TreeViewColumn("Working labels", renderer_text2, text=0)
        view2.append_column(columntext2)
        
        scw2.add(view2)
        vbox.pack_start(scw2, False, False, 0)
        

        scw3 = Gtk.ScrolledWindow(None, None)
        scw3.set_name("NETSCROLLWINDOW")
        scw3.set_size_request(scw_width, box_height)
        scw3.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        listmodel3 = Gtk.ListStore(str)
        view3 = Gtk.TreeView(model = listmodel3)
        view3.set_name("NETVIEW")
        renderer_text3 = Gtk.CellRendererText()
        columntext3 = Gtk.TreeViewColumn("Net labels", renderer_text3, text=0)
        view3.append_column(columntext3)
        
        scw3.add(view3)
        vbox.pack_start(scw3, False, False, 0)
        
        """
        scroll_height = int(self.screen_height * 0.3)
        scroll_window = Gtk.ScrolledWindow(None, None)
        scroll_window.set_name("NETSCROLLWINDOW")
        scroll_window.set_size_request(0, scroll_height)
        scroll_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.resource_box.pack_start(scroll_window, False, False, 0)

        listmodel = Gtk.ListStore(str, str)
        view = Gtk.TreeView(model = listmodel)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Image labels", renderer_text, text=0)
        view.append_column(columntext)
        renderer_text2 = Gtk.CellRendererText()
        columntext2 = Gtk.TreeViewColumn("Working labels", renderer_text2, text=1)
        view.append_column(columntext2)
        renderer_text3 = Gtk.CellRendererText()
        columntext3 = Gtk.TreeViewColumn("Net labels", renderer_text3, text=2)
        view.append_column(columntext3)

        scroll_window.add(view)
        """
    def set_resources(self):
        scroll_height = int(self.screen_height * 0.416)

        self.resource_scroll_window = Gtk.ScrolledWindow(None, None)
        self.resource_scroll_window.set_name("NETSCROLLWINDOW")
        self.resource_scroll_window.set_size_request(0, scroll_height)
        self.resource_scroll_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.resource_box.pack_start(self.resource_scroll_window, False, False, 0)

        self.list_images = Gtk.ListStore(str)
        view = Gtk.TreeView(model = self.list_images)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Images", renderer_text, text=0)
        view.append_column(columntext)


        self.resource_scroll_window.add(view)

    def set_files(self, path):
        self.current_path = path
        self.cv_width = self.darea.get_allocation().width
        self.cv_height = self.darea.get_allocation().height
        
        files = listdir(path)
        for image_file in files:
            self.list_images.append([image_file])
        
        filename = path+'/'+files[0]
        image = cv2.imread(filename)
        self.current_pix = self.im2pixbuf(image)
        self.list_iterator = bi_iterator(files)
        self.resource_scroll_window.show_all()

        self.darea.queue_draw()
        
    def next_image(self):
        next_iterator = self.list_iterator.next()
        filename = self.current_path+'/'+next_iterator
        print("size darea", self.cv_width, self.cv_height, type(next_iterator))
        if next_iterator != "None":
            image = cv2.imread(filename)
            self.current_pix = self.im2pixbuf(image)
            self.darea.queue_draw()
            print(filename)

    def prev_image(self):
        prev_iterator = self.list_iterator.prev()
        filename = self.current_path+'/'+prev_iterator
        if prev_iterator != "None":
            image = cv2.imread(filename)
            self.current_pix = self.im2pixbuf(image)
            self.darea.queue_draw()


    def im2pixbuf(self, image):
        image = cv2.resize(image, (self.cv_width, self.cv_height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = image.tobytes()
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, self.cv_width, self.cv_height, self.cv_width*3)
        return pix

    def wrap_drawing_area(self, drarea):
        self.darea = drarea
        self.darea.connect('draw', self.__on_draw)
        self.darea.connect('motion-notify-event', self.__motion_event)
        self.darea.connect('button-press-event', self.__drawing_clicked)
    
    def create_rectbox(self):
        self.clicked = True

    def __drawing_clicked(self, w, e):
        if e.button == 1:
            self.clicks_qty += 1
            #print('ebutton:', e.button)
            if self.clicks_qty == 1:
                self.current_rectangle.append([e.x, e.y, 0, 0])
            elif self.clicks_qty == 2:
                self.clicks_qty = 0
                x,y,w,h = self.current_rectangle[0]
                #self.rectangles.append([x,y,w,h])
                self.rectangles.insert(0, [x,y,w,h])
                self.current_rectangle.clear()
                self.current_rectangle = []
        
        elif e.button == 3:
            self.__delete_rectbox(e.x, e.y)    
        
        self.darea.queue_draw()


    def __on_draw(self, w, cr):
        if self.current_pix is not None:
            Gdk.cairo_set_source_pixbuf(cr, self.current_pix, 0, 0)
            cr.paint()
            cr.set_source_rgb(1,1,1)
            
            if len(self.rectangles) == 0:
                if len(self.current_rectangle) > 0:
                    cr.rectangle(self.current_rectangle[0][0], self.current_rectangle[0][1], self.current_rectangle[0][2], self.current_rectangle[0][3])
                    cr.stroke()
            else:
                if len(self.current_rectangle) > 0:
                    cr.rectangle(self.current_rectangle[0][0], self.current_rectangle[0][1], self.current_rectangle[0][2], self.current_rectangle[0][3])
                    cr.stroke()
                for x,y,w,h in self.rectangles:
                    cr.rectangle(x,y,w,h)
                    cr.stroke()
            

    def __motion_event(self, w, e):
        if self.clicks_qty == 1:
            w = e.x - self.current_rectangle[0][0]
            h = e.y - self.current_rectangle[0][1]
            self.current_rectangle[0][2] = w
            self.current_rectangle[0][3] = h
            
        self.darea.queue_draw()

    def __delete_rectbox(self, x, y):
        index = 0
        pop_index = -1
        for x1,y1,w,h in self.rectangles:
            x2 = x1 + w
            y2 = y1 + h
            if (x <= x2 and x >= x1) and (y <= y2 and y >= y1):
                pop_index = index
                break
            index += 1
        if pop_index != -1:
            self.rectangles.pop(pop_index)

    def return_resource_box(self):
        return self.resource_box



class bi_iterator():
    def __init__(self, collection):
        self.collection = collection
        self.index = 0
        self.max_index = len(collection)
        self.current_index = 0
        #print('max collection:', self.max_index)
    
    def next(self):
        if self.current_index < self.max_index-1: 
            self.current_index += 1
        else:
            return "None"
        return self.collection[self.current_index]
    
    def prev(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            return "None"
        return self.collection[self.current_index]
            