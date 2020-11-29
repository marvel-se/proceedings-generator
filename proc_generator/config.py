# -*- coding: utf-8 -*-
"""Configuration of the proceedings generator

* where to find data
* parameters of the event (name, date, ...)
"""

from __future__ import unicode_literals

### Main configuration parameters

data = {}

# SBQS data

# Input data:
data['path'] = '../SBQS2020_data'
data['delimiter'] = ','
data['article_table'] = 'SBQS2020_articles.csv'
data['session_table'] = 'SBQS2020_sessions.csv'
# Output path:
data['render_path'] = '../SBQS_proceedings'
data['chair_pkg_path'] = '../chairman package'



### Event parameters dict
c={}

# language, for <html lang="xx"> attribute:
c['lang'] = 'en'

# Event (conference) parameters:
c['event_name'] = 'SGE 2014'
c['event_date'] = '8—10 juillet 2014'
c['event_location']= 'Cachan (France)'
c['event_website'] = 'http://www.sge-conf.fr/sge-2014/'
c['event_logo'] = 'logo_sge.png'

c['website_credits'] = 'Pierre Haessig, laboratoire SATIE'
