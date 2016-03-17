#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Wrocławskie Krasnale - statyczna mapa. Dwarves of Wroclaw - a static map.
#
# Modified a BigMap 2 script.
# Source link: http://bigmap.osmz.ru/bigmap.php?xmin=71688&xmax=71764&ymin=43804&ymax=43825&zoom=17&scale=256&tiles=mapnik
#
# The MIT License (MIT)
#
# Copyright (c) 2016 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, math, re, io, urllib2, time, json, Image

def parameters():
    (zoom, xmin, ymin, xmax, ymax) = (17, 71688, 43804, 71764, 43825)
    xsize = (xmax - xmin + 1) * 256
    ysize = (ymax - ymin + 1) * 256
    return (zoom, xmin, ymin, xmax, ymax, xsize, ysize)

def fetch(url):
    print url
    while True:
        try:
            result = urllib2.urlopen(url).read()
            return result
        except Exception, e:
            print e
            time.sleep(2)
            print 'Retrying...'

def background():
    (zoom, xmin, ymin, xmax, ymax, xsize, ysize) = parameters()
    layer = 'http://tile.openstreetmap.org/%d/%d/%d.png'
    result = Image.new('RGB', (xsize, ysize))
    counter = 0
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            url = layer % (zoom, x, y)
            tile = fetch(url)
            image = Image.open(io.BytesIO(tile)).convert('RGB')
            result.paste(image, ((x - xmin) * 256, (y - ymin) * 256))
            counter += 1
            if 0 == counter % 10:
                time.sleep(2)
    result.save('dwarves.png')

def radians(degrees):
    return degrees * math.pi / 180.0

def distance(lon1, lat1, lon2, lat2):
    R = 6371000.0
    deltaLat = radians(lat2 - lat1) / 2.0
    deltaLon = radians(lon2 - lon1) / 2.0
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = math.sin(deltaLat) * math.sin(deltaLat)
    a += math.cos(lat1) * math.cos(lat2) * math.sin(deltaLon) * math.sin(deltaLon)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def digited(text):
    return None != re.search('[0-9]+', text)

def unique(dwarves):
    uniqued = {}
    for dwarf in dwarves:
        name = dwarf['Imie'].lower()
        if uniqued.has_key(name):
            previous = uniqued[name]
            if digited(previous['ulica']) and digited(dwarf['ulica']):
                if len(previous['ulica']) < len(dwarf['ulica']):
                    uniqued[name] = dwarf
            else:
                if digited(dwarf['ulica']):
                    uniqued[name] = dwarf
        else:
            uniqued[name] = dwarf
    return uniqued.values()

def fix(dwarves):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s,Wroclaw,Poland&key=%s'
    key = 'AIzaSyDnYKRBsYIKEzP9zTu0k9kCwCgePtq4vaM'
    for dwarf in dwarves:
        if 'Test' == dwarf['Imie']:
            dwarf['position']['lng'] = ''
            dwarf['position']['lat'] = ''
        try:
            lon = float(dwarf['position']['lng'])
            lat = float(dwarf['position']['lat'])
        except:
            continue
        away = distance(17.034730911254883, 51.11095877067957, lon, lat)
        if away < 1 or 30000 < away:
            address = dwarf['ulica']
            try:
                delimiter = address.find('ul.')
                if 0 < delimiter:
                    address = address[delimiter:]
                delimiter = address.find('pawilon')
                if 0 < delimiter:
                    address = address[:delimiter]
            except:
                continue
            address = urllib2.quote(address.replace(' ', '+').encode('UTF-8'))
            location = json.loads(fetch(url % (address, key)))
            location = location['results'][0]['geometry']['location']
            dwarf['position']['lng'] = location['lng']
            dwarf['position']['lat'] = location['lat']
    return dwarves

def merge(dwarves):
    groups = []
    for d1 in dwarves:
        found = False
        for group in groups:
            for d2 in group:
                try:
                    lon1 = float(d1['position']['lng'])
                    lat1 = float(d1['position']['lat'])
                    lon2 = float(d2['position']['lng'])
                    lat2 = float(d2['position']['lat'])
                except:
                    continue
                if distance(lon1, lat1, lon2, lat2) <= 9:
                    found = True
                    group.append(d1)
                    break
            if found:
                break
        if not found:
            groups.append([d1])
    dwarves = []
    for group in groups:
        if 1 == len(group):
            dwarves.append(group[0])
        else:
            companions = {}
            companions['Imie'] = ', '.join([dwarf['Imie'] for dwarf in group])
            companions['position'] = {}
            lngs = [float(dwarf['position']['lng']) for dwarf in group]
            companions['position']['lng'] = sum(lngs) / float(len(lngs))
            lats = [float(dwarf['position']['lat']) for dwarf in group]
            companions['position']['lat'] = sum(lats) / float(len(lats))
            dwarves.append(companions)
    return dwarves

def foreground(locale):
    (zoom, xmin, ymin, xmax, ymax, xsize, ysize) = parameters()
    E = 17.1084
    W = 16.8969
    N = 51.1311
    S = 51.0932
    spanLon = E - W
    spanLat = N - S
    url = 'http://krasnale.pl/admin/admin-ajax.php?action=ajax-wyszukaj-krasnala-mapa-show-all&lang=%s'
    dwarves = json.loads(fetch(url % locale))
    dwarves = unique(dwarves)
    dwarves = fix(dwarves)
    dwarves = merge(dwarves)
    svg = '<svg width="%d" height="%d" xmlns:xlink="http://www.w3.org/1999/xlink">' % (xsize, ysize)
    svg += '<style type="text/css"><![CDATA['
    svg += 'text {fill:#FF0000; font-size:11px; font-family:Arial; font-weight:bold;}'
    svg += 'circle {fill:#8B00CC; stroke:#8B00CC;}'
    svg += ']]></style>'
    svg += '<image xlink:href="dwarves.png" x="0" y="0" width="%d" height="%d"/>' % (xsize, ysize)
    spots = ''
    names = ''
    radius = 4
    for dwarf in dwarves:
        try:
            lon = float(dwarf['position']['lng'])
            lat = float(dwarf['position']['lat'])
        except:
            continue
        if distance(17.034730911254883, 51.11095877067957, lon, lat) < 1:
            print 'Clumped: %s' % dwarf['Imie']
            print dwarf['ulica']
            continue
        x = int(round(xsize * (lon - W) / spanLon))
        y = int(round(ysize * (lat - S) / spanLat))
        y = ysize - y
        spots += '<circle cx="%d" cy="%d" r="%d"/>' % (x, y, radius)
        name = dwarf['Imie'].encode('UTF-8').strip()
        names += '<text x="%d" y="%d">%s</text>' % (x + radius + 4, y, name)
    svg += spots
    svg += names
    svg += '</svg>'
    file = open('dwarves.%s.svg' % locale, 'wb')
    file.write(svg)
    file.close()
    os.system('convert dwarves.%s.svg dwarves.%s.png' % (locale, locale))
    os.remove('dwarves.%s.svg' % locale)

background()
foreground('en')
foreground('pl')
os.remove('dwarves.png')
