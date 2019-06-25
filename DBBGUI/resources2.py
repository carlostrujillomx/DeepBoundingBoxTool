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
import random
import colorsys

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
        
        self.DrawingImage = DrawingEvents(self.darea)
        
        collection = self.ImageResource.set_files(image_folder_path)
        self.images_iterator = bi_iterator(collection)

        filename = image_folder_path+'/'+collection[0]
        self.DrawingImage.wrap_labels_space(self.LabelResource)
        self.DrawingImage.set_drawing_image(filename)

        self.DBBnet = self.DboxResource.get_darknet()
        self.DBBnet_labels = self.DboxResource.get_net_labels()
        
        self.DrawingImage.wrap_darknet(self.DBBnet)
        self.DrawingImage.generate_label_colors(self.DBBnet_labels)
        
        self.LabelResource.wrap_drawing_event(self.DrawingImage)
        self.LabelResource.update_net_labels(self.DBBnet_labels)


    def next_image(self):
        if self.image_folder is not None:
            file_, index = self.images_iterator.next()
            if file_ is not "None":
                filename = self.image_folder+'/'+file_
                labels = self.DrawingImage.set_drawing_image(filename)
                obj_detections = self.DrawingImage.set_drawing_image(filename)
                self.ImageResource.set_view_cursor(index)
                self.LabelResource.update_ImageLabels(obj_detections)
        
    def prev_image(self):
        if self.image_folder is not None:
            file_, index = self.images_iterator.prev()
            if file_ is not "None":
                filename = self.image_folder+'/'+file_
                labels = self.DrawingImage.set_drawing_image(filename)
                self.ImageResource.set_view_cursor(index)

    def create_rectbox(self):
        self.DrawingImage.create_rectbox()

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
        
        self.current_key = None
        self.current_iter_ = None

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

        self.imagelistmodel = Gtk.ListStore(int,str)
        self.imageview = Gtk.TreeView(model = self.imagelistmodel)
        self.imageview.set_name('NETVIEW')
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property('editable', True)
        columntext = Gtk.TreeViewColumn('id', renderer_text, text = 0)
        renderer_text2 = Gtk.CellRendererText()
        renderer_text2.set_property('editable', True)
        columntext2 = Gtk.TreeViewColumn('label', renderer_text2, text = 1)
        
        self.imageview.append_column(columntext)
        self.imageview.append_column(columntext2)

        image_scw.add(self.imageview)

        self.labelsbox.pack_start(image_scw, False, False, 0)

        self.imageview.connect('key-press-event', self.__on_key_press_event)
        selection = self.imageview.get_selection()
        selection.connect('changed', self.__image_view_changed)

        renderer_text2.connect('edited', self.__set_text_edited)
        
    def update_ImageLabels(self, object_detections):
        self.imagelistmodel.clear()
        for key in object_detections:
            label, box, color, flag = object_detections.get(key)
            self.imagelistmodel.append([key,label])
        self.imageview.show_all()
        selection = self.imageview.get_selection()
    
    def __image_view_changed(self, selection):
        model, iter_ = selection.get_selected()
        self.current_iter_ = iter_
        if iter_ is not None:
            key = model[iter_][0]
            self.current_key = key
            self.drawing_image.edit_selection(key)
    
    def __on_key_press_event(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        #print('event:',e.state, 'key val, name:', e.keyval, Gdk.keyval_name(e.keyval))
        if val_name == 'Delete':
            self.drawing_image.delete_selection(self.current_key)
            self.imagelistmodel.remove(self.current_iter_)
            self.imageview.show_all()

    def __set_text_edited(self, w,p,text):
        self.imagelistmodel[p][1] = text
        self.drawing_image.modify_selection(self.current_key, text)

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
        
        wlabels_file = open('wlabels.txt', 'r')
        lines = wlabels_file.readlines()
        self.labels = []
        for line in lines:
            line = line.strip('\n')
            self.workinglistmodel.append([line])
            self.labels.append(line)
        
        self.workingview.show_all()
        

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

    def update_net_labels(self, labels):
        for label in labels:
            self.netlistmodel.append([label])
        self.netview.show_all()

    def wrap_drawing_event(self, drawing_image):
        self.drawing_image = drawing_image
        self.drawing_image.wrap_labels(self.labels)

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
        self.current_pix = None
        self.darea_width = self.darea.get_allocation().width
        self.darea_height = self.darea.get_allocation().height

        self.DBBT_net = None
        self.net_colors = {}
        self.rectangles = []
        self.current_rectangle = []
        self.object_detections = {}
        self.draw_cliked = False
        self.draw_flag = False

        self.darea.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)
        self.darea.connect('draw', self.__on_draw)
        self.darea.connect('motion-notify-event', self.__draw_motion)
        self.darea.connect("button-press-event", self.__drawing_clicked)

        self.menuItem = labelPopover()
        self.menuItem.wrap_drawing(self)

    def set_drawing_image(self, filename):
        self.rectangles = []
        image = cv2.imread(filename)
        self.current_pix = self.im2pixbuf(image)
        self.darea.queue_draw()
        return self.object_detections

    def im2pixbuf(self, image):
        self.object_detections = {}
        if self.DBBT_net is not None:
            detections = self.DBBT_net.make_inference(image)
            i = 0
            for detects in detections:
                label = detects[0].decode('utf-8')
                box = detects[2]
                fit_box = self.__get_fit_size(image, box)
                color = self.net_colors.get(label)
                self.object_detections.update({i:[label,fit_box,color, False]})
                i += 1
        image = cv2.resize(image, (self.darea_width, self.darea_height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = image.tobytes()
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, self.darea_width, self.darea_height, self.darea_width*3)
        return pix

    def generate_label_colors(self, labels):
        print('number of labels:', len(labels))
        n = len(labels)
        for i in range(n):
            rgb_color = colorsys.hsv_to_rgb(random.randint(0,256)/255, random.randint(0,256)/255, random.randint(120,256)/255)
            self.net_colors.update({labels[i]:rgb_color})

    def edit_selection(self, iter_):
        for key in self.object_detections:
            label, box, color, flag = self.object_detections.get(key)
            self.object_detections.update({key:[label, box, color, False]})
        self.edit_index = iter_
        label, box, color, flag = self.object_detections.get(iter_)
        self.object_detections.update({iter_:[label, box, color, True]})
        self.darea.queue_draw()

    def delete_selection(self, iter_):
        self.object_detections.pop(iter_, None)
        self.darea.queue_draw()

    def modify_selection(self, key, new_label):
        label, box, color, flag = self.object_detections.get(key)
        self.object_detections.update({key:[new_label, box, color, flag]})
    
    def add_object(self, label):
        box = self.current_rectangle[0]
        color = self.net_colors.get(label)
        n = len(self.object_detections)
        self.object_detections.update({n:[label,box,color, False]})
        self.darea.queue_draw()
        self.update_labels()

    def __on_draw(self, w, cr):
        if self.current_pix is not None:
            Gdk.cairo_set_source_pixbuf(cr, self.current_pix, 0, 0)
            cr.paint()
            if len(self.object_detections) == 0:
                if len(self.current_rectangle) > 0:
                    cr.rectangle(self.current_rectangle[0][0], self.current_rectangle[0][1], self.current_rectangle[0][2], self.current_rectangle[0][3])
                    cr.stroke()
            else:
                if len(self.current_rectangle) > 0:
                    cr.set_source_rgba(1,1,1,0.7)
                    cr.rectangle(self.current_rectangle[0][0], self.current_rectangle[0][1], self.current_rectangle[0][2], self.current_rectangle[0][3])
                    cr.fill()
                    cr.set_line_width(3)
                    cr.rectangle(self.current_rectangle[0][0], self.current_rectangle[0][1], self.current_rectangle[0][2], self.current_rectangle[0][3])
                    cr.stroke()
                    
                for key in self.object_detections:
                    label, box, color, flag = self.object_detections.get(key)
                    x,y,w,h = box
                    r,g,b = color
                    transparency = flag == True and 0.8 or 0.2
                    cr.set_source_rgba(r,g,b,transparency)
                    cr.rectangle(x,y,w,h)
                    cr.fill()
                    cr.set_source_rgb(r,g,b)
                    cr.set_line_width(3)
                    cr.rectangle(x,y,w,h)
                    cr.stroke()
    
    def __get_fit_size(self, image, box):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        w_orig = self.darea_width
        h_orig = self.darea_height
        w_net = self.DBBT_net.net_width
        h_net = self.DBBT_net.net_height

        x_c = x/w_net
        y_c = y/h_net
        w_r = w/w_net
        h_r = h/h_net
        x_r = x_c-w_r/2
        y_r = y_c-h_r/2

        x_fit = int(x_r*w_orig)
        y_fit = int(y_r*h_orig)
        w_fit = int(w_r*w_orig)
        h_fit = int(h_r*h_orig)

        return x_fit, y_fit, w_fit, h_fit

    def create_rectbox(self):
        self.draw_flag = True

    def __draw_motion(self, w, e):
        if self.draw_cliked:
            x,y,w,h = self.current_rectangle[0]
            w = e.x - x
            h = e.y - y
            self.current_rectangle.insert(0, [x,y, w, h])
            self.darea.queue_draw()
        
    def __drawing_clicked(self, w, e):
        if self.draw_flag:
            self.draw_cliked = not self.draw_cliked
        
        if self.draw_cliked:
            self.current_rectangle.clear()
            self.current_rectangle.append([e.x, e.y, 0,0])
        elif not self.draw_cliked and self.draw_flag:
            x,y,w,h = self.current_rectangle[0]
            w = e.x - x 
            h = e.y - y
            self.current_rectangle.insert(0, [x,y,w,h])
            self.draw_flag = False
            self.menuItem.show_menu(self.darea)
            self.darea.queue_draw()
            
    def wrap_darknet(self, dbbtnet):
        self.DBBT_net = dbbtnet
    
    def wrap_labels_space(self, labelsResource):
        self.labelsResource = labelsResource

    def clear_current_rectangle(self):
        self.current_rectangle.clear()
    
    def update_labels(self):
        self.labelsResource.update_ImageLabels(self.object_detections)
    
    def wrap_labels(self, labels):
        self.menuItem.wrap_labels(labels)


class labelPopover():
    def __init__(self):
        self.label_popover = Gtk.Popover()
        self.label_popover.set_name('labelPopover')
        self.popoverBox = Gtk.Box()

        self.label_entry = Gtk.Entry()
        self.label_entry.set_text('label')
        save_button = Gtk.Button('Save')
        self.popoverBox.pack_start(self.label_entry, False, False, 0)
        self.popoverBox.pack_start(save_button, False, False, 0)

        self.label_popover.add(self.popoverBox)
        
        save_button.connect('clicked', self.__button_popdown)
        #self.label_entry.connect('key-press-event', self.__press_popdown)
        self.label_entry.connect('key-release-event', self.__entry_key_popdown)

    def wrap_drawing(self, drawingImage):
        self.drawingImage = drawingImage
    
    def show_menu(self, widget):
        self.label_popover.set_relative_to(widget)
        self.label_popover.show_all()
    
    def __button_popdown(self, button):
        label = self.label_entry.get_text()
        self.drawingImage.add_object(label)
        self.drawingImage.clear_current_rectangle()
        self.label_popover.hide()
        self.drawingImage.darea.queue_draw()

    def __entry_key_popdown(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        if val_name == 'Return':
            label = self.label_entry.get_text()
            self.drawingImage.add_object(label)
            self.drawingImage.clear_current_rectangle()
            self.label_popover.hide()
            self.drawingImage.darea.queue_draw()
        else:
            self.suggestion.set_suggestion(self.label_entry)

    def wrap_labels(self, labels):
        self.suggestion = SecondaryPopOver(labels)

class SecondaryPopOver():
    def __init__(self, labels):
        self.labels = labels
        self.suggestion_popover = Gtk.Popover()
        self.suggestion_popover.set_name('labelPopover')
        self.suggestion_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        
        self.suggestion_popover.set_position(Gtk.PositionType.BOTTOM)
        self.suggestion_popover.set_modal(False)

        self.suglistmodel = Gtk.ListStore(str)
        self.sugview = Gtk.TreeView(model = self.suglistmodel)
        self.sugview.set_name('NETVIEW')
        render_text = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('sug', render_text, text = 0)
        self.sugview.append_column(columntext)

        self.suggestion_popover.set_size_request(200,500)
        self.suggestion_box.pack_start(self.sugview, True, True, 0)
        self.suggestion_popover.add(self.suggestion_box)
        #self.suggestion_box.pack_start(self.sugview, False, False, 0)
        #selection = self.sugview.get_selection()
        #selection.connect('changed', )

    def set_suggestion(self, widget):
        self.suglistmodel.clear()
        print('sug1:', len(self.suglistmodel))
        
        #self.suggestion_popover.hide()
        widget_text = widget.get_text()
        n = len(widget_text)
        print('key-pressed:', widget_text, n)
        self.suggestion_popover.set_relative_to(widget)
        i = 0
        for label in self.labels:
            t1 = label[:n]
            if t1 == widget_text: 
                print('suggestion:',label, type(label))
                self.suglistmodel.insert(i, [label])
                #self.suglistmodel.append([label])
                i+=1

        print('sug2:', len(self.suglistmodel))
        self.suggestion_popover.show()
        self.sugview.show()
        self.suggestion_box.show()
        
        #self.sugview.show()
        #self.suggestion_popover.show_all()
        #self.suggestion_box.show_all()
        #self.sugview.show_all()

    
