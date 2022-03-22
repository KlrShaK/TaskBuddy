import bdb

from flask import render_template, flash, redirect
from flask import current_app as app
from flask.helpers import url_for
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from application.models import *
from application.form import *


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    trackers_temp = None
    trackers_temp = Tracker.query.filter_by(user_id=current_user.get_id()).all()
    return render_template("dashboard.html", trackers=trackers_temp)


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # clearing the form
        form.username.data = ""
        form.password.data = ""
        userqueried = User.query.filter_by(user_name=username).first()
        if userqueried:
            if check_password_hash(userqueried.hashed_password, password):
                login_user(userqueried)
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong Password!!!")
        else:
            flash("User doesn't exists!!! Please register")

    return render_template("login.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been Logged out!! Login Again to use.")
    return redirect(url_for("login"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.firstname.data
        last_name = form.lastname.data
        user = User.query.filter_by(user_name=form.username.data).first()
        if user == None:
            u = User(user_name=form.username.data, hashed_password=generate_password_hash(form.password.data),
                     firstname=form.firstname.data, lastname=form.lastname.data)
            db.session.add(u)
            db.session.commit()
            # clearing the form
            form.username.data = ""
            form.password.data = ""
            form.firstname.data = ""
            form.lastname.data = ""
            form.checkpassword.data = ""
            flash("User Added successfully!!")
            return redirect(url_for("login"))
        else:
            flash("Username already exists!!")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"), 404


@app.route("/add_tracker/<currentUserId>", methods=['GET', 'POST'])
@login_required
def add_tracker(currentUserId):
    flash("You Cannot Change Tracker Type and Settings Later!")
    form = AddorEditTrackerForm(trackerType = 0)
    tracker = None
    if form.validate_on_submit():
        tracker_name = form.trackerName.data.upper()
        tracker_desc = form.trackerDesc.data
        tracker_type = form.trackerType.data
        if tracker_type == '0':
            tracker_sett = None
        else:
            tracker_sett = form.trackerSetting.data
            tracker_sett = str(tracker_sett.split(','))

        tracker = Tracker.query.filter_by(tracker_name=tracker_name, user_id=int(currentUserId)).first()
        if tracker == None:
            tracker = Tracker(tracker_name=tracker_name, user_id=int(currentUserId), description=tracker_desc, settings=tracker_sett
                        ,last_reviewed=datetime.now(), tracker_type=tracker_type)
            db.session.add(tracker)
            db.session.commit()
            flash("Deck has been added successfully!!!")
            return redirect(url_for("dashboard"))
        else:
            flash("Deck already exists!!!")
    return render_template("add_edit_tracker.html", form=form, form_title="Add")

# todo prefilled values
# todo update value of last_reviewed whenever new log is added
@app.route("/edit_tracker/<trackerid>", methods=['GET', 'POST'])
@login_required
def edit_tracker(trackerid):
    flash("You Can Only Change Tracker Name and Description")
    form = AddorEditTrackerForm()
    tracker = None
    if form.validate_on_submit():
        tracker = Tracker.query.filter_by(tracker_id=int(trackerid)).first()
        anothertracker = Tracker.query.filter_by(tracker_name=form.trackerName.data).first()

        if anothertracker is None:
            if form.trackerName.data != '': tracker.tracker_name = form.trackerName.data
            if form.trackerDesc.data != '': tracker.description = form.trackerDesc.data
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash("Tracker with Same Name Present")
    return render_template("add_edit_tracker.html", form_title="Edit", form=form)


@app.route("/delete_tracker/<trackerid>", methods=['GET', 'POST'])
@login_required
def delete_tracker(trackerid):
    tracker = Tracker.query.filter_by(tracker_id=int(trackerid)).first()
    if len(tracker.log) == 0:
        db.session.delete(tracker)
        db.session.commit()
        flash("Tracker Deleted!!!")
        return redirect(url_for("dashboard"))
    else:
        flash("Tracker have Logs, delete them first!!")
        return redirect(url_for("dashboard"))

@app.route("/add_log/<trackerid>", methods=['GET', 'POST'])
@login_required
def add_log(trackerid):
    temp_tracker = Tracker.query.filter_by(tracker_id=int(trackerid)).first()
    # todo this not publishing
    timestamp, value, notes = None, None, None
    log = None
    if temp_tracker.tracker_type != '0':
        choices = temp_tracker.settings
        flash("You Can Only choose value from {}".format(choices))
    # activate Form
    form = AddLogForm()
    if form.validate_on_submit():
        flash("validated")
        timestamp = form.timestamp.data
        print("time_stamp: ", timestamp)
        notes = form.notes.data
        log = Log.query.filter_by(timestamp=timestamp, tracker_id=int(trackerid), user_id=temp_tracker.user_id).first()
        if log is None:
            if temp_tracker.tracker_type == '0':
                value = float(form.value.data)
                log = Log(timestamp=timestamp, value=value, value_mcq_choice=None, notes= notes, tracker_id=int(trackerid), user_id=temp_tracker.user_id)
            else:
                choices = eval(temp_tracker.settings)
                temp_value = form.value.data
                if temp_value in choices:
                    value = temp_value
                    log = Log(timestamp=timestamp, value=None, value_mcq_choice=value, notes=notes, tracker_id=int(trackerid),
                              user_id=temp_tracker.user_id)
                else:
                    flash("Invalid Choice of values")

            db.session.add(log)
            db.session.commit()
            flash("Success")
            return "log_added_Sucessfully" #redirect(url_for("view_cards", deckid=deckid))
    flash("failed")
    print("form_errors",form.errors)
    return render_template("add_edit_log.html", form=form, formtitle="Add Log")

@app.route("/view_cards/<trackerid>", methods=['GET', 'POST'])
@login_required
def view_tracker(trackerid):
    # cards = None
    # cards = Card.query.filter_by(deck_id=trackerid)
    # return render_template("tracker.html", cards=cards, trackerid=trackerid)
    return "view card page"


@app.route("/delete_card/<cardid>/<trackerid>", methods=['GET', 'POST'])
@login_required
def delete_card(cardid, trackerid):
    # card = Card.query.filter_by(id=int(cardid)).first()
    # Card.query.filter_by(id=int(cardid)).delete()
    # deck = Deck.query.filter_by(deck_id=trackerid).first()
    # deck.deck_score -= card.card_score
    # db.session.commit()
    # flash("Card Deleted!!!")
    # return redirect(url_for("view_cards", trackerid=int(trackerid)))
    return "delete_card page"

@app.route("/edit_card/<cardid>", methods=['GET', 'POST'])
@login_required
def edit_card(cardid):
    # card = None
    # form = AddCardForm()
    # if form.validate_on_submit():
    #     card = Card.query.filter_by(id=int(cardid)).first()
    #     card.question, card.answer = form.question.data, form.answer.data
    #     db.session.commit()
    #     return redirect(url_for("view_cards", trackerid=card.deck_id))
    # return render_template("add_edit_log.html", form=form, formtitle="Edit")
    return "edit card page"

@app.route("/review_card/<cardid>", methods=['GET', 'POST'])
@login_required
def review_card(cardid):
    # form = ReviewCardForm()
    # card = Card.query.filter_by(id=int(cardid)).first()
    # if form.validate_on_submit():
    #     rating = form.rate.data
    #     card.card_score = int(rating)
    #     card.last_reviewed = datetime.now().strftime('%d-%m-%Y %H:%M')
    #     trackerid = card.deck_id
    #     deck = Deck.query.filter_by(deck_id=trackerid).first()
    #     cards = deck.cards
    #     deckscore = 0
    #     for card in cards:
    #         deckscore += card.card_score
    #     deck.deck_score = deckscore
    #     deck.last_reviewed = datetime.now().strftime('%d-%m-%Y %H:%M')
    #     db.session.commit()
    #     return redirect(url_for("view_cards", trackerid=int(card.deck_id)))
    #
    # return render_template("reviewcard.html", form=form, card=card)
    return "review_card page"

