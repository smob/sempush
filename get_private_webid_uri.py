#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# get_private_webid_uri 
# Python functions to request a private URI that requires a client certificate 
# to authenticate via WebID
#
# Copyright (c) 2010, Digital Enterprise Research Institute (DERI),NUI Galway.
# Author: Julia Anaya
# Email: julia dot anaya at gmail dot com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""get_private_webid_uri 

Python functions to request a private URI that requires a client certificate 
to authenticate via WebID

===Usage

from get_private_webid_uri import get_private_uri
result = get_private_uri(uri_to_get, cert_path, key_path)

:author:       julia
:copyright:    Digital Enterprise Research Institute (DERI),NUI Galway
:license:      GNU GPL version 3 or any later version 
                (details at http://www.gnu.org)
:contact:      julia dot anaya at gmail dot com
:dependencies: python (>= version 2.6)
"""

HUB_CERTIFICATE = 'hub_cert.pem'
HUB_CERTIFICATE = '/home/duy/deri/code/repositories/xmppwebid_cert_key.pem'
HUB_KEY = 'hub_key.key'
HUB_KEY = '/home/duy/deri/code/repositories/xmppwebid_key.key'
subscriber_private_uri = "https://localhost/smob/private"


import urllib2, httplib
import cookielib
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
  # http://www.osmonov.com/2009/04/client-certificates-with-urllib2.html
  def __init__(self, key, cert):
    urllib2.HTTPSHandler.__init__(self)
    self.key = key
    self.cert = cert
  def https_open(self, req):
    return self.do_open(self.getConnection, req)
  def getConnection(self, host, timeout=300):
    return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)

def get_private_uri(uri, cert, key):
  """Request a URI that requires a client certificate

  Args:
    uri: The URI string to request.
    cert: The x509 client certificate file path
    key: the certificate key file path

  Returns:
    An ascii string with the response.
  """
  cj = cookielib.LWPCookieJar()
  opener = urllib2.build_opener(HTTPSClientAuthHandler(key, cert), urllib2.HTTPCookieProcessor(cj))
  response = opener.open(uri)
  return response.read()


if __name__ == "__main__":
    results = get_private_uri(subscriber_private_uri, HUB_CERTIFICATE, HUB_KEY)
    print results



