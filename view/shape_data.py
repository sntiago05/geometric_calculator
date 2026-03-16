from models import (
    Rectangle, Circle, Triangle, RigthRectangle,
    Pentagon, Sphere, Parallelepiped, Cylinder, Cone,
)

FIGURAS_DISPONIBLES = [
    ("Rectangle",      Rectangle),
    ("Circle",         Circle),
    ("Triangle",       Triangle),
    ("Right Triangle", RigthRectangle),
    ("Pentagon",       Pentagon),
    ("Sphere",         Sphere),
    ("Parallelepiped", Parallelepiped),
    ("Cylinder",       Cylinder),
    ("Cone",           Cone),
]

ETIQUETA_DE_OPERACION = {
    "area":         "Area",
    "perimeter":    "Perimeter",
    "base":         "Base (from area)",
    "height":       "Height (from area)",
    "diameter":     "Diameter",
    "last_angle":   "Last angle",
    "hipotenuse":   "Hypotenuse",
    "last_leg":     "Last leg",
    "volume":       "Volume",
    "surface_area": "Surface area",
}



# Maps (shape_name, internal_op) → list of (var_name, display_label).
# var_name must match the model's __init__ parameter exactly.
# Example: ("Rectangle", "area") → [("width","Width"), ("height","Height")]
#   means: to calculate Rectangle area, show two fields: Width and Height
#   and pass them as Rectangle(width=..., height=...)
CAMPOS_POR_OPERACION = {
    
    ("Rectangle", "area"):         [("width",  "Width"),
                                    ("height", "Height")],
    ("Rectangle", "perimeter"):    [("width",  "Width"),
                                    ("height", "Height")],
    ("Rectangle", "base"):         [("area",   "Area"),
                                    ("height", "Height")],
    ("Rectangle", "height"):       [("area",   "Area"),
                                    ("width",  "Width")],

    ("Circle", "area"):            [("radius", "Radius")],
    ("Circle", "perimeter"):       [("radius", "Radius")],
    ("Circle", "diameter"):        [("radius", "Radius")],
    # 
    ("Triangle", "area"):          [("base",   "Base"),
                                    ("height", "Height")],
    ("Triangle", "perimeter"):     [("a",      "Side a"),
                                    ("b",      "Side b"),
                                    ("c",      "Side c")],
    ("Triangle", "last_angle"):    [("angle1", "Angle 1"),
                                    ("angle2", "Angle 2")],
    # 
    ("Right Triangle", "area"):       [("adjacent",  "Adjacent"),
                                       ("opposite",  "Opposite")],
    ("Right Triangle", "perimeter"):  [("adjacent",  "Adjacent"),
                                       ("opposite",  "Opposite"),
                                       ("hipotenuse","Hypotenuse")],
    ("Right Triangle", "hipotenuse"): [("adjacent",  "Adjacent"),
                                       ("opposite",  "Opposite")],
    ("Right Triangle", "last_angle"): [("angle",     "Known angle")],
    # 
    ("Pentagon", "area"):          [("side", "Side")],
    ("Pentagon", "perimeter"):     [("side", "Side")],
    # 
    ("Sphere", "volume"):          [("radius", "Radius")],
    ("Sphere", "surface_area"):    [("radius", "Radius")],
    #
    ("Parallelepiped", "volume"):       [("length", "Length"),
                                         ("width",  "Width"),
                                         ("height", "Height")],
    ("Parallelepiped", "surface_area"): [("length", "Length"),
                                         ("width",  "Width"),
                                         ("height", "Height")],
    #
    ("Cylinder", "volume"):        [("radius", "Radius"),
                                    ("height", "Height")],
    ("Cylinder", "surface_area"):  [("radius", "Radius"),
                                    ("height", "Height")],
    # 
    ("Cone", "volume"):            [("radius", "Radius"),
                                    ("height", "Height")],
    ("Cone", "surface_area"):      [("radius", "Radius"),
                                    ("height", "Height")],
}


# ── OPERACIONES_POR_FIGURA ────────────────────────────────────────────────────
# Built dynamically by combining the three dictionaries above.
#
# Final structure:
# {
#   "Rectangle": {
#       "Area":             [("width",  "Width"), ("height", "Height")],
#       "Perimeter":        [("width",  "Width"), ("height", "Height")],
#       "Base (from area)": [("area",   "Area"),  ("height", "Height")],
#       "Height (from area)":[("area",  "Area"),  ("width",  "Width")],
#   },
#   "Circle": {
#       "Area":      [("radius", "Radius")],
#       "Perimeter": [("radius", "Radius")],
#       "Diameter":  [("radius", "Radius")],
#   },
#   ... one entry per shape
# }

OPERACIONES_POR_FIGURA: dict[str, dict[str, list]] = {}

for nombre_figura, clase_modelo in FIGURAS_DISPONIBLES:
    # Instantiate with no args just to read available_operations
    # e.g. Rectangle() → available_operations = ["area", "perimeter", "base", "height"]
    instancia_temporal = clase_modelo()

    # Empty dict that will hold {display_label: [fields]} for this shape
    operaciones_de_esta_figura = {}

    for nombre_op_interno in instancia_temporal.available_operations:
        # Translate internal name to display label
        # e.g. "area" → "Area",  "surface_area" → "Surface area"
        label_bonito = ETIQUETA_DE_OPERACION.get(nombre_op_interno)

        # Build the key used to look up fields in CAMPOS_POR_OPERACION
        # e.g. ("Rectangle", "area")
        clave_campos = (nombre_figura, nombre_op_interno)

        # Only include if both the label and the fields are defined.
        # This guards against operations that exist in the model
        # but haven't been wired up in the UI yet.
        if label_bonito and clave_campos in CAMPOS_POR_OPERACION:
            # e.g. operaciones_de_esta_figura["Area"] = [("width","Width"),("height","Height")]
            operaciones_de_esta_figura[label_bonito] = CAMPOS_POR_OPERACION[clave_campos]

    # Store the completed dict for this shape
    # e.g. OPERACIONES_POR_FIGURA["Rectangle"] = {"Area": [...], "Perimeter": [...], ...}
    OPERACIONES_POR_FIGURA[nombre_figura] = operaciones_de_esta_figura
