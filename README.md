# HCA-Automatic-Byte-Filler-and-Replacer
This is a GUI program intended for Marvel Vs. Capcom: Infinite voice modding.

After extracting .hca files from a character's .uexp file using an exteranl program, this program uses those "source" files along with the user's own .hca "replacement" files to make voice modding easier. 
The 3 main functions of the program are: comparing the "source" and "replacement" file sizes and visually displaying what "replacement" files can be filled and which ones cannot, automatically filling 00 bytes in the user's "replacement" .hca files until they are the same file size as the "source" files, and automatically replacing the HCA code blocks in a character's .uexp file with the data in a .hca file.
