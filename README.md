# Geometric Calculator

A Python desktop app to calculate properties of 2D and 3D shapes — area, perimeter, volume, and more — with a simple visual preview of each shape.

## Requirements

- Python 3.10+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
```bash
pip install customtkinter
```

## How to run
```bash
python main.py
```

## How to use

1. Pick a shape from the left panel
2. Choose an operation (area, perimeter, volume…)
3. Enter the values
4. Hit **Calculate** — the result appears below, and a drawing of the shape shows on the left

> Only numbers are accepted. Invalid inputs show a warning message.

## Project structure
```
project/
├── models/         # Shape classes (Rectangle, Circle, Triangle…)
├── view/           # GUI layout and logic
├── utils/          # Validators and constants
└── main.py         # Entry point
```

## Adding a new shape

1. Create a class in `models/`
2. Register it in `models/__init__.py`
3. Add its operations in `view/shape_data.py`
4. Optionally add a draw function in `view/calculator.py`