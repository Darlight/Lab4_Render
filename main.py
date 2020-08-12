"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

lab4.py
Proposito: Un framebuffer simple para pintar un punto con modificaciones simples como:
- Cambiar de color de los puntos
- Crear un punto
- Modificaciones del tamaño de la venta principal
"""
from pathlib import Path
from tezt import Render
import os

dir_path = os.path.dirname(os.path.realpath( __file__))
model_path = os.path.join(dir_path, r'Models\wario.obj')

bitmap = Render()
bitmap.glCreateWindow()
print(bitmap.glInit())

bitmap.load(model_path, translate=(450, 225, 50), scale = (110, 110, 75))
bitmap.glFinish('output.bmp')