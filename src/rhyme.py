print ""
print "Dependencies: 'pronouncing', 'grammar_check'"

import os
import sys
import random
import pronouncing
import grammar_check

song_length = 4      # Number of lines
rhyme_interval = 2   # When to introduce a new rhyme
min_line_length = 15 # Min length of lines to consider
max_line_length = 55 # Max length of lines to consider
min_choices = 1      # Keep higher to increase quality under certain circumstances

lines = []

print ("")
print ("Rhyme Maker V1.0")
print ("")
print ("Instructions: Create file 'source.txt' in this directory")
print ("")
print ("Based on current settings, expect process to take up to " + str(1 + 1.5 * song_length * min_choices / rhyme_interval) + " minutes.")
print ("")

with open("source.txt") as sourceFile:
    for line in sourceFile:
		lines.extend(line.replace('\n', ' ').replace(',', '.').strip().split('.'))

processed_lines = []

for line in lines:
	if len(line) < max_line_length and len(line) > min_line_length:
		processed_lines.append(line)

lines = processed_lines

song = []
used_lines = []

sys.stdout.write("Processing")
sys.stdout.flush()
while (len(song) < song_length):
	sys.stdout.write('.')
	sys.stdout.flush()
	if len(song) == 0:
		first_line = random.choice(lines)
		song.append(first_line.rstrip('?:!.,;').strip())
		used_lines = [first_line]
	try:
		if len(song) % rhyme_interval == 0:
			next_line = random.choice(lines)
			song.append(next_line.rstrip('?:!.,;').strip())
			used_lines.append(next_line)
		else:
			rhymes = pronouncing.rhymes(song[-1].split()[-1].rstrip('?:!.,;'))
	
			choices = []	

			for rhyme in rhymes:
				for line in lines:
					if line not in used_lines:
						try:
							if line.split()[-1].rstrip('?:!.,;') == rhyme:
								choices.append(line)
								break;
						except IndexError:
							break;
			if len(choices) <= min_choices:
				song = []
			else:
				new_line = random.choice(choices)
				song.append(new_line)
				used_lines.append(new_line)
	except IndexError:
		song = []

print ("")

grammar = grammar_check.LanguageTool('en-US')
song_text = ""
for line in song:
	song_text += line + "; "
errors = grammar.check(song_text)

print ""
print "Found " + str(len(errors)) + " grammatical error(s)..."

#song_text = grammar.correct(song_text, errors)

#song = song_text.split('; ')

print ""
for line in song:
	print line
print ""		
