import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject 

#import bb_screen
#from DBBGUI.main_dbbt import DBBT
import DBBGUI

css_file = 'dbbt_style.css'

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path(css_file)
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    main_window = Gtk.Window()
    main_window.set_title("DeepBoundingBoxTool")
    main_window.connect('delete-event', Gtk.main_quit)
    main_window.set_border_width(0)
    main_window.set_position(Gtk.WindowPosition.CENTER)

    #screen = Gdk.Screen.get_default()
    #monitor_geo = screen.get_monitor_geometry(1)
    #x = monitor_geo.x
    #y = monitor_geo.y
    #main_window.move(x,y)
    main_window.fullscreen()

    #screen_class = bb_screen.Screen_BB2(main_window)
    #main_box = screen_class.return_main_box()
    screen_class = DBBGUI.DBBT(main_window)
    main_box = screen_class.return_main_dbbt_box()
    main_window.add(main_box)

    main_window.show_all()
    Gtk.main()



