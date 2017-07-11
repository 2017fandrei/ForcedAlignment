#import everything (asterisk symbol ("*")) from Tkinter module, containing the Tk toolkit
from tkinter import *
#from tkinter.messagebox import *   #import messagebox module
from tkinter.messagebox import showerror, showinfo

#from tkFileDialog module import class askopenfilename
from tkinter.filedialog import askopenfilename

import os
import subprocess

#can save file
import tkinter.filedialog

#will be the language for the spoken text
global lang

string_1 = """
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

string_2 = """
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

string_3 = '''
<table>
<tr>
<td style="text-align:center;">
<p>
<audio controls id="myAudio" ontimeupdate="myFunction1(this)">
   <source src="'''

string_4 = '''" type="audio/mpeg">
Your browser does not support the audio element.
</audio>
</p>
</td>
</tr>
'''

string_5 = """
<tr>
<td>
            <div style="width:80%; max-height:20em; margin: 0 auto; overflow:auto; text-align:justify" >
<ul>
<li>
"""

string_6 = """
</li>
</ul>
             </div>
</td>
</tr>
</table>

</body>
</html>
"""

languages = [('afr', 'afr', 2, 0), ('ara', 'ara', 2, 1), ('bul', 'bul', 2, 2), ('cat', 'cat', 2, 3), ('cym', 'cym', 2, 4), ('ces', 'ces', 2, 5), ('dan', 'dan', 2, 6), ('deu', 'deu', 2, 7), ('ell', 'ell', 2, 8), ('eng', 'eng', 2, 9), ('epo', 'epo', 3, 0), ('est', 'est', 3, 1), ('fas', 'fas', 3, 2), ('fin', 'fin', 3, 3), ('fra', 'fra', 3, 4), ('gle', 'gle', 3, 5), ('grc', 'grc', 3, 6), ('hrv', 'hrv', 3, 7), ('hun', 'hun', 3, 8), ('isl', 'isl', 3, 9), ('ita', 'ita', 4, 0), ('jpn', 'jpn', 4, 1), ('lat', 'lat', 4, 2), ('lav', 'lav', 4, 3), ('lit', 'lit', 4, 4), ('nld', 'nld', 4, 5), ('nor', 'nor', 4, 6), ('ron', 'ron', 4, 7), ('rus', 'rus', 4, 8), ('pol', 'pol', 4, 9), ('por', 'por', 5, 0), ('slk', 'slk', 5, 1), ('spa', 'spa', 5, 2), ('srp', 'srp', 5, 3), ('swa', 'swa', 5, 4), ('swe', 'swe', 5, 5), ('tur', 'tur', 5, 6), ('ukr', 'ukr', 5, 7)]

#define different functions
text_file=""
def TextFile():
    global text_file   # Needed to modify global copy of  text_file
    text_file=askopenfilename()
    print(text_file)

mp3_file=""
def mp3File():
    global mp3_file     # Needed to modify global copy of mp3_file
    mp3_file = askopenfilename()
    print(mp3_file)

html_file=""
def htmlFile():
    global html_file     # Needed to modify global copy of html_file
    html_f1=tkinter.filedialog.asksaveasfile(mode='w',defaultextension=".html")
    if html_f1 is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    html_file=html_f1.name
#    text2save=str(text.get(0.0,END))
#    html_f1.write(text2save)
    html_f1.close
    print(html_file)

def about():
    windowAbout.deiconify()

def on_closing():
        windowAbout.withdraw()

def ShowChoice():
    print(lang.get())

def run():
    if text_file == "":
        showerror("TEXT file", "You chose no text file!")
    elif mp3_file == "":
        showerror("MP3 file", "You chose no mp3 file!")
    elif html_file == "":
        showerror("HTML file", "You chose no html file!")
    else:
        print(text_file)    # No need for global declaration to read value of text_file
        print(mp3_file)     # No need for global declaration to read value of mp3_file
        print(html_file)    # No need for global declaration to read value of html file
        newFile = "temp_txt_file.txt"     #temporary txt file
        csv_file = "temp_csv_file.csv"    #temporary csv file


#####
# 1 #
#####

###########################################################
#  Split a file by punctuation and print it in a new file #
###########################################################

