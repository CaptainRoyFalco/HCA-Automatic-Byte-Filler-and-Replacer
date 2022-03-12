# HCA-Automatic-Byte-Filler-and-Replacer
This is a GUI program intended for Marvel Vs. Capcom: Infinite voice modding.
<br/>
<br/>
<br/>
After extracting .hca files from a character's .uexp file, this program uses those "Source" files along with the user's own .hca "Replacement" files to make voice modding easier.
<br/>
<br/>
The 3 main functions of the program are: **Comparing**, **Filling**, and **Replacing**.
<br/>
<br/>
The first function **Compares** the Source and Replacement files' file size and visually displays if the Replacement file is smaller than or equal to its corresponding Source file counterpart or is larger than it.
<br/>
<br/>
The second function takes the compared files and uses the Replacement files that have a file size less than or equal to its Source file counterpart. Those files are then automatically **Filled** with 00 bytes until it is the same file size as its counterpart.
<br/>
<br/>
The third function **Replaces** the audio data in a .uexp file with the user's own audio data from their .hca file(s). The user can choose to replace automatically or manually.
<br/>
<br/>
<br/>
A new function of Version 1.4 is the ability to **Extract** the audio data of a .uexp file and use it to create .hca files and/or log the information to the user.
<br/>
<br/>
<br/>
*For anyone looking at the .py files, the program was written with Python 2.7.15 in mind as that was the old music mod guide used.*
<br/>
