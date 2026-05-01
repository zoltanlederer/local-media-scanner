# Local Media Scanner

Scans a local media folder, extracts movie and TV show titles from folder names, looks up each one via the TMDB API, and exports the results to CSV.

## Requirements

- Python 3.x
- requests

## Installation

Clone the repo:
```bash
git clone https://github.com/zoltanlederer/local-media-scanner.git
cd local-media-scanner
```

Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Rename `config.example.py` to `config.py`.
Then edit `config.py` and add your TMDB API key. You can get one for free at [themoviedb.org](https://www.themoviedb.org/settings/api).

## Usage & Options

Usage:
```bash
python3 main.py
```

Options:
```bash
  -h, --help                    show this help message and exit
  -f, --folder                  select a folder for the scan
  -m, --media-type {movie,tv}   select the type of media: "movie" or "tv" for tv show.
```

## Examples

```bash
python3 main.py --media-type 'movie'  --folder '/media-folder/movies'

Scanning folders, please wait...
Found 9 folders to process.
Scanning 1/9: 04 Fast Five (2011) EXTENDED (1080p BluRay x265 HEVC 10bit AAC 7.1 Joy)
Scanning 2/9: Back to the Future
Scanning 3/9: Forrest.Gump.1994.REMASTERED.1080p.BluRay.x265-RARBG
Scanning 4/9: 01 Die.Hard.1988.1080p.BluRay.x265-RARBG
Scanning 5/9: Batman Begins (2005) (1080p BluRay x265 HEVC 10bit AAC 5.1 Joy)
Scanning 6/9: Almost Famous
Scanning 7/9: Spider-Man.3.1080p.2007.BluRay.x265-RARBG
Scanning 8/9: Fake Movie Title
Scanning 9/9: 2001 Harry.Potter.and.the.Sorcerers.Stone.2001.1080p.AMZN.WEB-DL.H.264
--------------------------------------------------
Scan complete.
  Matched:   8
  Unmatched: 1
  Total:     9
--------------------------------------------------
Do you want to save the results? 
It will be saved as "matched.csv" and "unmatched.csv". 
To confirm press "Enter", to quit "q": 
💾 The results were saved.
```

#### matched.csv sample:
| title | release_date | genres | tmdb_id | type |
|-------|-------------|--------|---------|------|
| Fast Five | 2011-04-20 | Action, Thriller, Crime | 51497 | movie |
| Back to the Future | 1985-07-03 | Adventure, Comedy, Science Fiction | 105 | movie |
| Forrest Gump | 1994-06-23 | Comedy, Drama, Romance | 13 | movie |
| Die Hard | 1988-07-15 | Action, Thriller | 562 | movie |
| Batman Begins | 2005-06-10 | Drama, Crime, Action | 272 | movie |
| Almost Famous | 2000-09-15 | Drama, Music | 786 | movie |
| Spider-Man 3 | 2007-05-01 | Action, Adventure, Science Fiction | 559 | movie |
| Harry Potter and the Philosopher's Stone | 2001-11-16 | Adventure, Fantasy | 671 | movie |

#### unmatched.csv sample:
| title | year | source_folder |
|-------|------|---------------|
| Fake Movie Title | | Fake Movie Title |

## Credits
[The Movie Database (TMDB) API](https://www.themoviedb.org)