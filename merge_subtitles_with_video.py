# Have you ever saw this error while trying to merge/embed subtitles
#  into a video file on Windows?
# 
# Fontconfig error: Cannot load default config file
# [Parsed_subtitles_0 @ 0000000002bf1ee0] No usable fontconfig configuration # file
# found, using fallback.
# Fontconfig error: Cannot load default config file
#
# This scripts merges subtitles (if present) and transcodes video files
# to H.264 mp4 video files with similar quality level.
# This will be applied to all video files found under the directory passed
# as an argument to the script or the current working directory otherwise.
# The script will also check if the ffmpeg binaries are present and located
# in unrestricted directory. It will also check for the presence of fonts
# configuration file and copy it to the right place if they are absent.
#
# This code is free software: you can redistribute it and/or modify it under the
# terms of  the  GNU  Lesser  General  Public  License  as published by the Free
# Software Foundation,  either version 3 of the License, or (at your option) any
# later version.
#
# This code is distributed in the hope that it will be useful, but  WITHOUT  ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See  the  GNU  Lesser  General  Public  License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with code. If not, see http://www.gnu.org/licenses/.

import os
import sys

def check():
    # Check if the base directory envirnonment variable is defined
    ffmpeg = ''
    try:
        ffmpeg = os.environ['FFMPEG_DIRECTORY']
    except:
        print 'Point FFMPEG_DIRECTORY environment variable to the location of FFMPEG'
        return None
    # Check if the binaries are not located in restricted directory
    if -1 != ffmpeg.lower().find('system32'):
        print 'The ffmpeg binaries cannot be under system32 directory'
        return None
    # Check if the binaries exist
    binaries = ffmpeg + os.sep + 'bin' + os.sep
    if not (os.path.exists(binaries + 'ffmpeg') or os.path.exists(binaries + 'ffmpeg.exe')):
        print 'Please download the ffmpeg binaries from www.ffmpeg.org'
        return None
    return binaries

def configure(binaries):
    # The fonts.conf must be under the directory with ffmpeg executable
    fonts = binaries + 'fonts'
    # Neme of the config file must be fonts.conf
    name = 'fonts.conf'
    # Point ffmped to its fonts.conf
    os.environ['FC_CONFIG_DIR'] = fonts
    os.environ['FC_CONFIG_FILE'] = fonts + os.sep + name
    # Check the presence of fonts directory
    if not os.path.exists(os.environ['FC_CONFIG_DIR']):
        os.mkdir(os.environ['FC_CONFIG_DIR'])
    # Check the presence of fonts.conf
    if not os.path.exists(os.environ['FC_CONFIG_FILE']):
        file = open(os.environ['FC_CONFIG_FILE'], 'wb')
        file.write('<fontconfig><dir>C:\WINDOWS\Fonts</dir></fontconfig>')
        file.close()

def target():
    # Use either the directory passed as argument or current one 
    if 1 < len(sys.argv):
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    return directory

def video(name):
    # Check if it is a video file
    for extension in ['.avi', '.mp4', '.mkv']:
        if name.endswith(extension):
            return True
    return False

def simplify(path):
    # Make sure we get rid of quote characters in file name
    return path.replace('"', '').replace('\'', '').replace(',', '')

def merge(binaries):
    # Generic command for merging subtitles with video
    command = binaries + 'ffmpeg -i "%s" -acodec libvo_aacenc -b:a 128k -ac 2 -vcodec libx264 %s "%s"'
    # Process all the files in target directory
    for root, dirs, files in os.walk(target()):
        for name in files:
            # Process only video files
            if video(name):
                original = name
                # Go to the directory where the file is located
                os.chdir(root)
                # Extract the name of the file without the extension
                name = name[:-4]
                # Assume the subtitles have the same name as the video file
                subtitles = name + '.srt'
                # Get rid of quote characters
                os.rename(original, simplify(original))
                original = simplify(original)
                merged = simplify(name) + '.srt.mp4'
                # Expand the command if subtitles are present (UTF-8 is assumed)
                if os.path.exists(subtitles):
                    os.rename(subtitles, simplify(subtitles))
                    subtitles = simplify(subtitles)
                    subtitles = '-vf subtitles="%s"' % subtitles
                else:
                    subtitles = ''
                # Run the conversion/merger
                os.system(command % (original, subtitles, merged))

# Check the presence and location of the binaries
binaries = check()
if None != binaries:
    if 'nt' == os.name:
        # Configure the fonts for the subtitles
        configure(binaries)
    # Merge the subtitles with the video
    merge(binaries)
