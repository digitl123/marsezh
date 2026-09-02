"""Подготовка обложек: срезаем леттербокс, кадрируем и вшиваем как data:URI."""
import base64, io, math, os

from PIL import Image, ImageEnhance

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
BG = (6, 6, 6)          # фон тёмной версии — виньетка растворяется точно в него


def trim_letterbox(im, thresh=1.0):
    """Срезает чёрные полосы сверху и снизу (видео 16:9 внутри вертикального кадра).

    Порог намеренно жёсткий: режем только строки, которые практически идеально
    чёрные, иначе у тёмных кадров срезается сама картинка. 16:9 внутри 9:16
    оставляет всего ~32 % высоты, поэтому нижняя граница проверки — 20 %.
    """
    g = im.convert("L")
    w, h = g.size
    rows = [sum(g.crop((0, y, w, y + 1)).getdata()) / w for y in range(h)]
    top = 0
    while top < h and rows[top] < thresh:
        top += 1
    bot = h - 1
    while bot > top and rows[bot] < thresh:
        bot -= 1
    if bot - top < h * 0.2:           # подозрительно мало — не трогаем
        return im
    return im.crop((0, top, w, bot + 1))


def enc(fname, box, quality=80, focus=0.5):
    """fname → data:URI JPEG, кадрированный по центру (focus — вертикальный центр кадра)."""
    im = trim_letterbox(Image.open(os.path.join(ASSETS, fname)).convert("RGB"))
    tw, th = box
    s = max(tw / im.width, th / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = max(0, min(im.height - th, round(im.height * focus - th / 2)))
    im = im.crop((left, top, left + tw, top + th))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def portrait(fname, box, crop=(0.0, 1.0), quality=86, brightness=1.0,
             cx=0.5, cy=0.58, rx=0.46, ry=0.60, inner=0.24, outer=0.84):
    """Портрет для героя: кадр вписывается по высоте в чёрное поле, периферия
    гасится виньеткой в чистый чёрный. Фон снимка тёмная комната, поэтому края
    растворяются прямо в #060606 — портрет «выплывает» из темноты, как
    вырезанное фото в референсе.
    """
    im = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
    top, bottom = crop
    im = im.crop((0, int(im.height * top), im.width, int(im.height * bottom)))
    tw, th = box
    k = th / im.height
    im = im.resize((max(1, round(im.width * k)), th), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)

    canvas = Image.new("RGB", (tw, th), BG)
    canvas.paste(im, ((tw - im.width) // 2, 0))

    mask = Image.new("L", (tw, th))
    px = mask.load()
    for y in range(th):
        dy = (y / th - cy) / ry
        for x in range(tw):
            dx = (x / tw - cx) / rx
            t = (math.sqrt(dx * dx + dy * dy) - inner) / (outer - inner)
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            px[x, y] = int(255 * (1 - t * t * (3 - 2 * t)))
    canvas = Image.composite(canvas, Image.new("RGB", (tw, th), BG), mask)

    buf = io.BytesIO()
    canvas.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
