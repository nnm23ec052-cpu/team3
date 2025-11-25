# CH1116 OLED Driver for 128x32 displays (0.91 inch)
# Works on RasPi Pico / Pico W

import framebuf
import time


class CH1116:
    def init(self, width, height, external_vcc=False):
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)

        self.framebuf = framebuf.FrameBuffer(
            self.buffer, self.width, self.height, framebuf.MONO_VLSB
        )

        self.external_vcc = external_vcc
        self.init_display()

    def write_cmd(self, cmd):
        raise NotImplementedError

    def write_data(self, buf):
        raise NotImplementedError

    def init_display(self):
        init_cmds = [
            0xAE,  # Display OFF
            0x20, 0x02,  # Page addressing mode
            0xB0,        # Page start
            0xC8,        # COM scan direction remap
            0x00,        # Lower column address
            0x10,        # Higher column address
            0x40,        # Start line = 0
            0x81, 0x50,  # Contrast
            0xA1,        # Segment remap
            0xA6,        # Normal display (not inverted)
            0xA8, 0x1F,  # Multiplex Ratio (for 32 height)
            0xD3, 0x00,  # Display offset
            0xD5, 0x80,  # Display clock divide ratio
            0xD9, 0x1F,  # Pre-charge
            0xDA, 0x02,  # COM pins hardware config
            0xDB, 0x20,  # VCOM level
            0x8D, 0x14,  # Charge pump
            0xAF         # Display ON
        ]

        for cmd in init_cmds:
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def fill(self, col=0):
        self.framebuf.fill(col)

    def pixel(self, x, y, col=1):
        self.framebuf.pixel(x, y, col)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 | page)  # Set page
            self.write_cmd(0x00)         # Lower column
            self.write_cmd(0x10)         # Higher column
            start = page * self.width
            end = start + self.width
            self.write_data(self.buffer[start:end])


class CH1116_I2C(CH1116):
    def init(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().init(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x00
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)
