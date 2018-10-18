esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.bin
ampy --port /dev/tty.SLAB_USBtoUART put boot.py
