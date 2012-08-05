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
from pyRdfa import pyRdfa


INPUT_LIST = [
        'http://localhost/data/AccessionDetails.html',
        'http://localhost/data/SelectAccessionByAccessionID.html'
    ]


def main():
    """ Reads in all the accessions page stored in the data folder and
    print all the information gathered.
    """
    proc = pyRdfa()
    graph = rdflib.Graph()
    #print dir(graph)
    for files in INPUT_LIST[1:]:
        graph = proc.graph_from_source(files, graph)
        #print files, len(graph)
    for s, p, o in graph:
        if isinstance(p, rdflib.term.URIRef) and 'cropontology' in str(p):
            graph.parse(p)
            #print p, len(graph)
    subject = rdflib.term.URIRef("https://www.eu-sol.wur.nl/passport/SelectAccessionByAccessionID.do?accessionID=EA01897")
    for p, o in graph.predicate_objects(subject=subject):
        if isinstance(p, rdflib.term.URIRef) and 'cropontology' in str(p):
            print p, o
            for p2, o2 in graph.predicate_objects(subject=p):
                print '  ', p2, o2

    #print graph.serialize(format='n3')


if __name__ == '__main__':
    main()
