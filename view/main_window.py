import tkinter as tk
import customtkinter as ctk

from view.colors import (
    COLOR_FONDO_PRINCIPAL,
    COLOR_FONDO_PANEL_IZQ,
    COLOR_FONDO_PAGINA,
    COLOR_ACENTO,
    COLOR_BOTON_INACTIVO,
    COLOR_BOTON_HOVER,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_FONDO_RESULTADO,
)
from view.shape_data import (
    FIGURAS_DISPONIBLES,
    OPERACIONES_POR_FIGURA,
    VALIDADORES_POR_FIGURA,
)
from view.calculator import ejecutar_calculo, FUNCION_DIBUJO
from utils.validators import validar_entry


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ShapePage(ctk.CTkFrame):
    """One page per shape: canvas on the left, controls on the right."""

    def __init__(self, parent, nombre_figura: str):
        super().__init__(parent, fg_color=COLOR_FONDO_PAGINA, corner_radius=15)
        self.nombre_figura = nombre_figura
        self.operaciones_disponibles = OPERACIONES_POR_FIGURA[nombre_figura]
        self.validate_cmmd = (self.register(validar_entry), "%P")
        self.campos_activos: dict[str, ctk.CTkEntry] = {}
        self._construir_layout()

    def _construir_layout(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self._construir_canvas()
        self._construir_panel_controles()

    def _construir_canvas(self):
        self.canvas_figura = tk.Canvas(
            self,
            bg=COLOR_FONDO_PAGINA,
            highlightthickness=0,
        )
        self.canvas_figura.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        self.canvas_figura.bind("<Configure>", self._redibujar_figura)

    def _redibujar_figura(self, event=None):
        funcion = FUNCION_DIBUJO.get(self.nombre_figura)
        if funcion:
            funcion(self.canvas_figura)

    def _construir_panel_controles(self):
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text=self.nombre_figura,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_ACENTO,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        ctk.CTkLabel(
            panel,
            text="Operation",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w",
        ).grid(row=1, column=0, sticky="w")

        self.combo_operaciones = ctk.CTkComboBox(
            panel,
            values=list(self.operaciones_disponibles.keys()),
            command=self._al_cambiar_operacion,
            fg_color=COLOR_BOTON_INACTIVO,
            border_color=COLOR_ACENTO,
            button_color=COLOR_ACENTO,
            button_hover_color=COLOR_BOTON_HOVER,
            text_color=COLOR_TEXTO_PRINCIPAL,
            dropdown_fg_color=COLOR_FONDO_PANEL_IZQ,
            dropdown_text_color=COLOR_TEXTO_PRINCIPAL,
            dropdown_hover_color=COLOR_BOTON_HOVER,
            width=260,
        )
        self.combo_operaciones.grid(row=2, column=0, sticky="w", pady=(4, 12))

        ctk.CTkFrame(panel, height=1, fg_color=COLOR_ACENTO).grid(
            row=3, column=0, sticky="ew", pady=(0, 12)
        )

        # Rebuilt every time the operation changes
        self.frame_campos = ctk.CTkFrame(panel, fg_color="transparent")
        self.frame_campos.grid(row=4, column=0, sticky="nsew", pady=20)
        self.frame_campos.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            panel,
            text="Calculate",
            command=self._al_calcular,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_BOTON_HOVER,
            text_color="#0d2a5c",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            height=40,
            cursor="hand2",
        ).grid(row=5, column=0, sticky="ew", pady=(16, 10))

        self.label_resultado = ctk.CTkLabel(
            panel,
            text="Result will appear here",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLOR_FONDO_RESULTADO,
            text_color=COLOR_TEXTO_PRINCIPAL,
            corner_radius=10,
            width=260,
            height=44,
            wraplength=250,  
            justify="left",  
            anchor="center",
        )
        self.label_resultado.grid(row=6, column=0, sticky="w", pady=(0, 8))

        primera_operacion = list(self.operaciones_disponibles.keys())[0]
        self._al_cambiar_operacion(primera_operacion)

    def _al_cambiar_operacion(self, operacion_seleccionada: str):
        """Destroys old fields and builds new ones for the selected operation."""
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_activos.clear()

        campos_necesarios = self.operaciones_disponibles.get(operacion_seleccionada, [])

        for fila_idx, (var_name, label_texto) in enumerate(campos_necesarios):
            ctk.CTkLabel(
                self.frame_campos,
                text=label_texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=COLOR_TEXTO_SECUNDARIO,
                width=90,
                anchor="w",
            ).grid(row=fila_idx, column=0, sticky="w", pady=5)

            campo_entrada = ctk.CTkEntry(
                self.frame_campos,
                placeholder_text=f"Enter {label_texto.lower()}",
                fg_color=COLOR_BOTON_INACTIVO,
                border_color="#3a5a8a",
                text_color=COLOR_TEXTO_PRINCIPAL,
                placeholder_text_color=COLOR_TEXTO_SECUNDARIO,
                height=34,
                validate="key",
                validatecommand=self.validate_cmmd,
            )
            campo_entrada.grid(
                row=fila_idx, column=1, sticky="ew", padx=(10, 0), pady=5
            )
            self.campos_activos[var_name] = campo_entrada

        self.label_resultado.configure(text="Result will appear here")

    def _al_calcular(self):
        """Reads fields, validates input, runs calculation, shows result."""
        operacion_actual = self.combo_operaciones.get()
        valores_ingresados = {}

        for var_name, campo_entrada in self.campos_activos.items():
            texto_ingresado = campo_entrada.get().strip()
            try:
                valores_ingresados[var_name] = float(texto_ingresado)
                print(var_name)
            except ValueError:
                self.label_resultado.configure(text=f"⚠  '{var_name}' must be a number")
                return
        validador = VALIDADORES_POR_FIGURA.get(self.nombre_figura)
        if validador:
            valido, mensaje = validador(valores_ingresados)
        if not valido:
            self.label_resultado.configure(text=mensaje)
            return

        try:
            resultado = ejecutar_calculo(
                self.nombre_figura, operacion_actual, valores_ingresados
            )
            self.label_resultado.configure(
                text=f"{operacion_actual}  =  {resultado:.4f}"
            )
        except Exception as error:
            self.label_resultado.configure(text=f"Error: {error}")


