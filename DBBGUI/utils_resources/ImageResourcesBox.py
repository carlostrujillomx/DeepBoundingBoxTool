import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

from os import listdir

class ImageResources():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.scw_width = int(self.screen_height * 0.3)
        self.box_height = int(self.screen_height * 0.416)

        self.set_ImagesWindow()

    def set_ImagesWindow(self):
        scroll_height = int(self.screen_height * 0.455)
        self.scrollWindow = Gtk.ScrolledWindow(None, None)
        self.scrollWindow.set_name('NETSCROLLWINDOW')
        self.scrollWindow.set_size_request(0, scroll_height)
        self.scrollWindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.listmodel = Gtk.ListStore(str)
        self.view = Gtk.TreeView(model = self.listmodel)
        self.view.set_name('NETVIEW')
        
        renderText = Gtk.CellRendererText()
    
        columntext = Gtk.TreeViewColumn('Images', renderText, text = 0)

        self.view.append_column(columntext)

        self.scrollWindow.add(self.view)

        self.selection = self.view.get_selection()
        self.selection.connect('changed', self.__on_changed)

    def update_files(self, folder_path):
        self.current_folder_path = folder_path
        files = listdir(self.current_folder_path)

        for image_file in files:
            self.listmodel.append([image_file])

        self.view.set_cursor(0)
        self.scrollWindow.show_all()

    def set_view_cursor(self, index):
        self.view.set_cursor(index)

    def __on_changed(self, selection):
        model, it = selection.get_selected()
        #pending set cursor
    
    def return_image_resources_box(self):
        return self.scrollWindow



