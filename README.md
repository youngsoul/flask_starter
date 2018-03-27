## Flask Starter

This project will be a starter project using Flask and creative-tim.com theme called:

[Get SH IT done](https://www.creative-tim.com/product/get-shit-done-kit)

This project will use flask-login, blueprints for a basic starter with a login and a landing page.  It will not use a database but this can be added later.

When you navigate to the index page: localhost:5000 if you are running a typical flask web server, if you are not logged in you will be redirected to the login page.  Once logged in you are navigated back to the index page.

From the index page, you are able to transition to another page, served from another blueprint.  Just a simple way to show navigating between blueprints and to make sure the static url resolution was working.


## Install

- flask
- flask-wtf
- flask-login

## Creative Tim Updates

* where you see:

*href="assets/img/apple-icon.png"*

Change this to use the url_for, for the 'static' folder

*href="{{ url_for('static', filename='assets/img/apple-icon.png') }}*

or, notice the url method around the jinja url_for,

*... style="background-image: url( {{ url_for('static', filename='assets/img/cover_4.jpg', _external=True) }} )">*


## Users

This flask starter does not use a database, but the users are defined in *config.py*


