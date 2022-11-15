
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Show, Artist


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db=db)
moment = Moment(app)


#----------------------------------------------------------------------------#
# Models. 
#----------------------------------------------------------------------------#





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


# -----------------------------------------------------------------------------
# CREATE
# -----------------------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  """
	The function allows user to submit a new venue, thus adding it to the database
  """

#   creating an instance of the VenueForm
  form = VenueForm(request.form)
  error=False
  if error == True:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed')
  else:
    flash('Venue ' + form.name.data + ' was successfully listed!')

  details = [form.name.data, form.city.data, form.state.data, form.address.data, form.genres.data, form.phone.data, form.image_link.data, form.facebook_link.data, form.website_link.data, form.seeking_description.data, form.seeking_talent.data]

  try:
    
    create_venue = Venue(
		name=details[0],
		city=details[1],
		state=details[2],
		address=details[3],
		genres=details[4],
		phone=details[5],
		image_link=details[6],
		facebook_link=details[7],
		website=details[8],
		seeking_description=details[9],
		seeking_talent=details[10]
	)

    db.session.add(create_venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  
  
  return render_template('pages/home.html')

# @app.route('/account/login', methods=['GET'])
# def create_account():
#   form = LoginForm()
#   return render_template('forms/login.html', form=form)

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# @app.route('/account/login', methods=['POST'])
# def create_account_submission():
#   form = LoginForm(request.form)
#   error = False
#   # if error == True:
#   #   flash(f'Wrong Details')
#   # else:
#   #   flash(f'Logged In Success')
#   try:
#     email = form.email.data
#     password = form.password.data
    
  #   userQuery = Login.query.get(email)
  #   if email in userQuery:
  #     flash(f'Account already exist')
  #     return render_template('pages/home.html')
  #   else:
  #     create_user = Login(email=email, password=password)
  #     db.session.add(create_user)
  #     db.session.commit()
  #     return render_template('pages/home.html')
  # except:
  #   error = True
  #   db.session.rollback()
  #   print(sys.exc_info())
  # finally:
  #   db.session.close()
  # return render_template('pages/home.html')

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  """
  The controller allows user to create a new artist and commit it to the database
  """
  form = ArtistForm(request.form)
  error = False
  if error == True:
    flash(f"An error occurred. Artist {form.name.data} could not be listed")
  else:
    flash(f'Artist {form.name.data} has been listed successfully')
  
  try:
    
    artistDetails = [form.name.data, form.city.data, form.state.data, form.phone.data, form.image_link.data, form.genres.data, form.facebook_link.data, form.website_link.data, form.seeking_venue.data, form.seeking_description.data]

    create_artist = Artist(name=artistDetails[0], city=artistDetails[1], state=artistDetails[2], phone=artistDetails[3], image_link=artistDetails[4], genres=artistDetails[5],  facebook_link=artistDetails[6], website=artistDetails[7], seeking_venue=artistDetails[8], seeking_description=artistDetails[9])

    db.session.add(create_artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return render_template('pages/home.html')



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  # The controller enable users to create or add a show to the database
  error = False
  form = ShowForm(request.form)
  showDetail = []

  if error == True:
    flash('An error occurred. Show could not be listed')
  else:
    flash('Show was successfully listed')
  
  try:
    showDetail.append(form.artist_id.data)
    showDetail.append(form.venue_id.data)
    showDetail.append(form.start_time.data)
    addShow = Show(
		artist_id=showDetail[0],
		venue_id=showDetail[1], 
		start_time=showDetail[2]
	)
    db.session.add(addShow)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


# --------------------------------------------------------------
# UPDATE
# --------------------------------------------------------------

# ============================== ARTIST ========================

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  # The controller query the details of an artist with id = artist_id from the database to enable the user to make changes

  form = ArtistForm()
  artistQuery = Artist.query.get(artist_id)
  
  
  if artistQuery:
    editDetail = [artistQuery.name, artistQuery.genres, artistQuery.phone, artistQuery.city, artistQuery.state, artistQuery.facebook_link, artistQuery.image_link, artistQuery.seeking_description, artistQuery.seeking_venue, artistQuery.website]

    form.name.data = editDetail[0]
    form.genres.data = editDetail[1]
    form.phone.data = editDetail[2]
    form.city.data = editDetail[3]
    form.state.data = editDetail[4]
    form.facebook_link.data = editDetail[5]
    form.image_link.data = editDetail[6]
    form.seeking_description.data = editDetail[7]
    form.seeking_venue.data = editDetail[8]
    form.website_link.data = editDetail[9]
  else:
    flash('Artist not found')
  
  return render_template('forms/edit_artist.html', form=form, artist=artistQuery)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  # The controller enables users to submit updated details of an artist with id = artist_id into the database

  form = ArtistForm(request.form)
  editDetail = [form.name.data, form.genres.data, form.phone.data, form.city.data, form.state.data, form.facebook_link.data, form.image_link.data, form.seeking_description.data, form.seeking_venue.data, form.website_link.data]

  error = False

  if error == True:
    flash('An error occured. Details could not be changed')
  else:
    flash('Artist details updated successfully')

  try:
    artistDetail = Artist.query.get(artist_id)

    artistDetail.name = editDetail[0]
    artistDetail.genres = editDetail[1]
    artistDetail.city = editDetail[3]
    artistDetail.state = editDetail[4]
    artistDetail.phone = editDetail[2]
    artistDetail.image_link = editDetail[6]
    artistDetail.facebook_link = editDetail[5]
    artistDetail.seeking_venue = editDetail[8]
    artistDetail.seeking_description = editDetail[7]
    artistDetail.website = editDetail[9]
    
    
    db.session.add(artistDetail)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))


# ====================== VENUE ===============================

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  # The controller query the details of a venue with id = venue_id from the database to enable the user to make changes

  venueQuery = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  

  if venueQuery:
    venueEdit = [venueQuery.name, venueQuery.city, venueQuery.state, venueQuery.address,  venueQuery.phone, venueQuery.image_link, venueQuery.facebook_link, venueQuery.genres, venueQuery.website, venueQuery.seeking_talent, venueQuery.seeking_description]

    form.name.data = venueEdit[0]
    form.city.data = venueEdit[1]
    form.state.data = venueEdit[2]
    form.address.data = venueEdit[3]
    form.phone.data = venueEdit[4]
    form.image_link.data = venueEdit[5]
    form.facebook_link.data = venueEdit[6]
    form.genres.data = venueEdit[7]
    form.website_link.data = venueEdit[8]
    form.seeking_talent.data = venueEdit[9]
    form.seeking_description.data = venueEdit[10]
  else:
    return render_template('errors/404.html')
  
  return render_template('forms/edit_venue.html', form=form, venue=venueQuery)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def venue_submission(venue_id):

  # The controller enables users to submit updated details of a venue with id = venue_id into the database
  
  form = VenueForm(request.form)
  venueEdit = [form.name.data, form.city.data, form.state.data, form.genres.data, form.phone.data, form.address.data, form.website_link.data, form.facebook_link.data, form.image_link.data, form.seeking_talent.data, form.seeking_description.data]

  error = False
  if error == True:
    flash('An error occurred. Venue details could not be changed')
  else:
    flash('Venue details successfully updated')
#   form = VenueForm(request.form)
  
  try:
    venueQuery = Venue.query.get(venue_id)

    venueQuery.name = venueEdit[0]
    venueQuery.city=venueEdit[1]
    venueQuery.state=venueEdit[2]
    venueQuery.address=venueEdit[5]
    venueQuery.phone=venueEdit[4]
    venueQuery.image_link=venueEdit[8]
    venueQuery.facebook_link=venueEdit[7]
    venueQuery.genres=venueEdit[3] 
    venueQuery.website=venueEdit[6]
    venueQuery.seeking_talent=venueEdit[9]
    venueQuery.seeking_description=venueEdit[10]
    
    db.session.add(venueQuery)
    db.session.commit()
    
  except Exception:
    db.session.rollback()
    print(sys.exc_info())
    flash("Venue was not edited successfully.")
  finally:
    db.session.close()
  

  return redirect(url_for('show_venue', venue_id=venue_id))

# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

# initializing a general variable to be used inthe subsequent controllers
saveTime = datetime.now()


@app.route('/venues/search', methods=['POST'])
def search_venues():

  # Enables the user to search for a specific venue, even with part of venue name

  searchResults = Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term') + '%')).all()
  data_result = []
  index = 0

  # looping through the query results for the searching term
  for venue in searchResults:
    data_result.insert(index, 
		{
			"id": venue.id,
			"name": venue.name,
			"num_upcoming_shows": len(Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>=saveTime).all())
		}
    )
    index += 1
  return render_template('pages/search_venues.html', results={
	"count": len(searchResults), "data": data_result
  }, search_term=request.form.get('search_term', ''))




@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  # Enables the user to search for a specific artist, even with part of artist name

  searchResults = Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term') + '%')).all()
  data_results = []
  index = 0
  
  for artists in searchResults:
    data_results.insert(index, 
		{
			"id": artists.id,
			"name": artists.name,
			"num_upcoming_shows": len(Show.query.filter(Show.artist_id==artists.id).filter(Show.start_time>=saveTime).all())
		}
    )
    index += 1
  
  return render_template('pages/search_artists.html', results={"count": len(searchResults), "data": data_results}, search_term=request.form.get('search_term', ''))


# ----------------------------------------------------------------
# READ
# ----------------------------------------------------------------


@app.route('/venues')
def venues():

  # Query all the venues in the database and display it for the user to interact with

  # initialing general variables
  index = 0
  filteredResult = []

  # query command
  venueQuery = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  # looping through the queried data of all the venues in the database
  for venue in venueQuery:

    # filtering the query data to organise them by state and city
    venueDetails = Venue.query.filter_by(state=venue.state, city=venue.city).all()
    venue_result = []
    for Avenue in venueDetails:
      venue_result.insert(index, 
        {
        "id": Avenue.id,
        "name": Avenue.name,
        "num_upcoming_shows": len(Show.query.filter(Show.venue_id==1).filter(Show.start_time>=saveTime).all())
      })
      
    filteredResult.insert(index,
      {
      "city": venue.city,
      "venues": venue_result,
      "state": venue.state
    }
    )
    index += 1

  return render_template('pages/venues.html', areas=filteredResult)

@app.route('/artists')
def artists():

  # Query all the artists in the database and display it for the user to interact with

  artistQuery = Artist.query.all()
  
  return render_template('pages/artists.html', artists=artistQuery)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
 
  """
    The controller enables users to view the details of a particular artist in the database
  """
  venueQuery = Venue.query.get(venue_id)
  data = {}
  error = False
  if error == True:
    flash('An error occurred. Page cannot be found!')
  else:
    flash(f'Details of {venueQuery.name}')
  
  try:
    if venueQuery:

      show_upcoming = Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time >= saveTime).all()

      for show in show_upcoming:
        id = show.artist_id
        artistName = show.artist.name
        artistImage = show.artist.image_link
        timeToShow = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        showUpcomingData = [{
          "artist_id": id,
          "artist_image_link": artistImage,
          "artist_name": artistName,
          "start_time": timeToShow
      }]


      show_past_query = Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < saveTime).all()
    

      for show in show_past_query:
        id = show.artist_id
        artistName = show.artist.name
        artistImage = show.artist.image_link
        timeToShow = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        pastShowsDetail = [{
          "artist_id": id,
          "artist_image_link": artistImage,
          "artist_name": artistName,
          "start_time": timeToShow
        }]
      data["id"] = venueQuery.id
      data["name"] = venueQuery.name
      data["genres"] = venueQuery.genres
      data["address"] = venueQuery.address
      data["city"] = venueQuery.city
      data["state"] = venueQuery.state
      data["phone"] = venueQuery.phone
      data["image_link"] = venueQuery.image_link
      data["facebook_link"] = venueQuery.facebook_link
      data["website"] = venueQuery.website
      data["seeking_talent"] = venueQuery.seeking_talent
      data["seeking_description"] = venueQuery.seeking_description
      data["past_shows"] = pastShowsDetail
      data["past_shows_count"] = len(pastShowsDetail)
      data["upcoming_shows"] = showUpcomingData
      data["upcoming_shows_count"] = len(showUpcomingData)
    else:
      return render_template('errors/404.html')
  except:
    error = True
    
  
  
  
  return render_template('pages/show_venue.html', venue=data)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  """
    The controller enables users to view the details of a particular artist in the database
  """
  
  artistQuery = Artist.query.get(artist_id)
  error = False
  data = {}
  if error == True:
    flash('An error occurred. Page cannot be found!')
    
  else:
    flash(f'Details of {artistQuery.name}')

  try:
    if artistQuery: 
      
  # querying the data from the database to populate it on the frontend/view
      artistPastShows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<saveTime).all()
      
  

      for show in artistPastShows:
        id = show.venue_id
        venueName = show.venue.name
        venueImage = show.venue.image_link
        timeToShow = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        pastShowsData = [{
          "venue_id": id,
          "venue_image_link": venueImage,
          "venue_name": venueName,
          "start_time": timeToShow
        }]

      artistUpcomingShows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>=saveTime).all()

      for show in artistUpcomingShows:
        id = show.venue_id
        venueName = show.venue.name
        venueImage = show.venue.image_link
        timeToShow = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        upcomingShowsData = [{
          "venue_id": id,
          "venue_image_link": venueImage,
          "venue_name": venueName,
          "start_time": timeToShow
        }]
      data["id"] = artistQuery.id
      data['name'] = artistQuery.name
      data['image_link'] = artistQuery.image_link
      data['phone'] = artistQuery.phone
      data["seeking_venue"] = artistQuery.seeking_venue
      data['state'] = artistQuery.state
      data['city'] = artistQuery.city
      data['website'] = artistQuery.website
      data['facebook_link'] = artistQuery.facebook_link
      data['genres'] = artistQuery.genres
      data['seeking_description'] = artistQuery.seeking_description
      data['past_shows'] = pastShowsData
      data['past_shows_count'] = len(pastShowsData)
      data['upcoming_shows'] = upcomingShowsData
      data['upcoming_shows_count'] = len(upcomingShowsData)
      
      
    else:
      return render_template('errors/404.html')
  except:
    error = True
  
  return render_template('pages/show_artist.html', artist=data)
    
  
  

@app.route('/shows')
def shows():
  
  show_query = Show.query.join(Artist).join(Venue).all()
  show_data = []
  index = 0

  for show in show_query:
    venueID = show.venue_id
    venueName = show.venue.name
    artistID = show.artist_id
    artistName = show.artist.name
    artistImage = show.artist.image_link

    showDetails = [venueID, venueName, artistID, artistName, artistImage]
    show_data.insert(index, {
      "venue_id": showDetails[0],
      "artist_id": showDetails[2],
      "venue_name": showDetails[1],
      "artist_name": showDetails[3],
      "artist_image_link": showDetails[4],
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
    index += 1
  return render_template('pages/shows.html', shows=show_data)

# -----------------------------------------------------------------
# DELETE
# -----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  error = False
  if error == True:
    flash('An error occurred. Venue could not be deleted')
  else:
    flash(f'Venue {venue_id} successfulled deleted')
  try:
    deleteItem = Venue.query.get(venue_id)
    db.session.delete(deleteItem)
    db.session.commit()
  except:
    error = True
    db.session.rollabck()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return render_template(url_for('index'))


# --------------------------------------------------------------
# ERROR
# --------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# ----------------------------------------------------------------
# LAUNCH
# ----------------------------------------------------------------

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)


# https://fullstackdevelopment.us.auth0.com/authorize?audience=login&response_type=token&client_id=502VNO6RYrsnl4LNu8GW5KfKI2NqE7Zj&redirect_uri=http://127.0.0.1:5000/artists