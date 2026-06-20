
import board
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


KEY_PINS = [
    board.GP6,  
    board.GP7,  
    board.GP8,  
]

ENCODER_A   = board.GP9
ENCODER_B   = board.GP10
ENCODER_SW  = board.GP11  

I2C_SDA = board.GP4
I2C_SCL = board.GP5

NEOPIXEL_PIN = board.GP16   
NUM_PIXELS   = 1



LAYERS = [
    
    {
        "name": "Media",
        "keys": [
            ("Mute",        "cc",    ConsumerControlCode.MUTE),
            ("Screenshot",  "mod",   (Keycode.GUI, Keycode.SHIFT, Keycode.S)),
            ("Layer →",     "layer", 1),
        ],
        "encoder_cw":  ("Vol+",   "cc", ConsumerControlCode.VOLUME_INCREMENT),
        "encoder_ccw": ("Vol-",   "cc", ConsumerControlCode.VOLUME_DECREMENT),
        "encoder_sw":  ("Play",   "cc", ConsumerControlCode.PLAY_PAUSE),
    },

  
    {
        "name": "Gaming",
        "keys": [
            ("Push-to-Talk", "key",   Keycode.CAPS_LOCK),
            ("Scoreboard",   "key",   Keycode.TAB),
            ("Layer →",      "layer", 2),
        ],
        "encoder_cw":  ("Next weapon", "key", Keycode.E),
        "encoder_ccw": ("Prev weapon", "key", Keycode.Q),
        "encoder_sw":  ("Reload",      "key", Keycode.R),
    },

  
    {
        "name": "CAD",
        "keys": [
            ("Undo",     "mod",   (Keycode.CONTROL, Keycode.Z)),
            ("Redo",     "mod",   (Keycode.CONTROL, Keycode.Y)),
            ("Layer →",  "layer", 0),
        ],
        "encoder_cw":  ("Zoom In",  "key", Keycode.EQUALS),   
        "encoder_ccw": ("Zoom Out", "key", Keycode.MINUS),
        "encoder_sw":  ("Fit View", "key", Keycode.F),
    },
]


OLED_WIDTH  = 128
OLED_HEIGHT = 32    


LAYER_COLOURS = [
    (0,   80, 255),   
    (0,  200,   0),   
    (200, 80,   0),   
]
