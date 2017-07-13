#import everything (asterisk symbol ("*")) from Tkinter module, containing the Tk toolkit
from __future__ import with_statement
from __future__ import absolute_import
from Tkinter import *
#from tkinter.messagebox import *   #import messagebox module
from tkMessageBox import showerror, showinfo
from tkFileDialog import askopenfilename

import os
import subprocess

#can save file
import tkFileDialog, FileDialog
from io import open
from itertools import izip

#will be the language for the spoken text
global lang

string_1 = u"""
<!DOCTYPE html>
<html>
<head>
<title>
Automagically synchronize audio and text (aka forced alignment) 
</title>
<meta charset="UTF-8"> 
</head>
<body>

<script>
"""

string_2 = u"""
function switchColors(element)
{
links=document.getElementsByTagName("span") ;
for (var i = 0 ; i < links.length ; i ++){
links.item(i).style.color = 'black' ;
links.item(i).style.backgroundColor = 'white' ;
}
element.style.color='red' ;
element.style.backgroundColor='yellow' ;
}

function goToTime(time) {
    var vid = document.getElementById("myAudio");
//first make sure the audio player is playing
    vid.play(); 
//second seek to the specific time you're looking for
    vid.currentTime = time;
   }

var spans = document.getElementsByTagName('span');

function myFunction1(event) {
for (var j=0;j<spans.length;j++) {
//document.write(spans[j].innerHTML);
var target = spans[j];
if (event.currentTime > times[j] && event.currentTime < times[j+1]){
target.style.color = "red";
target.style.backgroundColor = "yellow";
//target.style.font-weight = "bold";
} else{
target.style.color = "black";
target.style.backgroundColor = "white";
//target.style.font-weight = "normal";
}
}
}
</script>
"""

string_3 = u'''
<table>
<tr>
<td style="text-align:center;">
<p>
<audio controls id="myAudio" ontimeupdate="myFunction1(this)">
   <source src="'''

string_4 = u'''" type="audio/mpeg">
Your browser does not support the audio element.
</audio>
</p>
</td>
</tr>
'''

string_5 = u"""
<tr>
<td>
            <div style="width:80%; max-height:20em; margin: 0 auto; overflow:auto; text-align:justify" >
<ul>
<li>
"""

string_6 = u"""
</li>
</ul>
             </div>
</td>
</tr>
</table>

</body>
</html>
"""

languages = [(u'afr', u'afr', 2, 0), (u'ara', u'ara', 2, 1), (u'bul', u'bul', 2, 2), (u'cat', u'cat', 2, 3), (u'cym', u'cym', 2, 4), (u'ces', u'ces', 2, 5), (u'dan', u'dan', 2, 6), (u'deu', u'deu', 2, 7), (u'ell', u'ell', 2, 8), (u'eng', u'eng', 2, 9), (u'epo', u'epo', 3, 0), (u'est', u'est', 3, 1), (u'fas', u'fas', 3, 2), (u'fin', u'fin', 3, 3), (u'fra', u'fra', 3, 4), (u'gle', u'gle', 3, 5), (u'grc', u'grc', 3, 6), (u'hrv', u'hrv', 3, 7), (u'hun', u'hun', 3, 8), (u'isl', u'isl', 3, 9), (u'ita', u'ita', 4, 0), (u'jpn', u'jpn', 4, 1), (u'lat', u'lat', 4, 2), (u'lav', u'lav', 4, 3), (u'lit', u'lit', 4, 4), (u'nld', u'nld', 4, 5), (u'nor', u'nor', 4, 6), (u'ron', u'ron', 4, 7), (u'rus', u'rus', 4, 8), (u'pol', u'pol', 4, 9), (u'por', u'por', 5, 0), (u'slk', u'slk', 5, 1), (u'spa', u'spa', 5, 2), (u'srp', u'srp', 5, 3), (u'swa', u'swa', 5, 4), (u'swe', u'swe', 5, 5), (u'tur', u'tur', 5, 6), (u'ukr', u'ukr', 5, 7)]

#define different functions
text_file=u""
def TextFile():
    global text_file   # Needed to modify global copy of  text_file
    text_file=askopenfilename()
    print text_file

mp3_file=u""
def mp3File():
    global mp3_file     # Needed to modify global copy of mp3_file
    mp3_file = askopenfilename()
    print mp3_file

html_file=u""
def htmlFile():
    global html_file     # Needed to modify global copy of html_file
    html_f1=tkFileDialog.asksaveasfile(mode=u'w',defaultextension=u".html")
    if html_f1 is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    html_file=html_f1.name
#    text2save=str(text.get(0.0,END))
#    html_f1.write(text2save)
    html_f1.close
    print html_file

def about():
    windowAbout.deiconify()

def on_closing():
        windowAbout.withdraw()

def ShowChoice():
    print lang.get()

def run():
    if text_file == u"":
        showerror(u"TEXT file", u"You chose no text file!")
    elif mp3_file == u"":
        showerror(u"MP3 file", u"You chose no mp3 file!")
    elif html_file == u"":
        showerror(u"HTML file", u"You chose no html file!")
    else:
        print text_file    # No need for global declaration to read value of text_file
        print mp3_file     # No need for global declaration to read value of mp3_file
        print html_file    # No need for global declaration to read value of html file
        newFile = u"temp_txt_file.txt"     #temporary txt file
        csv_file = u"temp_csv_file.csv"    #temporary csv file


