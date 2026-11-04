"""Вшивает background.jpg прямо в angelglass.css (data URI).

Нужно, если клиент не находит картинку по относительному пути.
Запуск (из папки темы):  python embed-background.py
Работает с background.jpg / .jpeg / .png.
"""
import base64
import mimetypes
import pathlib
import re
import sys

here = pathlib.Path(__file__).parent
img = next((p for n in ("background.jpg", "background.jpeg", "background.png")
            if (p := here / n).exists()), None)
if img is None:
    sys.exit("Положи картинку background.jpg рядом со скриптом.")

mime = mimetypes.guess_type(img.name)[0] or "image/jpeg"
data = base64.b64encode(img.read_bytes()).decode()
uri = f'url("data:{mime};base64,{data}")'

css_path = here / "angelglass.css"
css = css_path.read_text(encoding="utf-8")
css, n = re.subn(r'url\("(?:background\.[a-z]+|data:[^"]+)"\)', uri, css, count=1)
if n == 0:
    sys.exit("В angelglass.css не нашёл строку url(\"background.jpg\").")
css_path.write_text(css, encoding="utf-8")
print("Готово: картинка вшита в angelglass.css. Перезагрузи темы в TeamSpeak.")
