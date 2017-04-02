#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from google.appengine.api import users
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
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "user": user, "logiran": logiran, "logout_url": logout_url,
            }
        else:
            logiran = False
            login_url = users.create_login_url("/")
            spremenljivke = {
                "user": user, "logiran": logiran, "login_url": login_url,
            }
        return self.render_template("guestbook.html", spremenljivke)

class ShraniHandler(BaseHandler):
    def post(self):
        email = cgi.escape(self.request.get("email"))
        sporocilo = cgi.escape(self.request.get("sporocilo"))

        user = users.get_current_user()
        if user:
            ime = user.nickname()
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            # Shrani sporocilo v bazo.
            spr = Sporocilo(ime=ime, email=email, sporocilo=sporocilo)
            spr.put()
            return self.render_template("uspesno_shranjeno.html", spremenljivke)
        else:
            return self.write("Ni ti uspelo.")

class VsaSporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query(Sporocilo.izbrisan == False).fetch()
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocila": sporocila, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("seznam.html", spremenljivke)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("posamezno_sporocilo.html", spremenljivke)

class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("uredi_sporocilo.html", spremenljivke)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.ime = cgi.escape(self.request.get("ime"))
        sporocilo.email = cgi.escape(self.request.get("email"))
        sporocilo.sporocilo = cgi.escape(self.request.get("sporocilo"))
        sporocilo.put()
        return self.redirect("/vsa-sporocila")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("izbrisi_sporocilo.html", spremenljivke)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        return self.redirect("/vsa-sporocila")

class IzbrisanaSporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query(Sporocilo.izbrisan == True).fetch()
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocila": sporocila, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("/izbrisana_sporocila.html", spremenljivke)

class ObnoviSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("/obnovi_sporocilo.html", spremenljivke)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = False
        sporocilo.put()
        return self.redirect("/vsa-sporocila")

class DokoncnoIzbrisiHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")
            spremenljivke = {
                "sporocilo": sporocilo, "logiran": logiran, "user": user, "logout_url": logout_url,
            }
            return self.render_template("/dokoncno_izbrisi.html", spremenljivke)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()
        return self.redirect("/izbrisana-sporocila")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/shrani', ShraniHandler),
    webapp2.Route('/vsa-sporocila', VsaSporocilaHandler),
    webapp2.Route('/posamezno-sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/posamezno-sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/posamezno-sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
    webapp2.Route('/izbrisana-sporocila', IzbrisanaSporocilaHandler),
    webapp2.Route('/posamezno-sporocilo/<sporocilo_id:\d+>/obnovi', ObnoviSporociloHandler),
    webapp2.Route('/posamezno-sporocilo/<sporocilo_id:\d+>/dokoncno-izbrisi', DokoncnoIzbrisiHandler),
], debug=True)
