import os.path
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
import tkinter.font as font
from PIL import ImageTk, Image

root = Tk()

root.title("feurnote - New File")
root.geometry("1300x465")
Current_file = None
Current_zoom = 11
Copy = None
top = None
fonts = StringVar()
fonts.set("Arial")
IMAGES = []


def save_as():
    global Current_file
    files = [("Feur", "*.feur"), ("Text file", "*.txt"), ("All Files", "*.*")]
    f = asksaveasfile(mode='wb', filetype=files, defaultextension=files)
    if f is not None:
        f.write(bytes(content.get("1.0", END).encode()))
        Current_file = f.name
        # f.write(bytes(str(IMAGES).encode()))
        root.title(f"feurnote - {f.name}")

        f.close()


def open_():
    global Current_file, photo, IMAGES
    files = [("Feur", "*.feur"), ("Text file", "*.txt"), ("All Files", "*.*")]

    f = askopenfile(mode="rb", filetype=files, defaultextension=files)
    if f is not None:

        with open(f.name, "rb"):
            imgs = f.readlines()[-1].decode()
        if type(eval(imgs)) == list:
            for indx, value in eval(imgs):
                print(indx, value)
                photo = ImageTk.PhotoImage(file=value)
                content.image_create(image=photo, index=indx)
                IMAGES.append([indx, value])

        contenu = f.read()

        content.replace("1.0", END, contenu.decode())
        Current_file = f.name
        root.title(f"feurnote - {f.name}")

        f.close()


def save_():
    global Current_file
    if Current_file is not None:
        with open(Current_file, "wb") as f:
            f.write(bytes(content.get("1.0", END).encode()))
            # f.write(bytes(str(IMAGES).encode()))
            f.close()
    elif Current_file is None:
        save_as()


def new_():
    global Current_file
    content.replace("1.0", END, "")
    Current_file = None
    root.title("feurnote - New File")


def zoom():
    global Current_zoom
    Current_zoom += 1
    content['font'] = (font.Font(family=fonts.get()), Current_zoom)


def unzoom():
    global Current_zoom
    Current_zoom -= 1
    content['font'] = (font.Font(family=fonts.get()), Current_zoom)


def destroyandchange():
    if top is not None:
        top.destroy()
        content.configure(face=(font.Font(family=fonts.get()), Current_zoom))


def setfont():
    global top, fonts
    x = root.winfo_x()
    y = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()
    top = Toplevel(root)
    top.geometry("230x40")
    top.title("Font name")
    top.geometry("+%d+%d" % (x + width / 2, y + height / 2))
    Entry(top, textvariable=fonts).place(relx=0.5, rely=0.5, anchor=CENTER)
    Button(top, text="Valide", command=destroyandchange).place(relx=0.9, rely=0.5, anchor=CENTER)


def copy_():
    global Copy
    Copy = content.selection_get()


def paste():
    global Copy
    if Copy is not None:
        content.insert(content.index(INSERT), Copy)


def cut():
    global Copy
    Copy = content.selection_get()
    content.delete("sel.first", "sel.last")


def insert_image():
    global photo
    formats_ = [".jpg", ".png", ".gif"]
    f = askopenfilename()
    if f is None:
        return
    if os.path.splitext(f)[1] not in formats_:
        return

    photo = ImageTk.PhotoImage(file=f)
    content.image_create(image=photo, index=content.index(INSERT))
    IMAGES.append([content.index(INSERT), f])


scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y, )
scrollbar2 = Scrollbar(root, orient=HORIZONTAL)
scrollbar2.pack(side=BOTTOM, fill=X)
content = Text(root, xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set,
               font=(font.Font(family=fonts.get(), ), Current_zoom), wrap="none", undo=True)
content.pack(fill=BOTH, expand=1)
scrollbar.config(command=content.yview)
scrollbar2.config(command=content.xview)

m = Menu(root)
root.config(menu=m)
file = Menu(m)
edit = Menu(m)

m.add_cascade(menu=file, label="File", underline=0)
m.add_cascade(menu=edit, label="Edit", underline=0)
file.add_command(label="New", command=new_, underline=0)
file.add_command(label="Open", command=open_, underline=0)
file.add_command(label="Save", command=save_, underline=0)
file.add_command(label="Save as", command=save_as, underline=0)
m.add_command(label="zoom+", underline=4,
              command=zoom)
m.add_command(label="zoom-", underline=4, command=unzoom)
m.add_command(label="setfont", command=setfont)

edit.add_command(label="Copy", command=copy_)
edit.add_command(label="Cut", command=cut)
edit.add_command(label="Paste", command=paste)
edit.add_separator()
edit.add_command(label="Insert Image", command=insert_image)
edit.add_separator()
edit.add_command(label="undo (ctrl + z)", command=content.edit_undo)
edit.add_command(label="redo (ctrl + y)", command=content.edit_redo)

if __name__ == '__main__':
    root.mainloop()
