# README

## Installation

Use the `requeriments.txt` file to install all packages:

```bash
pip install -r requirements.txt
```

## Usage

To use the different scripts first you need a `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`. Go with the following steps:

* Browse to https://developer.spotify.com/dashboard/applications
* Log in with your Spotify account.
* Click on `Create an app`.
* Pick an `App name` and `App description` of your choice and mark the checkboxes.
* After creation, you see your `Client Id` and you can click on `Show client secret` to unhide your ’Client secret’.
* Use your `Client id` and `Client secret` to retrieve a token from the Spotify API.

Once you get your credential to immortalize your app credentials in your source code, you can set environment variables like so:
```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

More details:
1. [Spotipy](https://spotipy.readthedocs.io) is a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform. Easy to download music previews.
2. [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
3. [Audio features](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features)
4. [Audio anaylsis](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis)
5. [Search for item](https://developer.spotify.com/documentation/web-api/reference/#/operations/search)

## Scripts

We implemented various scripts to gather Spotify metadata and previews based in Spotify ids.

1. `search_by_query.py`: searches queries with different input parameters (market, offset, genre, wildcard, and query).
* ```python
  python search_by_query.py -q pop -f genre -m US -w z
  ```
* ```python
  python search_by_query.py -q Rosalia -f artist -m ES -w z
  ```
2. `fetch_tracks.py`: This script fetches track preview and metadata analysis for a spotify id.
* ```python
  python fetch_tracks.py -t 2QrS0PaeXeeGCCLABYoQgE
  ```
* ```python
  python fetch_tracks.py -i spotify_ids.yaml
  ```
3. `generate_ids.py`: It is a random spotify id generator.
* ```python
  python generate_ids.py -n 10 -y 1930
  ```
4. `genre_ids.py`: It is a random spotify id generator based in a list of genres. It was used to generate **MusAV** dataset.
* ```python
  python genre_ids.py -n 15
  ```
5. `preview_in_markets.py`: This script checks the preview availability of an spotify id at all markets.

* ```python
  python preview_in_markets.py -i 4QhjtnNa45XS4JZOXMPbdw
  ```

Wildcard: a character used to get a list of song ids which include it in the song title or artist name.


# Building the genre dataset
- Set your SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI environment variables.
- Create a text file with a list of genres (one line per genre string) (see `test_genre_list` as an example)
- `cd src`
- Run search queries to search for tracks by each genre `./query_genre_spotifyids.sh ../test_genre_list | grep "preview: True"`.