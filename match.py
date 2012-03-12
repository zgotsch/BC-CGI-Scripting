#!c:/Python27/python.exe -u

## Code by Zach Gotsch licensed under the MIT Open Source License
## Copyright (c) 2012 Zach Gotsch
##
## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import cgitb
cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

def match(short_string, long_string, offset):
	score = 0
	for i in range(len(short_string)):
		score += match_char(short_string[i], long_string[(offset + i) % len(long_string)])
	return score

def match_char(a, b):
	if a != 'x' and a != 'o': raise Exception("Invalid character in short string")
	if b != 'x' and b != 'o': raise Exception("Invalid character in long string")
	return 1 if a == b else 0

def print_monospace(s):
	import sys
	if not debug:
		sys.stdout.write(monospace_tag_open)
	sys.stdout.write(s)
	if not debug:
		sys.stdout.write(monospace_tag_close)
		sys.stdout.write('<br/>')

debug = False
long_string = ""
short_string = ""
space = "&nbsp;"
ring = False
monospace_tag_open = '<span style="font-family: monospace">'
monospace_tag_close = '</span>'

if __name__ == "__main__":
	if debug == True:
		long_string = raw_input("Long string:")
		short_string = raw_input("Short string:")
		space = " "
	else:
		import cgi
		form = cgi.FieldStorage()
		long_string = form.getfirst('long_string', '').lower()
		short_string = form.getfirst('short_string', '').lower()
		ring = form.getfirst('ring') == "true"

	if(len(long_string) == 0 or len(short_string) == 0):
		print("Recieved bad input");
	else:
		high_score = -1
		high_index = -1
		max_first_index = len(long_string) if ring else len(long_string) - len(short_string) + 1
		for i in range(max_first_index):
			current_score = match(short_string, long_string, i)
			if current_score > high_score:
				high_score = current_score
				high_index = i

		print "\nscored %d at %d<br/>" % (high_score, high_index)
		print_monospace(long_string)
		print_monospace(space * high_index + short_string)
		print_monospace("%d%% match!" % (high_score * 100 / len(short_string)))
