#!/usr/bin/env python

import urwid
import os
from datetime import datetime


palette = [
    (None, "light gray", "black"),
    ("reversed", "standout", ""),
    ("body", "dark red", "white"),
    ("bodyrev", "black", "white"),
    ("dirs", "black", "light red"),
    ("dirsrev", "white", "dark red"),
    ("bg", "black", "dark blue"),
    ("reveal_focus", "black", "yellow"),
    ("text_highlight", "yellow,bold", ""),
]

class TopFrame(urwid.Columns):
    def __init__(self, browser_panel_list):
        self.panels = browser_panel_list
        self.focus_arr = []
        super().__init__(self.panels, dividechars=1)

    def keypress(self, size, key):
        if key in ['h']:
            self.focus_position = (self.focus_position - 1) % (len(self.panels))
            self.focus_arr.append(self.focus)
            return key
            
        elif key in ['l']:
            self.focus_position = (self.focus_position + 1) % (len(self.panels))
            return key
        else:
            return key


class BrowserPanel(urwid.ListBox):

    def __init__(self, path):
        self.current_path = path
        self.root_path = '/'
        self.previous_path = self.root_path
        self.hidden = False
        list_box = self.show_buttons()
        super().__init__(list_box)

    def gen_file_list(self):
        all_files = os.listdir(self.current_path)
        ret_list = []
        
        if self.current_path != '/':
            ret_list.append('..')
        if not self.hidden:
            for f in all_files:
                if f[0] != '.':
                    ret_list.append(f)
        else:
            ret_list = all_files

        return ret_list
                    
    def keypress(self, size, key):
        if key in ['j']:
            self.focus_position = (self.focus_position + 1) % (len(self.gen_file_list()))
            return key
        elif key in ['k']:
            self.focus_position = (self.focus_position - 1) % (len(self.gen_file_list()))
            return key
        else:
            return key

    def show_buttons(self):
        body = []
        
        for f in self.gen_file_list():
            button = urwid.Button(f)
            pathvar = os.path.join(self.current_path, f)
            if (os.path.isdir(pathvar)):
                urwid.connect_signal(button, 'click', self.update_list, pathvar)
                body.append(urwid.AttrMap(button, 'dirs', focus_map='dirsrev'))
            elif (os.path.isfile(pathvar)):
                body.append(urwid.AttrMap(button, 'body', focus_map='bodyrev'))

        walker = urwid.SimpleFocusListWalker(body)
        return walker

    def update_list(self, dirpath):
        dname = os.path.split(dirpath)
        self.previous_path = self.current_path
        self.current_path = dirpath


def exit_on_q(key):
    if key in ['q']:
        raise urwid.ExitMainLoop()


def create_frame(panel):
    title = "PyFi: A Terminal File Manager"
    today = datetime.now()
    today_f  = today.strftime("%d/%m/%Y %H:%M:%S")
    header_t = urwid.AttrMap(urwid.Text(('text_highlight', f"{title}")), 'reveal_focus')
    footer_t = urwid.AttrMap(urwid.Text(('text_highlight', f"{today_f}")), 'reveal_focus')
    main_frame = urwid.Frame(panel, header=header_t, footer=footer_t)
    return main_frame


def main():
    browser_panels = []
    for i in range(2):
        browser_panels.append(BrowserPanel(os.path.expanduser('~')))

    top_frame = TopFrame(browser_panels)

    main_frame = create_frame(top_frame)
    loop = urwid.MainLoop(main_frame, palette, unhandled_input=exit_on_q)
    loop.run()
    print(main_frame._selectable)

    
if __name__ == '__main__':
    main()
