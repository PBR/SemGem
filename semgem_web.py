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

Small web application to show the possibility of data integration from
different germplasm databases.

Dependencies:
* pyRdf from https://github.com/RDFLib/pyrdfa3
* Flask from http://flask.pocoo.org/
"""

from flask import (Flask, Response, render_template, request, redirect,
                   url_for, flash)
import datetime
import sys

from semgem import main as semgem

# Create the application.
APP = Flask(__name__)
APP.secret_key = "asda;ljlfsdan"

##  Web-app

@APP.route('/')
def index():
    """ Shows the front page.
    """
    print 'semgem %s -- %s -- %s' % (
        datetime.datetime.now(), request.remote_addr, request.url)
    return render_template('index.html')


@APP.route('/<eusol_id>', methods=['GET'])
def semgem_ui(eusol_id):
    """ Retrieves and displays information for the provided EU-SOL accession
    identifier.

    :arg eusol_id: the identifier of the accession of interest in the
        EU-SOL database, see https://www.eu-sol.wur.nl/

    """
    print 'semgem %s -- %s -- %s ** ' % (
        datetime.datetime.now(), request.remote_addr, request.url)
    try:
        (info, origins, origins_info, images) = semgem(eusol_id)
    except Exception, err:
        print >> sys.stderr, err.message
        flash("An error has occured, try again or please inform us.")
        return redirect(url_for('index'))
    return render_template(
        'result.html',
        accession=eusol_id,
        origins=origins,
        origins_info=origins_info,
        info=info,
        images=images)


@APP.route('/submit', methods=['POST'])
def submit():
    """ Redirects to the semgem method in order to provide a nice URL

    """
    print 'semgem %s -- %s -- %s' % (
        datetime.datetime.now(), request.remote_addr, request.url)
    eusol_id = request.form.get('eusol_id', None)
    if eusol_id:
        return redirect(url_for('semgem_ui', eusol_id=eusol_id))
    else:
        flash('No identifier provided')
        return redirect(url_for('index'))


if __name__ == '__main__':
    APP.debug = True
    APP.run()
