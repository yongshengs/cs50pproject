# Spotify Dashboard Web App for CS50P Final Project

#### Video Demo: https://youtu.be/3tIXlwv38L0

## Description
This web app utilizes Spotify Web APIs to retrieve data from your Spotify account. It is built using Flask as the backend framework and provides a user-friendly interface to access your playlists, followed artists, and top tracks.

## Prerequisites
Before getting started, make sure you have the following:
- Spotify Developer Account (can sign up using your personal Spotify account)
- Created an app using your Spotify Developer Account in order to have the client credentials
- Client ID and Client Secret obtained from your Spotify Developer Account's app
- Python 3.x installed on your system/virtual environment
- Check that you have the pip-installable libraries installed as provided in requirements.txt

## Features
Authorisation (utilising Spotify's Authorisation Code Flow)
- User login via Spotify account
- Request necessary permissions to access user data

My Playlists
- Display a list of user's saved playlists
- Show playlist name, creator, and a link to the playlist on Spotify

My Followed Artists
- Display a list of artists followed by the user
- Show artist name, follower count, popularity index, and a link to the artist's Spotify page

My Top Tracks
- Display the user's most listened-to tracks in the past 6 months
- Show track name, artist name, album name, and a link to the track on Spotify

## File Structure
- project.py: Backend logic and Flask routes.
- test_project.py: Unit tests for functions in project.py.
- requirements.txt: List of required Python packages.
- static/: Contains static files.
  - script.js: JavaScript for login and refresh functionality.
  - styles.css: CSS for web page styling.
- templates/: Contains HTML templates.
  - home.html: Home page with links to playlists, followed artists, and top tracks.
  - layout.html: Base HTML template for other pages.
  - login.html: Placeholder page with JavaScript logic for authentication.
  - playlists.html: Page displaying user's playlists.
  - followed-artists.html: Page displaying followed artists.
  - top-tracks.html: Page displaying top tracks.

## Usage
1. Create a Spotify Developer App and obtain your Client ID and Client Secret
2. Configure your environment variables for SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET with the obtained credentials.
3. Run the Flask application with this command in the terminal: python project.py (or python3 project.py)
4. Access the web app in your browser at http://localhost:5000.

## Design Choices
- Frontend: The application uses HTML, CSS, and JavaScript for the user interface.
- Backend: Flask is used to handle HTTP requests and responses.

## Additional Notes
- This project was developed as a part of my submission for the CS50P 2023 Final Project assignment.

## Acknowledgments and Thanks
- Thank you to the CS50 team at Harvard University for conducting such a informative course on Python. It was my pleasure and honour to have gone through and completed it.
