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

import Jetson.GPIO as GPIO
import json
import pandas

pin_defs, jetson_info = GPIO.gpio_pin_data.jetson_gpio_data.get(GPIO.model)
#print(jetson_info)
#print(pin_defs)
#print(json.dumps(jetson_info, indent=2))

print('Module Type: '+ GPIO.model)
print('')

pin_def_table = pandas.DataFrame.from_dict(pin_defs)
pin_def_table.set_axis(['Offset', 'Name', 'Chip', 'BOARD', 'BCM', 'CVM', 'TEGRA_SOC', 'PWM Dir', 'PWM ID', 'PADCTL'], axis=1, inplace=True)
print('Offset    -> Linux GPIO pin number (line offset inside chip, not global)')
print('Name      -> Linux exported GPIO name')
print('Chip      -> GPIO chip name/instance')
print('BOARD     -> Pin number (BOARD mode)')
print('BCM       -> Pin number (BCM mode)')
print('CVM       -> Pin name (CVM mode)')
print('TEGRA_SOC -> Pin name (TEGRA_SOC mode)')
print('PWM Dir   -> PWM chip sysfs directory')
print('PWM ID    -> PWM ID within PWM chip')
print('PADCTL    -> PADCTL Register Address')
print('')
print(pin_def_table)

