import os, md5, urllib
import models
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

class BaseHandler(webapp.RequestHandler):
	current_account = None

	def initialize(self, request, response):
		super(BaseHandler, self).initialize(request, response)
		user = users.get_current_user()
		if user:
			self.current_account = models.Account.all().filter('user =', user).get()
			
			if not self.current_account and not self.request.uri.endswith('/settings'):
				self.redirect("/settings")
				return
	
	def render(self, path, template_values={}):
		user = users.get_current_user()
		if user:
			auth_url = users.create_logout_url(self.request.uri)
			logged_in = True
		else:
			auth_url = users.create_login_url(self.request.uri)
			logged_in = False
		
		default_values = {
			'auth_url': auth_url,
			'logged_in': logged_in,
			'user': user
		}
		
		default_values.update(template_values)
		full_path = os.path.join(os.path.dirname(__file__), 'templates', path)
		self.response.out.write(template.render(full_path, default_values))
	
	def render_partial(self, path, template_values={}):
		full_path = os.path.join(os.path.dirname(__file__), 'templates', 'partials', path)
		return template.render(full_path, template_values)
	
	def require_auth(self, api=False):
		if not users.get_current_user():
			self.redirect(users.create_login_url(self.request.uri))
