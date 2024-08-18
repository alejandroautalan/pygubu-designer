Chào mừng đến với Pygubu!
============================================

`Pygubu` là một [phần mềm RAD](https://en.wikipedia.org/wiki/Rapid_application_development) tạo ra một môi trường phát triển giao diện người dùng cho module `Tkinter` từ Python _nhanh_ và _dễ dàng_.

Các giao diện được tạo ra sẽ được lưu lại trong tệp [XML](https://en.wikipedia.org/wiki/XML), và với _pygubu builder_ thì chúng có thể được nạp vào các ứng dụng một cách linh hoạt nếu cần thiết.

Pygubu lấy cảm hứng từ [Glade](https://glade.gnome.org).

Cài đặt
============

Phiên bản Pygubu hiện tại yêu cầu Python 3.8 trở lên.

Cài đặt bằng:

### pip

```bash
$ pip install pygubu-designer
```

### Trên Arch Linux với repository [AUR](https://aur.archlinux.org/packages/pygubu-designer)

```bash
$ yay -S pygubu-designer
```

Ảnh chụp màn hình
==========

<img src="pygubu-designer.png" alt="pygubu-desinger.png">

Sử dụng
=====

Mở Pygubu tùy thuộc vào hệ thống của bạn:

Nếu Python được đặt vào $PATH/%PATH%, hãy thử:

```bash
$ pygubu-designer
```

Nếu không được:

```bash
$ <vị trí Python>/Scripts/pygubu-designer
```

Bây giờ bạn có thể tạo ứng dụng Tkinter cho mình với các widget ở panel phía trên được gọi là `Widget Palette`.

Sau khi làm xong việc của mình, lưu lại công việc của bạn vào một tệp `.ui` (`File > Save`).

Dưới đây là một [ví dụ](examples/helloworld/helloworld.ui):

```xml
<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="height">200</property>
    <property name="resizable">both</property>
    <property name="title" translatable="yes">Hello World App</property>
    <property name="width">200</property>
    <child>
      <object class="ttk.Frame" id="mainframe">
        <property name="height">200</property>
        <property name="padding">20</property>
        <property name="width">200</property>
        <layout manager="pack">
          <property name="expand">true</property>
          <property name="side">top</property>
        </layout>
        <child>
          <object class="ttk.Label" id="label1">
            <property name="anchor">center</property>
            <property name="font">Helvetica 26</property>
            <property name="foreground">#0000b8</property>
            <property name="text" translatable="yes">Hello World !</property>
            <layout manager="pack">
              <property name="side">top</property>
            </layout>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
```

Nạp giao diện từ đoạn code trên với [Python](examples/helloworld/helloworld.py):

```python
# helloworld.py
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent # Thư mục nơi file này được đặt
PROJECT_UI = PROJECT_PATH / "helloworld.ui" # Thay đổi "helloworld.ui" với tên file của bạn


class HelloworldApp:
    def __init__(self, master=None):
        # 1: Tạo một builder và bảo nó nơi nó có thể tìm ảnh nếu có
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        # 2: Load một file .ui
        builder.add_from_file(PROJECT_UI)

        # 3: Gọi object được đặt id là "mainwindow" - ở đây là một tk.TopLevel
        # Thường chúng ta sẽ gọi widget trên cùng - thường là một cửa sổ hoặc dialog,
        # sau đó gọi các widget con.
        self.mainwindow = builder.get_object('mainwindow', master)

        # 4: Cho builder biết các hàm sẽ thực hiện khi có tương tác của người dùng
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = HelloworldApp()
    app.run()

```

Nếu trong file không có một widget nào có id đang được pygubu tìm kiếm, sẽ có lỗi:

```
Exception: Widget not defined.
```

Có thể xem [trang này](https://github.com/alejandroautalan/pygubu/issues/40) để hiểu hơn về vấn đề này.

Tài liệu
=============

Trang wiki của Pygubu: https://github.com/alejandroautalan/pygubu-designer/wiki.

Đây là một số tài liệu tốt về Tkinter và Tk:

- [TkDocs](http://www.tkdocs.com)
- [Graphical User Interfaces with Tk](https://docs.python.org/3/library/tk.html)
- [Tkinter 8.5 reference: a GUI for Python](https://tkdocs.com/shipman)
- [An Introduction to Tkinter](http://effbot.org/tkinterbook) [(archive)](http://web.archive.org/web/20200504141939/http://www.effbot.org/tkinterbook)
- [Tcl/Tk 8.5 Manual](http://www.tcl.tk/man/tcl8.5/)

Ngoài ra bạn có thể xem mẫu ở thư mục [examples](examples) hoặc xem video [này](http://youtu.be/wuzV9P8geDg).

Lịch sử thay đổi
=======

Ở đây: [HISTORY.md](HISTORY.md).
