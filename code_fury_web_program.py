import SimpleHTTPServer
import BaseHTTPServer
import os
import urlparse

import format_data

class KFHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        parsed = urlparse.parse_qs(data_string)
        print parsed
        fullfilename = parsed['file'][0]
        print fullfilename
        path, filename = os.path.split(fullfilename)
        fileroot = os.path.splitext(filename)[0]
        outpath = os.path.join(path, "Combenefit " + fileroot)
        print "Running"
        try:
            format_data.process_data_file(fullfilename, outpath)
        except BaseException as e:
            result = "Failure: " + str(e)
        else:
            result = "Success!! <br>   Output in \"" + outpath + '"'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        response = """<!doctype html>
                      <html>
                         <h1>Result: {result}</h1>
                         <a href="index.html">Go Back</a>
                      </html>""".format(result=result)
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)
        
        
        

print "Starting Code Fury Web!"

handler = KFHandler
server = BaseHTTPServer.HTTPServer(("0.0.0.0", 8000), handler)
server.serve_forever()

print "Running formatter"

#format_data.process_data_file("combenefit_code_fury_template.xlsx",
#                              "combenefit")

