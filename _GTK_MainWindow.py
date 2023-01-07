import gi

gi.require_version("Gtk","3.0")

from gi.repository import Gtk


class MyWindow(Gtk.Window):

    def __init__(self) -> None:
        super().__init__(title="ScrApp")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
    
        self.button = Gtk.Button(label="Start Scraping")
        self.actionLabel = Gtk.Label(label="Scrap a website now !", angle=0,halign=Gtk.Align.CENTER)
        self.url = Gtk.Label() 
        self.input = Gtk.Entry()
        # to change a property of a widget -> widget.props.propname = value
        self.button.connect("clicked", self.start_scraping)
        self.box.pack_start(self.actionLabel, True, True, 0)
        self.box.pack_start(self.url, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)

    def start_scraping(self, widget):
        print("Scraping started")
        self.actionLabel.props.label = "Scraping started ! "
        
# win = Gtk.Window()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
