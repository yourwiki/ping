#!/usr/bin/env python

import logging

from django.utils import simplejson

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from extensions import BaseHandler
from models import Update

class MainHandler(BaseHandler):
	def get(self):
		updates = self.get_updates()
		self.render('index.html', { 'updates': updates })
	
	def get_updates(self):
		updates = memcache.get("updates")
		if updates is not None:
			return updates
		else:
			updates = Update.gql("ORDER BY posted DESC LIMIT 15")
			memcache.add("updates", updates, (60 * 60 * 24 * 7))
			return updates

class UpdateHandler(BaseHandler):
	def post(self):
		update = Update()
		
		user = users.get_current_user()
		if user:
			update.author = user
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

application = webapp.WSGIApplication(
	[
		('/', MainHandler),
		('/ajax/update', UpdateHandler)
	],
	debug=True
)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
