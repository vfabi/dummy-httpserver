#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
  @project: dummy-httpserver
  @component: dummy-httpserver
  @copyright: © 2019 by vfabi
  @author: vfabi
  @support: vfabi
  @initial date: 2019-02-27 10:10:10
  @modification date:
  @license: this file is subject to the terms and conditions defined
    in file 'LICENSE', which is part of this source code package.
  @description:
    dummy-httpserver application entrypoint.
  @todo:
"""

import os
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    app_name = 'dummy-httpserver'
    app_description = 'Dummy http server to display internal data - hostname, ip address, env variables, etc. For test/debug purposes only.'

    def _get_environment_data(self):
        envvars = os.environ
        envvars['LS_COLORS'] = '---STRIPPED---'
        data = {
            'host_name': socket.gethostname(),
            'host_ip': socket.gethostbyname(socket.gethostname()),
            'envvars': envvars
        }
        return data

    def _generate_html(self, **kwargs):
        envvarslisthtml = []
        for envvar in kwargs['envvars']:
            envvarslisthtml.append(f"<i>{envvar} = {kwargs['envvars'][envvar]}</i></br>")
        envvarslisthtml_modified = ''.join(envvarslisthtml)

        html_style = r'''<style>
        body { background-color: #28B463; }
        h3 { color: #34495E; }
        p { color: white; }
        .meta {
            display: inline-block;
            background-color: #52BE80;
            color: white;
            padding: 8px;
        }
        .data {
            display: 70%;
            background-color: #138D75;
            color: white;
            padding: 8px;
        }
        </style>'''

        html_body = f'''<html>
        <head>
        {html_style}
        </head>
        <body>
        <h3>Meta</h3>
        <div class="meta">
            <p><b>Application: </b>{self.app_name}</p>
            <p><b>Description: </b>{self.app_description}</p>
        </div>
        <h3>Data</h3>
        <div class="data">
            <p><b>Hostname: </b>{kwargs['host_name']}</p>
            <p><b>IP address: </b>{kwargs['host_ip']}</p>
            <p><b>ENV: </b></p>
            {envvarslisthtml_modified}
        </div>
        </body><html>'''
        return html_body

    def do_GET(self):
        if self.path == "/healthcheck":
            self.send_response(200)
            self.end_headers()
        else:
            data = self._get_environment_data()
            html = self._generate_html(
                host_name=data['host_name'],
                host_ip=data['host_ip'],
                envvars=data['envvars']
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(html, 'utf8'))


if __name__ == "__main__":
    httpserver = HTTPServer(
        ('0.0.0.0', int(os.getenv('PORT', 8000))),
        SimpleHTTPRequestHandler
    )
    httpserver.serve_forever()
