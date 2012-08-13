#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
 (c) 2011, 2012 - Copyright Pierre-Yves Chibon

 Distributed under License GPLv3 or later
 You can find a copy of this license on the website
 http://www.gnu.org/licenses/gpl.html

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 MA 02110-1301, USA.


Demo program integrating information from different germplasm databases.

Dependencies:
* pyRdf from https://github.com/RDFLib/pyrdfa3
* rdflib from 
"""

import os
import rdflib
import urllib
from pyRdfa import pyRdfa


INPUT_LIST = [
        'http://localhost/data/AccessionDetails.html',
        'http://localhost/data/SelectAccessionByAccessionID.html'
    ]
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")


class Information(object):

    def __init__(self, trait=None, value=[], origin=None):
        self.trait = trait
        self.value = value
        self.origin = origin

    def add_value(self, value):
        self.value.append(value)


def get_info_accession(graph, uri, info=[]):
    subject = rdflib.term.URIRef(uri)
    origin = urllib.splitquery(uri)[0].rsplit('/')[2]
    for pred, objec in graph.predicate_objects(subject=subject):
        if isinstance(pred, rdflib.term.URIRef) \
            and 'cropontology' in str(pred):
            for obj in graph.objects(subject=pred, predicate=RDFS['label']):
                obj = str(obj)
                objec = str(objec)
                if not objec:
                    continue
                inf = Information(trait=obj, value=objec,
                        origin=origin)
                info.append(inf)
    return info


def main():
    """ Reads in all the accessions page stored in the data folder and
    print all the information gathered.
    """
    proc = pyRdfa()
    graph = rdflib.Graph()
    #print dir(graph)
    for files in INPUT_LIST:
        graph = proc.graph_from_source(files, graph)
        #print files, len(graph)
    for s, p, o in graph:
        if isinstance(p, rdflib.term.URIRef) and 'cropontology' in str(p):
            #print p
            graph.parse(p)
    
    info = get_info_accession(graph,
        "https://www.eu-sol.wur.nl/passport/SelectAccessionByAccessionID.do?accessionID=EA01897",
        info=[])
    info = get_info_accession(graph,
        "http://www.cgn.wur.nl/applications/cgngenis/AccessionDetails.aspx?acnumber=CGN14338",
        info=info)

    return info


if __name__ == '__main__':
    main()
