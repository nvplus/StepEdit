import csv
import sys
import json
import re
import os

ALLOWED_FILETYPES = ['sm']
NOTE_TITLES = ['playstyle', 'description', 'difficulty', 'rating', 'groove_radar']

filename=sys.argv[-1]
filetype = filename.split(".")[-1]

if filetype not in ALLOWED_FILETYPES:
    print("Filetype" " '" + filetype + "' " + "not recognized.")
    quit()

file = open(filename, 'r')

metadata = {}
diffs = []

notes_index = -1
curr_diff = {}
curr_diff_steps = []
curr_measure = []
curr_notes=[]
is_adding_chart = False


# Get bpms
match = re.search('#BPMS:([0-9.='+os.linesep+',]*);', file.read())
bpm_strings = match.group(1).split(',')

bpms = {}

for bpm_change in bpm_strings:
    bpm_change_line = bpm_change.split("=")
    bpms[bpm_change_line[0].strip()] = bpm_change_line[1].strip()
file.seek(0)

# Get stops
match = re.search('#STOPS:([0-9.='+os.linesep+',]*);', file.read())
stop_strings = match.group(1).split(',')
stops = {}

for stop in stop_strings:
    stop_line = stop.split("=")
    stops[stop_line[0].strip()] = stop_line[1].strip()

file.seek(0)

# process the rest of the data
for line in file.readlines():
    prefix = line[0]

    # Process metadata line (e.g. TITLE, ARTIST, OFFSET)
    if prefix == "#":
        match = re.match('#([A-Z]*):([A-Za-z0-9 .-]*);', line)

        if match:
            metadata[match.group(1)] = match.group(2)
    
    # We've started a new diff
    elif '/--' in line:
        is_adding_chart = True

    elif is_adding_chart:
        # we hit the start of a new diff
        if prefix == ";":

            # append our data to the current difficulty object
            for i, v in enumerate(curr_notes):
                if i == 4:
                    v = v.split(',')
                
                curr_diff[NOTE_TITLES[i]] = v

            curr_diff['steps'] = curr_diff_steps

            # append the difficulty's chart to the simfile's "diffs" object
            diffs.append(curr_diff)
            
            # reset all variables
            curr_diff = {}
            curr_diff_steps = []
            curr_notes = []
            is_adding_chart = False

        #  new measure
        elif prefix == ',':
            curr_diff_steps.append(curr_measure)
            curr_measure = []
        # we're on a step inside of a measure
        elif prefix.isalnum():
            curr_measure.append(line.strip()) 
        elif ':' in line:
            curr_notes.append(line.strip()[:-1])

file.close()

metadata["BPMS"] = bpms
metadata["STOPS"] = stops
simfile = {'metadata':metadata, 'diffs':diffs}

with open("result.json", "w") as outfile:
    json.dump(simfile, outfile)