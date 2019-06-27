import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
import cairo

import cv2
import math
import random
import colorsys

from DBBGUI import darknet
import os

class DrawingEvents():
    def __init__(self, darea, darea_width, darea_height):
        self.darea = darea
        self.darea_width = darea_width 
        self.darea_height = darea_height

        self.pix = None

        self.DBB_Net = None
        self.net_colors = {}
        self.w_colors = {}
        self.objects_detected = {}

        self.current_rectangle = []
        self.draw_clicked = False
        self.draw_flag = False

        self.darea.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)
        self.darea.connect('draw', self.__on_draw)
        #self.darea.connect('motion-notify-event', self.__draw_motion)
        #self.darea.connect("button-press-event", self.__drawing_clicked)

    def set_DBBNet(self, configPath, weightPath, metaPath):
        self.DBB_Net = DARKNET(configPath, weightPath, metaPath)

    def __get_fit_size(self, image, box):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        w_orig = self.darea_width
        h_orig = self.darea_height
        w_net = self.DBB_Net.net_width
        h_net = self.DBB_Net.net_height

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
    
    def generate_net_colors(self, labels):
        n = len(labels)
        r = int(n/3)
        h = 0
        s = 100
        v = 100

        step = 255/r

        for i in range(n):
            if i < r:
                h += step
            elif i < r*2:
                h += step
                s = 180
                v = 180
            elif i <  r*3:
                h += step
                s = 255
                v = 255
            if h >= 255:
                h = 0
            color = colorsys.hsv_to_rgb(h,s,v)
            self.net_colors.update({labels[i]:color})
        print(self.net_colors)

    def __on_draw(self, w, cr):
        if self.pix is not None:
            Gdk.cairo_set_source_pixbuf(cr, self.pix, 0, 0)
            cr.paint()
            if len(self.objects_detected) == 0:
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
                    
                for key in self.objects_detected:
                    label, box, color, flag = self.objects_detected.get(key)
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

    def wrap_LabelsWindow(self, LWindow):
        self.LWindow = LWindow

    def set_drawing(self, filename):
        self.objects_detected = {}
        image = cv2.imread(filename)
        if self.DBB_Net is not None:
            detections = self.DBB_Net.make_inference(image)
            i = 0
            for detect in detections:
                label = detect[0].decode('utf-8')
                box = detect[2]
                fit_box = self.__get_fit_size(image, box)
                color = self.net_colors.get(label)
                self.objects_detected.update({i:[label, fit_box, color, False]})
                i += 1
        self.pix = self.__im2pixbuf(image)
        self.darea.queue_draw()
                
    def __im2pixbuf(self, image):
        image = cv2.resize(image, (self.darea_width, self.darea_height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = image.tobytes()
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, self.darea_width, self.darea_height, self.darea_width*3)
        return pix

    def generate_working_colors(self, labels):
        n = len(labels)
        r = int(n/3)
        h = 0
        s = 100
        v = 100

        step = 255/r

        for i in range(n):
            if i < r:
                h += step
            elif i < r*2:
                h += step
                s = 180
                v = 180
            elif i <  r*3:
                h += step
                s = 255
                v = 255
            if h >= 255:
                h = 0
            color = colorsys.hsv_to_rgb(h,s,v)
            self.w_colors.update({labels[i]:color})
        
        print(self.w_colors)

    def edit_selection(self, it):
        for key in self.objects_detected:
            label, box, color, flag = self.objects_detected.get(key)
            self.objects_detected.update({key:[label, box, color, False]})
        self.edit_index = it
        label, box, color, flag = self.objects_detected.get(it)
        self.objects_detected.update({it:[label, box, color, True]})
        self.darea.queue_draw()
    
    def delete_selection(self, iter_):
        self.objects_detected.pop(iter_, None)
        self.darea.queue_draw()
    
    def modify_selection(self, key, new_label):
        label, box, color, flag = self.objects_detected.get(key)
        self.objects_detected.update({key:[new_label, box, color, flag]})
    
    def add_object(self, label):
        box = self.current_rectangle[0]
        color = self.net_colors.get(label) #change with working colors
        n = len(self.objects_detected)
        self.objects_detected.update({n:[label,box,color, False]})
        self.darea.queue_draw()
        #self.update_labels()

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

class LabelPop():
    def __init__(self, window):
        self.LPopover = Gtk.Popover()
        self.LPopover.set_name('labelPopover')
        self.PopoverBox = Gtk.Box()

        self.LEntry = Gtk.Entry()
        self.LEntry.set_text('Label')
        
        save_button = Gtk.Button('Save')

        self.PopoverBox.pack_start(self.LEntry, False, False, 0)
        self.PopoverBox.pack_start(save_button, False, False, 0)

        self.LPopover.add(self.PopoverBox)

        #save_button.connect('clicked', self.__save_button_clicked)
        #self.LEntry.connect('key-press-event', self.__entry_key_pressed)
    
