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
        self.darea.connect('motion-notify-event', self.__draw_motion)
        self.darea.connect("button-press-event", self.__drawing_clicked)
        self.menuItem = LabelPop()

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
        ratio = n/3
        step = 255/ratio

        h = 0
        s = 255
        v = 255
        
        for i in range(n):
            color = colorsys.hsv_to_rgb(h/255,s/255,v/255)
            self.net_colors.update({labels[i]: color})
            h += step*3
            if h >= 255:
                h = 0
                s -= step
                if s <= 0:
                    s = 255
                    v -= step
                    if  v<= 0:
                        v = 255
    
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
        self.LWindow.update_ImageLabels(self.objects_detected)
                
    def __im2pixbuf(self, image):
        image = cv2.resize(image, (self.darea_width, self.darea_height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = image.tobytes()
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, self.darea_width, self.darea_height, self.darea_width*3)
        return pix

    def generate_working_colors(self, labels):
        n = len(labels)
        ratio = n/3
        step = 255/ratio

        h = 0
        s = 255
        v = 255
        
        for i in range(n):
            color = colorsys.hsv_to_rgb(h/255,s/255,v/255)
            self.w_colors.update({labels[i]: color})
            h += step*3
            if h >= 255:
                h = 0
                s -= step
                if s <= 0:
                    s = 255
                    v -= step
                    if  v<= 0:
                        v = 255
        self.menuItem.wrap_labels(labels)
        self.menuItem.wrap_drawing(self)
        #print(self.w_colors)

    def update_labels(self):
        self.LWindow.update_ImageLabels(self.objects_detected)

    def edit_view_selection(self, it):
        for key in self.objects_detected:
            label, box, color, flag = self.objects_detected.get(key)
            self.objects_detected.update({key:[label, box, color, False]})
        self.edit_index = it

        label, box, color, flag = self.objects_detected.get(it)
        self.objects_detected.update({it:[label, box, color, True]})
        self.darea.queue_draw()

    def edit_selection(self, edit_key, edit_label):
        for key in self.objects_detected:
            label, box, color, flag = self.objects_detected.get(key)
            self.objects_detected.update({key:[label, box, color, False]})
        self.edit_index = edit_key

        label, box, color, flag = self.objects_detected.get(edit_key)
        color = self.w_colors.get(edit_label)
        self.objects_detected.update({edit_key:[edit_label, box, color, True]})
        self.darea.queue_draw()
    
    def delete_selection(self, iter_):
        self.objects_detected.pop(iter_, None)
        self.darea.queue_draw()
    
    def modify_selection(self, key, new_label):
        label, box, color, flag = self.objects_detected.get(key)
        self.objects_detected.update({key:[new_label, box, color, flag]})
    
    def add_object(self, label):
        box = self.current_rectangle[0]
        color = self.w_colors.get(label) #change with working colors
        n = len(self.objects_detected)
        self.objects_detected.update({n:[label,box,color, False]})
        self.darea.queue_draw()
        self.update_labels()

    def create_rectbox(self):
        self.draw_flag = True
    
    def clear_current_rectangle(self):
        self.current_rectangle.clear()
        self.darea.queue_draw()

    def __key_pressed(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        print('val name:', val_name)

    def __draw_motion(self, w, e):
        if self.draw_clicked:
            x,y,w,h = self.current_rectangle[0]
            w = e.x - x
            h = e.y - y
            self.current_rectangle.insert(0, [x,y, w, h])
            self.darea.queue_draw()
        
    def __drawing_clicked(self, w, e):
        if self.draw_flag:
            self.draw_clicked = not self.draw_clicked
        
        if self.draw_clicked:
            self.current_rectangle.clear()
            self.current_rectangle.append([e.x, e.y, 0,0])
        elif not self.draw_clicked and self.draw_flag:
            x,y,w,h = self.current_rectangle[0]
            w = e.x - x 
            h = e.y - y
            self.current_rectangle.insert(0, [x,y,w,h])
            self.draw_flag = False
            self.menuItem.show_menu(self.darea)
            self.darea.queue_draw()
    
    def save_detections(self):
        obj2save = []
        for key in self.objects_detected:
            for label in self.w_colors:
                nlabel, box, color, f = self.objects_detected.get(key)
                if nlabel == label:
                    obj2save.append(nlabel)
        print('labels saved:', obj2save)

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
    def __init__(self):
        self.LPopover = Gtk.Popover()
        self.LPopover.set_name('labelPopover')
        self.PopoverBox = Gtk.Box()

        self.LEntry = Gtk.Entry()
        self.LEntry.set_text('Label')
        
        save_button = Gtk.Button('Save')

        self.PopoverBox.pack_start(self.LEntry, False, False, 0)
        self.PopoverBox.pack_start(save_button, False, False, 0)

        self.LPopover.add(self.PopoverBox)

        save_button.connect('clicked', self.__save_button_clicked)
        self.LEntry.connect('key-release-event', self.__entry_key_pressed)
        

    def __popover_key(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        print('val_name:', val_name)
        
    def wrap_drawing(self, drawingImage):
        self.drawingImage = drawingImage

    def wrap_labels(self, labels):
        self.SuggestionPopover = SecondaryPopOver(labels, self.LEntry)

    def show_menu(self, widget):
        self.LPopover.set_relative_to(widget)
        self.LPopover.show_all()

    def __save_button_clicked(self, button):
        label = self.LEntry.get_text()
        self.drawingImage.add_object(label)
        self.drawingImage.clear_current_rectangle()
        self.LPopover.hide()
        self.drawingImage.darea.queue_draw()
    
    def __entry_key_pressed(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        print('val_name:', val_name)
        if val_name == 'Return':
            label = self.LEntry.get_text()
            self.drawingImage.add_object(label)
            self.drawingImage.clear_current_rectangle()
            self.LPopover.hide()
            self.drawingImage.darea.queue_draw()
        else:
            self.SuggestionPopover.set_suggestion()


class SecondaryPopOver():
    def __init__(self, labels, entry):
        self.entry = entry
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
        selection = self.sugview.get_selection()
        selection.connect('changed', self.__op_selected)

    def set_suggestion(self):
        self.suglistmodel.clear()
        print('sug1:', len(self.suglistmodel))
        
        #self.suggestion_popover.hide()
        #widget_text = widget.get_text()
        widget_text = self.entry.get_text()
        n = len(widget_text)
        print('key-pressed:', widget_text, n)
        self.suggestion_popover.set_relative_to(self.entry)
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
        
    def __op_selected(self, selection):
        model, self.it = selection.get_selected()
        if self.it is not None:
            label = model[self.it][0]
            self.entry.set_text(label)
            print('label selected:', label)
