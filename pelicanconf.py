#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Lance Albertson'
SITENAME = u'Lance Albertson'
SITEURL = ''
THEME = 'pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'cosmo'
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 5
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

GITHUB_USER = ''
ADDTHIS_PROFILE = 'ra-5297f22e2ba1d375'
GOOGLE_ANALYTICS = 'UA-7186407-1'
DISQUS_SITENAME = 'lancealbertson'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('osu open source lab', 'http://osuosl.org/'),
          ('the infallible collective', 'http://www.infalliblecollective.com/'),)

# Social widget
SOCIAL = (
          ('github', 'http://github.com/ramereth/'),
          ('linkedin', 'http://www.linkedin.com/in/ramereth'),
          ('twitter', 'http://twitter.com/ramereth'),
          ('google-plus', 'https://plus.google.com/105236849868554834121/posts'),
          ('youtube', 'http://www.youtube.com/ramereth'),)

DEFAULT_PAGINATION = 4

CSS_FILE = ( 'css/blog.css' )
STATIC_PATHS = ["media", "css", "favicon.png" ]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
