#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-time sitewide retrofit for rentflow-legal (rentflow.tabserve.com.tr):
1. Founder identity: Yunus Güneş -> Aycan Merve Güneş.
2. Article schema author: Organization -> Person.
3. Author-box: "Written by Tabserve" -> personal author line + link to central author profile.
Idempotent (safe to re-run).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD_AUTHOR = (
    '<div class="author-box"><img class="ab-logo" src="/assets/logo.svg" alt="Tabserve" width="56" height="56">'
    '<div class="ab-body"><b>Written by Tabserve</b><p>We\'re an independent app studio building simple, useful '
    'mobile apps for travel, trips and rentals — OneBag, Routevia and RentFlow. We share practical guides to help you '
    'pack smarter, travel better and manage rentals with less hassle.</p><div class="follow"><span>Follow us:</span>'
)
NEW_AUTHOR = (
    '<div class="author-box"><img class="ab-logo" src="/assets/logo.svg" alt="Aycan Merve Güneş — Tabserve" width="56" height="56">'
    '<div class="ab-body"><b>Written by <a href="https://www.tabserve.com.tr/author.html">Aycan Merve Güneş</a></b>'
    '<p style="color:var(--muted);font-size:13px;margin:2px 0 8px">Independent Full Stack Developer · Founder of Tabserve</p>'
    '<p>Aycan builds and maintains Tabserve\'s apps — OneBag, Routevia and RentFlow — and writes practical, '
    'tested guides to help landlords manage rentals with less hassle.</p><div class="follow"><span>Follow us:</span>'
)

SIMPLE_REPLACEMENTS = [
    ("Yunus Güneş", "Aycan Merve Güneş"),
    (
        '"author": {"@type": "Organization", "name": "Tabserve"}',
        '"author": {"@type": "Person", "name": "Aycan Merve Güneş", "jobTitle": "Independent Full Stack Developer", "url": "https://www.tabserve.com.tr/author.html"}',
    ),
    (
        '"author":{"@type":"Organization","name":"Tabserve"}',
        '"author":{"@type":"Person","name":"Aycan Merve Güneş","jobTitle":"Independent Full Stack Developer","url":"https://www.tabserve.com.tr/author.html"}',
    ),
]

EXTS = {".html", ".xml", ".json", ".txt"}
SKIP_DIRS = {"_gen", "__pycache__", ".git", "node_modules"}

changed_files = 0
for path in ROOT.rglob("*"):
    if path.is_dir() or path.suffix not in EXTS:
        continue
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    for old, new in SIMPLE_REPLACEMENTS:
        text = text.replace(old, new)
    text = text.replace(OLD_AUTHOR, NEW_AUTHOR)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed_files += 1
        print(f"  {path.relative_to(ROOT)}")

print(f"\n{changed_files} dosya güncellendi.")
