import struct
import time

from pimoroni_i2c import PimoroniI2C

# The code reader has the I2C ID of hex 0c, or decimal 12.
TINY_CODE_READER_I2C_ADDRESS = 0x0C

# How long to pause between sensor polls.
TINY_CODE_READER_DELAY = 0.05

TINY_CODE_READER_LENGTH_OFFSET = 0
TINY_CODE_READER_LENGTH_FORMAT = "H"
TINY_CODE_READER_MESSAGE_OFFSET = TINY_CODE_READER_LENGTH_OFFSET + struct.calcsize(TINY_CODE_READER_LENGTH_FORMAT)
TINY_CODE_READER_MESSAGE_SIZE = 254
TINY_CODE_READER_MESSAGE_FORMAT = "B" * TINY_CODE_READER_MESSAGE_SIZE
TINY_CODE_READER_I2C_FORMAT = TINY_CODE_READER_LENGTH_FORMAT + TINY_CODE_READER_MESSAGE_FORMAT
TINY_CODE_READER_I2C_BYTE_COUNT = struct.calcsize(TINY_CODE_READER_I2C_FORMAT)

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)


def read_qr_code(timeout):
    result = None
    while timeout > 0.0:
        read_data = bytearray(TINY_CODE_READER_I2C_BYTE_COUNT)
        i2c.readfrom_into(TINY_CODE_READER_I2C_ADDRESS, read_data)

        message_length,  = struct.unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
        message_bytes = struct.unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)

        if message_length > 0:
            try:
                result = bytearray(message_bytes[0:message_length]).decode("utf-8")
                break
            except:
                print("Couldn't decode as UTF 8")
                pass

        time.sleep(TINY_CODE_READER_DELAY)
        timeout -= TINY_CODE_READER_DELAY
    return result
