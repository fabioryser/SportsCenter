from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
# initialize the database
db = SQLAlchemy(app)

#Create db model
class Players(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    shirt_number = db.Column(db.Integer)
    role = db.Column(db.String(25), nullable = False)
    #Create a function to return a string when we add something
    tickets = relationship("Ticket",backref="ticketer")
    # Create a function to retrun a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(50), nullable=False)
    ticket_description = db.Column(db.String(200), nullable=False)
    # pub_date = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    cost = db.Column(db.Integer)
    asigned_to = db.Column(db.Integer, ForeignKey('player.id'))

    def __repr__ (self):
        return '<Name %r>' % self.id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/TeamMembers", methods=['POST', 'GET'])
def team_members():
    if request.method == "POST":
        player_first_name = request.form['first_name']
        player_last_name = request.form['last_name']
        player_shirt_number = request.form['shirt_number']
        player_role = request.form['role']
        new_player = Players(first_name = player_first_name, last_name = player_last_name, shirt_number = player_shirt_number, role = player_role)
        #
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/TeamMembers')
        except:
            return "There was an error adding a player"
    else:
        players = Players.query.order_by(Players.id)
        return render_template("players.html", players=players)

@app.route('/delete/<int:id>')
def delete(id):
    player_to_delete = Players.query.get_or_404(id)
    try:
        db.session.delete(player_to_delete)
        db.session.commit()
        return redirect('/TeamMembers')
    except:
        return "There was a problem deleting this player!"

@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    player_to_update = Players.query.get_or_404(id)
    if request.method == "POST":
        player_to_update.first_name = request.form['first_name']
        player_to_update.last_name = request.form['last_name']
        player_to_update.shirt_number = request.form['shirt_number']
        player_to_update.role = request.form['role']
        try:
            db.session.commit()
            return redirect('/TeamMembers')
        except:
            return "There was a problem updating your player"
    else:
        return render_template('update.html', player_to_update=player_to_update)

@app.route('/Tickets', methods=['POST','GET'])
def tickets():
    if request.method == "POST":
        ticket_for = request.form["names"]
        ticket_name = request.form['ticket_name']
        ticket_description = request.form['ticket_description']
        # ticket_pub_date = request.for["pub_date"]
        cost = request.form['cost']
        new_ticket = Ticket(ticket_name = ticket_name, ticket_description = ticket_description, asigned_to = ticket_for, cost=cost)
        try:
            db.session.add(new_ticket)
            db.session.commit()
            return redirect('/Tickets')
        except:
            return "There was an error adding a ticket"
    else:
        tickets = Ticket.query.order_by(Ticket.ticket_id)
        players = Players.query.all()
        return render_template("tickets.html", tickets=tickets, players=players)

if __name__ == '__main__':
    app.run(port=1337, debug=True)