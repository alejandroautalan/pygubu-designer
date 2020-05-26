# encoding: utf-8


class LogPanelManager(object):
    def __init__(self, app):
        self.app = app
        builder = self.app.builder
        self.btn_messages = builder.get_object('btn_messages')
        self.txt_log = builder.get_object('txt_log')
        self.buttonsvar = builder.get_variable('bpanel_buttonsvar')
        self.bpanel = builder.get_object('bpanel')
        self.gcontainer = builder.get_object('bp_container')
        self.gbuttons = builder.get_object('bp_buttons')
        self.mainpw = builder.get_object('mainpw')
        self.mainpw.bind('<Configure>', self.pwindow_configure)
        self.mainpw_sash_pos = None
        self.gcontainer.pack_forget()
        self.btn_messages_label = self.btn_messages.cget('text')
        self.unread = 0

    def pwindow_configure(self, event):
        self.mainpw_sash_pos = None
        
    def update_sash(self, action='show'):
        pwh = self.mainpw.winfo_height()
        gch = self.bpanel.winfo_reqheight()
        gbh = self.gbuttons.winfo_height()
        newpos = pwh-gch
        hidden_pos = pwh - (gbh+5)
        if action == 'show':
            if self.mainpw_sash_pos is not None:
                if self.mainpw_sash_pos > hidden_pos:
                    self.mainpw_sash_pos = newpos
                newpos = self.mainpw_sash_pos
        elif action == 'hide':
            newpos = hidden_pos
            self.mainpw_sash_pos = self.mainpw.sashpos(0)
        self.mainpw.sashpos(0, newpos)
        
    def on_bpanel_button_clicked(self):
        #print(self.pwindow.sashpos(0))
        value = self.buttonsvar.get()
        if value == 'messages':
            self.unread = 0
            self.btn_messages.config(text=self.btn_messages_label)
            self.gcontainer.pack(side='top', expand=True, fill='both')
            self.gcontainer.after_idle(self.update_sash)
        else:
            self.gcontainer.after_idle(
                lambda x='hide':self.update_sash(x))
            self.gcontainer.pack_forget()
    
    def _log_set_text(self, text):
        tktext = self.txt_log
        tktext.config(state='normal')
        tktext.delete('0.0', 'end')
        tktext.insert('0.0', text)
        tktext.config(state='disabled')
    
    def _log_add_text(self, text):
        tktext = self.txt_log
        tktext.config(state='normal')
        tktext.insert('end', text+'\n')
        tktext.config(state='disabled')
        tktext.see('end')
    
    def log_message(self, msg, level):
        if self.buttonsvar.get() != 'messages':
            self.unread = self.unread + 1
            # log panel is not visible, update label
            label = '{0} ({1})'.format(self.btn_messages_label, self.unread)
            self.btn_messages.config(text=label)
        self._log_add_text(msg)
