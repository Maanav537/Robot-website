import gpiod
import time,os
import neopixel
import board

class lightbar:
	l_pin = 21
	led_count = 8
	def activate():
		pixels = neopixel.NeoPixel(board.D21,8,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB)
		pixels.fill(255,255,255)
	def deactivate():
		pixels = neopixel.NeoPixel(board.D21,8,brightness=0,auto_write=True,pixel_order=neopixel.GRB)
		pixels.fill(255,255,255)
		
#test debug
pixels = neopixel.NeoPixel(board.D21,8,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB)
pixels.fill(255,255,255)
time.sleep(1)
pixels = neopixel.NeoPixel(board.D21,8,brightness=0,auto_write=True,pixel_order=neopixel.GRB)
pixels.fill(255,255,255)
