import tkinter as tk

from view.colors import (
    COLOR_ACENTO,
    COLOR_DIBUJO_RELLENO,
    COLOR_DIBUJO_BORDE,
    COLOR_DIBUJO_TEXTO,
)
from view.shape_data import ETIQUETA_DE_OPERACION, FIGURAS_DISPONIBLES


def ejecutar_calculo(nombre_figura: str, label_operacion: str, valores: dict) -> float:
    """
    Instantiates the model class and calls the matching calculate method.
    Example: ejecutar_calculo("Rectangle", "Area", {"width":5, "height":3}) → 15.0
    """
    
    nombre_op_interno = next(
        (k for k, v in ETIQUETA_DE_OPERACION.items() if v == label_operacion), None
    )
    if not nombre_op_interno:
        raise ValueError(f"Operation '{label_operacion}' not found in mapping")

    clase_modelo = next(
        (cls for name, cls in FIGURAS_DISPONIBLES if name == nombre_figura), None
    )
    if not clase_modelo:
        raise ValueError(f"Shape '{nombre_figura}' not found")

    
    instancia = clase_modelo(**valores)

    # "area" → "calculate_area"
    nombre_metodo = f"calculate_{nombre_op_interno}"
    metodo = getattr(instancia, nombre_metodo, None)
    if not metodo:
        raise ValueError(
            f"Method '{nombre_metodo}' not found in {clase_modelo.__name__}"
        )

    return metodo()

def dibujar_rectangulo(canvas: tk.Canvas):
    """Draws a rectangle with width and height labels."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    x1, y1, x2, y2 = w * 0.15, h * 0.25, w * 0.85, h * 0.75
    canvas.create_rectangle(
        x1, y1, x2, y2, fill=COLOR_DIBUJO_RELLENO, outline=COLOR_DIBUJO_BORDE, width=2
    )
    canvas.create_text(
        (x1 + x2) / 2, y2 + 14, text="width", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 9)
    )
    canvas.create_text(
        x2 + 18,
        (y1 + y2) / 2,
        text="height",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 9),
    )
    canvas.create_line(
        x1, y2 + 6, x2, y2 + 6, fill=COLOR_ACENTO, width=1, arrow=tk.BOTH
    )
    canvas.create_line(
        x2 + 6, y1, x2 + 6, y2, fill=COLOR_ACENTO, width=1, arrow=tk.BOTH
    )


def dibujar_circulo(canvas: tk.Canvas):
    """Draws a circle with radius line."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    cx, cy = w / 2, h / 2
    r = min(w, h) * 0.35
    canvas.create_oval(
        cx - r,
        cy - r,
        cx + r,
        cy + r,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_line(cx, cy, cx + r, cy, fill=COLOR_ACENTO, width=2)
    canvas.create_text(
        cx + r / 2,
        cy - 10,
        text="r",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )
    canvas.create_oval(
        cx - 3, cy - 3, cx + 3, cy + 3, fill=COLOR_ACENTO, outline=COLOR_ACENTO
    )


def dibujar_triangulo(canvas: tk.Canvas):
    """Draws an isosceles triangle with base and height."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    puntos = [w * 0.5, h * 0.1, w * 0.1, h * 0.85, w * 0.9, h * 0.85]
    canvas.create_polygon(
        puntos, fill=COLOR_DIBUJO_RELLENO, outline=COLOR_DIBUJO_BORDE, width=2
    )
    canvas.create_text(
        w * 0.5, h * 0.92, text="base", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )
    canvas.create_text(
        w * 0.25, h * 0.52, text="a", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )
    canvas.create_text(
        w * 0.75, h * 0.52, text="c", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )
    canvas.create_line(
        w * 0.5, h * 0.1, w * 0.5, h * 0.85, fill=COLOR_ACENTO, width=1, dash=(4, 4)
    )
    canvas.create_text(
        w * 0.57, h * 0.48, text="h", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )


def dibujar_triangulo_rectangulo(canvas: tk.Canvas):
    """Draws a right triangle with legs and hypotenuse."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    ax, ay = w * 0.15, h * 0.85
    bx, by = w * 0.15, h * 0.15
    cx2, cy2 = w * 0.85, h * 0.85
    puntos = [ax, ay, bx, by, cx2, cy2]
    canvas.create_polygon(
        puntos, fill=COLOR_DIBUJO_RELLENO, outline=COLOR_DIBUJO_BORDE, width=2
    )
    sq = 10
    canvas.create_rectangle(
        ax, ay - sq, ax + sq, ay, outline=COLOR_ACENTO, fill="", width=1
    )
    canvas.create_text(
        ax - 18, (ay + by) / 2, text="opp", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )
    canvas.create_text(
        (ax + cx2) / 2, ay + 14, text="adj", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 8)
    )
    canvas.create_text(
        (bx + cx2) / 2 + 10,
        (by + cy2) / 2 - 10,
        text="hyp",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 8),
    )


def dibujar_pentagono(canvas: tk.Canvas):
    """Draws a regular pentagon with one side highlighted."""
    import math

    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    cx, cy = w / 2, h / 2
    r = min(w, h) * 0.38
    puntos = []
    for i in range(5):
        angulo = math.pi / 2 + 2 * math.pi * i / 5
        puntos.extend([cx + r * math.cos(angulo), cy - r * math.sin(angulo)])
    canvas.create_polygon(
        puntos, fill=COLOR_DIBUJO_RELLENO, outline=COLOR_DIBUJO_BORDE, width=2
    )
    canvas.create_line(
        puntos[0], puntos[1], puntos[2], puntos[3], fill=COLOR_ACENTO, width=2
    )
    canvas.create_text(
        cx, cy + r + 16, text="side", fill=COLOR_DIBUJO_TEXTO, font=("Arial", 9)
    )


