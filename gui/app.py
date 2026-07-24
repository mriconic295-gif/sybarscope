import customtkinter as ctk
from gui.deshboard import SecurityDashboard as Dashboard

class App(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config

        # 🌟 Window Configuration
        self.title("🛡️ CyberScope - Advanced Threat Recon & Intelligence")
        self.geometry("1100x750")
        self.minsize(950, 650)

        # 🎨 Theme Settings
        ctk.set_appearance_mode(config.get("theme", "Dark"))
        ctk.set_default_color_theme("blue")

        # 📐 Main Grid Layout Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 🚀 Build UI Components
        self.build_sidebar()
        self.build_main_container()

    def build_sidebar(self):
        """ડાબી બાજુની ક્રેઝી અને પ્રોફેશનલ સાઈડબાર"""
        self.sidebar = ctk.CTkFrame(
            self, 
            width=220, 
            corner_radius=0, 
            fg_color=("#E5E7EB", "#111827")  # Deep Cyber Blue/Dark
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        # 🏷️ App Title / Brand
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="⚡ CYBERSCOPE", 
            font=("Consolas", 22, "bold"),
            text_color=("#1F2937", "#38BDF8")  # Cyan Accent
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar, 
            text="v2.5 Recon Suite", 
            font=("Segoe UI", 11, "italic"),
            text_color=("#6B7280", "#9CA3AF")
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 25))

        # 🔘 Navigation Buttons
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="🔍 Recon Dashboard",
            font=("Segoe UI", 13, "bold"),
            height=40,
            corner_radius=10,
            fg_color=("#3B82F6", "#1D4ED8"),
            hover_color=("#2563EB", "#1E40AF"),
            anchor="w"
        )
        self.btn_dashboard.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        # 🌗 Theme Switcher (Dark / Light Toggle)
        self.theme_label = ctk.CTkLabel(
            self.sidebar, 
            text="🎨 Appearance Mode:", 
            font=("Segoe UI", 11, "bold")
        )
        self.theme_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")

        self.theme_switch = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light", "System"],
            font=("Segoe UI", 11),
            dropdown_font=("Segoe UI", 11),
            command=self.change_theme
        )
        self.theme_switch.set(self.config.get("theme", "Dark"))
        self.theme_switch.grid(row=7, column=0, padx=15, pady=(5, 20), sticky="ew")

    def build_main_container(self):
        """મુખ્ય ડેશબોર્ડ કન્ટેનર"""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Dashboard View
        self.dashboard = Dashboard(self.main_container, self.config)
        self.dashboard.grid(row=0, column=0, sticky="nsew")

    def change_theme(self, new_mode: str):
        """થિમ બદલવા માટેનું ફંક્શન"""
        ctk.set_appearance_mode(new_mode)

    def run(self):
        self.mainloop()
