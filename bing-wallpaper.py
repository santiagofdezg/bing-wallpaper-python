#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from urllib.request import urlopen, urlretrieve
import json
import re

BING_BASE_URL = "https://bing.com"
BING_IMAGE_DAY_URL = "https://bing.com/HPImageArchive.aspx?format=js&n="


def parse_picture_url(batch):
    """Get the relative urls of the pictures from the API."""
    if not batch:
        # Obtain only the latest picture
        bing_url = BING_IMAGE_DAY_URL + "1"
    else:
        bing_url = BING_IMAGE_DAY_URL + str(batch)

    response = urlopen(bing_url).read().decode("utf8")
    urls = [picture["url"] for picture in json.loads(response)["images"]]
    return urls


def get_filename(url, filename, batch, index):
    """If filename is not provided, return the original picture name. Otherwise,
    it returns the parameter filename and adds an index if the script is running
    on batch mode."""
    if filename:
        new_filename = filename
        if batch:
            new_filename = new_filename.replace(".jpg", f"_{str(index)}.jpg")
    else:
        # The "id" field of the URL always starts with "OHR."
        new_filename = url[url.find("OHR.") + 4 : url.find("&")]
    return new_filename


if __name__ == "__main__":

    # Define the parser
    parser = argparse.ArgumentParser(
        prog="python3 bing-wallpaper.py",
        description="Download the latest picture of the day from Bing.com and "
        "saves it to a directory.",
        epilog="Copyright (C) 2022 Santiago Fernández González",
    )
    parser.add_argument(
        "-b",
        "--batch",
        help="Download the latest <N> pictures.",
        metavar="N",
        type=int,
        dest="batch",
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Force download of picture. This will overwrite the picture if the "
        "filename already exists. [default: False].",
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
        "if it does not exist. [default: working directory].",
        type=str,
        default=os.getcwd(),
        dest="picturedir",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Do not display log messages. [default: False].",
        action="store_true",
        default=False,
        dest="quiet",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        help="The resolution of the image to retrieve. Default and recommended "
             "is 1920x1080 (usually doesn't contain watermarks).",
        type=str,
        default="1920x1080",
        choices=["1920x1200", "1920x1080", "800x480", "400x240"],
        dest="resolution",
    )

    # Parse
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("[PARSE ERROR] Check the command and parameters.")
        sys.exit(1)

    # If a filename is provided verify that it is correct or fix it
    if args.filename and not args.filename.endswith(".jpg"):
        args.filename = args.filename + ".jpg"

    # Create the picture directory if it doesn't already exist
    Path(args.picturedir).mkdir(parents=True, exist_ok=True)

    # Obtain the URLs to download the pictures
    relative_urls = parse_picture_url(args.batch)

    for i, url in enumerate(relative_urls):
        # Build the absolute URL and set the desired resolution
        absolute_url = BING_BASE_URL + re.sub(r"[0-9]*x[0-9]*", args.resolution, url)

        # Get the file name for the picture
        filename = get_filename(absolute_url, args.filename, args.batch, i)
        local_file_path = os.path.join(args.picturedir, filename)

        # Check if the file already exists
        if args.force or not Path(local_file_path).is_file():
            if not args.quiet:
                print(f"Downloading: {filename}")
            urlretrieve(absolute_url, local_file_path)
        else:
            if not args.quiet:
                print(f"Skipping: {filename}")
