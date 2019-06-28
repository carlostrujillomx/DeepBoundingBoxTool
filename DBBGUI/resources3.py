import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
import cairo

from DBBGUI.utils_resources import DLBox, LabelsWindow, ImageResourcesBox, DrawingResource


import os
from os import listdir

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
        
        self.DLFiles = DLBox.DeepLearningBox(self.window)
        DLFilesBox = self.DLFiles.return_netBox()
        self.resource_box.pack_start(DLFilesBox, False, False, 0)

        self.LWindow = LabelsWindow.LabelClasses(self.window)
        LWindowBox = self.LWindow.return_NetLabelsBox()
        self.resource_box.pack_start(LWindowBox, False, False, spacing)

        self.IResources = ImageResourcesBox.ImageResources(self.window)
        IRBox = self.IResources.return_image_resources_box()
        self.resource_box.pack_start(IRBox, False, False, 0)

        self.DLFiles.wrap_LWindow(self.LWindow)

    def set_drawingResource(self, darea, dw, dh):
        self.drawingImage = DrawingResource.DrawingEvents(darea, dw, dh)
        self.DLFiles.wrap_drawing(self.drawingImage)
        self.drawingImage.generate_working_colors(self.LWindow.get_workingLabels())
        self.drawingImage.wrap_LabelsWindow(self.LWindow)
        self.LWindow.wrap_drawing(self.drawingImage)

    def  update_Imagefiles_resources(self, path):
        self.image_folder = path
        self.IResources.update_files(path)
        self.imageIterator = bi_iterator(path)
        filename, index = self.imageIterator.current()
        self.IResources.set_view_cursor(index)
        self.drawingImage.set_drawing(filename)
        
    def next_image(self):
        if self.image_folder is not None:
            filename, index = self.imageIterator.next()
            if filename is not "None":
                self.IResources.set_view_cursor(index)
                self.drawingImage.set_drawing(filename)
        
    def prev_image(self):
        if self.image_folder is not None:
            filename, index = self.imageIterator.prev()
            if filename is not "None":
                self.IResources.set_view_cursor(index)
                self.drawingImage.set_drawing(filename)
    
    def create_rectbox(self):
        self.drawingImage.create_rectbox()

    def delete_rectbox(self):
        self.drawingImage.clear_current_rectangle()

    def save_detections(self):
        self.drawingImage.save_detections()

    def set_save_folder(self, save_path):
        self.drawingImage.set_save_folder(save_path)

    def return_resource_box(self):
        return self.resource_box

class bi_iterator():
    def __init__(self, path):
        self.collection = []
        files = listdir(path)
        for file_ in files:
            self.collection.append(path+'/'+file_)
        self.index = 0
        self.max_index = len(self.collection)
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

    def current(self):
        return self.collection[self.current_index], self.current_index
    



