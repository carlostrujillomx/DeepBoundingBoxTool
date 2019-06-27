import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

class LabelClasses():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.LabelsBox = Gtk.Box()

        self.CFLabels = CurrentFileLabels(self.window)
        CFLabelsWindow = self.CFLabels.return_currentFileWindow()

        self.WLabels = WorkingLabels(self.window)
        WLabelsWindow = self.WLabels.return_workingLabelsWindow()

        self.NLabels = NetLabels(self.window)
        NLabelsWindow = self.NLabels.return_NetLabelsWindow()

        self.LabelsBox.pack_start(CFLabelsWindow, False, False, 0)
        self.LabelsBox.pack_start(WLabelsWindow, False, False, 0)
        self.LabelsBox.pack_start(NLabelsWindow, False, False, 0)

    def wrap_drawing(self, drawingEvent):
        self.CFLabels.wrap_drawing(drawingEvent)
        self.WLabels.wrap_drawing(drawingEvent)
        
    def update_ImageLabels(self, objects_detected):
        self.CFLabels.update_ImageLabels(objects_detected)

    def get_workingLabels(self):
        return self.WLabels.get_labels()

    def update_net_labels(self, labels):
        self.NLabels.update_net_labels(labels)

    def return_NetLabelsBox(self):
        return self.LabelsBox

class CurrentFileLabels():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.box_height = int(self.screen_height * 0.3)
        self.box_width = int(self.screen_width*0.178)
        self.scw_width = int(self.box_width/3)

        self.setImageLabels()
        
    def setImageLabels(self):
        self.scrollWindow = Gtk.ScrolledWindow(None, None)
        self.scrollWindow.set_name('NETSCROLLWINDOW')
        self.scrollWindow.set_size_request(self.scw_width, self.box_height)
        self.scrollWindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.listmodel = Gtk.ListStore(str, int)
        self.view = Gtk.TreeView(model = self.listmodel)
        self.view.set_name('NETVIEW')
        
        renderText = Gtk.CellRendererText()
        renderText.set_property('editable', True)
        
        columntext = Gtk.TreeViewColumn('Label', renderText, text = 0)

        self.view.append_column(columntext)

        self.scrollWindow.add(self.view)

        selection = self.view.get_selection()
        selection.connect('changed', self.__image_view_changed)

        self.view.connect('key-press-event', self.__on_key_press_event)
        renderText.connect('edited', self.__set_text_edited)
        

    def update_ImageLabels(self, objects_detected):
        self.listmodel.clear()
        for key in objects_detected:
            label, box, color, flag = objects_detected.get(key)
            self.listmodel.append([label, key])
        self.view.show_all()
        
        selection = self.view.get_selection()
    
    def wrap_drawing(self, drawingEvent):
        self.drawingEvent = drawingEvent

    def __image_view_changed(self, selection):
        model, self.it, = selection.get_selected()
        if self.it is not None:
            self.key = int(model[self.it][1])
            self.drawingEvent.edit_view_selection(self.key)
            #self.drawingEvent.edit_selection(self.key)
    
    def __on_key_press_event(self, w, e):
        val_name = Gdk.keyval_name(e.keyval)
        print('val_name:', val_name)
        if val_name == 'Delete':
            self.drawingEvent.delete_selection(self.key)
            self.listmodel.remove(self.it)
            self.view.show_all()
    
    def __set_text_edited(self, w, p, text):
        #print('edited:', text, type(text), len(text))
        self.listmodel[p][0] = text
        self.drawingEvent.edit_selection(self.key, text)
        #self.current_text = text
        #self.drawingEvent.modify_selection(self.key, text)
            
    def return_currentFileWindow(self):
        return self.scrollWindow

class WorkingLabels():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.box_height = int(self.screen_height * 0.3)
        self.box_width = int(self.screen_width*0.178)
        self.scw_width = int(self.box_width/3)

        self.set_workingLabels()
    
    def wrap_drawing(self, drawingEvent):
        self.drawingEvent = drawingEvent

    def set_workingLabels(self):
        self.scrollWindow = Gtk.ScrolledWindow(None, None)
        self.scrollWindow.set_name('NETSCROLLWINDOW')
        self.scrollWindow.set_size_request(self.scw_width, self.box_height)
        self.scrollWindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.listmodel = Gtk.ListStore(str)
        self.view = Gtk.TreeView(model = self.listmodel)
        self.view.set_name('NETVIEW')
        
        renderText = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('WLabels', renderText, text = 0)

        self.view.append_column(columntext)

        self.scrollWindow.add(self.view)

        wlabels_file = open('wlabels.txt', 'r')
        lines = wlabels_file.readlines()
        self.labels = []

        for line in lines:
            line = line.strip('\n')
            self.listmodel.append([line])
            self.labels.append(line)
        
        self.view.show_all()
        
    def get_labels(self):
        return self.labels

    def return_workingLabelsWindow(self):
        return self.scrollWindow

class NetLabels():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width
        self.screen_height = monitor_geo.height

        self.box_height = int(self.screen_height * 0.3)
        self.box_width = int(self.screen_width*0.178)
        self.scw_width = int(self.box_width/3)

        self.set_NetLabels()
    
    def set_NetLabels(self):
        self.scrollWindow = Gtk.ScrolledWindow(None, None)
        self.scrollWindow.set_name('NETSCROLLWINDOW')
        self.scrollWindow.set_size_request(self.scw_width, self.box_height)
        self.scrollWindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.listmodel = Gtk.ListStore(str)
        self.view = Gtk.TreeView(model = self.listmodel)
        self.view.set_name('NETVIEW')
        
        renderText = Gtk.CellRendererText()
        columntext = Gtk.TreeViewColumn('NetLabels', renderText, text = 0)

        self.view.append_column(columntext)

        self.scrollWindow.add(self.view)
    
    def update_net_labels(self, labels):
        for label in labels:
            self.listmodel.append([label])
        self.view.show_all()
    
    def return_NetLabelsWindow(self):
        return self.scrollWindow

