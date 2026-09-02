#!/usr/bin/env python3
"""Собирает тёмную версию: index-dark.html (файл) и artifact-dark.html (для публикации)."""
import html, os

import base64

from imgutil import ASSETS, enc, portrait


def asset_uri(fname, mime):
    with open(os.path.join(ASSETS, fname), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

ROOT = os.path.dirname(os.path.abspath(__file__))

IC_IG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.06 1.8.25 2.23.42.56.21.96.47 1.38.89'
         '.42.42.68.82.9 1.38.16.43.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85'
         'c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.43.16-1.06.36'
         '-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22'
         '-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.17-.43-.36-1.06-.42-2.23C2.17 15.58 2.16 15.2'
         ' 2.16 12s.01-3.58.07-4.85c.06-1.17.25-1.8.42-2.23.21-.56.47-.96.89-1.38.42-.42.82-.68'
         ' 1.38-.89.43-.17 1.06-.36 2.23-.42C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07'
         'S4.9.33 4.14.63a5.9 5.9 0 0 0-2.13 1.38A5.9 5.9 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01'
         ' 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91a5.9 5.9 0 0 0 1.38 2.13 5.9'
         ' 5.9 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27'
         '-.06 2.15-.26 2.91-.56a5.9 5.9 0 0 0 2.13-1.38 5.9 5.9 0 0 0 1.38-2.13c.3-.76.5-1.64.56'
         '-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0'
         ' 0-1.38-2.13A5.9 5.9 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0z"/>'
         '<path d="M12 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zM12 16a4 4 0 1 1 4-4'
         ' 4 4 0 0 1-4 4z"/><circle cx="18.41" cy="5.59" r="1.44"/></svg>')
IC_TT = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.59 2.59'
         ' 0 1 1 .77-5.06V9.69a5.67 5.67 0 0 0-.77-.05A5.66 5.66 0 1 0 15.54 15.3V8.78a7.35 7.35'
         ' 0 0 0 4.3 1.38V7.07a4.29 4.29 0 0 1-3.24-1.25z"/></svg>')
IC_TG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M21.94 4.4 18.9 19.1c-.23 1.02-.84 1.27-1.7.79l-4.7-3.46-2.27 2.18c-.25.25-.46.46'
         '-.95.46l.34-4.8 8.73-7.9c.38-.34-.08-.53-.59-.19L6.98 12.98 2.34 11.5c-1.01-.32-1.03-1.01'
         '.21-1.5l18.13-6.99c.84-.31 1.58.2 1.26 1.39z"/></svg>')


# три обложки под заголовком — аналог ряда скриншотов проектов в референсе
HERO_THUMBS = [
    ("ig_3600000_DclMpHksZb6.jpg", "3,6 млн"),
    ("ig_1200000_DcGW1ZSM9k7.jpg", "1,2 млн"),
    ("ig_501000_DcLhRE6sA91.jpg",  "501 тыс."),
]

WORKS = [
    ("ig_3600000_DclMpHksZb6.jpg", "3,6 млн",  "Легендарные мемы",       "Мемы · один промт",       "мемы"),
    ("ig_1200000_DcGW1ZSM9k7.jpg", "1,2 млн",  "Новости Алматы",         "Фейк-новость · кино",     "фейк-новости"),
    ("ig_911000_DcqcrDaMzgG.jpg",  "911 тыс.", "Легендарные мемы, ч. 3", "Мемы · серия",            "мемы"),
    ("ig_900000_DcnzdYGMuPB.jpg",  "900 тыс.", "Легендарные мемы, ч. 2", "Мемы · серия",            "мемы"),
    ("ig_535000_DX_1EtdsjtI.jpg",  "535 тыс.", "Сцена у моря",           "Кинематографика",         "кино"),
    ("ig_501000_DcLhRE6sA91.jpg",  "501 тыс.", "Новости UFC",            "Фейк-новость · спорт",    "фейк-новости"),
    ("ig_318000_Dcs8TVGsKcM.jpg",  "318 тыс.", "Школьные мемы",          "Мемы · к 1 сентября",     "мемы"),
    ("ig_38000_DciyxYPsQmu.jpg",   "38 тыс.",  "Одна камера",            "Тутор · несколько ракурсов", "тутор"),
    ("ig_31900_DcYbTYnMh3q.jpg",   "31,9 тыс.", "Коллаборация",          "Интеграция · блогер",     "коллаба"),
    ("ig_31700_DceGaxhM6HP.jpg",   "31,7 тыс.", "26 дней",               "Кинематографика",         "кино"),
    ("ig_25400_DcOH6UjMASZ.jpg",   "25,4 тыс.", "Стадионный концерт",    "Кино · которого не было", "кино"),
    ("ig_25000_DbqeWKVMHh-.jpg",   "25 тыс.",  "Вьетнам без работы",     "Кино · тревел",           "кино"),
]

