

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

import keymap  
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
cc = ConsumerControl(usb_hid.devices)


_raw_keys = []
for pin in keymap.KEY_PINS:
    p = digitalio.DigitalInOut(pin)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    _raw_keys.append(p)

keys = [Debouncer(p) for p in _raw_keys]


_enc_sw_raw = digitalio.DigitalInOut(keymap.ENCODER_SW)
_enc_sw_raw.direction = digitalio.Direction.INPUT
_enc_sw_raw.pull = digitalio.Pull.UP
enc_sw = Debouncer(_enc_sw_raw)


encoder = rotaryio.IncrementalEncoder(keymap.ENCODER_A, keymap.ENCODER_B)
last_enc_pos = encoder.position


pixels = None
if keymap.NEOPIXEL_PIN is not None:
    pixels = neopixel.NeoPixel(
        keymap.NEOPIXEL_PIN, keymap.NUM_PIXELS, brightness=0.15, auto_write=True
    )

def set_pixel_for_layer(layer_idx):
    if pixels is not None:
        pixels[0] = keymap.LAYER_COLOURS[layer_idx % len(keymap.LAYER_COLOURS)]


displayio.release_displays()

i2c = busio.I2C(scl=keymap.I2C_SCL, sda=keymap.I2C_SDA, frequency=400_000)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=keymap.OLED_WIDTH, height=keymap.OLED_HEIGHT
)


main_group = displayio.Group()


lbl_layer = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=2,
    y=8,
    scale=1,
)


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
    lbl_action.text = action_name[:20]   
  
current_layer = 0

def get_layer():
    return keymap.LAYERS[current_layer]


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
        if isinstance(payload, (list, tuple)):
            kbd.press(*payload)
        else:
            kbd.press(payload)
        kbd.release_all()

    elif atype == "cc":
        cc.send(payload)

    elif atype == "macro":
        
        for k in payload:
            kbd.press(k)
            time.sleep(0.05)
            kbd.release_all()
            time.sleep(0.02)

    elif atype == "layer":
        current_layer = payload % len(keymap.LAYERS)
        set_pixel_for_layer(current_layer)

    update_display(get_layer()["name"], label_str)


set_pixel_for_layer(current_layer)
update_display(get_layer()["name"], "Ready")
print("Functional Hub Macropad — ready")


while True:
    layer = get_layer()

    
    for k in keys:
        k.update()
    enc_sw.update()

    
    for idx, k in enumerate(keys):
        if k.fell:   
            action = layer["keys"][idx]
            fire(action)

  
    if enc_sw.fell:
        fire(layer["encoder_sw"])

    
    pos = encoder.position
    delta = pos - last_enc_pos
    last_enc_pos = pos

    if delta > 0:
        for _ in range(abs(delta)):
            fire(layer["encoder_cw"])
    elif delta < 0:
        for _ in range(abs(delta)):
            fire(layer["encoder_ccw"])

    time.sleep(0.005)  
