# Syncify
#### Description:

[Syncify](https://kaezr.pythonanywhere.com/) is a web app that enables you to effortlessly convert your Spotify playlists into YouTube playlists with just a few clicks!

To get started, connect your Spotify and YouTube accounts to the app through the `Authorize` page, located in the top right corner of the Home Page.

Once you've linked your Spotify and YouTube accounts, you'll gain access to the rest of the website.

On the `Spotify playlists` page, you can browse through your Spotify playlists and enjoy the following features:

- View a playlist, which displays a table containing details for each song in the playlist, including a link to the song on Spotify and the total playlist duration.
- Delete a playlist from your Spotify account.
- Convert your playlist to YouTube. This feature generates a table of YouTube videos based on your Spotify playlist, with a link to each video. You can review the suggested videos, exclude any that are incorrect, and finalize the playlist.

The `YouTube playlists` page offers identical features to the `Spotify playlists` page, except for playlist conversion.

#### APIs used:

- YouTube Data API v3 -> [Documentation](https://developers.google.com/youtube/v3/getting-started?hl=en)
- Spotify Web API -> [Documentation](https://developer.spotify.com/documentation/web-api)

#### Libraries used:

The following libraries were utilized in the development of Syncify:

- `flask` - Web app framework.
- `flask-session` - Storage of session cookies.
- `spotipy` - Interaction with the Spotify Web API using Python.
- `python-dotenv` - Secure storage of API credentials in a `.env` file.
- `google-api-python-client` - Interaction with the YouTube Data API v3 using Python.
- `google-auth` and `google-auth-oauthlib` - OAuth2 usage for connecting user's YouTube account to Syncify.
- `isodate` - Parsing of YouTube API's `ISO 8601` durations to seconds for proper display of video durations in playlists.

All the required libraries to run the application are listed in the `requirements.txt` file.

#### Tech stack used:

Syncify was built using the following technologies:

- Python
- Flask
- HTML and CSS
- Jinja
- Bootstrap Framework for HTML pages

#### Running the app on your own:

To run the application on your own, follow these steps (assuming you are using a `bash` terminal in your codespace):

- (Optional but recommended) Create a virtual environment:
    - Create a virtual environment using the command `python -m .venv <virtualenvname>` in the desired directory.
    - Activate the virtual environment using the command `source <virtualenvname>/Scripts/Activate` on Windows. To deactivate the virtual environment, run `deactivate`.
- Clone the repository using `git clone` in a directory of your choice.
- In the same directory, run `pip install -r requirements.txt` to install all the necessary libraries.
- **Obtain your API credentials from YouTube and Spotify**:
    - Refer to the [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api) to obtain your `CLIENT_ID` and `CLIENT_SECRET`. Create a `.env` file in your app directory and add two variables, `SPOTIFY_ID` and `SPOTIFY_SECRET`, containing your respective credentials.
    - Follow the [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3/getting-started?hl=en) to create an OAuth2.0 Client. Download the resulting `.json` file, rename it to `client_secrets.json`, and place it in your app directory.
- Ensure that you add proper Redirect URIs to both Spotify and YouTube APIs; otherwise, a `Redirect_URI_Mismatch` error will occur during user authentication.
- Until your API Client is fully verified by Spotify/Google, OAuth2 authentication to user accounts will only be available to 'testers' added by you in the Developer dashboards.

#### File Explanations:

- /static
    - `icon.ico` - Tab icon.
    - `styles.css` - CSS file used by all HTML files in `/templates`.
- /templates
    - `auth.html` - Authorization page that displays connections to Spotify and YouTube.
    - `convert.html` - Page displaying the proposed playlist before confirming conversion.
    - `index.html` - Homepage of the app.
    - `layout.html` - HTML file containing the navigation bar, used as the base for all other pages.
    - `playlist.html` - Page displaying all YouTube/Spotify playlists associated with the user.
    - `view.html` - Page displaying tabulated data about a playlist of the user's choice.
- `.gitignore` - Git file that excludes unnecessary/sensitive files (such as `.env` and `client_secrets.json`) from being committed to the GitHub repository.
- `app.py` - The main Python file containing all the necessary code to run the web application. It imports functions from `auth_spot.py`, `auth_yt.py`, and `helpers.py`.
- `auth_spot.py` - Python file containing code for performing and validating user authentication with Spotify.
- `auth_yt.py` - Python file containing code for performing and validating user authentication with YouTube.
- `helpers.py` - Python file containing helper functions that aid in the proper display of playlist and track durations in `view.html` and `convert.html`.
- `README.md` - The file you are currently reading ;)
- `requirements.txt` - A text file containing the names of all the libraries necessary to run Syncify.
