import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 


class MENU():
    def __init__(self, window):
        self.window = window
        #self.screen = Gdk.Screen.get_default()
        self.screen = window.get_screen()
        monitor_geo = self.screen.get_monitor_geometry(0)
        self.screen_width = monitor_geo.width #self.screen.get_width()
        self.screen_height = monitor_geo.height #self.screen.get_height()
        
        menu_width = int(self.screen_width * 0.05)
        self.menu_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu_box.set_size_request(menu_width, 0)
        self.menu_box.set_name('MENU_BOX')

        self.resources_charged = False

        self.set_open_folder()
        self.set_save_folder()
        self.set_prev_button()
        self.set_next_button()
        self.set_verify_button()
        self.set_unsave_changes()
        self.set_check_boxes()
        self.set_separator()
        self.set_edit_button()
        self.set_cancel_button()
        self.set_zoomin_button()
        self.set_zoomout_button()
        self.set_zoomfit_button()

    def set_open_folder(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.42)
        img_height = img_width

        button = Gtk.Button("Open Folder", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-imágenes-de-carpetas-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

        button.connect('clicked', self.__open_folder_clicked)


    def set_save_folder(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.42)
        img_height = img_width

        button = Gtk.Button("Save Folder", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-abrir-carpeta-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

    def set_prev_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.5)
        img_height = img_width

        button = Gtk.Button("Prev", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-galón-izquierdo-filled-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

        button.connect('clicked', self.__prev_button_clicked)

    def set_next_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.5)
        img_height = img_width

        button = Gtk.Button("Next", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-chebrón-hacia-la-derecha-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

        button.connect('clicked', self.__next_button_clicked)

    def set_verify_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("Veify", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-casilla-de-verificación-marcada-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

    def set_unsave_changes(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.5)
        img_height = img_width

        self.save_button = Gtk.Button("Save", xalign = 0.5, yalign = 0.5) 
        self.save_button.set_name("FolderButton")
        self.save_button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-guardar-96.png', img_width, img_height)
        self.unsave_img = Gtk.Image.new_from_pixbuf(pix)

        self.save_button.set_image(self.unsave_img)
        self.save_button.set_always_show_image(True)
        self.save_button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(self.save_button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)
        
    def set_check_boxes(self):
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.set_name("ButtonBox")
        #button_width = int(self.screen_width*0.01)
        #button_height = button_width
        
        yolo_checkbutton = Gtk.CheckButton("YOLO")
        VOC_checkbutton = Gtk.CheckButton("PASCAL\nVOC")

        box.pack_start(yolo_checkbutton, False, False, 0)
        box.pack_start(VOC_checkbutton, False, False, 0)

        self.menu_box.pack_start(box, False, False, 0)

    def set_separator(self):
        width = int(self.screen_width*0.05)
        separator_box = Gtk.Box()
        box = Gtk.Box()
        box.set_size_request(width, 0)
        separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
        separator_box.pack_start(box, True, False, 0)
        box.pack_start(separator, True, True, 0)
        
        self.menu_box.pack_start(separator_box, False, False, 20)

    def set_edit_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("   Create\n RectBox", xalign = 0.5, yalign = 0.5)
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-editar-imagen-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

        button.connect('clicked', self.__create_rectbox)
    
    def set_cancel_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("   Delete\n RectBox", xalign = 0.5, yalign = 0.5)
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-eliminar-imagen-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

    def set_zoomin_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("Zoom In", xalign = 0.5, yalign = 0.5)
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-expandir-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)
    
    def set_zoomout_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("Zoom Out", xalign = 0.5, yalign = 0.5)
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-achicar-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)
    
    def set_zoomfit_button(self):
        box = Gtk.Box()
        
        button_width = int(self.screen_width*0.045)
        button_height = button_width
        img_width = int(button_width*0.55)
        img_height = img_width

        button = Gtk.Button("Fit", xalign = 0.5, yalign = 0.5)
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-para-ampliar-el-tamaño-real-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

    def wrap_resources(self, resources_cl):
        self.resources_cl = resources_cl

    def __open_folder_clicked(self, button):
        dialog = Gtk.FileChooserDialog('Choose a Folder', self.window, Gtk.FileChooserAction.SELECT_FOLDER|Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        image_folder_path = dialog.get_filename()
        dialog.destroy()
        if response == -5:
            self.__set_resources(image_folder_path)

    def __set_resources(self, path):
        #self.resources_cl.set_files(path)
        self.resources_cl.update_Imagefiles_resources(path)
        self.resources_charged = True

    def __next_button_clicked(self, button):
        if self.resources_charged:
            self.resources_cl.next_image()

    def __prev_button_clicked(self, button):
        if self.resources_charged:
            self.resources_cl.prev_image()
    
    def wrap_drawing(self, drawing_cl):
        self.drawing_wrapped = drawing_cl

    def __create_rectbox(self, button):
        print('creating rectbox')
        self.resources_cl.create_rectbox()

    def return_menu_box(self):
        return self.menu_box



