import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get username of current user and assign to variable
    db_username = db.execute("SELECT username FROM users WHERE id IN (?)", session["user_id"])
    current_user = db_username[0]
    username = current_user.get("username")

    # Get inventory information for stocks
    inventory = db.execute("SELECT DISTINCT symbol, SUM(shares) FROM inventory WHERE username = (?) GROUP BY symbol", username)

    # Get cash value from user table
    users = db.execute("SELECT cash FROM users WHERE username = (?)", username)

    cash = users[0].get("cash")

    # Get number of distinct stocks to define number of iterations
    db_rows = db.execute("SELECT COUNT(DISTINCT symbol) FROM inventory WHERE username = (?)", username)
    r_rows = db_rows[0].get("COUNT(DISTINCT symbol)")
    rows = range(r_rows)

    # Define totals variable for use in grand total calculation
    totals = 0 + cash

    # Iterate on stock data to get stock value totals
    for stock in rows:

        # Get stock symbol for user
        db_symbol = db.execute("SELECT DISTINCT symbol FROM buys WHERE username = (?)", username)
        current_symbol = db_symbol[stock]
        symbol = current_symbol.get("symbol")

        # Get price infor for stock
        stock_info = lookup(symbol)
        price = stock_info["price"]

        # Get number of bought shares for the stock
        db_shares = db.execute("SELECT SUM(shares) FROM buys WHERE symbol = (?) AND username = (?)", symbol, username)
        shares = db_shares[0].get("SUM(shares)")

        # Add totals based on the price of the stocks and share ownership
        totals = totals + price * shares

    # Return user to home page and pass variables
    return render_template("index.html", inventory=inventory, lookup=lookup, usd=usd, users=users, sum=sum, int=int, totals=totals)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure stock symbol is a valid length
        if not len(request.form.get("symbol")) <= 5:
            return apology("stock symbol length is invalid", 400)

        # Ensure number of shares is entered
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # Ensure a valid number of shares was submitted
        shares_entry = request.form.get("shares")
        if not shares_entry.isdigit():
            return apology("number of shares must be an integer", 400)
        if not int(shares_entry) > 0:
            return apology("number of shares must be an integer", 400)
        if not float(shares_entry).is_integer():
            return apology("number of shares must be an integer", 400)

        # Look up current stock information based on submitted symbol, handle error if stock doesn't return a value
        if lookup(request.form.get("symbol")) is None:
            return apology("please enter a valid stock", 400)
        else:
            stock_info = lookup(request.form.get("symbol"))

        # Set symbol variable
        symbol = stock_info["symbol"]

        # Set shares variable
        shares = int(request.form.get("shares"))

        # Set price variable
        price = float(stock_info["price"])

        # Set total cost variable
        cost = shares * price

        # Get current date and time
        date = datetime.now()

        # Get username of current user and assign to variable
        db_username = db.execute("SELECT username FROM users WHERE id IN (?)", session["user_id"])
        current_user = db_username[0]
        username = current_user.get("username")

        # Look up user's remaining cash from database and assign to variable
        db_cash = db.execute("SELECT cash FROM users WHERE id IN (?)", session["user_id"])
        current_cash = db_cash[0]
        cash = int(current_cash.get("cash"))

        # Get new cash value after stock purchase
        new_cash = float(cash - cost)

        # Inform user they cannot make the purchase and prevent it if remaining cash is less than the purchase amount
        if not (float(cash) - cost) > 0:
            return apology("you cannot afford this purchase", 400)

        # Create database table for buys if it has not already been created
        db.execute("CREATE TABLE IF NOT EXISTS buys (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, date DATETIME2 NOT NULL)")

        # Add purchase to database table for buys
        db.execute("INSERT INTO buys (username, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)",
                   username, symbol, shares, price, date)

        # Create database table for inventory if it has not already been created
        db.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL)")

        # Check to see if shares already exist for user
        check_shares = db.execute("SELECT shares from inventory WHERE username = ? AND symbol = ?", username, symbol)

        if len(check_shares) == 0:
            db.execute("INSERT INTO inventory (username, symbol, shares) VALUES(?, ?, ?)", username, symbol, shares)
        else:
            new_shares = shares + check_shares[0].get("shares")
            db.execute("UPDATE inventory SET shares = ? WHERE username = ? AND symbol = ?", new_shares, username, symbol)

        # Update user's cash amount after purchase in database
        db.execute("UPDATE users SET cash = ? WHERE username = ?", new_cash, username)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get username of current user and assign to variable
    db_username = db.execute("SELECT username FROM users WHERE id IN (?)", session["user_id"])
    current_user = db_username[0]
    username = current_user.get("username")

    # Get table from database for buys
    buys = db.execute("SELECT symbol, shares, price, date FROM buys WHERE username = (?)", username)

    # Get table from database for sells
    sells = db.execute("SELECT symbol, shares, price, date FROM sells WHERE username = (?)", username)

    # Render history page and send tables to page for display
    return render_template("history.html", buys=buys, sells=sells, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure stock symbol is a valid length
        if not len(request.form.get("symbol")) <= 5:
            return apology("stock symbol length is invalid", 400)

        # Ensure symbol does not contain special character
        if any(not char.isalnum() for char in request.form.get("symbol")):
            return apology("symbol cannot contain a special character", 400)

        # Ensure symbol does not contains number
        if any(char.isnumeric() for char in request.form.get("symbol")):
            return apology("symbol cannot contain a number", 400)

        # Look up current stock information based on submitted symbol, handle error if stock doesn't return a value
        if lookup(request.form.get("symbol")) is None:
            return apology("please enter a valid stock", 400)

        # Define response variable for lookup to pass information to html page
        response = lookup(request.form.get("symbol"))

        # Redirect user to page where quote is displayed
        return render_template("quoted.html", response=response, usd=usd)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password meets length complexity
        elif not len(request.form.get("password")) >= 8:
            return apology("password must be 8 characters or greater", 400)

        # Ensure password contains special character
        if not any(not char.isalnum() for char in request.form.get("password")):
            return apology("password must contain a special character", 400)

        # Ensure password contains number
        if not any(char.isnumeric() for char in request.form.get("password")):
            return apology("password must contain a number", 400)

        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Define username variable based on input
        username = request.form.get("username")

        # Add user and hashed password to database
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Check to see if username already exists, if it does - return error message
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("username already exists", 400)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a stock symbol was selected
        if not request.form.get("symbol"):
            return apology("must select stock symbol", 400)

        # Ensure number of shares was submitted
        if not int(request.form.get("shares")) > 0:
            return apology("must input number of shares as a positive integer", 400)

        # Look up current stock information based on submitted symbol
        stock_info = lookup(request.form.get("symbol"))

        # Set symbol variable
        symbol = stock_info["symbol"]

        # Set shares variable
        shares = int(request.form.get("shares"))

        # Set price variable
        price = float(stock_info["price"])

        # Set total sale variable
        sale = shares * price

        # Get current date and time
        date = datetime.now()

        # Get username of current user and assign to variable
        db_username = db.execute("SELECT username FROM users WHERE id IN (?)", session["user_id"])
        current_user = db_username[0]
        username = current_user.get("username")

        # Look up user's remaining cash from database and assign to variable
        db_cash = db.execute("SELECT cash FROM users WHERE id IN (?)", session["user_id"])
        current_cash = db_cash[0]
        cash = int(current_cash.get("cash"))

        # Get new cash value after stock purchase
        new_cash = float(cash + sale)

        # Check to see if shares already exist for user
        check_shares = db.execute("SELECT shares from inventory WHERE username = ? AND symbol = ?", username, symbol)

        # Create entry for stock if the user doesn't have any, apologize if they are trying to sell more than they have, else update entry
        if len(check_shares) == 0:
            db.execute("INSERT INTO inventory (username, symbol, shares) VALUES(?, ?, ?)", username, symbol, shares)
        if check_shares[0].get("shares") < shares:
            return apology("you do not have enough shares for this sale", 400)
        if check_shares[0].get("shares") - shares == 0:
            db.execute("DELETE FROM inventory WHERE username = ? AND symbol = ?", username, symbol)
        else:
            new_shares = check_shares[0].get("shares") - shares
            db.execute("UPDATE inventory SET shares = ? WHERE username = ? AND symbol = ?", new_shares, username, symbol)

        # Create database table for sells if it has not already been created
        db.execute("CREATE TABLE IF NOT EXISTS sells (sale_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, date DATETIME2 NOT NULL)")

        # Add sale to database
        db.execute("INSERT INTO sells (username, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)",
                   username, symbol, shares, price, date)

        # Update user's cash amount after sale in database
        db.execute("UPDATE users SET cash = ? WHERE username = ?", new_cash, username)

        # Redirect user to home page
        return redirect("/")
    else:
        # Get username of current user and assign to variable
        db_username = db.execute("SELECT username FROM users WHERE id IN (?)", session["user_id"])
        current_user = db_username[0]
        username = current_user.get("username")

        # Get selections of stocks owned to sell
        inventory = db.execute("SELECT DISTINCT symbol from inventory WHERE username = ? ORDER BY symbol", username)

        return render_template("sell.html", inventory=inventory)
