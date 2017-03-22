#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("guestbook.html")

class ShraniHandler(BaseHandler):
    def post(self):
        ime = self.request.get("ime")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        if not ime:
            ime = "Neznan"
        if not email:
            email = "Ni mail-a"
        if "<script>" in sporocilo:
            return self.write("Ni ti uspelo!!")

        # Shrani sporocilo v bazo.
        spr = Sporocilo(ime=ime, email=email, sporocilo=sporocilo)
        spr.put()
        return self.write("Uspesno shranjeno v Knjigo gostov.")

class VsaSporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query().fetch()
        spremenljivke = {
            "sporocila": sporocila
        }
        return self.render_template("seznam.html", spremenljivke)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/shrani', ShraniHandler),
    webapp2.Route('/vsa-sporocila', VsaSporocilaHandler),
], debug=True)
