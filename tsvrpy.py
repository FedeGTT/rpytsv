#!/usr/bin/env python
# extracts translated text from .tsv files, removes extra spaces and quotes and enters it into Ren'Py files; saves as .rpy.txt as a safety measure
# expected structure of the .tsv files: no header, column A = id, column B = character, column C = source language; coulmn D = target language

import glob # list .rpy.tsv files in directory
import re # regex

# regex to extract translations
transl = re.compile(r'\t.*\t(?P<tr>.*)', re.MULTILINE)

# create a list for .rpy.tsv files
tsv = []
# add all .rpy.tsv files to the list
for f in glob.glob("*.rpy.tsv"):
    tsv.append(f)

# open every file and extract the translation
for f in tsv:
    # open .rpy.tsv input file; encoding = "UTF-8" due to cyrillic and chinese characters
    with open(str(f), "r", encoding = "UTF-8") as tsv_input:
        # slice the last four characters of the .rpy.tsv filename to obtain a .rpy filename
        rpyf = str(f)[:-4]
        # read the whole input file and store it in string
        string = tsv_input.read()
        # create a list on which to store the translation
        translation_list = []
        # search for the translation using regex
        for m in transl.finditer(string):
            # add to the translation without leading or trailing spaces
            translation_list.append(m.group(1).strip())
        # open .rpy file
        with open(rpyf, "r", encoding = "UTF-8") as rpy:
            # read the whole .rpy file and store it in a list containing each line of the file as a list item
            rpy_list = rpy.readlines()
            # counter for translation_list
            n = 0
            # create and open .rpy.txt output file
            with open(rpyf + ".txt", "w", encoding = "UTF-8") as output:
                # obtain ids of the rpy_list list where the translation needs to be added
                rpy_id = [i for i, item in enumerate(rpy_list) if re.search('^    (?P<type>extend|new|[^\s]{1,2})\s*\"(?P<text>.*)\"', item)]
                # insert the translations
                for m in rpy_id:
                    # repr() makes sure \n are parsed correctly, .strip() removes leading and trailing spaces, ', "
                    rpy_list[m] = re.sub(r'\"\"', '\"' + repr(translation_list[n]).strip(" \'\"") + '\"', rpy_list[m])
                    # increase the counter
                    n += 1
                # save on .txt
                for item in rpy_list:
                    output.write("%s" % item)