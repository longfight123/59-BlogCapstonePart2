"""Personal Blog (Capstone Part 1)

This 'Flask' app website is the second part of a 'Blog Capstone' project.
It has 4 pages: The index, about, contact and an individual blog post page.
There are 2 HTML templates used in inheritance to keep specific elements on each page.
The blog posts data are obtained from an API. 'Jinja' templating is used
to render 'Python' code inside the HTML templates. The static files (CSS, img, JS) were provided
by the instructor.

This script requires that 'Flask', 'requests', 'smtplib',
and 'python_dotenv' be installed within the Python
environment you are running this script in.

"""

from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv('.env')
GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

app = Flask(__name__)

response = requests.get(url='https://api.npoint.io/4af156202f984d3464c3')
response.raise_for_status()
data = response.json()


@app.route('/')
def get_all_posts():
    """the landing page, displays all blog posts

    GET: Landing page
    """
    return render_template('index.html', allposts=data)


@app.route('/about')
def get_about_page():
    """the about page, displays information about the blog

    GET: About page
    """
    return render_template('about.html')


@app.route('/contact')
def get_contact_page():
    """the contact page, displays a form

    GET: Contact page
    """
    return render_template('contact.html')


@app.route('/blogpost/<int:num>')
def get_post(num):
    """the individual blog post page, displays one blog post

    GET: Individual blog post page
    """
    blogpost = data[num]
    return render_template('post.html', post=blogpost)


@app.route('/form-entry', methods=['POST'])
def receive_data():
    """When a contact me form is submitted, a POST request is made to this route

    POST: Sends email with data in form
    """
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=GMAIL_USERNAME, password=GMAIL_PASSWORD)
        connection.sendmail(from_addr=request.form["email"], to_addrs=os.getenv('GMAIL_USERNAME'),
                            msg=f'Subject: Day-60-Contact \n\nName {request.form["name"]}\nEmail: {request.form["email"]}'
                                f'\nPhone: {request.form["phone"]}\nMessage: {request.form["message"]}')
    return '<h1>Successfully sent your message! </h1>'

if __name__ == '__main__':
    app.run(debug=True)