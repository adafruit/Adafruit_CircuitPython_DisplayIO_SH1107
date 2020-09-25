Introduction
============
DisplayIO driver for SH1107 monochrome displays. DisplayIO drivers enable terminal output. This driver depends on a future (TBD) quirk added to DisplayIO. 


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython Version 5+ <https://github.com/adafruit/circuitpython>`_
* Adafruit SH1107 128 x 64 OLED display, used for testing.

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example (see example for more)
=============

.. code-block:: python

    import board
    import displayio
    import terminalio
    import bitmap_label as label # from adafruit_display_text
    import mdroberts1243_displayio_sh1107

    displayio.release_displays()
    #oled_reset = board.D9

    # Use for I2C
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

    # SH1107 is vertically oriented 64x128
    WIDTH = 128
    HEIGHT = 64
    BORDER = 2

    display = mdroberts1243_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

    # Make the display context
    splash = displayio.Group(max_size=10)
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