class MainWindow(ctk.CTk):
    """Main window: left nav panel + right ShapePage panel."""

    def __init__(self):
        super().__init__(fg_color=COLOR_FONDO_PRINCIPAL)
        self.title("Geometric Calculator")
        self.geometry("960x640")
        self.resizable(True, True)

        self.boton_activo: ctk.CTkButton | None = None
        self.paginas: dict[str, ShapePage] = {}
        self.botones_nav: dict[str, ctk.CTkButton] = {}

        self._construir_layout()
        self._cambiar_figura("Rectangle")

    def _construir_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._construir_panel_navegacion()
        self._construir_panel_figuras()

    def _construir_panel_navegacion(self):
        panel_nav = ctk.CTkFrame(
            self,
            fg_color=COLOR_FONDO_PANEL_IZQ,
            corner_radius=15,
            width=200,
        )
        panel_nav.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        panel_nav.grid_propagate(False)
        panel_nav.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_nav,
            text="Shapes",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).grid(row=0, column=0, padx=14, pady=(18, 8), sticky="w")

        for indice, (nombre_figura, _) in enumerate(FIGURAS_DISPONIBLES):
            boton = ctk.CTkButton(
                panel_nav,
                text=nombre_figura,
                command=lambda nombre=nombre_figura: self._cambiar_figura(nombre),
                fg_color=COLOR_BOTON_INACTIVO,
                hover_color=COLOR_BOTON_HOVER,
                text_color=COLOR_TEXTO_PRINCIPAL,
                anchor="w",
                corner_radius=10,
                height=42,
                cursor="hand2",
                font=ctk.CTkFont(size=12),
            )
            boton.grid(row=indice + 1, column=0, padx=10, pady=3, sticky="ew")
            self.botones_nav[nombre_figura] = boton

    def _construir_panel_figuras(self):
        panel_figuras = ctk.CTkFrame(self, fg_color="transparent")
        panel_figuras.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        panel_figuras.grid_columnconfigure(0, weight=1)
        panel_figuras.grid_rowconfigure(0, weight=1)

        for nombre_figura, _ in FIGURAS_DISPONIBLES:
            pagina = ShapePage(panel_figuras, nombre_figura)
            pagina.grid(row=0, column=0, sticky="nsew")
            pagina.grid_remove()
            self.paginas[nombre_figura] = pagina

    def _cambiar_figura(self, nombre_figura: str):
        """Shows the selected shape page and updates nav button styles."""
        for pagina in self.paginas.values():
            pagina.grid_remove()

        self.paginas[nombre_figura].grid()

        for nombre, boton in self.botones_nav.items():
            if nombre == nombre_figura:
                boton.configure(
                    fg_color=COLOR_ACENTO,
                    text_color="#0d2a5c",
                    font=ctk.CTkFont(size=12, weight="bold"),
                )
            else:
                boton.configure(
                    fg_color=COLOR_BOTON_INACTIVO,
                    text_color=COLOR_TEXTO_PRINCIPAL,
                    font=ctk.CTkFont(size=12, weight="normal"),
                )