IG_URL = "https://www.instagram.com/marsezh.ai/"
# ЗАМЕНИТЬ на реальную ссылку гугл-формы, когда Марсэж её пришлёт
FORM_URL = "https://forms.gle/"

# бегущая строка: половина дублируется, чтобы петля была бесшовной
TICKER = ["21,9 млн просмотров", "мемы", "фейк-новости", "4,4 млн на одном ролике",
          "кино", "коллаборации", "туторы бесплатно", "16,5 тыс. подписчиков"]
HOT = {"21,9 млн просмотров", "4,4 млн на одном ролике", "16,5 тыс. подписчиков"}


def ticker_html():
    half = "".join(
        f'<span class="{"hot" if t in HOT else ""}">{html.escape(t)}</span><i></i>'
        for t in TICKER
    )
    return half + half


def thumbs_html():
    return "\n          ".join(
        f'<a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Ролик, {views} просмотров">'
        f'<img src="{enc(f, (300, 467), 78)}" alt="" loading="lazy"><span>{views}</span></a>'
        for f, views in HERO_THUMBS
    )


def works_html():
    out = []
    for fname, views, title, sub, tag in WORKS[:6]:
        out.append(
            f'<a class="work" href="{IG_URL}" target="_blank" rel="noopener">'
            '<span class="shot">'
            f'<img src="{enc(fname, (460, 818), 79)}" alt="{html.escape(title)}" loading="lazy">'
            f'<span class="tag">{html.escape(tag)}</span>'
            f'<span class="views tnum">{views}</span>'
            '</span>'
            '<span class="meta"><span>'
            f'<b>{html.escape(title)}</b><span>{html.escape(sub)}</span>'
            '</span><span class="watch">Смотреть</span></span></a>'
        )
    return "\n        ".join(out)


tpl = open(os.path.join(ROOT, "template-dark.html"), encoding="utf-8").read()
tpl = tpl.replace("{{HERO_PHOTO}}",
                  portrait("ig_12700_Db8Ijaesk4h.jpg", (1060, 900), crop=(0.12, 0.62),
                            cx=0.52, cy=0.62, rx=0.44, ry=0.60, inner=0.20, outer=0.80))
tpl = tpl.replace("{{HERO_THUMBS}}", thumbs_html())
tpl = tpl.replace("{{S1}}", enc("ig_3600000_DclMpHksZb6.jpg", (720, 495), 80, 0.42))
tpl = tpl.replace("{{S2}}", enc("ig_31900_DcYbTYnMh3q.jpg",  (720, 495), 80, 0.40))
tpl = tpl.replace("{{S3}}", enc("ig_38000_DciyxYPsQmu.jpg",  (720, 495), 80, 0.45))
tpl = tpl.replace("{{WORKS}}", works_html())
tpl = tpl.replace("{{TICKER}}", ticker_html())
tpl = tpl.replace("{{FORM}}", FORM_URL)
tpl = tpl.replace("{{MARS}}", asset_uri("mars.webp", "image/webp"))
tpl = tpl.replace("{{IC_IG}}", IC_IG).replace("{{IC_TT}}", IC_TT).replace("{{IC_TG}}", IC_TG)
assert "{{" not in tpl, "остались незаполненные плейсхолдеры"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
         '?family=Manrope:wght@400;500;600;700;800&display=swap">\n')

HEAD = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Марсэж — ИИ-креатор</title>
<meta name="description" content="Марсэж — ИИ-креатор. Вирусные ролики на нейросетях: 21,9 млн просмотров, 4,4 млн на одном ролике.">
{FONTS}</head>
<body>
"""

dst = os.path.join(ROOT, "index-dark.html")
open(dst, "w", encoding="utf-8").write(HEAD + tpl + "\n</body>\n</html>\n")
print("index-dark.html:", round(os.path.getsize(dst) / 1024), "KB")

art = os.path.join(ROOT, "artifact-dark.html")
open(art, "w", encoding="utf-8").write(
    "<title>Марсэж на чёрном</title>\n" + FONTS + "\n" + tpl)
print("artifact-dark.html:", round(os.path.getsize(art) / 1024), "KB")
