#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — June 2014
""" Read CSV table of all contributions to the conference
"""

from __future__ import division, print_function

import io
import csv
import re


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def read_articles(fname):
    '''read CSV table of the articles contributed to the conference
    
    Returns a generator
    '''
    re_affil = re.compile(r'\((\d+)\)')
    
    with io.open(fname, encoding='utf-8') as f:
        c = csv.reader(utf_8_encoder(f), delimiter=';')
        
        # 1) Read the headers
        header = c.next()
        header = [head.lower() for head in header]
        yield header
        
        for line in c:
            item = {head: line[idx].decode('utf-8') for idx, head in enumerate(header)}
            if item['type'] != u'FULLTEXT': #or \
               #item['statut'] != u'Accepté':
                # filters out the ABSTRACT contributions
                # or not yet accepted papers
                continue
            
            # Manually fill blanks:
            if item['topics'] == '':
                item['topics'] = 'no topic'
            if item['id_session'] == '':
                item['id_session'] = 'SO-XX-X'
            
            # Process the authors field to split names
            authors = item['authors'].split(', ')
            authors_split = []
            
            for auth in authors:
                # Affiliation(s):
                affil = re_affil.findall(auth)
                affil = [int(ai)-1 for ai in affil]
                # Author name:
                name, count = re_affil.subn('', auth)
                assert len(affil) == count
                name = name.strip()
                
                authors_split.append((name, affil))
            # end for each author
            item['authors_split'] = authors_split
            item['authors_no_affil'] = re_affil.subn('', item['authors'])[0]
            # first author + "et al." if more than one
            authors_etal = authors_split[0][0]
            if len(authors_split) > 1:
                authors_etal += ' et al.'
            item['authors_etal'] = authors_etal

            yield item


def read_sessions(fname):
    return []

if __name__ == '__main__':
    # Example:
    articles = read_articles('../SGE2014_data/fichier_retravail_4juin2014.csv')
    articles = list(articles)
    
    header, articles = articles[0], articles[1:]
    
    print('Header:')
    print(', '.join(header))
    
    print('One article:')
    print(articles[0]['title'])
    print('nb articles: {:d}'.format(len(articles)))