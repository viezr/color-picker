#!/usr/bin/env python3
'''
Screen color identifier at mouse point, color chooser.
Features:
    - show zoomed area around mouse
    - show color-block filled by color of pixel under mouse
    - show rgb and hex color index of pixel under mouse
    - show mouse coordinates
    - change choosen color by clicking on color-block
Button with "target" icon, activate main function.
Afer mouse click on pixel, main function stops
and by default save hex index of color to clipboard
'''

from time import time
import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageGrab, ImageTk


class Color_picker(tk.Tk):
    '''
    GUI class
    '''
    def __init__(self):
        '''
        Initial GUI
        '''
        tk.Tk.__init__(self, className="Sport timer")

        label_bg = "black"
        label_fg = "#ffffff"
        label_font = "roboto, 12"
        green_bg = "#28a745"
        green_ac = "#1e7b34"
        green_hl = "#0f3e1a"
        yellow_bg = "#ffc107"
        yellow_ac = "#b38600"
        yellow_hl = "#664d00"
        grey_bg = "#6c757d"
        grey_ac = "#474d52"
        grey_hl = "#242629"

        self.title("Color picker")
        self.geometry("224x288")
        self.attributes("-topmost", True)
        self.configure(background=grey_bg)
        self.overlay = None

        for col in [0, 2, 7]:
            self.grid_columnconfigure(col, minsize=8)
        self.grid_columnconfigure(1, minsize=128)
        self.grid_columnconfigure(3, minsize=32)

        for row in [0, 2, 6, 8]:
            self.grid_rowconfigure(row, minsize=8)
        self.grid_rowconfigure(1, minsize=128)
        for row in [3, 4, 5, 7]:
            self.grid_rowconfigure(row, minsize=24)

        self.hex_label_var = tk.StringVar()
        self.hex_label_var.set(label_fg)
        self.rgb_label_var = tk.StringVar()

        self.cv_size = 128
        self.labels_width = 16

        self.img_resources = Image.open("resources.png")
        self.pil_image = self.img_resources.crop((0, 24, 128, 25))
        self.pil_image = self.pil_image.resize((self.cv_size, self.cv_size),
            resample=Image.BOX)
        self.pil_image = ImageTk.PhotoImage(image=self.pil_image)
        self.picker_image = self.img_resources.crop((0, 0, 24, 24))
        self.picker_image = ImageTk.PhotoImage(image=self.picker_image)
        self.clipboard_image = self.img_resources.crop((24, 0, 48, 24))
        self.clipboard_image = ImageTk.PhotoImage(image=self.clipboard_image)
        self.chooser_image = self.img_resources.crop((48, 0, 72, 24))
        self.chooser_image = ImageTk.PhotoImage(image=self.chooser_image)


        self.image_canvas = tk.Canvas(self, bg="white", width=self.cv_size,
            height=self.cv_size)
        self.image_canvas_container = self.image_canvas.create_image(
            0, 0, image=self.pil_image, anchor="nw")
        self.image_canvas.grid(row=1, column=1)

        self.color_canvas = tk.Canvas(self, bg="white", width=28,
            height=self.cv_size, relief="raised", cursor="circle")
        self.color_canvas.grid(row=1, column=3)
        self.color_canvas_container = self.color_canvas.create_image(2, 52,
            image=self.chooser_image, anchor="nw")
        self.color_canvas.bind('<Button-1>', self.change_color)

        self.hex_label = tk.Label(self, text = "hex color",
            width=self.labels_width, bg=label_bg, fg=yellow_bg, font=label_font)
        self.hex_label.grid(row=3, column=1)

        self.rgb_label = tk.Label(self, text = "rgb color",
            width=self.labels_width, bg=label_bg, fg=yellow_bg, font=label_font)
        self.rgb_label.grid(row=4, column=1)

        self.coordinates = tk.Label(self, text = "coordinates",
            width=self.labels_width, bg=label_bg, fg=yellow_bg, font=label_font)
        self.coordinates.grid(row=5, column=1)

        self.hex_cpy_button = tk.Button(self, text="cp", command=self.hex_clipboard,
             padx=5, highlightcolor=yellow_hl, highlightbackground=yellow_hl,
             activebackground=yellow_ac, activeforeground="black", bg=yellow_bg,
             fg="black", font=label_font, image=self.clipboard_image)
        self.hex_cpy_button.grid(row=3, column=3)

        self.rgb_cpy_button = tk.Button(self, text="cp", command=self.rgb_clipboard,
            padx=5, highlightcolor=yellow_hl, highlightbackground=yellow_hl,
            activebackground=yellow_ac, activeforeground="black", bg=yellow_bg,
            fg="black", font=label_font, image=self.clipboard_image)
        self.rgb_cpy_button.grid(row=4, column=3)

        self.get_color_button = tk.Button(self, text="x", command=self.open_overlay,
            padx=5, highlightcolor=green_hl, highlightbackground=green_hl,
            activebackground=green_ac, activeforeground="white", bg=green_bg,
            fg="white", font=label_font, image=self.picker_image)
        self.get_color_button.grid(row=5, column=3)

        self.quit_button = tk.Button(self, text="QUIT", command=quit, padx=24,
            highlightcolor=grey_hl, highlightbackground=grey_hl,
            activebackground=grey_ac, activeforeground="white",
            bg=grey_bg, fg="white", font=label_font)
        self.quit_button.grid(row=7, column=1, columnspan=4)

    def change_color(self, event):
        '''
        Choose color from palette
        '''
        def_color = self.hex_label_var.get()
        color = askcolor(def_color,title="Tkinter Color Chooser")
        if color[0]:
            self.color_canvas.configure(bg = color[1])
            self.hex_label_var.set(color[1])
            self.hex_label.configure(text = self.hex_label_var.get())
            self.rgb_label_var.set(f"rgb{color[0]}")
            self.rgb_label.configure(text = self.rgb_label_var.get())

    def open_overlay(self):
        '''
        Overlay fullscreen window for capture pixels color
        '''
        self.overlay = tk.Toplevel(self)
        self.overrideredirect(True)
        self.overlay.title("Choose pixel")
        self.overlay.geometry("1920x1080")
        self.overlay.configure(background="")
        self.overlay.attributes("-fullscreen", True)
        self.overlay.bind('<Button-1>', self.quit_overlay)
        self.overlay.bind('<Motion>', self.motion)
        self.bind('<Motion>', self.motion)
        self.overlay.wait_visibility(self.overlay)
        self.main_up()

    def main_up(self):
        '''
        Up main frame above overlay for updating info of mouse moving
        '''
        self.attributes('-topmost', True)
        self.lift()
        self.update()
        self.overlay.after(2000, self.main_up)

    def motion(self, event):
        '''
        Capture part of screen (canvas_size / zoom_scale) and get pixel color
        under mouse point. Update information at main window.
        '''
        zoom_scale = 8
        capture_size = self.cv_size / zoom_scale
        x, y = event.x, event.y
        x, y = x - 1, y - 1 # little point correction
        crop_x1, crop_y1 = x - capture_size / 2, y - capture_size / 2
        crop_x2, crop_y2 = crop_x1 + capture_size, crop_y1 + capture_size
        img = ImageGrab.grab( bbox=(crop_x1, crop_y1, crop_x2, crop_y2) )
        img = img.resize((self.cv_size, self.cv_size), resample=Image.BOX)
        self.pil_image = ImageTk.PhotoImage(img)
        self.image_canvas.itemconfig(self.image_canvas_container, image=self.pil_image)

        position_str = 'x: ' + str(x) + ' y: ' + str(y)
        self.coordinates.configure(text = position_str)

        r, g, b = rgb_color = img.getpixel((64,64))
        self.rgb_label.configure(text = f"rgb({r}, {g}, {b})")
        self.rgb_label_var.set(rgb_color)

        hex_color = "#"
        for i in [r, g, b]:
            if i < 16:
                hex_color += f"0{i:x}"
            else:
                hex_color += f"{i:x}"
        self.hex_label.configure(text = hex_color)
        self.hex_label_var.set(hex_color)

        try:
            self.color_canvas.configure(bg = hex_color)
        except:
            self.hex_label_var.set("Err." + hex_color)

    def quit_overlay(self, event):
        '''
        Quit overlay
        '''
        self.unbind('<Motion>')
        self.hex_clipboard()
        self.overlay.destroy()

    def hex_clipboard(self):
        '''
        Copy hex color to clipboard
        '''
        self.clipboard_clear()
        self.clipboard_append(self.hex_label_var.get())
        self.update()

    def rgb_clipboard(self):
        '''
        Copy rgb color to clipboard
        '''
        self.clipboard_clear()
        self.clipboard_append(self.rgb_label_var.get())
        self.update()

def quit():
    """
    Quit application
    """
    app.destroy()

if __name__ == "__main__":
    app = Color_picker()
    app.mainloop()
