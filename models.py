from google.appengine.ext import db

class Update(db.Model):
	author = db.UserProperty()
	body = db.StringProperty(multiline=True)
	posted = db.DateTimeProperty(auto_now_add=True)
