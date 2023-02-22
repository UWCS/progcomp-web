#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from progcomp import app

if __name__ == '__main__':
    dirpath = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dirpath, "progcomp.sock")
    WSGIServer(app, bindAddress=path).run()
