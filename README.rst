Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-displayio-sh1107/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/displayio-sh1107/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SH1107/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SH1107/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

DisplayIO driver for SH1107 monochrome displays. DisplayIO drivers enable terminal output.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython Version 6+ <https://github.com/adafruit/circuitpython>`_ A new quirk in 6.0 for SH1107
* An SH1107 OLED display, eg. `Adafruit FeatherWing 128 x 64 OLED <https://www.adafruit.com/product/4650>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading the
`Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-displayio_sh1107/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-displayio-sh1107

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-displayio-sh1107

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-displayio-sh1107

Usage Example
=============

.. code-block:: python

    import board
    import displayio
    import terminalio
    import bitmap_label as label # from adafruit_display_text
    import adafruit_displayio_sh1107

    displayio.release_displays()
    #oled_reset = board.D9

    # Use for I2C
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

    # SH1107 is vertically oriented 64x128
    WIDTH = 128
    HEIGHT = 64
    BORDER = 2

    display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

    # Make the display context
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle in black
    inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/displayio-sh1107/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SH1107/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
