from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style#, Entry
from tkinter import *
import os
from math import ceil
import argparse

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to the folder whose subfolders will be scanned")
    return parser.parse_args().path


class MainWindow:
    def __init__(self, window = None):
        self.window = window if window else Tk()
        self.window.title("StorageExplorer")
        self.window.geometry("300x0")
        self.window.resizable(0,0)
        self.window.update()
        self.main_folder = self.folder_selector()
        self.current_folder = self.main_folder
        if not self.main_folder:
            return
        self.window.title("Scanning...")
        self.data = {x[0]: [{"name": y, "size": 0, "folder": True} for y in x[1]] + [{"name": z, "size": 0, "folder": False} for z in x[2]] for x in os.walk(self.main_folder)}
        self.get_sizes(self.data, self.main_folder)
        self.window.title("StorageExplorer")
        self.window.geometry("")

        self.current_site = [1]
        self.max_amount = 20
        self.create_table()
        self.window.mainloop()

    def folder_selector(self):
        path = get_args()
        if path:
            return os.path.realpath(path)
        else:
            return filedialog.askdirectory(parent=self.window)

    def get_sizes(self, data, current_path):
        if not data.get(current_path):
            return 0
        size = 0
        for item in data[current_path]:
            if item["folder"]:
                tmp = self.get_sizes(data, os.path.join(current_path, item["name"]))
            else:
                try:
                    tmp = os.path.getsize(os.path.join(current_path, item["name"]))
                except FileNotFoundError:
                    tmp = 0
                except OSError:
                    tmp = 0
            item["size"] = tmp
            size += tmp
        return size


    def create_table(self):
        """
        Creates a custom made table in a list style
        :return: None
        """

        s = Style()
        Button(self.window, text="Back", command=self.menu_backwards, state=NORMAL if self.current_folder != self.main_folder else DISABLED).grid(column=0, row=0, sticky=N + W)


        w = Text(self.window, height=1, borderwidth=0)
        w.insert(1.0, self.current_folder)
        w.grid(column=1, row=0)
        w.configure(state="disabled")
        w.configure(inactiveselectbackground=w.cget("selectbackground"))
        
        pager_frame = Frame(self.window)
        pager_frame.grid(column=2, row=0, sticky=E)

        frame = Frame(self.window, name="table")
        frame.grid(column=0, row=1, columnspan=3, sticky=E)
        spin = Spinbox(pager_frame, from_=1, to=ceil(len(self.data[self.current_folder]) / self.max_amount) + 1, width=len(str(ceil(len(self.data[self.current_folder]) / self.max_amount))) + 1, command=lambda: self.get_spin(spin.get()))
        spin.grid(column=0, row=0)
        spin.delete(0, "end")
        spin.insert(0, self.current_site[-1])
        spin.bind("<Key>", lambda a: self.get_spin(spin.get(), a)) 
        Label(pager_frame, text=f'/ {ceil(len(self.data[self.current_folder]) / self.max_amount)}').grid(
            column=1, row=0)
        Button(pager_frame, text="Prev", command=self.site_prev,
               state=DISABLED if self.current_site[-1] == 1 else NORMAL).grid(column=2, row=0)
        Button(pager_frame, text="Next", command=self.site_next,
               state=DISABLED if self.current_site[-1] == ceil(len(self.data[self.current_folder]) / self.max_amount) else NORMAL).grid(
            column=3, row=0)
        table = sorted(self.data[self.current_folder], key=lambda a: a["size"], reverse=True)[(self.current_site[-1] - 1) * self.max_amount:self.current_site[-1] * self.max_amount]
        Canvas(frame, width=800, height=10).grid(row=0, column=0, columnspan=3)
        for row in range(len(table)):
            current_item = table[row]
            Button(frame, text="Open", command=lambda a=table[row]["name"]: self.menu_forwards(a), state=NORMAL if current_item["folder"] else DISABLED).grid(row=row * 2 + 1, column=0, sticky=W)
            Label(frame, text=table[row]["name"], font=("Arial", 10)).grid(row=row * 2 + 1, column=1)
            
            value = (table[row]["size"], sum([x["size"] for x in self.data[self.current_folder]]))
            layout_name = f'{int(value[0])} / {int(value[1])}' if value[1] else str(value[0])
            background = get_hex_color(value)
            s.layout(layout_name,
                     [('LabeledProgressbar.trough',
                       {'children': [('LabeledProgressbar.pbar', {}),
                                     ("LabeledProgressbar.label", {"sticky": ""})], 'sticky': 'NSWE'})])
            s.configure(layout_name, text=layout_name)
            s.configure(layout_name, background=background)
            p = Progressbar(frame, orient="horizontal", length=300, style=layout_name)
            p.grid(row=row * 2 + 1, column=2, sticky=E)
            if value[1]:
                p["value"] = value[0] / value[1] * 100
            else:
                p["value"] = 0

            c = Canvas(frame, width=800, height=10)
            if row != len(table) - 1:
                c.create_line(0, 5, 800, 5)
            c.grid(row=row * 2 + 2, column=0, columnspan=3)


    def get_spin(self, text, a = None):
        if not a or a.keycode == 13:  # if Enter was pressed
            try:
                tmp = int(text)
                if 0 < tmp <= ceil(len(self.data[self.current_folder]) / self.max_amount):
                    self.current_site[-1] = tmp
                self.reload()
            except ValueError:
                print("Not a valid value")
            


    def menu_forwards(self, a):
        """
        Navigates into the given attribute.
        If the click doesn't get released on the object then nothing happens.

        :param a: Path to navigate as str
        :return: None
        """
        self.current_folder = os.path.join(self.current_folder, a)
        self.current_site.append(1)
        self.reload()

    def menu_backwards(self):
        """
        Navigates out of the current menu if possible
        :return:
        """
        self.current_folder = os.path.dirname(self.current_folder)
        self.current_site.pop()
        self.reload()

    
    def site_next(self):
        """
        navigates to the next site if possible

        :return: None
        """
        if self.current_site[-1] < ceil(len(self.data[self.current_folder])) / self.max_amount:
            self.current_site[-1] += 1
            self.reload()

    def site_prev(self):
        """
        navigates to the previous site if possible

        :return: None
        """
        if self.current_site[-1] > 1:
            self.current_site[-1] -= 1
            self.reload()

    def reload(self):
        """
        Destroys every element and replaces them with new data.

        :return: None
        """
        self.window.geometry(f'{self.window.winfo_width()}x{self.window.winfo_height()}')
        for child in self.window.winfo_children():
            child.destroy()
        self.create_table()
        self.window.update()
        self.window.geometry("")


def get_hex_color(value: tuple):
    """
    Converts a value between 0.0 and 1.0 into a color.
    The color palette starts with green, then yellow and from 0.75 it turns red

    :param value: tuple between 0.0 and 1.0
    :return: color as hex string
    """
    from math import ceil
    if value[1]:
        if value[0] < int(value[1] * 0.75):
            result = "#%0.2XFF00" % int(value[0] / ceil(value[1] * 0.75) * 255)
        else:
            result = "#FF%0.2X00" % int(
                ((value[0] - int(value[1] * 0.25)) * -1 + ceil(value[1] * 0.75)) / ceil(
                    value[1] * 0.25) * 255)
    else:
        result = "#FF0000"
    return result


if __name__ == "__main__":
    MainWindow()
