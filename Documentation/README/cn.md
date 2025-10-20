# Pygubu 项目说明

[Español 版本在此查看](Documentation/README/es.md)。更多语言翻译请访问[此处](Documentation/README)

欢迎使用 Pygubu!
============================================

`Pygubu` 是一款专为 Python `tkinter` 模块设计的 [RAD 工具](https://en.wikipedia.org/wiki/Rapid_application_development)，致力于实现用户界面的**快速**、**高效**开发。

通过该工具设计的用户界面将以 [XML](https://en.wikipedia.org/wiki/XML) 格式保存，并可通过 _pygubu 构建器_ 在应用程序中动态加载。

Pygubu 的设计灵感源自 [Glade](https://gitlab.gnome.org/GNOME/glade)。

## 安装指南

最新版 pygubu 要求 Python >= 3.9

可通过以下方式安装 pygubu-designer：

### pip 安装

```bash
pip install pygubu-designer
```

### Arch Linux ([AUR](https://aur.archlinux.org/packages/pygubu-designer))

```bash
yay pygubu-designer
```

### Windows 用户注意事项

若 Python 安装路径包含空格（如 `C:\Program Files\Python312`），可能会触发错误。请选择以下解决方案：

1. 执行命令时添加引号：

```batch
"C:\Program Files\Python312\Scripts\pygubu-designer.exe"
```

2. 将 Python 添加至系统 PATH：
- 打开 **系统属性** > **环境变量**
- 在**系统变量**中选择 `Path` > **编辑**
- 添加 Python 安装路径（如 `C:\Program Files\Python312`）

3. 使用短路径格式：

```batch
C:\PROGRA~1\Python312\Scripts\pygubu-designer.exe
```

## 界面预览

<img src="pygubu-designer.png" alt="pygubu-designer 界面截图">

## 使用说明

根据系统类型，在终端输入对应命令：

### 类 Unix 系统

```bash
pygubu-designer
```

### Windows 系统

```batch
C:\Python3\Scripts\pygubu-designer.exe
```

（`C:\Python3` 需替换为实际 Python 安装路径）

通过顶部面板的 `组件库` 开始创建 tkinter 应用程序界面。完成设计后，通过菜单栏 `文件 > 保存` 将界面定义保存为 `.ui` 文件。

以下是通过 pygubu 创建的 [helloworld.ui](examples/helloworld/helloworld.ui) 示例：

```xml
<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <!-- XML 界面定义内容 -->
</interface>
```

应用程序脚本示例 ([helloworld.py](examples/helloworld/helloworld.py))：

```python
# helloworld.py
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"

class HelloworldApp:
    def __init__(self, master=None):
        # 1. 初始化构建器并配置资源路径
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        
        # 2. 加载界面文件
        builder.add_from_file(PROJECT_UI)
        
        # 3. 创建主窗口
        self.mainwindow = builder.get_object('mainwindow', master)
        
        # 4. 绑定回调函数
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = HelloworldApp()
    app.run()
```

注意事项：
- `PROJECT_UI` 需替换为实际保存的界面文件名
- `get_object()` 中的控件名需与 XML 中定义的主容器名一致，否则会触发 `Widget not defined` 错误（详见 [此问题](https://github.com/alejandroautalan/pygubu/issues/40)）

## 文档资源

访问 [项目 Wiki](https://github.com/alejandroautalan/pygubu-designer/wiki) 获取完整文档。

推荐参考资源：
- [TkDocs](http://www.tkdocs.com)
- [Python 官方 GUI 文档](https://docs.python.org/3/library/tk.html)
- [Tkinter 8.5 参考指南](https://tkdocs.com/shipman)
- [Tkinter 入门教程](http://effbot.org/tkinterbook) ([存档版](http://web.archive.org/web/20200504141939/http://www.effbot.org/tkinterbook))
- [Tcl/Tk 9.0 Manual](https://www.tcl-lang.org/man/tcl9.0/TkCmd/index.html)
- [Tcl/Tk 8.6 Manual](https://www.tcl-lang.org/man/tcl8.6/TkCmd/contents.htm)

更多实践示例请查看 [示例目录](examples)，或观看 [入门视频教程](http://youtu.be/wuzV9P8geDg)。

## 版本历史

更新日志请查阅 [HISTORY.md](HISTORY.md)。
```
