
import board
import digitalio
import storage
import usb_hid


boot_btn = digitalio.DigitalInOut(board.GP6)
boot_btn.direction = digitalio.Direction.INPUT
boot_btn.pull = digitalio.Pull.UP

if boot_btn.value:
    storage.disable_usb_drive()
    usb_hid.enable(
        (usb_hid.Device.KEYBOARD, usb_hid.Device.CONSUMER_CONTROL, usb_hid.Device.MOUSE)
    )


boot_btn.deinit()
