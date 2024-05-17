import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def loadReservations():
    with open('reservations.json') as res:
        listOfReservations = json.load(res)['reservations']
        return listOfReservations


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
reservations = loadReservations()


@app.route('/')
def index(error=None):
    return render_template('index.html', error=error)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        return index(error='No club found with that email address')
    return render_template('welcome.html', club=club[0], competitions=competitions, clubs=clubs)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    maxPlaces = min(int(foundClub['points']), (12 - getClubNbReservations(foundClub, foundCompetition)))
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition, maxPlaces=maxPlaces)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    clubBookedPlaces = getClubNbReservations(club, competition)

    #max 12 places
    if clubBookedPlaces + placesRequired > 12:
        if clubBookedPlaces == 0:
            flash('You can only book a maximum of 12 places for a competition')
        else:
            flash('You can only book a maximum of 12 places for a competition and you have already booked ' + str(clubBookedPlaces) + ' places')

    # Check if the club has enough points
    elif int(club['points']) >= placesRequired:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = str(int(club['points']) - placesRequired)  # Deduct the points from the club's total
        # Update the reservations
        addReservation(club, competition, placesRequired)
        flash('Great-booking complete!')
    else:
        flash('Not enough points to complete this booking.')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

def addReservation(club, competition, places):
    # Créer une nouvelle réservation
    new_reservation = {'club': club['name'], 'competition': competition['name'], 'places': places}

    # Vérifier si une réservation similaire existe déjà
    for reservation in reservations:
        if reservation['club'] == club['name'] and reservation['competition'] == competition['name']:
            # Si oui, ajouter les places à la réservation existante
            reservation['places'] += places
            break
    else:
        # Si non, ajouter la nouvelle réservation à la liste
        reservations.append(new_reservation)

def getClubNbReservations(club, competition):
    clubBookedPlaces = 0
    for reservation in reservations:
        if reservation['club'] == club['name'] and reservation['competition'] == competition['name']:
            clubBookedPlaces = reservation['places']
    return int(clubBookedPlaces)