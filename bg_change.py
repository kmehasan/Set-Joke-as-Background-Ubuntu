import subprocess
from PIL import Image, ImageDraw, ImageFont

import requests
from requests.exceptions import HTTPError
import os

from string import ascii_letters
import textwrap

home_directory = os.path.expanduser( '~' )

def imgCreate(text):
	W, H = 1366, 768
	img = Image.new('RGB', (W, H), color = 'black')

	d = ImageDraw.Draw(img)
	font = ImageFont.truetype(f'{home_directory}/.local/share/fonts/Fasthand-Regular.ttf', 52)
	
	# Create DrawText object
	draw = ImageDraw.Draw(im=img)
	# Calculate the average length of a single character of our font.
	# Note: this takes into account the specific font and font size.
	avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
	# Translate this average length into a character count
	max_char_count = int(img.size[0] * .8 / avg_char_width)
	# Create a wrapped text object using scaled character count
	text = textwrap.fill(text=text, width=max_char_count)
	# Add text to the image
	draw.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#808080', anchor='mm')
	
	img.save(home_directory+'/bg.png')

def getJoke():

	while True:
		try:
		    response = requests.get('https://v2.jokeapi.dev/joke/Programming?safe-mode&type=single')
		    response.raise_for_status()
		    # access JSOn content
		    jsonResponse = response.json()
		    print("Entire JSON response")
		    return jsonResponse['joke']

		except HTTPError as http_err:
		    print(f'HTTP error occurred: {http_err}')
		except Exception as err:
		    print(f'Other error occurred: {err}')


imgCreate(getJoke())
path = f"file:///{home_directory}/bg.png"
subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", path])


