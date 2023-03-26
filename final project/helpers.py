from flask import redirect, render_template, url_for
from functools import wraps
from flask_dance.contrib.azure import azure
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not azure.authorized:
            try:  
                if not azure.authorized:
                    return redirect(url_for("azure.login"))
                resp = azure.get("/v1.0/me")
                assert resp.ok
                return render_template('index.html', user_name=resp.json()["displayName"])
            except TokenExpiredError as e:
                return redirect(url_for("azure.login"))
        return f(*args, **kwargs)
    return decorated_function



