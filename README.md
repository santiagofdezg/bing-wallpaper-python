# Bing.com wallpaper scrapper

## Information
This is a script to download the latest picture of the day from Bing.com and saves it to a directory. The script also contains a batch option to download the `n` latest pictures. It is inspired by Alejandro Figueroa's bash script [`bing-wallpaper`](https://github.com/thejandroman/bing-wallpaper).

## Use
- Run the script from the terminal to download the image of the day from Bing.com
```commandline
$ python3 bing-wallpaper.py 
```
- To see available parameters, run the script with the `--help` flag
```commandline
$ python3 bing-wallpaper.py --help
usage: python3 bing-wallpaper.py [-h] [-b N] [-f] [-n FILENAME]
                                 [-p PICTUREDIR] [-q]
                                 [-r {1920x1200,1920x1080,800x480,400x240}]

Download the latest picture of the day from Bing.com and saves it to a
directory.

optional arguments:
  -h, --help            show this help message and exit
  -b N, --batch N       Download the latest <N> pictures.
  -f, --force           Force download of picture. This will overwrite the
                        picture if the filename already exists. [default:
                        False].
  -n FILENAME, --filename FILENAME
                        The name of the downloaded picture. Defaults to the
                        upstream name.
  -p PICTUREDIR, --picturedir PICTUREDIR
                        The full path to the picture download directory. It
                        will be created if it does not exist. [default:
                        working directory].
  -q, --quiet           Do not display log messages. [default: False].
  -r {1920x1200,1920x1080,800x480,400x240}, 
    --resolution {1920x1200,1920x1080,800x480,400x240}
                        The resolution of the image to retrieve. Default and
                        recommended is 1920x1080 (usually doesn't contain
                        watermarks).

Copyright (C) 2022 Santiago Fernández González
```