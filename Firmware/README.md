# Functional Hub — RP2040 Macropad Firmware

## Hardware (from schematic)
| Function        | RP2040 Pin |
|-----------------|-----------|
| SW1 (Key 0)     | GP6       |
| SW2 (Key 1)     | GP7       |
| SW3 (Key 2)     | GP8       |
| Encoder A       | GP9       |
| Encoder B       | GP10      |
| Encoder Button  | GP11      |
| OLED SDA        | GP4       |
| OLED SCL        | GP5       |
| NeoPixel        | GP16      |

> **If your schematic differs**, only edit `keymap.py` — `code.py` never needs touching for pin changes.

---

## Flashing steps

1. **Install CircuitPython 9.x**
   - Hold BOOTSEL on RP2040 → connect USB → drag `adafruit-circuitpython-raspberry_pi_pico-en_US-9.x.x.uf2` onto the `RPI-RP2` drive.
   - Drive reappears as `CIRCUITPY`.

2. **Install libraries**  
   Download the [CircuitPython 9.x library bundle](https://circuitpython.org/libraries) and copy these folders/files into `CIRCUITPY/lib/`:
   ```
   adafruit_hid/
   adafruit_display_text/
   adafruit_displayio_ssd1306.mpy
   adafruit_debouncer.mpy
   neopixel.mpy
   ```

3. **Copy firmware files**  
   Copy all three files to the root of `CIRCUITPY/`:
   ```
   boot.py
   code.py
   keymap.py
   ```
   Eject safely → replug. The device enumerates as a USB HID keyboard.

---

## Usage

### Boot modes
| Condition           | Result                                  |
|---------------------|-----------------------------------------|
| SW1 NOT held        | HID macropad (storage hidden from host) |
| SW1 held at boot    | CIRCUITPY drive visible + REPL          |

### Layers (cycle with SW3)
| Layer | Name   | Colour |
|-------|--------|--------|
| 0     | Media  | Blue   |
| 1     | Gaming | Green  |
| 2     | CAD    | Amber  |

### Default bindings

**Layer 0 — Media**
| Input        | Action            |
|--------------|-------------------|
| SW1          | Mute              |
| SW2          | Win+Shift+S (snip)|
| SW3          | Next layer        |
| Enc CW       | Volume Up         |
| Enc CCW      | Volume Down       |
| Enc Push     | Play/Pause        |

**Layer 1 — Gaming**
| Input    | Action       |
|----------|--------------|
| SW1      | Caps Lock (PTT) |
| SW2      | Tab (scoreboard)|
| SW3      | Next layer   |
| Enc CW   | E (next item)|
| Enc CCW  | Q (prev item)|
| Enc Push | R (reload)   |

**Layer 2 — CAD**
| Input    | Action   |
|----------|----------|
| SW1      | Ctrl+Z   |
| SW2      | Ctrl+Y   |
| SW3      | Next layer|
| Enc CW   | Zoom In  |
| Enc CCW  | Zoom Out |
| Enc Push | F (fit)  |

---

## Customising
All bindings, pins, and OLED size are in `keymap.py`. Add more layers by appending to the `LAYERS` list — no changes to `code.py` needed.

## No OLED / No NeoPixel?
- **No OLED:** Comment out the `import adafruit_displayio_ssd1306` block and the `update_display` calls in `code.py`, or just leave as-is (it will error silently after 3 retries and keep running).
- **No NeoPixel:** Set `NEOPIXEL_PIN = None` in `keymap.py`.
