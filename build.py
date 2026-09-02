#!/usr/bin/env python3
"""Собирает index.html: подставляет реальные обложки роликов в шаблон как data:URI."""
import html, os

from imgutil import enc

ROOT = os.path.dirname(os.path.abspath(__file__))

TILES = [
    ("ig_3600000_DclMpHksZb6.jpg", "3,6 млн", "«Легендарные мемы». Собран одним промтом", "мемы"),
    ("ig_1200000_DcGW1ZSM9k7.jpg", "1,2 млн", "Новости Алматы: молния в «Земной шар»", "фейк-новости"),
    ("ig_911000_DcqcrDaMzgG.jpg",  "911 тыс.", "«Легендарные мемы», часть 3", "мемы"),
    ("ig_900000_DcnzdYGMuPB.jpg",  "900 тыс.", "«Легендарные мемы», часть 2", "мемы"),
    ("ig_535000_DX_1EtdsjtI.jpg",  "535 тыс.", "Кинематографичная сцена у моря", "кино"),
    ("ig_501000_DcLhRE6sA91.jpg",  "501 тыс.", "Новости UFC: скандал в октагоне", "фейк-новости"),
    ("ig_318000_Dcs8TVGsKcM.jpg",  "318 тыс.", "«Школьные мемы» к 1 сентября", "мемы"),
    ("ig_38000_DciyxYPsQmu.jpg",   "38 тыс.", "Одна камера — несколько ракурсов", "тутор"),
    ("ig_31900_DcYbTYnMh3q.jpg",   "31,9 тыс.", "Коллаборация с блогером", "коллаба"),
    ("ig_31700_DceGaxhM6HP.jpg",   "31,7 тыс.", "«26 дней = новая жизнь»", "кино"),
    ("ig_25400_DcOH6UjMASZ.jpg",   "25,4 тыс.", "Стадионный концерт, которого не было", "кино"),
    ("ig_25000_DbqeWKVMHh-.jpg",   "25 тыс.", "«Вьетнам без работы»", "кино"),
]

EYE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
       '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/>'
       '<circle cx="12" cy="12" r="2.6"/></svg>')

def tiles_html():
    out = []
    for fn, views, cap, tag in TILES:
        out.append(
            '<a class="tile" href="https://www.instagram.com/marsezh.ai/" target="_blank" rel="noopener">'
            f'<img src="{enc(fn,(420,747),78)}" alt="{html.escape(cap)}" loading="lazy">'
            '<span class="veil"></span>'
            f'<span class="plat">{html.escape(tag)}</span>'
            '<span class="meta">'
            f'<span class="views tnum">{EYE}{views}</span>'
            f'<span class="cap">{html.escape(cap)}</span>'
            '</span></a>'
        )
    return "\n        ".join(out)

tpl = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
tpl = tpl.replace("{{IMG_HERO}}", enc("tiktok_avatar.jpg", (860, 860), 84))
tpl = tpl.replace("{{IMG_S1}}", enc("ig_3600000_DclMpHksZb6.jpg", (760, 475), 80))
tpl = tpl.replace("{{IMG_S2}}", enc("ig_31900_DcYbTYnMh3q.jpg", (760, 475), 80))
tpl = tpl.replace("{{IMG_S3}}", enc("ig_38000_DciyxYPsQmu.jpg", (760, 475), 80))
tpl = tpl.replace("{{TILES}}", tiles_html())

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Марсэж — ИИ-креатор</title>
<meta name="description" content="Марсэж — ИИ-креатор. Вирусные ролики на нейросетях: 21,9 млн просмотров, 4,4 млн на одном ролике.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Manrope:wght@400;500;700;800&family=JetBrains+Mono:wght@400;600&display=swap">
</head>
<body>
"""

dst = os.path.join(ROOT, "index.html")
open(dst, "w", encoding="utf-8").write(HEAD + tpl + "\n</body>\n</html>\n")

# версия для публикации ссылкой (Artifact сам оборачивает страницу в <html>/<head>)
ART = """<title>Марсэж</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Manrope:wght@400;500;700;800&family=JetBrains+Mono:wght@400;600&display=swap">

"""
art = os.path.join(ROOT, "artifact.html")
open(art, "w", encoding="utf-8").write(ART + tpl)
print("artifact.html:", round(os.path.getsize(art) / 1024), "KB")
print("index.html:", round(os.path.getsize(dst) / 1024), "KB")
