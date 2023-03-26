# PALOVERSE
#### Video Demo:  https://www.youtube.com/watch?v=OIWbbDr3c-I
#### Description:
Paloverse is a a web application that I built using Flask, Jinja2, HTML, CSS, Python, and JavaScript. The application authenticates users via Azure AD and
uses XML API (GET) to get data. This web application is meant to serve as a convenient place to bring key information together from Palo Alto infrastructure such as Prisma Cloud, SD-WAN, ADEM, GlobalProtect, Panorama, and Next Generation Firewalls.

I utilize a helpers file to display an error message in the event that form entry does not meet requirements and also a decorator for requiring that users be
authenticated via Azure AD to view pages specified. For this application, I've applied that to every page, so a user cannot see anything unless they have an active
session and/or have been authenticated via my Azure AD tenant.

For the main application (Python), I configured the application per the Flask documentation and hosted it on my laptop with a virtual environment (venv) setup.
This required me to set a secret key for sessions, as well as do some other research as I wanted to host it locally for development. I initially had
a register and login setup with a local database to store hashed passwords. As I worked more on the project, I realized that this isn't really that useful or secure
for use in the real world, so I switched over to authenticating users via Azure AD. This was one of the most challenging parts of the project, because there were
several knowledge gaps I had to fill to get it working.

First, I had to create an Azure AD tenant. This was simple enough, and Microsoft really does make this kind of stuff easy on developers which was really nice.
Next, I had to figure out what library to use to enable this authentication. This part was difficult, because there are quite a few choices and not all of them had
great documentation. After much trial and error, I stumbled upon flask dance, which makes OAuth pretty straightforward with my flask application. After finding all
of the relevant information and doing quite a bit of testing, I got it working and was able to force users to authenticate via my Azure AD tenant with MFA. It
worked quite well, but I was getting session errors after an hour which would make it impossible to continue navigating to the site. After much research and
testing, I added some error handling to my helper file and applied it to every page. I also had to do some workarounds for ssl to avoid issues, but since this
is a project the workarounds were fine and met my needs. It was very rewarding getting this all working and I learned a lot about designing secure systems.

Ideally, I would have liked to display information in tables via XML API but that was not possible with my lab firewalls. They have limitations as this application
is much more useful when run in an enterprise environment. To replicate what that would look like, I used CSV and JSON files as they are close to what you would get
via an API GET. I then go through that data, put it into various lists, and display it in a table that in some cases has been enhanced via JavaScript. The result
is an aesthetically pleasing and easy to navigate web application with extremely relevant information and management tools/links for a Network and/or Security Engineer that uses Palo Alto Networks products in their environment.