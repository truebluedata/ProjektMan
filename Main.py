import webapp2,logging,urllib,os
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
import jinja2

class Person(db.Model):
	name=db.StringProperty() #name of the person
	score=db.FloatProperty() #score assigned after complex algorithm
	projects=db.ListProperty(db.Key) #can belong to multiple projects

#main project
class Project(db.Model):
	name=db.StringProperty()
	description=db.TextProperty()
	deadline=db.DateTimeProperty()
	score=db.FloatProperty() #score of a project based on qualities and other factors again algo required
	@property
	def members(self):
		return Person.gql("WHERE projects = :1",self.key()) #can have multiple members , many to many

#Excuses = one to many relation with person

class Excuse(db.Model):
	person=db.ReferenceProperty(Person,collection_name='excuses')
	title=db.TextProperty()
	description=db.TextProperty()

#Tasks are the roles of a person
	
class Tasks(db.Model):
	project=db.ReferenceProperty(Project,collection_name='pro_tasks') #tasks of a particular project
	person=db.ReferenceProperty(Person,collection_name='per_tasks')  #tasks of a particular person
	deadline=db.DateTimeProperty()
	title=db.TextProperty() #title
	description=db.TextProperty() #description of task


class Review(db.Model):
	project=db.ReferenceProperty(Project,collection_name='pro_reviews') #reviews of project
	reviewer=db.ReferenceProperty(Person,collection_name='per_reviews') #reviews by a person
	title=db.TextProperty()
	description=db.TextProperty()
	stars=db.FloatProperty() #what stars the reviewer gives

