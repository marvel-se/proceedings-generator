#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — June 2014
""" Generator for the html files of the proceedings
"""

from __future__ import division, print_function, unicode_literals

import os.path
from os.path import join
import shutil
import io
import jinja2
from jinja2 import Environment, FileSystemLoader

from data_reader import read_articles, read_sponsors, read_sessions

### Read configuration
config = {}
execfile('config.py', {}, config)

config_vars = config['c']
data = config['data']


### Read and process the list of articles
articles = list(read_articles(join(data['path'], data['article_table'])) )
header, articles = articles[0], articles[1:]

# sort articles list by first author
articles.sort(key= lambda item: item['authors'])
config_vars['articles'] = articles

print('{:d} articles read from table "{}"'.format(len(articles),
                                                data['article_table']))


### build topic -> [articles] mapping:
topics = {}

for art in articles:
    top = art['topic']
    if top not in topics:
        topics[top] = []
    # Append article to its topic:
    topics[top].append(art)

print('\nTopics stats:')
for top in sorted(topics):
    n_art = len(topics[top])
    n_poster = len([art for art in topics[top] if art['media'] == 'poster'])
    n_oral = len([art for art in topics[top] if art['media'] == 'oral'])
    print(' - "{}": {:d} article(s)'.format(top, n_art), end=' ')
    print('({:d} orals, {:d} posters)'.format(n_oral, n_poster))

# build topic codes:
topics_code = {top: '{:03d}'.format(idx)
               for idx, top in enumerate(sorted(topics))}

config_vars['topics'] = topics

### build session -> [articles] mapping:
sessions = {}

for art in articles:
    s_id = art['id_session']
    if s_id not in sessions:
        sessions[s_id] = []
    # Append article to its session:
    sessions[s_id].append(art)

# Read session description
fname_sessions = join(data['path'], data['session_table'])

sessions_details = read_sessions(fname_sessions)

# Check that each session used in article table has a description:
for s_id in sessions:
    assert s_id in sessions_details

# put empty list of articles for unused sessions
for s_id in sessions_details:
    if s_id not in sessions:
        sessions[s_id] = []

# Build the sessions groups (synchronous sessions)
sessions_groups = {}
for s_id in sessions_details:
    s_date = sessions_details[s_id]['date']
    s_begin = sessions_details[s_id]['begin']
    s_end = sessions_details[s_id]['end']

    if s_date not in sessions_groups:
        sessions_groups[s_date] = {}
    if (s_begin, s_end) not in sessions_groups[s_date]:
        sessions_groups[s_date][s_begin, s_end] = {}

    sessions_groups[s_date][s_begin, s_end][s_id] = sessions_details[s_id]


print('\nSessions stats:')
for s_id in sorted(sessions):
    n_art = len(sessions[s_id])
    print(' - "{}": {:d} article(s)'.format(s_id, n_art))

config_vars['sessions'] = sessions
config_vars['sessions_groups'] = sessions_groups


### build author -> [articles] mapping:
authors = {}

for art in articles:
    art_authors = [name for name, affil in art['authors_split']]
    for auth in art_authors:
        if auth not in authors:
            authors[auth] = []
        # Append article to its author:
        authors[auth].append(art)

# author index:
letter = ''
author_index = {}
for auth in sorted(authors.keys()):
    if auth[0] != letter:
        letter = auth[0]
        author_index[letter] = auth


print('\nAuthors stats:')
print('{:d} authors found'.format(len(authors)))

config_vars['authors']      = authors
config_vars['author_index'] = author_index



### Read the sponsors:
fname_sponsors = join(data['path'], data['sponsor_table'])

if os.path.exists(fname_sponsors):
    sponsors  = read_sponsors(fname_sponsors)
    print('{:d} sponsors found'.format(len(sponsors)))
else:
    sponsors = []
    print('No sponsors')

config_vars['sponsors'] = sponsors

print('Copying logo files', end=': ')
# Copy logo files:
for spons in sponsors:
    print(spons['logo'], end=', ')
    logo_src = join(data['path'], spons['logo'])
    logo_dest = join(data['render_path'], 'images', spons['logo'])
    shutil.copyfile(logo_src, logo_dest)
print()

### Write web pages:

# Create a template "Environment":
templ_path = os.path.dirname(__file__)
loader =  FileSystemLoader(templ_path)
env = Environment(loader=loader, undefined=jinja2.StrictUndefined)
env.globals['topics_code'] = topics_code
env.globals['sessions_details'] = sessions_details

# 1) Index page:
template = env.get_template('index.html')

with io.open(join(data['render_path'], 'index.html'),
             'w', encoding='utf-8') as out:
    out.write(template.render(config_vars, root_path='.'))

# 2) List of articles:
template = env.get_template('article_list.html')

with io.open(join(data['render_path'], 'article_list.html'),
             'w', encoding='utf-8') as out:
    out.write(template.render(config_vars, root_path='.'))

# 3) Detailed article pages:
template = env.get_template('article_detail.html')

for art in articles:
    fname = 'article_{:s}.html'.format(art['docid'])
    #print(fname)
    with io.open(join(data['render_path'], 'articles', fname),
                 'w', encoding='utf-8') as out:
        out.write(template.render(config_vars, article=art, root_path='..'))

# 4) Detailed topic pages:
template = env.get_template('topic_detail.html')

for top in topics:
    fname = 'topic_{}.html'.format(topics_code[top])
    print(fname)
    with io.open(join(data['render_path'], 'topics', fname),
                 'w', encoding='utf-8') as out:
        out.write(template.render(config_vars, topic=top,
                                  articles=topics[top], root_path='..'))

# 5) List of authors:
template = env.get_template('author_list.html')

with io.open(join(data['render_path'], 'author_list.html'),
             'w', encoding='utf-8') as out:
    out.write(template.render(config_vars, root_path='.'))

# 6a) List of sessions
template = env.get_template('session_list.html')

with io.open(join(data['render_path'], 'session_list.html'),
             'w', encoding='utf-8') as out:
    out.write(template.render(config_vars, root_path='.'))
    
# 6b) Complete programe of sessions (for printed booklet)
template = env.get_template('session_program.html')

with io.open(join(data['render_path'], 'session_program.html'),
             'w', encoding='utf-8') as out:
    out.write(template.render(config_vars, root_path='.'))

# 6c) Detailed session pages
template = env.get_template('session_detail.html')

for s_id in sessions:
    fname = 'session_{:s}.html'.format(s_id)
    #print(fname)
    with io.open(join(data['render_path'], 'sessions', fname),
                 'w', encoding='utf-8') as out:
        out.write(template.render(config_vars, session=sessions_details[s_id], root_path='..'))
