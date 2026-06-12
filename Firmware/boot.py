"""
boot.py — Functional Hub Macropad
Runs before code.py. Enables USB HID (keyboard + consumer control).
Hold SW1 (GP6) on boot to enter REPL/mass-storage mode for flashing.
"""
import board
import digitalio
import storage
import usb_hid

# --- BOOT MODE BUTTON ---
# Hold SW1 on boot → stay in storage/REPL mode (for editing files)
boot_btn = digitalio.DigitalInOut(board.GP6)
boot_btn.direction = digitalio.Direction.INPUT
boot_btn.pull = digitalio.Pull.UP

if boot_btn.value:
    # Button NOT held → normal HID macropad mode
    # Disable mass storage so the host sees a clean HID device
    storage.disable_usb_drive()
    usb_hid.enable(
        (usb_hid.Device.KEYBOARD, usb_hid.Device.CONSUMER_CONTROL, usb_hid.Device.MOUSE)
    )
# else: button held → CircuitPython exposes CIRCUITPY drive + REPL

boot_btn.deinit()
