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

        self.keywordlist = ''
        self.flag_filekwList = False

        self.algo = Algo_G()
        self.algo._KILL = False
        # self.box = Gtk.Box(spacing=6)
        self.grid = Gtk.Grid()
        # self.add(self.box)
        self.add(self.grid)
        
        self.input_widget = Gtk.Entry()
        self.input_widget.set_text("type a keyword here...")
        # self.box.pack_start(self.input_widget, True, True, 0)
    
        self.start_btn = Gtk.Button(label="Start Scraping")
        self.actionLabel = Gtk.Label(label="Scrap a website now !", angle=0,halign=Gtk.Align.CENTER)
        self.url = Gtk.Label(label="url")
        self.default_entry = Gtk.Entry()
        self.default_entry.set_text("www.wallpapeflare.com")
        self.default_entry.set_editable(False)
        self.keyword = Gtk.Label(label="keyword:") 
        self.chooseButton = Gtk.Button(label="choose a file")
        self.btn_createList = Gtk.Button(label="create a list of keywords")


        self.grid.add(self.url)
        self.grid.attach_next_to(self.default_entry, self.url, Gtk.PositionType.BOTTOM,1,2)
        self.grid.attach_next_to(self.keyword,self.default_entry,Gtk.PositionType.BOTTOM,1,3)
        # to change a property of a widget -> widget.props.propname = value
        self.handler_start_btn_id = self.start_btn.connect("clicked", self.start_scraping)
        self.handler_choose_btn = self.chooseButton.connect("clicked", self.choose_file)
        # self.box.pack_start(self.actionLabel, True, True, 0)
        # self.box.pack_start(self.url, True, True, 0)
        # self.box.pack_start(self.start_btn, True, True, 0)
        self.grid.attach_next_to(self.input_widget,self.keyword, Gtk.PositionType.BOTTOM, 1,4)
        self.grid.attach_next_to(self.chooseButton,self.input_widget, Gtk.PositionType.BOTTOM,1,5)
        self.grid.attach_next_to(self.btn_createList,self.chooseButton, Gtk.PositionType.RIGHT,1,5)
        self.grid.attach(self.start_btn, 1, 2, 2, 2)
        self.grid.attach_next_to(self.actionLabel,self.start_btn, Gtk.PositionType.TOP, 2, 1)

    def start_scraping(self, widget):
        print("Scraping started")
        if self.flag_filekwList:
            self.input = self.keywordlist
        else:
            self.input = self.parse_input(widget, self.input_widget.get_text())
        self.algo._KILL = False
        
        self.actionLabel.props.label = "Scraping started ! "
        self.start_btn.props.label = "STOP"
        self.start_btn.disconnect(self.handler_start_btn_id)
        self.handler_start_btn_id = self.start_btn.connect("clicked", self.stop_scraping)
        
        key_word_list = self.algo.define_key_word_entry(self.input)
        self.action = Thread(target=self.algo.main_iteration,args=[key_word_list, 2])
        self.action.start()
        print('number of page to scrap is currently hard coded and is equal to: 1')


    def stop_scraping(self,widget):
        
        self.algo.__setattr__('_KILL',True)
        print("scraping stopped successfully")
        self.action.join()
        self.start_btn.disconnect(self.handler_start_btn_id)
        self.handler_start_btn_id = self.start_btn.connect("clicked", self.start_scraping)
        self.start_btn.props.label="Start scraping"
        self.actionLabel.props.label = "Scraping stoped ! "
        self.actionLabel.props.label = "Start Scraping now ! "
            
    def parse_input(self, widget, user_input):
        if ' ' in user_input:
            print('keyword must use the "+" sign not spaces between words')
            print('replacing all spaces by "+"')
            user_input = user_input.replace(' ','+')
        return user_input

    def choose_file(self,widget):
        fileChooser = Gtk.FileChooserDialog(title="choose a file",parent=self, action=Gtk.FileChooserAction.OPEN)
        fileChooser.add_buttons(Gtk.STOCK_CANCEL,
                                     Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN,
                                     Gtk.ResponseType.OK,)

        self.add_filters(fileChooser)

        response = fileChooser.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            self.keywordlist = fileChooser.get_filename()
            self.flag_filekwList = True
            print("File selected:" + self.keywordlist)
            self.input_widget.props.text = self.keywordlist
            fileChooser.destroy()
            return fileChooser.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel Clicked")
        fileChooser.destroy()
        

    def add_filters(self, fileChooser):

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        fileChooser.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        fileChooser.add_filter(filter_py)
        
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        fileChooser.add_filter(filter_any)



# win = Gtk.Window()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
