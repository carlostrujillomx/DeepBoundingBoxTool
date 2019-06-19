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

        self.image_folder = None

        box_width = int(self.screen_width * 0.178)
        self.resource_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.resource_box.set_name('MENU_BOX')
        self.resource_box.set_size_request(box_width, 0)
        
        self.panelManager()

    def panelManager(self):
        spacing = int(self.screen_height * 0.01)
        self.DboxResource = DeepLearningBox(self.window)
        dbox = self.DboxResource.get_net_box()
        self.resource_box.pack_start(dbox, False, False, 0)

        self.LabelResource = LabelClasses(self.window)
        lbox = self.LabelResource.return_NetLabelsBox()
        self.resource_box.pack_start(lbox, False, False, spacing)

        self.ImageResource = ImageResources(self.window)
        ibox = self.ImageResource.return_image_resources_box()
        self.resource_box.pack_start(ibox, False, False, 0)

    def wrap_drawing_area(self, darea):
        self.darea = darea

    def set_files(self, image_folder_path):
        self.image_folder = image_folder_path
        self.drawing_width = self.darea.get_allocation().width 
        self.drawing_height = self.darea.get_allocation().height
        collection = self.ImageResource.set_files(image_folder_path)
        self.images_iterator = bi_iterator(collection)

        self.DrawingImage = DrawingEvents(self.darea)
        filename = image_folder_path+'/'+collection[0]
        self.DrawingImage.set_drawing_image(filename)

    def next_image(self):
        if self.image_folder is not None:
            file_, index = self.images_iterator.next()
            if file_ is not "None":
                filename = self.image_folder+'/'+file_
                self.DrawingImage.set_drawing_image(filename)
                self.ImageResource.set_view_cursor(index)
        
    def prev_image(self):
        if self.image_folder is not None:
            file_, index = self.images_iterator.prev()
            if file_ is not "None":
                filename = self.image_folder+'/'+file_
                self.DrawingImage.set_drawing_image(filename)
                self.ImageResource.set_view_cursor(index)

    def return_resource_box(self):
        return self.resource_box        


