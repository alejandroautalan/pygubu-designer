# helloworld.py
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "holamundo.ui"


class HolamundoApp:
    def __init__(self, master=None):
        # 1: Crear un builder y configurar el path de recursos (si usas imágenes)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        # 2: Cargar un archivo UI
        builder.add_from_file(PROJECT_UI)

        # 3: Crear la ventana principal
        self.mainwindow = builder.get_object("mainwindow", master)

        # 4: Conectar callbacks
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = HolamundoApp()
    app.run()
