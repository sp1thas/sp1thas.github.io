#!/usr/bin/env python

from __future__ import unicode_literals
from datetime import date
import time
import os

AUTHOR = 'Panagiotis Simakis'
SITENAME = 'Panagiotis Simakis Personal Website'
SITEURL = 'https://sp1thas.github.io'
USER_LOGO_URL = '/images/home.png'
INDEX_TITLE = 'Home'
INDEX_DESC = 'Description of Site'

TIMEZONE = 'Europe/Athens'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = "%b %d, %Y"

THEME = "voce"

PLUGIN_PATHS = ["plugins", os.path.join(THEME, "plugins")]

LOAD_CONTENT_CACHE = False
SLUGIFY_SOURCE = 'basename'

# Theme specific
TAGLINE = "Site Tagline"
MANGLE_EMAILS = False
GLOBAL_KEYWORDS = ("keywords",)

SOCIAL = (
    ("GitHub", "https://github.com/sp1thas"),
    ("Twitter", "https://twitter.com/sp1thas"),
    ("Linkedin", "https://www.linkedin.com/in/psimakis/"),
    ("Stackoverflow", "https://stackoverflow.com/users/6779252/panagiotis-simakis"),
)

LINKS = (
    ("Home", "/"),
    ("Resume", "/pages/resume"),
)

DEFAULT_PAGINATION = 8

RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 50

ARCHIVES_URL = "archives"
ARCHIVES_SAVE_AS = 'archives.html'
ARTICLE_URL = 'articles/{slug}'
ARTICLE_SAVE_AS = 'articles/{slug}.html'
PAGE_URL = 'pages/{slug}'
PAGE_SAVE_AS = 'pages/{slug}.html'
TAGS_URL = 'tag/{slug}'

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'images/favicon-16x16.png': {'path': 'favicon-16x16.png'},
    'images/favicon-32x32.png': {'path': 'favicon-32x32.png'},
    'images/favicon-96x96.png': {'path': 'favicon-96x96.png'},
}
