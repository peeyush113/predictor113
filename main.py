#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import cgi
import webapp2
import jinja2
import re
from predict import predict

# env for loading local template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


predictObj = predict()
data = predict.createData(predictObj)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            "jobSeekerData" : data[1],
            "jobProviderData" : data[0]
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))

class getSuggest(webapp2.RequestHandler):
    def post(self):
        suggestions = predict.suggest(predictObj, int(cgi.escape(self.request.get('selectedId'))))
        self.response.write(suggestions)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getSuggest', getSuggest)
], debug=True)