def dibujar_esfera(canvas: tk.Canvas):
    """Draws a sphere with radius and equatorial ellipse."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    cx, cy = w / 2, h / 2
    r = min(w, h) * 0.35
    canvas.create_oval(
        cx - r,
        cy - r,
        cx + r,
        cy + r,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_oval(
        cx - r,
        cy - r * 0.25,
        cx + r,
        cy + r * 0.25,
        fill="",
        outline=COLOR_DIBUJO_BORDE,
        width=1,
        dash=(4, 4),
    )
    canvas.create_line(cx, cy, cx + r, cy, fill=COLOR_ACENTO, width=2)
    canvas.create_text(
        cx + r / 2,
        cy - 12,
        text="r",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )
    canvas.create_oval(
        cx - 3, cy - 3, cx + 3, cy + 3, fill=COLOR_ACENTO, outline=COLOR_ACENTO
    )


def dibujar_paralelepipedo(canvas: tk.Canvas):
    """Draws a parallelepiped in isometric perspective."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    ox, oy = w * 0.2, h * 0.55
    bw, bh, d = w * 0.45, h * 0.35, w * 0.18
    dy = d * 0.5
    canvas.create_polygon(
        ox,
        oy,
        ox + bw,
        oy,
        ox + bw,
        oy + bh,
        ox,
        oy + bh,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_polygon(
        ox,
        oy,
        ox + d,
        oy - dy,
        ox + bw + d,
        oy - dy,
        ox + bw,
        oy,
        fill="#1a3050",
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_polygon(
        ox + bw,
        oy,
        ox + bw + d,
        oy - dy,
        ox + bw + d,
        oy + bh - dy,
        ox + bw,
        oy + bh,
        fill="#152840",
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_text(
        (ox + ox + bw) / 2,
        oy + bh + 14,
        text="length",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 8),
    )
    canvas.create_text(
        ox - 22,
        (oy + oy + bh) / 2,
        text="h",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 9),
    )
    canvas.create_text(
        ox + bw + d / 2 + 8,
        oy - dy - 8,
        text="w",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 9),
    )


def dibujar_cilindro(canvas: tk.Canvas):
    """Draws a cylinder with radius and height."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    cx = w / 2
    rw, rh = w * 0.32, h * 0.12
    top_y, bot_y = h * 0.18, h * 0.78
    canvas.create_rectangle(
        cx - rw,
        top_y,
        cx + rw,
        bot_y,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_oval(
        cx - rw,
        bot_y - rh,
        cx + rw,
        bot_y + rh,
        fill="#152840",
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_oval(
        cx - rw,
        top_y - rh,
        cx + rw,
        top_y + rh,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_line(cx, top_y, cx + rw, top_y, fill=COLOR_ACENTO, width=2)
    canvas.create_text(
        cx + rw / 2,
        top_y - 12,
        text="r",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )
    canvas.create_line(
        cx + rw + 8,
        top_y,
        cx + rw + 8,
        bot_y,
        fill=COLOR_ACENTO,
        width=1,
        arrow=tk.BOTH,
    )
    canvas.create_text(
        cx + rw + 22,
        (top_y + bot_y) / 2,
        text="h",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )


def dibujar_cono(canvas: tk.Canvas):
    """Draws a cone with radius and height."""
    canvas.delete("all")
    w, h = canvas.winfo_width() or 200, canvas.winfo_height() or 160
    cx = w / 2
    apex_y, base_y = h * 0.1, h * 0.82
    rw, rh = w * 0.35, h * 0.08
    canvas.create_polygon(
        cx,
        apex_y,
        cx - rw,
        base_y,
        cx + rw,
        base_y,
        fill=COLOR_DIBUJO_RELLENO,
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_oval(
        cx - rw,
        base_y - rh,
        cx + rw,
        base_y + rh,
        fill="#152840",
        outline=COLOR_DIBUJO_BORDE,
        width=2,
    )
    canvas.create_line(cx, apex_y, cx, base_y, fill=COLOR_ACENTO, width=1, dash=(4, 4))
    canvas.create_text(
        cx + 10,
        (apex_y + base_y) / 2,
        text="h",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )
    canvas.create_line(cx, base_y, cx + rw, base_y, fill=COLOR_ACENTO, width=2)
    canvas.create_text(
        cx + rw / 2,
        base_y - 12,
        text="r",
        fill=COLOR_DIBUJO_TEXTO,
        font=("Arial", 10, "bold"),
    )


FUNCION_DIBUJO = {
    "Rectangle": dibujar_rectangulo,
    "Circle": dibujar_circulo,
    "Triangle": dibujar_triangulo,
    "Right Triangle": dibujar_triangulo_rectangulo,
    "Pentagon": dibujar_pentagono,
    "Sphere": dibujar_esfera,
    "Parallelepiped": dibujar_paralelepipedo,
    "Cylinder": dibujar_cilindro,
    "Cone": dibujar_cono,
}
