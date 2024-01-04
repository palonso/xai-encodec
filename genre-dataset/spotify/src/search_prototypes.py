import argparse
import time
import click
from search_by_query import main as search

parser = argparse.ArgumentParser(description='Search genre prototypes on Spotify API')
parser.add_argument('file_prototypes', type=str, help='Input TSV file with prototypes to search (genre, artist, title)')
parser.add_argument('file_matches', type=str, help='Output TSV file with search results from Spotify API (genre, artist, title, spotify_id, spotify_artist, spotify_title')
args = parser.parse_args()
FILE_PROTOTYPES = args.file_prototypes
FILE_MATCHES = args.file_matches


def select_candidate(candidate_tracks):
    print("\n")
    print(f">>> Select a match for the track {artist} - {track}:")
    choices = []
    for i, candidate_track in enumerate(candidate_tracks):
        print(f'{i}. {" - ".join(candidate_track)}')
        choices.append(f'{i}')
    i_nomatch  = len(candidate_tracks)
    print(f'{i_nomatch}. NO MATCH')
    choices.append(f'{i_nomatch}')
    choice = int(click.prompt("Select:", type=click.Choice(choices), show_default=False))
    if choice == i_nomatch:
        return None
    else:
        return candidate_tracks[choice]


with open(FILE_MATCHES, 'w') as f, open(FILE_PROTOTYPES, 'r') as f_in:
    for line in f_in:
        line = line.strip().split('\t')
        genre, artist, track = line[0], line[1], line[2]
        print(f'Searching a match for {genre} - {artist} - {track}')

        query = f"artist:{artist} track:{track}"
        candidate_tracks = search(query, filter=None, limit=10, offset=0, wildcard=None, market=None)

        match = None
        # First, try to match automatically.
        for candidate_track in candidate_tracks:
            print(candidate_track[0], artist, candidate_track[1], track)
            if candidate_track[0].lower() == artist.lower() and candidate_track[1].lower() == track.lower():
                print("Found exact match")
                match = candidate_track

        # If a match was not found, ask user to select the match manually.
        if match is None:
            if len(candidate_tracks):
                match = select_candidate(candidate_tracks)

        if match is None:
            f.write(f'{genre}\t{artist}\t{track}\tNO MATCH\n')
        else:
            f.write(f'{genre}\t{artist}\t{track}\t{match[2]}\t{match[0]}\t{match[1]}\n')
        time.sleep(3)
