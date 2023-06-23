# Personal media organizer/player

Personal media organizer, meant to organise
a media library and generate playlists.

It has been developped to stay a local application.
The rational is that, today, even if we do have music or video stored
on a computer, a web interface is more appealing.
My goal was just to make a web interface to play the music I have on
my computer.

## Installation

```sh
poetry install           # Install back dependencies
poetry run yoyo apply    # Apply migrations
cd front/
npm install              # Install front dependencies
npm run dev              # 
```

## Cli

To launch the CLI, just run:

```
./run.sh
```

### Current CLI options

```
usage: cli_main.py [-h] [--webm] [--no-webm] [-hd] [-sd] [--limit [LIMIT]] [-s [SHIFT]]
                   [-l] [--last-by-id] [--shuffle] [--no-play] [--display-playlist]
                   [--best] [-g] [--clean-database]
                   [term]

vplaylist 2nd version

positional arguments:
  term                  term to search

options:
  -h, --help            show this help message and exit
  --webm, --only-webm   only webms
  --no-webm             no webms
  -hd, --hd, --only-hd  only hd vids
  -sd, --sd, --only-sd  only sd vids
  --limit [LIMIT]       limit number of vids (by default 150
  -s [SHIFT], --shift [SHIFT]
                        shift things
  -l, --last            give lasts vids
  --last-by-id          give lasts vids by id
  --shuffle             force to shuffle vids
  --no-play             don't play
  --display-playlist    Display the full playlist
  --best                best based on config
  -g, --generate        generate DB
  --clean-database      clean database

```

## Web interface

```
./run_web.sh
```

The browse to `localhost:3000`
