# Copyright (c) 2020-2022, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from setuptools import setup
import sys
import os
import re

AVAILABLE_BOARDS = {
    'RAIBOARD_AGX': 'compatible with RAIBOARD-AGX',
    'DSBOARD_AGXMAX': 'compatible with DSBOARD-AGXMAX rev-1.2 or newer',
    'DSBOARD_AGXMAX_Rev-1.1': 'compatible with DSBOARD-AGXMAX rev-1.0 or 1.1',
    'DSBOARD_AGX': 'compatible with DSBOARD-AGX',
    'MILBOARD_ORNX': 'compatible with MILBOARD-ORNX',
    'RAIBOARD_ORNX': 'compatible with RAIBOARD-ORNX',
    'DSBOARD_ORNX': 'compatible with DSBOARD-ORNX',
    'DSBOARD_ORNX_LAN': 'compatible with DSBOARD-ORNX-LAN rev-1.1 or newer',
    'DSBOARD_ORNX_LAN_Rev-1.0': 'compatible with DSBOARD-ORNX-LAN rev-1.0',
    'DSBOARD_XV2': 'compatible with DSBOARD-XV2',
    'DSBOARD_NX2': 'compatible with DSBOARD-NX2 rev-1.23 or newer',
    'DSBOARD_NX2_Rev-1.22': 'compatible with DSBOARD-NX2 rev-1.22',
    'DSBOARD_NX2_Rev-1.21': 'compatible with DSBOARD-NX2 from rev-1.0 to rev-1.21'
}

def print_board_help():
    print("Available board types for --board:\n")
    for board, desc in AVAILABLE_BOARDS.items():
        print(f"  {board:<26} {desc}")
    print("")

board_arg = None
show_help = False
args = sys.argv[:]
sys.argv = []
skip_next = False
for i, arg in enumerate(args):
    if skip_next:
        skip_next = False
        continue
    if arg in ('-h', '--help'):
        show_help = True
        sys.argv.append(arg)
    elif arg.startswith('--board='):
        board_arg = arg.split('=', 1)[1]
    elif arg == '--board':
        if i + 1 < len(args):
            board_arg = args[i+1]
            skip_next = True
    else:
        sys.argv.append(arg)

if show_help:
    print_board_help()

if board_arg:
    if board_arg not in AVAILABLE_BOARDS:
        print(f"Error: Invalid board type '{board_arg}'.\n")
        print_board_help()
        sys.exit(1)

    file_path = os.path.join('lib', 'python', 'Jetson', 'GPIO', 'gpio_pin_data.py')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        content = re.sub(
            r"^FORECR_BOARD_TYPE\s*=\s*['\"].*?['\"]", 
            "FORECR_BOARD_TYPE = '{0}'".format(board_arg), 
            content, 
            flags=re.MULTILINE
        )
        
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Configured FORECR_BOARD_TYPE as '{board_arg}'")
    else:
        print(f"Warning: {file_path} not found. Could not set board type.")
        sys.exit(1)


classifiers = ['Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name                          = 'Jetson.GPIO',
      version                       = '2.1.12',
      author                        = 'NVIDIA',
      author_email                  = 'linux-tegra-bugs@nvidia.com',
      description                   = 'A module to control Jetson GPIO channels',
      long_description              = open('README.md').read(),
      long_description_content_type = 'text/markdown',
      license                       = 'MIT',
      keywords                      = 'Jetson GPIO',
      url                           = 'https://github.com/forecr/jetson-gpio',
      classifiers                   = classifiers,
      package_dir                   = {'': 'lib/python/'},
      packages                      = ['Jetson', 'Jetson.GPIO', 'RPi', 'RPi.GPIO'],
      package_data                  = {'Jetson.GPIO': ['99-gpio.rules',]},
      include_package_data          = True,
      entry_points={
          'console_scripts': [
              'jetson-gpio-pinmux-lookup=Jetson.GPIO.gpio_pinmux_lookup:main'
          ]
      },
)