#####
# 1 #
#####

###########################################################
#  Split a file by punctuation and print it in a new file #
###########################################################

#Remove the newline character in the text file and concantenate all the file in one string
#https://stackoverflow.com/questions/4319236/remove-the-newline-character-in-a-list-read-from-a-file

        with open(text_file, u'r') as input:
            lines = input.readlines()

        line_witout_NewLine = []
        for line in xrange(len(lines)):
            line_witout_NewLine.append(lines[line].strip(u'\n'))

        witout_new_line = u" ".join(line_witout_NewLine)

#Split the file with multiple delimiters, keeping them (,?!,;)
#First add a mark for every delimiter then split the string at the delimiter
#https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
        mark = u'@#$%^&'

        if mark in witout_new_line:
            print u"Choose another mark!\n"
            exit
        else:
            print u"MARK doesn't exists. It's OK."

        final = witout_new_line.replace(u'. ',u'.' + mark).replace(u'! ',u'!' + mark).replace(u'? ',u'?' + mark).replace(u'; ',u';' + mark).replace(u', ',u',' + mark).split(mark)

#print the new file 
        with open(newFile, u'w') as output:
            for line in final:
                output.write(line + u'\n')
#####
# 2 #
#####

####################
#  create csv file #
####################
        string1 = u'task_language=' + lang.get() + u'|os_task_file_format=csv|is_text_type=plain'
        print string1
#        subprocess.Popen(['python3', '-m', 'aeneas.tools.execute_task', mp3_file, newFile, 'task_language=eng|os_task_file_format=csv|is_text_type=plain', csv_file]).wait()
        subprocess.Popen([u'python2', u'-m', u'aeneas.tools.execute_task', mp3_file, newFile, string1, csv_file]).wait()


#####
# 3 #
#####

#create html file


        times_array = []
        transcript_array = []
#line_split = ['1','1','1','1']
        line_split = []
        with open(csv_file, u'r') as f:
            with open(html_file, u"w") as f1:
                f1.write(string_1)
                f1.write(u"var times = [")
                for line in f:
                    line_split = line.split(u",")
                    times_array.append(line_split[1])
                    say = line_split[3:]
                    say = u",".join(say)
                    say = say[1:-1]
                    transcript_array.append(unicode(say))
                    f1.write(line_split[1] + u', ')
                times_array.append(line_split[2])    
                f1.write(line_split[2])
                f1.write(u"];")
                f1.write(u"\n")
                f1.write(string_2)
                f1.write(string_3)
                f1.write(unicode(mp3_file))
                f1.write(string_4)
                f1.write(string_5)
                for (time, line) in izip(times_array, transcript_array):
                        f1.write(u'    ' + u'<span  onclick="switchColors(this); goToTime(' + time + u');">' + line[:-1] + u'</span>')
                        f1.write(u"\n")
                f1.write(string_6)
        print u"DONE!"
        showinfo(u"DONE", u"DONE!")

        
#We initialize Tkinter by crieating a Tk root widget. A root widget is a window with title bar and decoration provided by the window manager; it must be created before any other widgets and is is unique.
root = Tk()
root.title(u"Forced alignment with aeneas")

#Create a top-level window
#Create a Toplevel widget that is a rectangular region on the screen displayed in a separate top-level window. Such windows usually have title bars, borders, and other window decorations.
windowAbout = Toplevel()
windowAbout.withdraw()   #Hide the windowAbout window
help = u"ForcedAlignment\n\nForcedAlignment is a graphical tool to automatically synchronize audio and text.\nIt generates a html file with an audio player and a list.\nFor more information read the README.md file." #define a string
msg = Message(windowAbout, text = help) #Create a message widget
msg.config(bg=u'lightgreen', font=(u'times', 24, u'italic'))
msg.pack(expand=True, fill=u'both')
windowAbout.protocol(u"WM_DELETE_WINDOW", on_closing)   #if we click the close button "x" function on_close will be executed


#Create the Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label=u"Text File", command=TextFile)
filemenu.add_command(label=u"MP3 File", command=mp3File)
filemenu.add_command(label=u"html File", command=htmlFile)
filemenu.add_separator()
filemenu.add_command(label=u"Exit", command=root.quit)
menu.add_cascade(label=u"File", menu=filemenu)

runmenu = Menu(menu, tearoff=0)
runmenu.add_command(label=u"Run", command=run)
menu.add_cascade(label=u"Run", menu=runmenu)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label=u"About...", command=about)
menu.add_cascade(label=u"Help", menu=helpmenu)

lang = StringVar()
lang.set(u"eng")  # initializing the choice, i.e. ENG

Label(root, 
      text=u"""Choose the spoken language:""",
      justify = CENTER
      ).grid(row = 1, column = 0, columnspan = 10)

for txt, val, r, c in languages:
    Radiobutton(root, 
                text=txt,
                variable=lang, 
                command=ShowChoice,
                value=val).grid(row = r, column = c)

mainloop()
