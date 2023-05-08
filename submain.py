#!/usr/bin/env python
import urwid
import os


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


class BrowserPanel(urwid.ListBox):
    def __init__(self, path):
        self.current_path = path
        self.root_path = '/'
        self.previous_path = self.root_path
        self.hidden = False
        walker = self.show_buttons()
        super().__init__(walker)

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
            print(os.path.split(pathvar))
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

def main():

    p = BrowserPanel(os.path.expanduser('~'))

    loop = urwid.MainLoop(p, palette, unhandled_input=exit_on_q)
    loop.run()

if __name__ == '__main__':
    main()
