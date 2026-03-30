# Copyright (c) 2019-2022, NVIDIA CORPORATION. All rights reserved.
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

import argparse
from lib.python.Jetson.GPIO.gpio_pin_data import FORECR_COMPATIBLE_BOARD_TYPES, FORECR_BOARD_TYPE

gpio_pin_data_file = "lib/python/Jetson/GPIO/gpio_pin_data.py"
keyword = "FORECR_BOARD_TYPE"
print_extra_messages = False

def get_lib_board_config():
    # Read the gpio_pin_data.py file again
    with open(gpio_pin_data_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(keyword):
                return(line.replace('\n', ''))


def get_system_config():
    with open("/proc/device-tree/model", "r") as file:
        lines = file.readlines()
        for line in lines:
            if print_extra_messages:
                print("System model: " + line)

            if "ORNXLAN" in line:
                line = line.replace('ORNXLAN', 'ORNX-LAN')

            if "DSBOX" in line:
                line = line.replace('DSBOX', 'DSBOARD')
            elif "RAIBOX" in line:
                line = line.replace('RAIBOX', 'RAIBOARD')
            elif "MILBOX" in line:
                line = line.replace('MILBOX', 'MILBOARD')

            return(line.replace('\n', ''))


def find_compatible_board_config(system_config):
    for board_name in FORECR_COMPATIBLE_BOARD_TYPES:
        if board_name in system_config:
            if print_extra_messages:
                print(board_name + " found")
            return(board_name)
        else:
            if print_extra_messages:
                print(board_name + " not found")

    return(FORECR_BOARD_TYPE) # If none of the compatible board names matched, use the default one


def update_lib_board_config(new_board_config):
    new_board_config = find_compatible_board_config(new_board_config)
    new_line = keyword + " = '" + new_board_config + "'"

    # Read the gpio_pin_data.py file
    with open(gpio_pin_data_file, "r") as file:
        lines = file.readlines()

    board_config_found = False
    default_board_config = ""

    # Update the new board name
    with open(gpio_pin_data_file, "w") as file:
        for line in lines:
            if line.startswith(keyword):
                default_board_config = line
                file.write(new_line + "\n")  # Replace the line
                board_config_found = True  # Mark that the line was found
            else:
                file.write(line)

        if not board_config_found:
            file.write(new_line)  # Add new setting at the end

    if print_extra_messages:
        print(gpio_pin_data_file + " updated for " + new_board_config + " successfully!")


print("*** Jetson-GPIO Configuration Tool for forecr products ***")
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interactive", action='store_true', help="Run with iteractive mode (to verify the board config and/or change it manually)")
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.help:
    parser.print_help()
    exit()
if args.verbose:
    print_extra_messages = True
if args.interactive:
    print("Interactive Mode: On")

print("Default " + get_lib_board_config())

update_lib_board_config(get_system_config())

print("New " + get_lib_board_config())

if args.interactive:
    selection = input('Do you want to change it? [y/n] ').lower()
    if selection.startswith('y'):
        print("")
        print("Compatible board list:")
        for board_name in FORECR_COMPATIBLE_BOARD_TYPES:
            print("--> " + board_name)
        print("")
        update_lib_board_config(input('Please type the correct board config: '))
        print("New " + get_lib_board_config())
    else:
        print("Skipping...")

print("Done.")