class DeepLearningBox():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.dbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.set_net_box()
        self.set_files_loaded()

    def set_net_box(self):
        spacing = int(self.screen_height * 0.01)
        label_spacing = int(self.screen_width * 0.005)
        self.net_box = Gtk.Box()
        net_label = Gtk.Label("Model Path:")
        net_button = Gtk.Button("Select Path")

        self.net_box.pack_start(net_label, False, False, label_spacing)
        self.net_box.pack_start(net_button, True, False, 0)
        self.dbox.pack_start(self.net_box, False, False, spacing)

        net_button.connect('clicked', self.__net_button_clicked)
    
    def set_files_loaded(self):
        spacing = int(self.screen_height * 0.02)
        scroll_height = int(self.screen_height * 0.12)

        self.net_scw = Gtk.ScrolledWindow(None, None)
        self.net_scw.set_name("NETSCROLLWINDOW")
        self.net_scw.set_size_request(0, scroll_height)
        self.net_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.dbox.pack_start(self.net_scw, False, False, spacing)

        self.net_listmodel = Gtk.ListStore(str)
        view = Gtk.TreeView(model = self.net_listmodel)
        view.set_name("NETVIEW")
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn("Files loaded", renderer_text, text=0)
        view.append_column(columntext)

        self.net_scw.add(view)

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
    
    def get_darknet(self):
        return self.DBBT_net

    def get_net_labels(self):
        return self.net_labels

    def get_net_box(self):
        return self.dbox




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

        print('[INFO]: NEURAL DATA load finished')

    def make_inference(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_rsz = cv2.resize(image_rgb, (self.net_width,self.net_height))
        darknet.copy_image_from_bytes(self.darknet_image, rgb_rsz.tobytes())
        detections = darknet.detect_image(self.net, self.meta_net, self.darknet_image, thresh=0.25)
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
        names_file = open(names, 'r')
        line_names = names_file.readlines()
        for line_name in line_names:
            line_name = line_name.strip('\n')
            names_list.append(line_name)
    
        self.metafile.close()
        names_file.close()

        return names_list


class LabelClasses():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.box_height = int(self.screen_height * 0.3)
        self.box_width = int(self.screen_width*0.178)
        self.scw_width = int(self.box_width/3)
        
        self.labelsbox = Gtk.Box()
        self.labelsbox.set_size_request(0, self.box_height)
        self.set_ImageLabels()
        self.set_WorkingLabels()
        self.set_NetLabels()

    def set_ImageLabels(self):
        image_scw = Gtk.ScrolledWindow(None, None)
        image_scw.set_name("NETSCROLLWINDOW")
        image_scw.set_size_request(self.scw_width, self.box_height)
        image_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.imagelistmodel = Gtk.ListStore(str)
        self.imageview = Gtk.TreeView(model = self.imagelistmodel)
        self.imageview.set_name('NETVIEW')
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('Image Labels', renderer_text, text = 0)
        self.imageview.append_column(columntext)

        image_scw.add(self.imageview)

        self.labelsbox.pack_start(image_scw, False, False, 0)

    def set_WorkingLabels(self):
        working_scw = Gtk.ScrolledWindow(None, None)
        working_scw.set_name("NETSCROLLWINDOW")
        working_scw.set_size_request(self.scw_width, self.box_height)
        working_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.workinglistmodel = Gtk.ListStore(str)
        self.workingview = Gtk.TreeView(model = self.workinglistmodel)
        self.workingview.set_name('NETVIEW')
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('Working Labels', renderer_text, text = 0)
        self.workingview.append_column(columntext)

        working_scw.add(self.workingview)

        self.labelsbox.pack_start(working_scw, False, False, 0)
        
    def set_NetLabels(self):
        net_scw = Gtk.ScrolledWindow(None, None)
        net_scw.set_name("NETSCROLLWINDOW")
        net_scw.set_size_request(self.scw_width, self.box_height)
        net_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.netlistmodel = Gtk.ListStore(str)
        self.netview = Gtk.TreeView(model = self.netlistmodel)
        self.netview.set_name('NETVIEW')
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('Net Labels', renderer_text, text = 0)
        self.netview.append_column(columntext)

        net_scw.add(self.netview)

        self.labelsbox.pack_start(net_scw, False, False, 0)

    def return_NetLabelsBox(self):
        return self.labelsbox


class ImageResources():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.set_scrollImages()

    
    def set_scrollImages(self):
        scroll_height = int(self.screen_height * 0.416)
        self.image_scw = Gtk.ScrolledWindow(None, None)
        self.image_scw.set_name('NETSCROLLWINDOW')
        self.image_scw.set_size_request(0, scroll_height)
        self.image_scw.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.list_images = Gtk.ListStore(str)
        self.image_view = Gtk.TreeView(model = self.list_images)
        self.image_view.set_name('NETVIEW')
        renderer_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('Images', renderer_text, text = 0)
        self.image_view.append_column(columntext)

        self.selection = self.image_view.get_selection()
        self.selection.connect('changed', self.__on_changed)

        self.image_scw.add(self.image_view)
    
    def set_files(self, image_folder_path):
        self.current_image_folder_path = image_folder_path
        files = listdir(image_folder_path)
        for image_file in files:
            self.list_images.append([image_file])
        self.image_view.set_cursor(0)
        self.image_scw.show_all()
        
        return files

    def set_view_cursor(self, index):
        self.image_view.set_cursor(index)

    def __on_changed(self, selection):
        model, iter_ = selection.get_selected()
        #print(model[iter_][0])
        
    def return_image_resources_box(self):
        return self.image_scw


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
            return "None", self.current_index
        return self.collection[self.current_index], self.current_index
    
    def prev(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            return "None", self.current_index
        return self.collection[self.current_index], self.current_index


class DrawingEvents():
    def __init__(self, darea):
        self.darea = darea
        self.darea_width = self.darea.get_allocation().width
        self.darea_height = self.darea.get_allocation().height
        
        self.rectangles = []
        self.current_rectangle = []

        self.darea.connect('draw', self.__on_draw)

    def set_drawing_image(self, filename):
        self.rectangles = []
        image = cv2.imread(filename)
        self.current_pix = self.im2pixbuf(image)
        self.darea.queue_draw()

    
    def im2pixbuf(self, image):
        #if self.DBBT_net is not None:
        #    detections = self.DBBT_net.make_inference(image)
        #    self.__draw_boxes(detections, image)
        image = cv2.resize(image, (self.darea_width, self.darea_height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = image.tobytes()
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, self.darea_width, self.darea_height, self.darea_width*3)
        return pix

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