import cgi
import grip
import os
import SimpleHTTPServer
import SocketServer
import sys
import urllib
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

PORT = 6419


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<head>\n<title>Directory listing for %s</title>\n"
                % displaypath)
        f.write("<style type=\"text/css\">" +
            open("markdown.css").read() +
            "</style></head>"
        )
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                if name == ".git":
                    continue
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n")
        fname = path + '/README.md'
        if os.path.isdir(path) and os.path.isfile(fname):
            f.write(grip.render_content(unicode(open(fname).read())))
        f.write("</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def hack_markdown(self, content):
        content = unicode(content, 'utf-8')
        return (
            "<html><head><style type=\"text/css\">" +
            open("markdown.css").read() +
            "</style></head>" +
            grip.render_content(content) +
            "</body></html>"
        )

    def hack_language(self, language, content):
        return self.hack_markdown(
            "```" + language + "\n" +
            content +
            "\n```"
        )

    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return
        content = open(path).read()
        if self.path.endswith(".ico"):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return
        elif self.path.endswith(".html"):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return
        elif self.path.endswith(".md"):
            response = self.hack_markdown(content)
        elif self.path.endswith(".sh") or self.path.endswith(".bash"):
            response = self.hack_language('bash', content)
        elif self.path.endswith(".sql"):
            response = self.hack_language('sql', content)
        elif self.path.endswith(".diff"):
            response = self.hack_language('diff', content)
        elif self.path.endswith(".java"):
            response = self.hack_language('java', content)
        elif self.path.endswith(".js"):
            response = self.hack_language('js', content)
        elif self.path.endswith(".css"):
            response = self.hack_language('css', content)
        elif self.path.endswith(".py"):
            response = self.hack_language('python', content)
        else:
            response = (
                "<html><pre>" +
                content.replace("&", "&amp;")
                .replace(">", "&gt;").replace("<", "&lt;") +
                "</pre></html>"
            )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)


print "serving at port", PORT
httpd = SocketServer.TCPServer(("0.0.0.0", PORT), MyHandler, False)
httpd.allow_reuse_address = True
httpd.server_bind()
httpd.server_activate()
httpd.serve_forever()