#Remove the newline character in the text file and concantenate all the file in one string
#https://stackoverflow.com/questions/4319236/remove-the-newline-character-in-a-list-read-from-a-file

        with open(text_file, 'r') as input:
            lines = input.readlines()

        line_witout_NewLine = []
        for line in range(len(lines)):
            line_witout_NewLine.append(lines[line].strip('\n'))

        witout_new_line = " ".join(line_witout_NewLine)

#Split the file with multiple delimiters, keeping them (,?!,;)
#First add a mark for every delimiter then split the string at the delimiter
#https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
        mark = '@#$%^&'

        if mark in witout_new_line:
            print("Choose another mark!\n")
            exit
        else:
            print("MARK doesn't exists. It's OK.")

        final = witout_new_line.replace('. ','.' + mark).replace('! ','!' + mark).replace('? ','?' + mark).replace('; ',';' + mark).replace(', ',',' + mark).split(mark)

#print the new file 
        with open(newFile, 'w') as output:
            for line in final:
                output.write(line + '\n')
#####
# 2 #
#####

####################
#  create csv file #
####################
        string1 = 'task_language=' + lang.get() + '|os_task_file_format=csv|is_text_type=plain'
        print(string1)
#        subprocess.Popen(['python3', '-m', 'aeneas.tools.execute_task', mp3_file, newFile, 'task_language=eng|os_task_file_format=csv|is_text_type=plain', csv_file]).wait()
        subprocess.Popen(['python3', '-m', 'aeneas.tools.execute_task', mp3_file, newFile, string1, csv_file]).wait()


#####
# 3 #
#####

#create html file


        times_array = []
        transcript_array = []
#line_split = ['1','1','1','1']
        line_split = []
        with open(csv_file, 'r') as f:
            with open(html_file, "w") as f1:
                f1.write(string_1)
                f1.write("var times = [")
                for line in f:
                    line_split = line.split(",")
                    times_array.append(line_split[1])
                    say = line_split[3:]
                    say = ",".join(say)
                    say = say[1:-1]
                    transcript_array.append(str(say))
                    f1.write(line_split[1] + ', ')
                times_array.append(line_split[2])    
                f1.write(line_split[2])
                f1.write("];")
                f1.write("\n")
                f1.write(string_2)
                f1.write(string_3)
                f1.write(mp3_file)
                f1.write(string_4)
                f1.write(string_5)
                for (time, line) in zip(times_array, transcript_array):
                        f1.write('    ' + '<span  onclick="switchColors(this); goToTime(' + time + ');">' + line[:-1] + '</span>')
                        f1.write("\n")
                f1.write(string_6)
        print("DONE!")
        showinfo("DONE", "DONE!")

        
#We initialize Tkinter by crieating a Tk root widget. A root widget is a window with title bar and decoration provided by the window manager; it must be created before any other widgets and is is unique.
root = Tk()
root.title("Forced alignment with aeneas")

#Create a top-level window
#Create a Toplevel widget that is a rectangular region on the screen displayed in a separate top-level window. Such windows usually have title bars, borders, and other window decorations.
windowAbout = Toplevel()
windowAbout.withdraw()   #Hide the windowAbout window
help = "ForcedAlignment\n\nForcedAlignment is a graphical tool to automatically synchronize audio and text.\nIt generates a html file with an audio player and a list.\nFor more information read the README.md file." #define a string
msg = Message(windowAbout, text = help) #Create a message widget
msg.config(bg='lightgreen', font=('times', 24, 'italic'))
msg.pack(expand=True, fill='both')
windowAbout.protocol("WM_DELETE_WINDOW", on_closing)   #if we click the close button "x" function on_close will be executed


#Create the Menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Text File", command=TextFile)
filemenu.add_command(label="MP3 File", command=mp3File)
filemenu.add_command(label="html File", command=htmlFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=filemenu)

runmenu = Menu(menu, tearoff=0)
runmenu.add_command(label="Run", command=run)
menu.add_cascade(label="Run", menu=runmenu)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="About...", command=about)
menu.add_cascade(label="Help", menu=helpmenu)

lang = StringVar()
lang.set("eng")  # initializing the choice, i.e. ENG

Label(root, 
      text="""Choose the spoken language:""",
      justify = CENTER
      ).grid(row = 1, column = 0, columnspan = 10)

for txt, val, r, c in languages:
    Radiobutton(root, 
                text=txt,
                variable=lang, 
                command=ShowChoice,
                value=val).grid(row = r, column = c)

mainloop()
