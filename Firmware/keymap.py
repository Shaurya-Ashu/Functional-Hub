"""
keymap.py — Functional Hub Macropad Configuration
Edit this file to change key bindings, encoder behaviour, and OLED layout.

PIN MAPPING (from schematic):
  SW1  → GP6    SW2  → GP7    SW3  → GP8    (dedicated tact switches)
  ENC_A → GP9   ENC_B → GP10  ENC_SW → GP11 (rotary encoder)
  I2C_SDA → GP4  I2C_SCL → GP5               (OLED SSD1306)
  NEOPIXEL → GP16  (if fitted, optional)

Layers:
  0 — Default  (media / shortcuts)
  1 — Gaming   (WASD macros)
  2 — CAD      (Fusion360 / KiCad shortcuts)
"""

import board
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ── GPIO PINS ────────────────────────────────────────────────────────────────

KEY_PINS = [
    board.GP6,   # SW1  — top-left
    board.GP7,   # SW2  — top-right
    board.GP8,   # SW3  — bottom (layer cycle / confirm)
]

ENCODER_A   = board.GP9
ENCODER_B   = board.GP10
ENCODER_SW  = board.GP11   # encoder push-button

I2C_SDA = board.GP4
I2C_SCL = board.GP5

NEOPIXEL_PIN = board.GP16   # set to None if not fitted
NUM_PIXELS   = 1

# ── LAYER DEFINITIONS ────────────────────────────────────────────────────────
# Each entry: ("label", action_type, payload)
#   action_type: "key"  → single Keycode
#                "mod"  → (modifier_keycode, key)
#                "cc"   → ConsumerControlCode
#                "macro"→ list of Keycodes pressed in sequence
#                "layer"→ switch to layer index

LAYERS = [
    # ── Layer 0: MEDIA / SHORTCUTS ──────────────────────────────────────────
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

    # ── Layer 1: GAMING ──────────────────────────────────────────────────────
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

    # ── Layer 2: CAD (KiCad / Fusion 360) ───────────────────────────────────
    {
        "name": "CAD",
        "keys": [
            ("Undo",     "mod",   (Keycode.CONTROL, Keycode.Z)),
            ("Redo",     "mod",   (Keycode.CONTROL, Keycode.Y)),
            ("Layer →",  "layer", 0),
        ],
        "encoder_cw":  ("Zoom In",  "key", Keycode.EQUALS),   # KiCad scroll-zoom
        "encoder_ccw": ("Zoom Out", "key", Keycode.MINUS),
        "encoder_sw":  ("Fit View", "key", Keycode.F),
    },
]

# ── OLED ─────────────────────────────────────────────────────────────────────
OLED_WIDTH  = 128
OLED_HEIGHT = 32    # SSD1306 128×32; change to 64 if you have 128×64

# ── NEOPIXEL LAYER COLOURS (R, G, B) ─────────────────────────────────────────
LAYER_COLOURS = [
    (0,   80, 255),   # Layer 0 — blue
    (0,  200,   0),   # Layer 1 — green
    (200, 80,   0),   # Layer 2 — amber
]
