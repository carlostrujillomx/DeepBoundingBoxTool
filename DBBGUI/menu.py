import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 


class MENU():
    def __init__(self, window):
        self.window = window
        self.screen = window.get_screen()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        menu_width = int(self.screen_width * 0.05)
        self.menu_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu_box.set_size_request(menu_width, 0)
        self.menu_box.set_name('MENU_BOX')

        self.set_open_folder()
        self.set_save_folder()
        self.set_prev_button()
        self.set_next_button()
        self.set_verify_button()
        self.set_unsave_changes()
        self.set_check_boxes()


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

        button = Gtk.Button("Next", xalign = 0.5, yalign = 0.5) 
        button.set_name("FolderButton")
        button.set_size_request(button_width, button_height)
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size('graphics/icons8-galón-izquierdo-filled-96.png', img_width, img_height)
        img = Gtk.Image.new_from_pixbuf(pix)

        button.set_image(img)
        button.set_always_show_image(True)
        button.set_image_position(Gtk.PositionType.TOP)
        box.pack_start(button, True, True, 0)
        self.menu_box.pack_start(box, False, False, 0)

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
        VOC_checkbutton = Gtk.CheckButton("VOC PASCAL")

        box.pack_start(yolo_checkbutton, False, False, 0)
        box.pack_start(VOC_checkbutton, False, False, 0)

        self.menu_box.pack_start(box, False, False, 0)



    def return_menu_box(self):
        return self.menu_box