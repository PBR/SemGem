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

from flask import Flask, Response, render_template, request, redirect, url_for
import datetime

from semgem import main as semgem

# Create the application.
APP = Flask(__name__)

##  Web-app


@APP.route('/')
def index():
    """ Shows the front page.
    Fills in the index.html template.
    """
    print 'semgem %s -- %s -- %s' % (datetime.datetime.now(),
        request.remote_addr, request.url)
    (info, images) = semgem()
    return render_template('index.html', info=info, images=images)


if __name__ == '__main__':
    APP.debug = True
    APP.run()
