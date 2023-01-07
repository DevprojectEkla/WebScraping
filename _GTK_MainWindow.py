import sys
import gi
from threading import Thread

gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from WebSiteScrapping import Algo_G
from time import sleep

class MyWindow(Gtk.Window):

    def __init__(self) -> None:
        super().__init__(title="ScrApp")

        self.algo = Algo_G()
        self.algo._KILL = False
        # self.box = Gtk.Box(spacing=6)
        self.grid = Gtk.Grid()
        # self.add(self.box)
        self.add(self.grid)

        self.input_widget = Gtk.Entry()
        self.input_widget.set_text("type a keyword here...")
        # self.box.pack_start(self.input_widget, True, True, 0)
    
        self.button = Gtk.Button(label="Start Scraping")
        self.actionLabel = Gtk.Label(label="Scrap a website now !", angle=0,halign=Gtk.Align.CENTER)
        self.url = Gtk.Label(label="url")
        self.default_entry = Gtk.Entry()
        self.default_entry.set_text("www.wallpapeflare.com")
        self.default_entry.set_editable(False)
        self.keyword = Gtk.Label(label="keyword:") 
        self.grid.add(self.url)
        self.grid.attach_next_to(self.default_entry, self.url, Gtk.PositionType.BOTTOM,1,2)
        self.grid.attach_next_to(self.keyword,self.default_entry,Gtk.PositionType.BOTTOM,1,3)
        # to change a property of a widget -> widget.props.propname = value
        self.handler_btn_id = self.button.connect("clicked", self.start_scraping)
        # self.box.pack_start(self.actionLabel, True, True, 0)
        # self.box.pack_start(self.url, True, True, 0)
        # self.box.pack_start(self.button, True, True, 0)
        self.grid.attach_next_to(self.input_widget,self.keyword, Gtk.PositionType.BOTTOM, 1,4)
        self.grid.attach(self.button, 1, 2, 2, 2)
        self.grid.attach_next_to(self.actionLabel,self.button, Gtk.PositionType.TOP, 2, 1)

    def start_scraping(self, widget):
        print("Scraping started")
        self.input = self.parse_input(widget, self.input_widget.get_text())
        self.algo._KILL = False
        
        self.actionLabel.props.label = "Scraping started ! "
        self.button.props.label = "STOP"
        
        self.button.disconnect(self.handler_btn_id)
        self.handler_btn_id = self.button.connect("clicked", self.stop_scraping)
        key_word_list = self.algo.define_key_word_entry(self.input)
        dirname , filename = self.algo.prepare_name_directory(self.input)
        self.action = Thread(target=self.algo.main_iteration,args=[key_word_list,dirname,filename, 2])
        self.action.start()
        print('number of page to scrap is currently hard coded and is equal to: 1')


    def stop_scraping(self,widget):
        
        self.algo.__setattr__('_KILL',True)
        print("scraping stopped successfully")
        self.action.join()
        self.button.disconnect(self.handler_btn_id)
        self.handler_btn_id = self.button.connect("clicked", self.start_scraping)
        self.button.props.label="Start scraping"
        self.actionLabel.props.label = "Scraping stoped ! "
        self.actionLabel.props.label = "Start Scraping now ! "
            
    def parse_input(self, widget, user_input):
        if ' ' in user_input:
            print('keyword must use the "+" sign not spaces between words')
            print('replacing all spaces by "+"')
            user_input = user_input.replace(' ','+')
        return user_input




# win = Gtk.Window()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
