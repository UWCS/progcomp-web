#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from progcomp import app
from os import path

if __name__ == '__main__':
    dirpath = path.dirname(path.realpath(__file__))
    path = path.join(dirpath, "progcomp.sock")
    WSGIServer(app, bindAddress=path).run()
