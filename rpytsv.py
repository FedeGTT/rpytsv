#!/usr/bin/env python
# extracts source text and translated text from Ren'Py files and saves the data in .tsv files for CAT tools
# column A: identifier, column B: character, column C: source; coulmn D: target

import glob # list .rpy files in directory
import re # regex

# regex to extract ids
regex_id = re.compile(r'^translate \w*\s*(?P<id>.+):(?P<id_content>[\s\S]+?)(?=translate|\Z)', re.MULTILINE)
# regex to extract characters
regex_character = re.compile(r'^    # (?P<character>.*?)\s*\"', re.MULTILINE)
# regex to extract characters and source text
regex_source = re.compile(r'^    (# |old)(?P<character>.*?)\s*\"(?P<text>.*)\"', re.MULTILINE)

# create a list for .rpy files
rpy = []
# add all .rpy files to the list
for f in glob.glob('*.rpy'):
    rpy.append(f)

# open every file, extract data and save it
for f in rpy:
    # open .rpy input file; encoding = 'UTF-8' due to special characters (e.g. cyrillic, chinese)
    with open(str(f), 'r', encoding = 'UTF-8') as rpy_file:
        # read the whole input file and store it in input
        input = rpy_file.read()

        # extract all characters and create regex_target
        # create a set to store all characters
        character = set()
        # search for all existing characters using regex and add them to the set (if a character is already part of the set, does nothing)
        for i in regex_character.finditer(input):
            character.add(i.group(1))
        # create a string with all characters for regex
        character_regex = ''
        # add the character followed by '|'
        for i in character:
            character_regex += i + '|'
        # regex to extract characters and translated text
        regex_target = re.compile(r'^    (?P<character>' + character_regex + 'extend|new)\s*\"(?P<text>.*)\"', re.MULTILINE)

        # create and open .rpy.tsv output file
        with open(str(f) + '.tsv', 'w', encoding = 'UTF-8') as tsv_file:
            # write the header row
            tsv_file.write('ID\tCharacter\tSource\tTarget')
            # search for ids using regex
            for i in regex_id.finditer(input):
                # create a list for characters
                character_list = []
                #create a list for source texts
                source_list = []
                # search for characters and source text using regex
                for j in regex_source.finditer(i.group(2)):
                    # add character to list
                    character_list.append(j.group(2))
                    # add source text to list
                    source_list.append(j.group(3))
                # create a list for target texts
                target_list = []
                # search for target text using regex and add target text to list
                for k in regex_target.finditer(i.group(2)):
                    target_list.append(k.group(2))
                # write to the output file a newline followed by id, character, source text and translated text found, separated by tabulations
                for character, source, target in zip(character_list, source_list, target_list):
                    tsv_file.write('\n{}\t{}\t{}\t{}'.format(i.group(1),character,source,target))