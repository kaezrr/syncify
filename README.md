# Syncify
#### Description:
[Syncify](https://kaezr.pythonanywhere.com/) is a web app that you can use to convert your Spotify playlists to YouTube playlists with the just a couple of clicks!
<br>
First connect your Spotify and YouTube account to app through the `Authorize` page, available on the top right corner of the Home Page.

<br>
After connecting your accounts to both Spotify and YouTube, you will have access to the rest of the website.

<br>
Through the `Spotify playlists` page you can browse through your playlists on Spotify and have access to features such as :

+ View a playlist, which will provide a table on the details of every song in that playlist, and a link to that song on Spotify and the total duration of that playlist.
+ Delete a playlist from your Spotify account.
+ And last but not least, convert your playlist to YouTube, which will provide a table of YouTube videos that the apps algorithm has picked based on your Spotify playlist, with a link to each of them. Then you can choose to exclude any videos you think are incorrect and finalize the playlist.

`YouTube playlists` page contains identical features to the `Spotify playlists` except conversion of playlists.

#### APIs used:
+ YouTube Data API v3 -> [Documentation](https://developers.google.com/youtube/v3/getting-started?hl=en)
+ Spotify Web API -> [Documentation](https://developer.spotify.com/documentation/web-api)

#### Libraries used:
+ `flask` for the web app framework.
+ `flask-session` to store session cookies.
+ `spotipy` to interact with the Spotify Web API via Python.
+ `python-dotenv` to store API credentials in a `.env` file for security purposes.
+ `google-api-python-client` to interact with the YouTube Data API v3 via Python.
+ `google-auth` and `google-auth-oauthlib` to use OAuth2 to connect user's YouTube account to Syncify
+ `isodate` to parse YouTube API's `ISO 8601` durations to seconds to display video durations properly while viewing playlists. 

All the libraries required to run the application are listed in the `requirements.txt` file.

#### Tech stack used:
+ Python
+ Flask
+ HTML and CSS
+ Jinja
+ Bootstrap Framework for HTML pages

#### Running the app on your own:
>The follow steps assume you are using a `bash` terminal in your codespace.

Incase you want to run the application on your own you can do so by doing the following steps:
+ (Optional but recommended) Create a virtual environment.
    - Create one using the command `python -m .venv <virtualenvname>` in the directory where you want to store your virtual environment.
    - Then activate it using the command `source <virtualenvname>/Scripts/Activate` on Windows. You can deactivate the virtual environment by running `deactivate`.
+ `git clone` the repository in a directory of your choice.
+ In the same directory run `pip install -r requirements.txt` to install all the required libraries at once. 
+ **Get your API credentials from YouTube and Spotify**
    - Follow [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api) till you get your `CLIENT_ID` and `CLIENT_SECRET`. In your app directory create a `.env` file and create two variables `SPOTIFY_ID` and `SPOTIFY_SECRET` and store your `CLIENT_ID` and `CLIENT_SECRET` in them respectively.
    - Follow [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3/getting-started?hl=en) till you can create an OAuth2.0 Client. Then you will have the option to download a `.json` file, download it and rename it to `client_secrets.json` and store it in your app directory.
+ Remember to add proper Redirect_URIs to both Spotify and YouTube API, or it will return a `Redirect_URI_Mismatch` error upon user authentication.
+ Until your API Client gets properly verified by Spotify/Google. OAuth2 authentication to user accounts will only be restricted to 'testers' added by you to the Developer dashboards.

#### File Explanations:
+ /static
    - `icon.ico` - Tab icon.
    - `styles.css` - CSS file that runs that all the HTML files in `/templates` use.
+ /templates
    - `auth.html` - Authorization page that displays the connections to Spotify and YouTube.
    - `convert.html` - Page that displays the proposed playlist before confirming conversion.
    - `index.html`  - Homepage of the app.
    - `layout.html` - HTML file that contains the navigation bar and from which all other pages extend from.
    - `playlist.html` - Page that displays all the YouTube/Spotify playlists that the user has.
    - `view.html` - Page that displays tabulated data about a playlist of the user's choice.
+ `.gitignore` - Git file that ignores unneccesary/sensitive files such as `.env` and `client_secrets.json` while committing to the GitHub repository.
+ `app.py` - The main python file that contains all the necessary code to run the web application, needs `auth_spot.py`, `auth_yt.py` and `helpers.py` to import functions necessary to run the app.
+ `auth_spot.py` - Python file that contains all the code that performs and validates user authentication to Spotify.
+ `auth_yt.py` - Python file that contains all the code that performs and validates user authentication to YouTube.
+ `helpers.py` - Python file that contains some helper functions mainly that aid in proper display of playlist and track durations in `view.html` and `convert.html`.
+ `README.md` - The file you are reading right now ;)
+ `requirements.txt` - A text file containing the names of all the libraries necessary to run Syncify.