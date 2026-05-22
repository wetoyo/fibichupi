from flask import Flask, render_template, request, session, redirect, url_for
import auth
app = Flask(__name__)
app.secret_key = '5d13cfb7ed33261d8f37a3d1b54632e67c328d6f674a174cefd31ac5d1938e66'

@app.route("/", methods=["GET", "POST"])
def homepage():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("user_id").strip()
        password = request.form.get("password").strip()
        if auth.user_exists(username):
            if auth.login(username, password):
                session["user_id"] = username
                return redirect(url_for("homepage"))
            else:
                error_msg = "Password is incorrect."
        else:
            error_msg = "User does not exist. Please register."
    return render_template("login.html", error = error_msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("user_id").strip()
        password = request.form.get("password").strip()
        result = auth.register(username, password)
        if result == "Registered":
            return redirect(url_for("login"))
        else:
            error_msg = result
    return render_template("register.html", error=error_msg)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/create_market", methods=["GET", "POST"])
def create_market():
    if not require_login():
        return redirect(url_for("login"))
    error_msg = ""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not title:
            error_msg = "Title is required."
        else:
            mid = data.create_market(title, description, current_user())
            return redirect(url_for("market", market_id=mid))
    return render_template("create_market.html", error=error_msg, user=current_user())

@app.route("/market/<int:market_id>", methods=["GET"])
def market(market_id):
    if not require_login():
        return redirect(url_for("login"))
    m = data.get_market(market_id)
    if not m:
        return redirect(url_for("homepage"))
    totals = data.get_market_totals(market_id)
    price = data.current_price(market_id)
    bets = data.get_market_bets(market_id)
    return render_template(
        "bet.html",
        market=m,
        totals=totals,
        price=price,
        bets=bets,
        user=current_user(),
        balance=data.get_balance(current_user()),
        is_creator=(m["creator_id"] == current_user()),
    )

@app.route("/market/<int:market_id>/bet", methods=["POST"])
def place_bet(market_id):
    if not require_login():
        return redirect(url_for("login"))
    side = request.form.get("side")
    try:
        amount = int(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    result = data.place_bet(current_user(), market_id, side, amount)
    if result != "ok":
        flash(result)
    return redirect(url_for("market", market_id=market_id))

@app.route("/market/<int:market_id>/resolve", methods=["POST"])
def resolve(market_id):
    if not require_login():
        return redirect(url_for("login"))
    result_side = request.form.get("result")
    msg = data.resolve_market(market_id, result_side, current_user())
    if msg != "ok":
        flash(msg)
    return redirect(url_for("market", market_id=market_id))


@app.route("/profile", methods=["GET"])
def profile():
    if not require_login():
        return redirect(url_for("login"))
    user = current_user()
    return render_template(
        "profile.html",
        user=user,
        balance=data.get_balance(user),
        bets=data.get_user_bets(user),
        markets=data.get_user_markets(user),
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
