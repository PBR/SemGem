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
* rdflib from https://github.com/RDFLib/rdflib
* pyRdf from https://github.com/RDFLib/pyrdfa3 (only required for version
    older than 4.0.1)
"""

import os
import StringIO
import urllib2

import rdflib
import urllib
try:
    from rdflib.plugins.parsers.pyRdfa import pyRdfa
except ImportError:
    from pyRdfa import pyRdfa


EUSOL_URL = 'https://www.eu-sol.wur.nl/test/passport/' \
            'SelectAccessionByAccessionID.do?accessionID=%s'
EUSOL2_URL = 'https://www.eu-sol.wur.nl/passport/' \
            'SelectAccessionByAccessionID.do?accessionID=%s'
CGN_URL = 'http://applicaties.wageningenur.nl/applications/cgngenis/' \
          'AccessionDetails.aspx?acnumber=%s'

RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")


def get_images_in_graph(graph, subjects):
    """ Retrieve the FOAF:Image present in the graph. """
    output = []
    for subject in subjects:
        subject = rdflib.term.URIRef(subject)
        output.extend([objec for objec in graph.objects(
            subject=subject, predicate=FOAF['Image'])])
    return output


def get_info_accession(graph, uri, info):
    subject = rdflib.term.URIRef(uri)
    for pred, objec in graph.predicate_objects(subject=subject):
        #print pred, objec
        if isinstance(pred, rdflib.term.URIRef) \
                and 'cropontology' in str(pred):
            for obj in graph.objects(subject=pred, predicate=RDFS['label']):
                #print '--', obj, objec, origin
                obj = str(obj)
                objec = str(objec)
                if not objec:
                    continue
                if obj in info:
                    if uri in info[obj]:
                        info[obj][uri].append(objec)
                    else:
                        info[obj][uri] = [objec]
                else:
                    info[obj] = {uri: [objec]}
    return info


def main(eusol_id):
    """ Reads in all the accessions page stored in the data folder and
    print all the information gathered.

    :arg eusol_id: the eusol identifier of the genome to investigate.

    """
    proc = pyRdfa()
    graph = rdflib.Graph()
    eusol_url = EUSOL_URL % eusol_id
    graph = proc.graph_from_source(eusol_url, graph)
    for sub, pred, obj in graph:
        if isinstance(pred, rdflib.term.URIRef) and 'cropontology' in str(pred):
            stream = urllib2.urlopen(pred)
            text = stream.read()
            stream.close()
            text = text.replace('%3A', ':')
            graph = graph.parse(StringIO.StringIO(text), format="nt")
        if pred == RDFS['seeAlso']:
            graph = proc.graph_from_source(obj, graph)

    # Temporary hack until the version in test is the same as the version in
    # prod
    eusol_url = EUSOL2_URL % eusol_id

    subjects = [eusol_url]
    info = {}
    info = get_info_accession(graph, eusol_url, info)

    # Dynamically retrieve the CGN identifier from the EU-SOL information
    if 'donor accession number' in info:
        cgn_id = info['donor accession number'][eusol_url][0]
        cgn_url = CGN_URL % cgn_id
        info = get_info_accession(graph, cgn_url, info)
        subjects.append(cgn_url)

    images = get_images_in_graph(graph, subjects)

    origins = set()
    origins_info = {}
    for trait in info:
        for source in info[trait]:
            url = urllib.splitquery(source)[0].rsplit('/')[2]
            if url not in origins_info:
                origins.add(url)
                origins_info[url] = source

    return (info, origins, origins_info, images)


if __name__ == '__main__':
    main('EA01897')
