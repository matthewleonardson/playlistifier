# Playlistifer

Playlistifer is a simple python script that will scan a Spotify user's liked songs and transfer them to a formal Spotify playlist. My motivation for this project was to avoid the "smart shuffle" feature that Spotify seems to force you to use when listening to liked songs directly from "Liked Songs." 

# Usage

This script requires you to have a Spotify developer account. More specifically, you need a Spotify Client ID and Client secret. You should be able to set that up [here](https://developer.spotify.com/dashboard). Then, create a `.env` file in the root folder of the repository with the fields `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` cooresponding to those Spotify values. You also need to set a `SPOTIPY_REDIRECT_URI` in the `.env` file, but this can be any localhost link, such as `https://localhost:8888/callback`, regardless of whether you are running a local server. 

With your `.env` setup, run main.py with your Spotify username as the only argument. You will have to do a little weirdness with copy and pasting the redirect URI into the console after authenticating with Spotify, but you should only have to do this once. If the script runs, you should have a new Spotify playlist with all your liked songs!

# Dependencies

This project relies on the `dotenv` and `spotipy` Python packages.