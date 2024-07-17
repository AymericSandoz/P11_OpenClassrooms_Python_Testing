import json
from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
from datetime import datetime


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


def saveDataToJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def saveAllData():
    """ save clubs, competitions and reservations to JSON files """
    saveDataToJson({'clubs': clubs}, 'clubs.json')
    saveDataToJson({'competitions': competitions}, 'competitions.json')
    saveDataToJson({'reservations': reservations}, 'reservations.json')


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
reservations = loadReservations()


@app.route('/')
def index(error=None):
    return render_template('index.html', error=error, clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    current_date = datetime.now()
    print(session)
    club = [club for club in clubs if club['email'] == request.form['email']]
    print(request.form['email'])
    print(club)
    if not club:
        return index(error='No club found with that email address')

    for competition in competitions:
        competition_date = datetime.strptime(
            competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date > current_date:
            competition['canBook'] = True
        else:
            competition['canBook'] = False

    session['email'] = request.form['email']
    return render_template('welcome.html', club=club[0], competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if 'email' not in session:
        return redirect(url_for('index'))
    foundClub = [c for c in clubs if c['name'] == club][0]

    # check de sécurité pour éviter de réserver pour un autre club
    if session['email'] != foundClub['email']:
        flash("You can't make a reservation for another club")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    current_date = datetime.now()
    competition_date = datetime.strptime(
        foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date < current_date:
        flash('This competition has already taken place')
        abort(403)
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    maxPlaces = min(int(
        foundClub['points']), (12 - getClubNbReservations(foundClub, foundCompetition)))
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition, maxPlaces=maxPlaces)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    print(session)
    if 'email' not in session:
        return redirect(url_for('index'))
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    clubBookedPlaces = getClubNbReservations(club, competition)

    # max 12 places
    if clubBookedPlaces + placesRequired > 12:
        if clubBookedPlaces == 0:
            flash('You can only book a maximum of 12 places for a competition')
        else:
            flash('You can only book a maximum of 12 places for a competition and you have already booked ' +
                  str(clubBookedPlaces) + ' places')

    # Check if the club has enough points
    elif int(club['points']) >= placesRequired:
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces']) - placesRequired
        # Deduct the points from the club's total
        club['points'] = str(int(club['points']) - placesRequired)
        # Update the reservations
        addReservation(club, competition, placesRequired)
        # Save the updated data to the JSON file
        saveAllData()
        flash('Great-booking complete!')
    else:
        flash('Not enough points to complete this booking.')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def addReservation(club, competition, places):
    # Créer une nouvelle réservation
    new_reservation = {
        'club': club['name'], 'competition': competition['name'], 'places': places}

    # Vérifier si une réservation similaire existe déjà
    for reservation in reservations:
        if reservation['club'] == club['name'] and reservation['competition'] == competition['name']:
            # Si oui, ajouter les places à la réservation existante
            reservation['places'] = int(reservation['places']) + places
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
