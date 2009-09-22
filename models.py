from google.appengine.ext import db

class Account(db.Model):
	user = db.UserProperty(auto_current_user_add=True, required=True)
	screen_name = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)

class Update(db.Model):
        author = db.ReferenceProperty(Account)
        body = db.StringProperty(multiline=True)
        posted = db.DateTimeProperty(auto_now_add=True)

