import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

from os import listdir

class DeepLearningBox():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.dbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.set_net_box()
        self.set_scrollWindowFiles()

    def set_net_box(self):
        spacing = int(self.screen_height * 0.01)
        label_spacing = int(self.screen_width * 0.005)
        self.net_box = Gtk.Box()
        net_label = Gtk.Label("Model Path:")
        net_button = Gtk.Button("Select Path")

        self.net_box.pack_start(net_label, False, False, label_spacing)
        self.net_box.pack_start(net_button, False, False, 0)
        
        self.dbox.pack_start(self.net_box, False, False, spacing)

        net_button.connect('clicked', self.__net_button_clicked)
    
    def set_scrollWindowFiles(self):
        spacing = int(self.screen_height * 0.02)
        scroll_height = int(self.screen_height * 0.14)

        scrollBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.scrollWindow = Gtk.ScrolledWindow(None, None)
        self.scrollWindow.set_name('NETSCROLLWINDOW')
        self.scrollWindow.set_size_request(0, scroll_height)
        self.scrollWindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        
        self.listmodel = Gtk.ListStore(str)
        view = Gtk.TreeView(model = self.listmodel)
        view.set_name('NETVIEW')
        renderText = Gtk.CellRendererText()
        columnText = Gtk.TreeViewColumn('Files Loaded', renderText, text = 0)
        view.append_column(columnText)

        self.scrollWindow.add(scrollBox)
        scrollBox.pack_start(view, True, True, 0)

        self.dbox.pack_start(self.scrollWindow, False, False, spacing)

    def wrap_drawing(self, drawingEvent):
        self.drawingEvent = drawingEvent

    def wrap_LWindow(self, LWindow):
        self.LWindow = LWindow

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
            self.listmodel.append([net_file])
        self.scrollWindow.show_all()

        self.drawingEvent.set_DBBNet(configPath, weightPath, metaPath)
        labels = self.drawingEvent.DBB_Net.load_classes()
        self.LWindow.update_net_labels(labels)
        self.drawingEvent.generate_net_colors(labels)

    def return_netBox(self):
        return self.dbox