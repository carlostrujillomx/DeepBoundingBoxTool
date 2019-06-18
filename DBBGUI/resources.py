import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
import cairo

from os import listdir
import cv2
import math
from copy import deepcopy
from DBBGUI import darknet
import os


class ResourcesPanel():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height
        
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
        self.DBBT_net = None

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

        net_button.connect('clicked', self.__net_button_clicked)

    def set_files_loaded(self):
        spacing = int(self.screen_height * 0.02)
        scroll_height = int(self.screen_height * 0.12)

        self.net_scw = Gtk.ScrolledWindow(None, None)
        self.net_scw.set_name("NETSCROLLWINDOW")
        self.net_scw.set_size_request(0, scroll_height)
        self.net_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.resource_box.pack_start(self.net_scw, False, False, spacing)

        self.net_listmodel = Gtk.ListStore(str)
        view = Gtk.TreeView(model = self.net_listmodel)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Files loaded", renderer_text, text=0)
        view.append_column(columntext)

        self.net_scw.add(view)

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

        self.image_listmodel = Gtk.ListStore(str)
        self.image_view = Gtk.TreeView(model = self.image_listmodel)
        self.image_view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Image labels", renderer_text, text=0)
        self.image_view.append_column(columntext)
        
        scw1.add(self.image_view)
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

        self.listmodel3 = Gtk.ListStore(str)
        self.view3 = Gtk.TreeView(model = self.listmodel3)
        self.view3.set_name("NETVIEW")
        renderer_text3 = Gtk.CellRendererText()
        columntext3 = Gtk.TreeViewColumn("Net labels", renderer_text3, text=0)
        self.view3.append_column(columntext3)
        
        scw3.add(self.view3)
        vbox.pack_start(scw3, False, False, 0)
        
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
        self.rectangles = []
        self.image_listmodel.clear()
        next_iterator = self.list_iterator.next()
        filename = self.current_path+'/'+next_iterator
        if next_iterator != "None":
            image = cv2.imread(filename)
            self.current_pix = self.im2pixbuf(image)
            self.darea.queue_draw()
            
    def prev_image(self):
        self.rectangles = []
        self.image_listmodel.clear()
        prev_iterator = self.list_iterator.prev()
        filename = self.current_path+'/'+prev_iterator
        if prev_iterator != "None":
            image = cv2.imread(filename)
            self.current_pix = self.im2pixbuf(image)
            self.darea.queue_draw()

    def im2pixbuf(self, image):
        if self.DBBT_net is not None:
            detections = self.DBBT_net.make_inference(image)
            self.__draw_boxes(detections, image)
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
            if self.clicks_qty == 1:
                self.current_rectangle.append([e.x, e.y, 0, 0])
            elif self.clicks_qty == 2:
                self.clicks_qty = 0
                x,y,w,h = self.current_rectangle[0]
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

    def __net_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog('Choose a Folder', self.window, Gtk.FileChooserAction.SELECT_FOLDER|Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        net_path = dialog.get_filename()
        dialog.destroy()
        if response == -5:
            self.__set_net_files(net_path)
    
    def __set_net_files(self, path):
        files = listdir(path)
        configPath = None
        weightPath = None
        metaPath = None
        for net_file in files:
            if net_file.endswith('.cfg'):
                configPath = path+'/'+net_file
            elif net_file.endswith('.weights'):
                weightPath = path+'/'+net_file
            elif net_file.endswith('.data'):
                metaPath = path+'/'+net_file
            self.net_listmodel.append([net_file])
        self.net_scw.show_all()

        self.DBBT_net = DARKNET(configPath, weightPath, metaPath)
        self.net_labels = self.DBBT_net.load_classes()

        for net_label in self.net_labels:
            self.listmodel3.append([net_label])
        self.view3.show_all()

    def __draw_boxes(self, detections, image):
        for detects in detections:
            classification = detects[0].decode('utf-8')
            confidence = detects[1]
            box = detects[2]
            x1,y1,w,h = self.__get_upsampled_size(image, box)
            x2 = x1+w
            y2 = y1+h
            #cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)
            #self.__draw_classification(image, [x1,y1,w,h], classification)
            self.rectangles.insert(0, [x1,y1, w, h])
            self.image_listmodel.append([classification])
        self.image_view.show_all()
        self.darea.queue_draw()

    def __get_upsampled_size(self, image, box):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        #w_orig = image.shape[1]
        #h_orig = image.shape[0]
        w_orig = self.cv_width
        h_orig = self.cv_height
        w_net = self.DBBT_net.net_width
        h_net = self.DBBT_net.net_height

        x_c = x/w_net
        y_c = y/h_net
        w_ratio = w/w_net
        h_ratio = h/h_net
        x_ratio = x_c-w_ratio/2
        y_ratio = y_c-h_ratio/2

        x_up = int(x_ratio*w_orig)
        y_up = int(y_ratio*h_orig)
        w_up = int(w_ratio*w_orig)
        h_up = int(h_ratio*h_orig)

        return x_up, y_up, w_up, h_up

    def __draw_classification(self, image, box,classification):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        w_orig = image.shape[1]

        x1 = x
        y1 = y
        x2 = x+int(w*0.5)
        y2 = y+int(h*0.2)
        y_text = y + int(h*0.15)
        draw_index = w/(w_orig*0.3)
        cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), -1)
        cv2.putText(image, classification, (x,y_text), cv2.FONT_HERSHEY_SIMPLEX, draw_index, (255,255,255), 1)

    def return_resource_box(self):
        return self.resource_box



class bi_iterator():
    def __init__(self, collection):
        self.collection = collection
        self.index = 0
        self.max_index = len(collection)
        self.current_index = 0
        
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
            

class DARKNET():

    def __init__(self, configPath, weightPath, metaPath):
        print('[INFO]: loading NEURAL DATA')
        if not os.path.exists(configPath) or not os.path.exists(weightPath) or not os.path.exists(metaPath):
            raise ValueError('Invalid configuration files directory please verify all files are in place')
        
        self.metaPath = metaPath
        self.net = darknet.load_net_custom(configPath.encode('ascii'), weightPath.encode('ascii'), 0 ,1)
        self.meta_net = darknet.load_meta(metaPath.encode('ascii'))
        self.net_width = darknet.network_width(self.net)
        self.net_height = darknet.network_height(self.net)
        self.darknet_image = darknet.make_image(self.net_width, self.net_height, 3)

        #self.load_classes()
        print('[INFO]: NEURAL DATA load finished')

    def make_inference(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_rsz = cv2.resize(image_rgb, (self.net_width,self.net_height))
        darknet.copy_image_from_bytes(self.darknet_image, rgb_rsz.tobytes())
        detections = darknet.detect_image(self.net, self.meta_net, self.darknet_image, thresh=0.25)
        #print('detections:', detections)
        return detections

    def load_classes(self):
        names_list = []
        self.metafile = open(self.metaPath, 'r')
        lines = self.metafile.readlines()
        for line in lines:
            line_strip = line.strip('\n')
            line_split = line_strip.split(' ')
            if line_split[0] == 'names':
                names = line_split[2]
                #print('NAMES=', line_split[2])
            #print('meta:',line_split)
        names_file = open(names, 'r')
        line_names = names_file.readlines()
        for line_name in line_names:
            line_name = line_name.strip('\n')
            names_list.append(line_name)
            #print('name:', line_name)

        self.metafile.close()
        names_file.close()

        return names_list
