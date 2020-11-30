# Website template for conference proceedings

## Data Structure for EMS Conference Proceedings

Database required to produce the proceedings of the EMS 2014 conference, in the form of a mini website. Mini-site to be pre-loaded on the participants' USB key.

### 1. Table of articles

### 1.1. One Table

Table with one item per row, with the following columns :
Columns provided automatically by Siences Conf : :

* an identifier, unique by article (created by Sciences Conf, e.g. 30288)  
* the title of the article
* the list of authors, e.g. "\<Last name> \<First name>(1,2), \<Last name2> \<First name2> (2)".
* affiliation of the authors (form to be specified), e.g. "(1) SATIE, (2) LGEP".
* the abstract text

"Manual" columns

* the session code e.g. SOA1 (ordinary session, slot A, n1), SPA
* session order number, e.g. 4 (only for oral sessions)
* the topic text, e.g. "power integration".

### 1.2. The Folder

which contains all the PDF articles, with the file name of the paper file identifier (ex: 30288.pdf), this goes into a directory inside the data folder, i.e. <conference_nameDataFolder>/articles/, e.g. EMS2014Data/articles/

## 2. Session tables

Oral and poster sessions

* code,  e.g. SOA1
* full session name: "Power Integration", "Session Poster A".
* place (room) : text
* date and time, e.g. text 2pm - 4pm
* one or two chairman (for oral sessions)

## 3 Topic tables

Not necessary, as there is no info to add.
