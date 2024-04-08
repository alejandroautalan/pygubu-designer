import tkinter as tk
import tkinter.ttk as ttk
import pygubu
import pygubu.widgets.simpletooltip as tooltip
import pygubudesigner.services.widgets.treecomponentpaletteui as baseui
from pygubudesigner.i18n import translator
from pygubu.stockimage import StockImage, StockImageException


baseui.i18n_translator = translator


class TreeVisualState:
    def __init__(self, tree: ttk.Treeview):
        self.tree: ttk.Treeview = tree
        self.expanded_nodes = []
        self.focus = None

    def save(self):
        self.expanded_nodes = []
        for item in self.tree.get_children():
            if self.tree.item(item, "open"):
                self.expanded_nodes.append(item)
        self.focus = self.tree.focus()

    def restore(self):
        for item in self.expanded_nodes:
            if self.tree.exists(item):
                self.tree.item(item, open=True)
        if self.focus and self.tree.exists(self.focus):
            self.tree.see(self.focus)


class TreeComponentPalette(baseui.TreeComponentPaletteUI):
    KEY_PRESS_CB_MILISECONDS = 800

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.on_add_widget = None  # callback to call on double click.
        self._keypress_cbid = None
        self.cptree.filter_func = self.custom_filter
        tooltip.create(self.fb_show_alltk, "Show all Tk widgets")
        self.setup_styles()
        self.visual_state = TreeVisualState(self.cptree)
        btn_image = StockImage.get("cancel-circle-16")
        self.btn_filter_cancel.configure(image=btn_image)
        self.project_custom_widget_prefixes = []

    def setup_styles(self):
        s = ttk.Style(self)
        s.configure("TreeComponentPalette.Treeview", rowheight=30)

    def custom_filter(
        self, tree: ttk.Treeview, itemid: str, fvalue: str
    ) -> bool:
        txt = tree.item(itemid, "text").lower()
        match_found = fvalue in txt
        return match_found

    def on_filter_keypress(self, event=None):
        if self._keypress_cbid is not None:
            self.after_cancel(self._keypress_cbid)
        self._keypress_cbid = self.after(
            self.KEY_PRESS_CB_MILISECONDS, self._on_filter_keypress_after
        )

    def _on_filter_keypress_after(self, event=None):
        self.on_do_filter(event)
        self._cbid = None

    def on_do_filter(self, event=None):
        self.cptree.filter_by(self.filter_text_var.get())

    def on_filter_clear(self):
        self.filter_text_var.set("")
        self.cptree.filter_by("")

    def on_show_alltk(self):
        self.build_tree()

    def build_tree(self):
        self.visual_state.save()
        self.cptree.filter_remove()
        items = self.cptree.get_children()
        self.cptree.delete(*items)
        self.create_treeview_widget_list()
        self.cptree.filter_by(self.filter_text_var.get())
        self.visual_state.restore()

    def create_treelist(self):
        omit_tagset = {"tk", "ttk"}

        # create unique tag set
        tagset: set = set()
        for c in pygubu.builder.CLASS_MAP.keys():
            wc = pygubu.builder.CLASS_MAP[c]
            tagset.update((str(tag) for tag in wc.tags))
        tagset.difference_update(omit_tagset)

        # Put every class in defined sections
        treelist = []
        for c in pygubu.builder.CLASS_MAP.keys():
            wc = pygubu.builder.CLASS_MAP[c]

            is_tk_only = "tk" in wc.tags and "ttk" not in wc.tags
            if is_tk_only and not self.var_show_alltk.get():
                continue

            if wc.public is False:
                show_widget = False
                for prefix in self.project_custom_widget_prefixes:
                    if c.startswith(prefix):
                        show_widget = True
                        break
                if show_widget is False:
                    continue
            ctags = set((str(tag) for tag in wc.tags)) - omit_tagset
            sections = tagset & ctags
            for s in sections:
                treelist.append((s, wc))

        # sort tags by group and label
        def by_label(t):
            return f"{t[0]}{t[1].group}{t[1].label}"

        treelist.sort(key=by_label)
        return treelist

    def create_treeview_widget_list(self):
        treelist = self.create_treelist()
        widgetlisttv = self.cptree

        # Default widget image:
        default_image = ""
        try:
            default_image = StockImage.get("22x22-tk.default")
        except StockImageException:
            pass

        # Start building widget tree selector
        sections = {}
        for key, wc in treelist:
            section = key
            # insert section
            if section not in sections:
                sections[section] = widgetlisttv.insert(
                    "", "end", iid=hash(section), text=section
                )
            # insert widget
            w_image = default_image
            try:
                w_image = StockImage.get("22x22-{0}".format(wc.classname))
            except StockImageException:
                pass

            label = f" {wc.label}"
            widgetlisttv.insert(
                sections[section],
                "end",
                text=label,
                image=w_image,
                tags="widget",
                values=(wc.classname,),
            )
        widgetlisttv.tag_bind("widget", "<Double-1>", self.on_widgetlist_dclick)

    def on_widgetlist_dclick(self, event):
        tv = event.widget
        sel = tv.selection()
        if sel:
            item = sel[0]
            classname = tv.item(item, "values")[0]
            self.on_add_widget_event(classname)

    def on_add_widget_event(self, cname):
        if self.on_add_widget:
            self.on_add_widget(cname)
