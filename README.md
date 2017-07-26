# LatinVerbFinder
Generates a list all the words that could be first person verbs and their line numbers.

This relies on calls to William Whitaker's Words (https://github.com/mk270/whitakers-words) from the command line, so you will need to have it installed and in your path when you run this program.

This program only filters the output from Words, which unfortunately often includes words which are unattested forms, other words that share forms (e.g., loco, locare will show up when the word is locus in the ablative). So it still requires checking by hand

I originally wrote this to find first person verbs in Caesar, although you could find other forms just as easily by changing the regular expressions in lines 21, 24, 72-74.

**Usage**

./firstperson.py <text> 
You can use the option --no_clean after the text if you want to prevent the program from deleting the intermediate files, namely first_person.csv, a list of words to be passed to the dictionary and their line numbers, and WWW.txt, which is the raw output from William Whitaker's Words.

This program requires python >= 3.5.


**LICENSE**

This program is distributed as is without warranty and is made freely availabele to anyone who wishes to use it, for any purpose.
