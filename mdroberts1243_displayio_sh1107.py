# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries
# Modified 2020 by Mark Roberts (mdroberts1243)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`mdroberts1243_displayio_sh1107`
================================================================================

DisplayIO driver for SH1107 monochrome displays


* Author(s): Scott Shawcroft, Mark Roberts (mdroberts1243)

Implementation Notes
--------------------

**Hardware:**

* `Adafruit FeatherWing 128 x 64 OLED - SH1107 128x64 OLED <https://www.adafruit.com/product/4650>`_

**Software and Dependencies:**

* Adafruit CircuitPython (version 5+) firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* A quirk is required on DisplayIO -- TBD

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/mdroberts1243/mdroberts1243_CircuitPython_DisplayIO_SH1107.git"

# Sequence from sh1107 framebuf driver formatted for displayio init
_INIT_SEQUENCE = (
    b"\xae\x00"         # display off, sleep mode
    b"\xdc\x01\x02"     # display start line = 2 (POR = 0)
    b"\x81\x01\x2f"     # contrast setting = 0x2f
    b"\x20\x00"         # page addressing mode (POR)
    b"\xa0\x00"         # segment remap = 0 (POR=0, down rotation)
    b"\xc0\x00"         # common output scan direction = 0 (0 to n-1 (POR=0))
    b"\xa8\x01\x7f"     # multiplex ratio = 128 (POR)
    b"\xd3\x01\x60"     # set display offset mode = 0x60
    b"\xd5\x01\x51"     # divide ratio/oscillator: divide by 2, fOsc (POR)
    b"\xd9\x01\x22"     # pre-charge/dis-charge period mode: 2 DCLKs/2 DCLKs (POR)
    b"\xdb\x01\x35"     # VCOM deselect level = 0.770 (POR)
    b"\xb0\x00"         # set page address = 0 (POR)
    b"\xa4\x00"         # entire display off, retain RAM, normal status (POR)
    b"\xa6\x00"         # normal (not reversed) display
    b"\xAF\x00\x00"     # DISPLAY_ON
)

# pylint: disable=too-few-public-methods
class SH1107(displayio.Display):
    """SSD1107 driver"""

    def __init__(self, bus, **kwargs):
        # Patch the init sequence for 32 pixel high displays.
        init_sequence = bytearray(_INIT_SEQUENCE)
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            height = kwargs["width"]
#        init_sequence[16] = height - 1  # patch mux ratio
#        if kwargs["height"] == 32:
#            init_sequence[25] = 0x02  # patch com configuration
        super().__init__(
            bus,
            init_sequence,
            **kwargs,
            color_depth=1,
            grayscale=True,
            pixels_in_byte_share_row=False,
            set_column_command=None, # sh1107 doesn't have a traditional set column command
            set_row_command=None, # sh1107 will set page, actually.
            data_as_commands=True, # I hope this means 0x80 for each byte in the init sequence.
            set_vertical_scroll=0xD3,
            brightness_command=0x81,
            single_byte_bounds=True,
            # for sh1107 use column and page addressing.
            #                lower column command = 0x00 - 0x0F
            #                upper column command = 0x10 - 0x17
            #                set page address     = 0xB0 - 0xBF (16 pages)
            column_and_page_addressing=True, # New quirk for sh1107
        )
