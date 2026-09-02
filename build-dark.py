#!/usr/bin/env python3
"""Собирает тёмную версию: index-dark.html (файл) и artifact-dark.html (для публикации)."""
import html, os

from imgutil import enc, portrait

ROOT = os.path.dirname(os.path.abspath(__file__))

IC_IG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">'
         '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
         '<circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/></svg>')
IC_TT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">'
         '<path d="M15 3.5c.4 2.6 2 4.2 4.6 4.5v3.2c-1.8.1-3.4-.4-4.8-1.4v5.9c0 3.6-2.7 5.9-5.9 5.5'
         '-2.7-.3-4.7-2.5-4.8-5.2-.1-3.1 2.4-5.7 5.6-5.6v3.3c-1.3-.3-2.5.6-2.5 1.9 0 1.2 1 2.1 2.2 2.1'
         ' 1.3 0 2.2-.9 2.2-2.3V3.5H15z"/></svg>')
IC_TG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">'
         '<path d="M21 4 3 10.5l5 1.8L18.5 6.8 10.5 14v4.6l2.7-3.2 4.6 3.4L21 4z"/></svg>')

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
