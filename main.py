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

import webapp2
import cgi
import re


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signin</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        User Signup
    </h1>
"""

page_footer = """
</body>
</html>
"""

edit_header = "<h3>FEED ME YOUR PERSONAL INFORMATION</h3>"
add_form = """
<form action="/signup" method="post">
    <table>
        <tbody>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input name="username" type="text" value="{0}" required/>
                    <span class="error">{1}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input name="password" type="password" value="" required/>
                    <span class="error">{2}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="verify">Verify Password</label>
                </td>
                <td>
                    <input name="verify" type="password" value="" required/>
                    <span class="error">{3}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email">Email (Optional)</label>
                </td>
                <td>
                    <input name="email" type="email" value="{4}"/>
                    <span class="error">{5}</span>
                </td>
            </tr>
        </tbody>
    </table>
    <input type="submit" value="FEED">
</form>
"""
home_form = """
<form action="/" method="get">
    <input type="submit" value="Sign Out"/>
</form>
"""

new_post = """
<!DOCTYPE html>
<html>
<head>
    <title>Signed IN</title>
</head>
<body>
    <h2>Welcome, {0}</h2>
    <p> Thank yeww for that!</p>
</body>
<form action="/" method="get">
    <input type="submit" value="Sign Out"/>
</form>
</html>
"""
class Signed_in(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(new_post.format(username))
        else:
            self.redirect('/in')

class Signup(webapp2.RequestHandler):
    def get(self):
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''
        main_content = edit_header + add_form.format("","","","","","") + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)
    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        validusername = ""
        validemail = ""
        if valid_username(username):
            validusername = username
        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True
        if not valid_password(password):
            error_password = "That wasn't a valid password."
            have_error = True
        if password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True
        if valid_email(email):
            validemail = email
        if not valid_email(email):
            error_email = "That's not a valid email."
            have_error = True
        if have_error == False:
            self.redirect('/in?username=' + username)
        if have_error == True:
            main_content = edit_header + add_form.format(validusername, error_username, error_password, error_verify, validemail, error_email)
            content = page_header + main_content + page_footer
            self.response.write(content)

class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect('/signup')





USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/signup",Signup),
    ('/in',Signed_in)
], debug=True)
