import customtkinter as ctk

class InfoCard(ctk.CTkFrame):
    """
    એક નાનું માહિતી આપતું કાર્ડ (જેમ કે IP, Domain, Status બતાવવા માટે)
    """
    def __init__(self, parent, title: str, value: str = "N/A", icon: str = "ℹ️", **kwargs):
        super().__init__(
            parent, 
            corner_radius=10, 
            fg_color=("#F3F4F6", "#1E293B"), 
            border_width=1, 
            border_color=("#E5E7EB", "#334155"),
            **kwargs
        )
        self.grid_columnconfigure(1, weight=1)

        # Icon Label
        self.icon_label = ctk.CTkLabel(self, text=icon, font=("Segoe UI", 20))
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=10)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self, 
            text=title, 
            font=("Segoe UI", 11, "bold"), 
            text_color=("#6B7280", "#9CA3AF")
        )
        self.title_label.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(8, 0))

        # Value Label
        self.value_label = ctk.CTkLabel(
            self, 
            text=value, 
            font=("Consolas", 12, "bold"), 
            text_color=("#1F2937", "#F8FAFC")
        )
        self.value_label.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 8))

    def update_value(self, new_value: str):
        """કાર્ડની વેલ્યુ અપડેટ કરવા માટે"""
        self.value_label.configure(text=new_value)


class StatusBadge(ctk.CTkFrame):
    """
    સ્ટેટસ બતાવવા માટેનું નાનું બેજ (જેમ કે Secure, Risk, Active)
    """
    def __init__(self, parent, text: str = "INFO", status_type: str = "info", **kwargs):
        
        # Color schemes based on status
        colors = {
            "success": ("#DEF7EC", "#03543F", "#0E9F6E"),
            "warning": ("#FEF08A", "#713F12", "#EAB308"),
            "danger":  ("#FDE8E8", "#9B1C1C", "#F05252"),
            "info":    ("#E1EFFE", "#1E429F", "#3F83F8")
        }
        bg_light, text_dark, border_col = colors.get(status_type, colors["info"])

        super().__init__(
            parent, 
            corner_radius=12, 
            fg_color=bg_light, 
            border_width=1, 
            border_color=border_col,
            **kwargs
        )

        self.label = ctk.CTkLabel(
            self, 
            text=text.upper(), 
            font=("Segoe UI", 10, "bold"), 
            text_color=text_dark
        )
        self.label.pack(padx=8, pady=2)


class SectionHeader(ctk.CTkFrame):
    """
    ડેશબોર્ડમાં વિભાગો અલગ પાડવા માટેનું સ્ટાઇલિશ સેક્શન હેડર
    """
    def __init__(self, parent, title: str, icon: str = "📌", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self, 
            text=f"{icon}  {title}", 
            font=("Segoe UI", 14, "bold"), 
            text_color=("#111827", "#38BDF8")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=(5, 10))

        self.separator = ctk.CTkFrame(self, height=2, fg_color=("#D1D5DB", "#334155"))
        self.separator.grid(row=0, column=1, sticky="ew", padx=(0, 5))
