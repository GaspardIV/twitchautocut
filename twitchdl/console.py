# -*- coding: utf-8 -*-

import sys

from argparse import ArgumentParser, ArgumentTypeError
from collections import namedtuple

from twitchdl.exceptions import ConsoleError
from twitchdl.output import print_err
from . import commands, __version__


Command = namedtuple("Command", ["name", "description", "arguments"])

CLIENT_WEBSITE = 'https://github.com/ihabunek/twitch-dl'


def time(value):
    """Parse a time string (hh:mm or hh:mm:ss) to number of seconds."""
    parts = [int(p) for p in value.split(":")]

    if not 2 <= len(parts) <= 3:
        raise ArgumentTypeError()

    hours = parts[0]
    minutes = parts[1]
    seconds = parts[2] if len(parts) > 2 else 0

    if hours < 0 or not (0 <= minutes <= 59) or not (0 <= seconds <= 59):
        raise ArgumentTypeError()

    return hours * 3600 + minutes * 60 + seconds


COMMANDS = [
    Command(
        name="videos",
        description="List videos from a channel",
        arguments=[
            (["channel_name"], {
                "help": "channel name",
                "type": str,
            }),
            (["-l", "--limit"], {
                "help": "Number of videos to fetch (default 10, max 100)",
                "type": int,
                "default": 10,
            }),
            (["-o", "--offset"], {
                "help": "Offset for pagination of results. (default 0)",
                "type": int,
                "default": 0,
            }),
            (["-s", "--sort"], {
                "help": "Sorting order of videos. (default: time)",
                "type": str,
                "choices": ["views", "time"],
                "default": "time",
            }),
        ],
    ),
    Command(
        name="download",
        description="Download a video",
        arguments=[
            (["video"], {
                "help": "video ID, clip slug, or URL",
                "type": str,
            }),
            (["-w", "--max_workers"], {
                "help": "maximal number of threads for downloading vods "
                        "concurrently (default 20)",
                "type": int,
                "default": 20,
            }),
            (["-s", "--start"], {
                "help": "Download video from this time (hh:mm or hh:mm:ss)",
                "type": time,
                "default": None,
            }),
            (["-e", "--end"], {
                "help": "Download video up to this time (hh:mm or hh:mm:ss)",
                "type": time,
                "default": None,
            }),
            (["-f", "--format"], {
                "help": "Video format to convert into, passed to ffmpeg as the "
                        "target file extension (default: mkv)",
                "type": str,
                "default": "mkv",
            }),
            (["-k", "--keep"], {
                "help": "Don't delete downloaded VODs and playlists after merging.",
                "action": "store_true",
                "default": False,
            }),
        ],
    ),
]

COMMON_ARGUMENTS = [
    (["--debug"], {
        "help": "show debug log in console",
        "action": 'store_true',
        "default": False,
    }),
    (["--no-color"], {
        "help": "disable ANSI colors in output",
        "action": 'store_true',
        "default": False,
    })
]


def get_parser():
    description = "A script for downloading videos from Twitch"

    parser = ArgumentParser(prog='twitch-dl', description=description, epilog=CLIENT_WEBSITE)
    parser.add_argument("--version", help="show version number", action='store_true')

    subparsers = parser.add_subparsers(title="commands")

    for command in COMMANDS:
        sub = subparsers.add_parser(command.name, help=command.description)

        # Set the function to call to the function of same name in the "commands" package
        sub.set_defaults(func=commands.__dict__.get(command.name))

        for args, kwargs in command.arguments + COMMON_ARGUMENTS:
            sub.add_argument(*args, **kwargs)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print("twitch-dl v{}".format(__version__))
        return

    if "func" not in args:
        parser.print_help()
        return

    try:
        args.func(**args.__dict__)
    except ConsoleError as e:
        print_err(e)
        sys.exit(1)
