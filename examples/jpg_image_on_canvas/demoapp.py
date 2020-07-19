import os
import pygubu
from PIL import Image, ImageTk


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "demoapp.ui")


class DemoApp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('topdemo')
        builder.connect_callbacks(self)
        
        canvas = builder.get_object('canvas1')
        # Load image in canvas
        fpath = os.path.join(PROJECT_PATH, 'seaside400.jpg')
        aux = Image.open(fpath)
        self.img = ImageTk.PhotoImage(aux)
        canvas.create_image(0, 0, image=self.img, anchor='nw')
        
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = DemoApp()
    app.run()

