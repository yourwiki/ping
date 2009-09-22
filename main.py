#!/usr/bin/env python

import logging

from django.utils import simplejson

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import extensions
import models

class MainHandler(extensions.BaseHandler):
	def get(self):
		updates = self.get_updates()
		self.render('index.html', { 'updates': updates })
	
	def get_updates(self):
		updates = memcache.get("updates")
		if updates is not None:
			return updates
		else:
			updates = models.Update.gql("ORDER BY posted DESC LIMIT 15")
			memcache.add("updates", updates, (60 * 60 * 24 * 7))
			return updates

class UpdateHandler(extensions.BaseHandler):
	def post(self):
		update = models.Update()
		
		if self.current_account:
			update.author = self.current_account
		else:
			self.response.set_status(400)
			return
		
		if self.request.get('update_body'):
			update.body = self.request.get('update_body')
		else:
			self.response.set_status(400)
			return
		
		memcache.delete('updates', 0)
		update.put()
		
		response = {
			'body': update.body,
			'update': self.render_partial('update.html', { 'update': update })
		}
		self.response.out.write(simplejson.dumps(response))

class SettingsHandler(extensions.BaseHandler):
	def get(self):
		self.render('settings.html')
		
	def post(self):
		# save settings
		pass

application = webapp.WSGIApplication(
	[
		('/', MainHandler),
		('/ajax/update', UpdateHandler),
		('/settings', SettingsHandler)
	],
	debug=True
)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
