# HCA-Automatic-Byte-Filler-and-Replacer
This is a GUI program intended for Marvel Vs. Capcom: Infinite voice modding.

After extracting .hca files from a character's .uexp file using an exteranl program, this program uses those "source" files along with the user's own .hca "replacement" files to make voice modding easier.

The 3 main functions of the program are: comparing the "source" and "replacement" file sizes and visually displaying what "replacement" files can be filled and which ones cannot, automatically filling 00 bytes in the user's "replacement" .hca files until they are the same file size as the "source" files, and automatically replacing the HCA code blocks in a character's .uexp file with the data in a .hca file.



Here is some notes on some of the options in the options menu.




**Automatically Sort Added Files?**

In the option menu, there is an option labeled "Automatically Sort Added Files?" By default it is checked. To work properly, this option requires a hexadecimal, decimal, or octal number in the filename (that of which is based on the "Set Number Base" option). For the chosen Source files, the program will try to read for a number at the end of the filename first and, if it can't find one, it then tries to read a number at the front. For Replacement files, the program will only try to read for a number at the start of the file. Based on the number obtained, the program will then sort the files accordingly. If there is an error that occurs (like finding a hex number when it's trying to read for decimal numbers), then the files will most likey not sort properly.
