#!/usr/bin/env python

# builtin imports
import os
import sys
import typing
import pathlib
import argparse
import subprocess

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

# module imports
from services.log import _logger
from services import filedata
from config.config import config_obj


def parse_args():
    parser = argparse.ArgumentParser(description="Add an file to the database as an asset item")
    parser.add_argument('filename', action="store", nargs=1, default=None, help="The filepath of the file we're submitting")
    args = parser.parse_args()
    return args


def get_thumbnail_path(filepath: str = '') -> str:
    """
    Take a file path and figure out a thumbnail path

    Args:
        filepath: the path of the file you want the thumbnail path for

    Returns:
        thumbnail_filepath
    """
    directory = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    filename = os.path.splitext(basename)[0]
    thumbnail_filepath = f'{directory}/{filename}.thumb{config_obj.thumbnail_extension}'
    return thumbnail_filepath


def make_thumbnail(src: str = '') -> typing.Union[None, str]:
    """
    Determine the file type and make an appropriate thumbnail for it

    Args:
        src: the file path you want to make a thumbnail for

    Returns:
        dst: the thumbnail that we just made
    """
    _logger.info(f'Making a thumbnail for: {src}\n')
    thumbnail_cmd = f'ffprobe -i {src}'
    dst = get_thumbnail_path(filepath=src)
    if not os.path.exists(src):
        _logger.info(f'\tThat image: ({src}) does not appear to exist, exiting thumbnailer')
        return None

    file_type = filedata.get_ftype(filepath=src)

    # it's a still image
    if file_type.lower() in ['.png', '.bmp', '.jpg', '.tif', '.tiff']:
        thumbnail_cmd = f'ffmpeg -y -hide_banner -loglevel {config_obj.ffmpeg_loglevel} -i {src} -vf scale={config_obj.thumbnail_x_size}:{config_obj.thumbnail_y_size} {dst}'

    # it's a movie file
    elif file_type.lower() in ['.mp4', '.mov', '.webm', '.mkv']:
        # static thumbnail
        thumbnail_cmd = f'ffmpeg -y -hide_banner -loglevel {config_obj.ffmpeg_loglevel} -i {src} -vf scale={config_obj.thumbnail_x_size}:{config_obj.thumbnail_y_size} -ss {config_obj.movie_thumbnail_frame} -vframes 1 {dst}'
        # TODO: add ability to write out a scrubnail

    # it's an audio file (make a waveform image?)
    elif file_type.lower() in ['.mp3', '.wav', '.aiff', '.aif']:
        thumbnail_cmd = f'ffmpeg -y -hide_banner -loglevel {config_obj.ffmpeg_loglevel} -i {src} -filter_complex "showwavespic=s={config_obj.thumbnail_x_size}x{config_obj.thumbnail_y_size}:split_channels=1" -vframes 1 {dst}'

    # it's a text file (screen-cap and shrink?)
    elif file_type.lower() in ['.txt', '.doc', '.docx', '.rtf', '.epub', '.html', '.py']:
        # TODO: we may have to just store a standard text icon, copy it over to the dst name, and use that
        thumbnail_cmd = f'ffmpeg -video_size {config_obj.thumbnail_x_size}x{config_obj.thumbnail_y_size} -chars_per_frame 60000 -i {src} -frames:v 1 {dst}'

    # it's an archive type of file
    elif file_type.lower() in ['.zip', '.rar', '.gzip', '.tar']:
        thumbnail_cmd = f''

    # It's a type of file we have not anticipated
    else:
        return None

    # run the thumbnail command with subprocess
    # TODO: would rather have all logger stuff go into a .log file that gets pushed up to s3 with the asset
    #       This would allow us to troubleshoot possible issues that happened during submission
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(thumbnail_cmd, shell=True, stdout=fp)
        # print(f'command output: {p.communicate()}')
    return dst


if __name__ == '__main__':
    my_args = parse_args()
    print(my_args)
    make_thumbnail(src=my_args.filename[0])
