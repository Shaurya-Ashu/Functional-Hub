"""
code.py — Functional Hub Macropad Firmware
Hardware: RP2040 (Raspberry Pi) on Functional Hub PCB
Runtime:  CircuitPython 9.x
Features: 3 keys · rotary encoder (CW/CCW/push) · SSD1306 OLED · NeoPixel · 3 layers

Required CircuitPython libraries (copy to /lib on CIRCUITPY):
  adafruit_hid          (bundle)
  adafruit_display_text (bundle)
  adafruit_displayio_ssd1306
  adafruit_debouncer
  neopixel              (bundle)

Flash CircuitPython 9.x UF2 for RP2040 from circuitpython.org before use.
"""

import time
import board
import busio
import displayio
import terminalio
import digitalio
import rotaryio
import neopixel
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import adafruit_displayio_ssd1306

import keymap  # ← all pin/layer config lives here

# ────────────────────────────────────────────────────────────────────────────
# HID setup
# ────────────────────────────────────────────────────────────────────────────
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
cc = ConsumerControl(usb_hid.devices)

# ────────────────────────────────────────────────────────────────────────────
# Keys — debounced digital inputs, active LOW (internal pull-up)
# ────────────────────────────────────────────────────────────────────────────
_raw_keys = []
for pin in keymap.KEY_PINS:
    p = digitalio.DigitalInOut(pin)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    _raw_keys.append(p)

keys = [Debouncer(p) for p in _raw_keys]

# Encoder push-button (debounced)
_enc_sw_raw = digitalio.DigitalInOut(keymap.ENCODER_SW)
_enc_sw_raw.direction = digitalio.Direction.INPUT
_enc_sw_raw.pull = digitalio.Pull.UP
enc_sw = Debouncer(_enc_sw_raw)

# ────────────────────────────────────────────────────────────────────────────
# Rotary encoder
# ────────────────────────────────────────────────────────────────────────────
encoder = rotaryio.IncrementalEncoder(keymap.ENCODER_A, keymap.ENCODER_B)
last_enc_pos = encoder.position

# ────────────────────────────────────────────────────────────────────────────
# NeoPixel (optional)
# ────────────────────────────────────────────────────────────────────────────
pixels = None
if keymap.NEOPIXEL_PIN is not None:
    pixels = neopixel.NeoPixel(
        keymap.NEOPIXEL_PIN, keymap.NUM_PIXELS, brightness=0.15, auto_write=True
    )

def set_pixel_for_layer(layer_idx):
    if pixels is not None:
        pixels[0] = keymap.LAYER_COLOURS[layer_idx % len(keymap.LAYER_COLOURS)]

# ────────────────────────────────────────────────────────────────────────────
# OLED — SSD1306 via I2C (128×32 or 128×64)
# ────────────────────────────────────────────────────────────────────────────
displayio.release_displays()

i2c = busio.I2C(scl=keymap.I2C_SCL, sda=keymap.I2C_SDA, frequency=400_000)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=keymap.OLED_WIDTH, height=keymap.OLED_HEIGHT
)

# Build a simple two-line display group
main_group = displayio.Group()

# Line 1: layer name
lbl_layer = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=2,
    y=8,
    scale=1,
)

# Line 2: last action
lbl_action = label.Label(
    terminalio.FONT,
    text="Ready",
    color=0xFFFFFF,
    x=2,
    y=22,
    scale=1,
)

main_group.append(lbl_layer)
main_group.append(lbl_action)
display.show(main_group)

def update_display(layer_name, action_name):
    lbl_layer.text  = f"[{layer_name}]"
    lbl_action.text = action_name[:20]   # truncate to fit 128px wide

# ────────────────────────────────────────────────────────────────────────────
# Layer state
# ────────────────────────────────────────────────────────────────────────────
current_layer = 0

def get_layer():
    return keymap.LAYERS[current_layer]

# ────────────────────────────────────────────────────────────────────────────
# Action dispatcher
# ────────────────────────────────────────────────────────────────────────────
def fire(action):
    """
    action tuple: ("label", type, payload)
    Handles key, mod, cc, macro, layer actions.
    """
    global current_layer
    label_str, atype, payload = action

    if atype == "key":
        kbd.press(payload)
        kbd.release_all()

    elif atype == "mod":
        # payload = (modifier, key) OR (modifier, key1, key2, …)
        if isinstance(payload, (list, tuple)):
            kbd.press(*payload)
        else:
            kbd.press(payload)
        kbd.release_all()

    elif atype == "cc":
        cc.send(payload)

    elif atype == "macro":
        # payload = list of Keycodes pressed one at a time in sequence
        for k in payload:
            kbd.press(k)
            time.sleep(0.05)
            kbd.release_all()
            time.sleep(0.02)

    elif atype == "layer":
        current_layer = payload % len(keymap.LAYERS)
        set_pixel_for_layer(current_layer)

    update_display(get_layer()["name"], label_str)

# ────────────────────────────────────────────────────────────────────────────
# Startup
# ────────────────────────────────────────────────────────────────────────────
set_pixel_for_layer(current_layer)
update_display(get_layer()["name"], "Ready")
print("Functional Hub Macropad — ready")

# ────────────────────────────────────────────────────────────────────────────
# Main loop
# ────────────────────────────────────────────────────────────────────────────
while True:
    layer = get_layer()

    # ── Debounce all keys ────────────────────────────────────────────────────
    for k in keys:
        k.update()
    enc_sw.update()

    # ── Physical key presses ─────────────────────────────────────────────────
    for idx, k in enumerate(keys):
        if k.fell:   # fell = just pressed (active LOW)
            action = layer["keys"][idx]
            fire(action)

    # ── Encoder push ─────────────────────────────────────────────────────────
    if enc_sw.fell:
        fire(layer["encoder_sw"])

    # ── Encoder rotation ─────────────────────────────────────────────────────
    pos = encoder.position
    delta = pos - last_enc_pos
    last_enc_pos = pos

    if delta > 0:
        for _ in range(abs(delta)):
            fire(layer["encoder_cw"])
    elif delta < 0:
        for _ in range(abs(delta)):
            fire(layer["encoder_ccw"])

    time.sleep(0.005)   # ~200 Hz poll; keeps CPU load low
