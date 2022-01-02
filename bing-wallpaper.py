#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from urllib.request import urlopen, urlretrieve
import json
import re

BING_BASE_URL = "http://bing.com"
BING_IMAGE_DAY_URL = "http://bing.com/HPImageArchive.aspx?format=js&n=1"

# Define the parser
parser = argparse.ArgumentParser(
    prog="python3 bing-wallpaper.py",
    description="Download the latest picture of the day from Bing.com and "
                "saves it to a directory.",
    epilog="Copyright (C) 2022 Santiago Fernández González",
)
parser.add_argument(
    "-f",
    "--force",
    help="Force download of picture. This will overwrite the picture if the "
         "filename already exists. [default: False]",
    action="store_true",
    default=False,
    dest="force",
)
parser.add_argument(
    "-n",
    "--filename",
    help="The name of the downloaded picture. Defaults to the upstream name.",
    type=str,
    dest="filename",
)
parser.add_argument(
    "-p",
    "--picturedir",
    help="The full path to the picture download directory. It will be created "
         "if it does not exist. [default: working directory]",
    type=str,
    default=os.getcwd(),
    dest="picturedir",
)
parser.add_argument(
    "-q",
    "--quiet",
    help="Do not display log messages. [default: False]",
    action="store_true",
    default=False,
    dest="quiet",
)
parser.add_argument(
    "-r",
    "--resolution",
    help="The resolution of the image to retrieve. Supported resolutions: "
         "1920x1200, 1920x1080, 800x480, 400x240. Default and recommended is "
         "1920x1080 (usually doesn't contain watermarks).",
    type=str,
    default="1920x1080",
    dest="resolution",
)

# Parse
try:
    args = parser.parse_args()
except argparse.ArgumentError:
    print("[PARSE ERROR] Revise command.")
    sys.exit(1)


# Create the picture directory if it doesn't already exist
Path(args.picturedir).mkdir(parents=True, exist_ok=True)

# Obtain the URL to download the image
response = urlopen(BING_IMAGE_DAY_URL).read().decode("utf8")
image_data = json.loads(response)["images"]
relative_url = image_data[0]["url"]

# Build the absolute URL and set the desired resolution
url = BING_BASE_URL + re.sub(r"[0-9]*x[0-9]*", args.resolution, relative_url)

# Get the file name
if args.filename:
    filename = args.filename
else:
    # The "id" field of the URL always starts with "OHR."
    filename = url[url.find("OHR.") + 4 : url.find("&")]
local_file_path = os.path.join(args.picturedir, filename)

# Check if the file already exists
if args.force or not Path(local_file_path).is_file():
    if not args.quiet:
        print(f"Downloading: {filename}")
    urlretrieve(url, local_file_path)
else:
    if not args.quiet:
        print(f"Skipping: {filename}")
