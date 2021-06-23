# HCA-Automatic-Byte-Filler-and-Replacer
This is a GUI program intended for Marvel Vs. Capcom: Infinite voice modding.
<br/>
<br/>
After extracting .hca files from a character's .uexp file using an exteranl program, this program uses those "Source" files along with the user's own .hca "Replacement" files to make voice modding easier.
<br/>
<br/>
The 3 main functions of the program are: comparing the "Source" and "Replacement" file sizes and visually displaying what "Replacement" files can be filled and which ones cannot, automatically filling 00 bytes in the user's "Replacement" .hca files until they are the same file size as the "source" files, and automatically replacing the HCA code blocks in a character's .uexp file with the data in a .hca file.
<br/>
<br/>
<br/>
Here is some notes on some of the options in the Options Menu.
<br/>
<br/>
**Change Source Color**
<br/>
Change the color of the Source section.
<br/>
<br/>
**Change Replace Color**
<br/>
Change the color of the Replacement section.
<br/>
<br/>
**Set Byte Unit**
<br/>
Change the unit that the labels will display. 0 is for Bytes, 1 is for Kilobytes, 2 is for Megabytes, 3 is for Gigabytes, and 4 is for Terabytes.
<br/>
<br/>
**Decimal Position to Round to:**
<br/>
Change the decimal place that the label will round to. Input a negative number to have no rounding at all. If the rounded decimal place would make a number equal to 0, then the label will the display the rounded number in scientific notation.
<br/>
<br/>
**Set Number Base**
<br/>
Change the number base that the program will read in. 1 is for Hexadecimal, 2 is for Decimal, and 3 is for Octal. For example, with Set Number Base as 2 and "Automatically Sort Files"  is checked, the program will sort the given files based on the decimal base.
<br/>
<br/>
Hexadecimal (Base 16):

    0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  A,  B,  C,  D,  E,  F
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 1A, 1B, 1C, 1D, 1E, 1F
    20, 21 ...
<br/>
Decimal (Base 10):

    0,  1,  2,  3,  4,  5,  6,  7,  8,  9
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
    20, 21, 22, ...
<br/>
Octal (Base 8):

    0, 1, 2, 3, 4, 5, 6, 7
    10, 11, 12, 13, 14, 15, 16, 17
    20, 21 ...
<br/>

**Read the first 3 characters in a file name?**
<br/>
If checked, the program will try to read a number from the first 3 characters of a file name and use the number it found to automatically determine where the .hca file goes to which HCA header in a .uexp file.
If unchecked, the user will have to manually input the number offset that corresponds to the HCA header in a .uexp file.
The number read/given is based on what the number base is. If Set Number Base is 3, for example, then the program will only octal numbers it reads from a file name or is given.
<br/>
<br/>
**Automatically Sort Added Files?**
<br/>
If checked, the program will try to sort multiple added files based on the numbers found in its file name. For the chosen Source files, the program will try to read for a number at the end of the filename first and, if it can't find one, it then tries to read a number at the front. For Replacement files, the program will only try to read for a number at the start of the file. Based on the number obtained, the program will then sort the files accordingly. If there is an error that occurs (like finding a hex number when it's trying to read for decimal numbers), then the files will most likey not sort properly.
The number read is based on what the number base is.
If unchecked, then the program will add multiple files based on how they were selected in the file explorer.
<br/>
<br/>
**Change Search String**
<br/>
Change the hex string that the program will search for when reading a .uexp file. The default hex string finds the HCA headers in a .uexp file while not including HCA code strings that are not apart of the header.
<br/>
<br/>
**Use Debug Mode?**
<br/>
If checked, windows pop up when Replacing the .uexp HCA headers with your .hca files. The first pop-up shows the HCA headers that the program found. This might help you understand why your voice mod isn't working properly (like if you accidently overwritten a HCA header, which makes voice lines not come out properly). If "Read the first 3 characters in a file name?" is checked, then a second pop-up will appear. This pop-up lets you know what the program read the number in the file names as.
<br/>
<br/>
<br/>
<br/>
*The program was written with Python 2.7.15 in mind as that was the old music mod guide used.*
<br/>
