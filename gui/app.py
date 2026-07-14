import customtkinter as ctk
from gui.deshboard import Dashboard

class App(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.title("CyberScope - Cybersecurity Tool")
        self.geometry("1000x700")
        ctk.set_appearance_mode(config.get("theme", "Dark"))
        ctk.set_default_color_theme("blue")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.dashboard = Dashboard(self, config)
        self.dashboard.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.mainloop()
