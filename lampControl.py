import time
from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver

# --- Configuration ---
# Define the color you want the strip to be.
# Color(red, green, blue) with values from 0-255.
# For example, YELLOW is Color(255, 255, 0)
LAMP_COLOR = Color(255, 255, 255) 
OFF = Color(0, 0, 0)

# Initialize the driver for a strip of 8 LEDs
try:
    driver = WS2812SpiDriver(spi_bus=0, spi_device=0, led_count=8)
    strip = driver.get_strip()
except Exception as e:
    print(f"Error initializing LED strip: {e}")
    print("Please ensure SPI is enabled and the rpi5_ws2812 library is installed correctly.")
    exit()

def lampOn(color):
    """Sets all pixels to the specified color and updates the strip."""
    strip.set_all_pixels(color)
    strip.show()

def lampOff():
    """Turns all pixels off and updates the strip."""
    strip.set_all_pixels(OFF)
    strip.show()

# --- Main Execution ---
if __name__ == "__main__":
    print("Turning lamp on. Press Ctrl+C to turn off and exit.")
    
    try:
        # Set the lamp to the desired color
        lampOn(LAMP_COLOR)
        
        # Keep the script running in an infinite loop
        # The LEDs will stay in the state they were set to
        while True:
            time.sleep(1) # Sleep to reduce CPU usage

    except KeyboardInterrupt:
        # This block runs when you press Ctrl+C
        print("\nExiting program.")
    
    finally:
        # This block runs regardless of how the try block exits
        # to ensure the lights are turned off cleanly.
        print("Turning lamp off.")
        lampOff()