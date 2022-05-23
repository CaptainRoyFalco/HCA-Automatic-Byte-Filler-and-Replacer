# HCA Automatic Byte Filler and Replacer
This is a GUI program intended to automate the tedious aspects of **Marvel Vs. Capcom: Infinite** voice modding. Here is a link to my [voice mod guide for the game](https://docs.google.com/document/d/1MPjwjBE9sqXvlK4UT_aToQ4cZlcnWK_qAILtVo2ATHE/edit?usp=sharing). If you have any questions about the program, you can contact me on [reddit](https://www.reddit.com/user/Captian_Roy_Falco)
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
*For anyone looking at the .py files, the program was written with Python 2.7.15 in mind as that was what the [old music mod guide](https://docs.google.com/document/d/1Yle_VsMJ9xEuOkC2doPk0BmgHsloMa-B5F4502H_flk/edit?usp=sharing) used to work.*
<br/>
<br/>
<br/>
<br/>
## HCA Automatic Byte Filler and Replacer - Version 1.4 Manual
### Program Window:
#### ADD button
- This button is always enabled. A prompt is given to select either SOURCE or REPLACEMENT. The two choices correspond with their respective HCA File container. After selecting a container, the file explorer appears for you to find and select the .hca files that will be placed in the chosen container.
- The added files will have an index position of the file in the program, the name of the file, and its file size. Ex: “ 2 | 00A_CV – 1 ( x01 ).hca | 5.09 KB ”. The unit of the file size is determined by the Set Byte Unit option in the options menu.
#### DEL button
- This button is enabled while there is a file in one of the HCA File containers. A window appears with a list of files from each section that can be deleted. Pressing the “Delete Selected … File(s)” button of its section will remove the selected files from its container. Pressing “Delete all … Files” will remove every file from its container.
- You select a file by clicking it with your mouse. You can select multiple files by holding the click (Mouse1) and moving your mouse to another file, clicking with the SHIFT key, or clicking single files with the CTRL key on your keyboard.
#### SORT button
- This button is enabled while there are at least two files in either of the HCA file containers. A window appears with a list of files from each section which you can manually sort. Before you can start manually sorting the files, you must input a number in the input field. The number determines which index to move the chosen file(s) to. Once a file is selected, the “Move File(s)” button is enabled. This button will move the selected file(s) to inputted index position and the files will show their new index as a result of the change. To apply your manual sorting to the files, press the ”Apply Changes” button.
- With the “Auto Sort … Files” buttons, every file in the button’s corresponding section will be automatically sorted. The button will only be enabled when every file is not already sorted with its method of natural/human sorting (this same sorting method is used for the “Automatically Sort Added Files?” option).
- You select a file by clicking it with your mouse. You can select multiple files by holding the click (Mouse1) and moving your mouse to another file, clicking with the SHIFT key, or clicking single files with the CTRL key on your keyboard.
#### Scroll buttons
- Source Up/Source Down: Scroll through the files in the Source HCA Files container
- Replace Up/Replace Down: Scroll through the files in the Replacement HCA Files container
- Both Up/Both Down: Scroll through the files in both containers. The amount scrolled by is determined by the “For scrolling with ‘Both’ buttons” setting of the “Change File Scroll Buttons Increment” option in the options menu
- “To File” buttons: Scroll to the first/last index of the button’s corresponding section
	- “To First (S) File”: Go to the first Source file
	- “To First File (R)”: Go to the first Replacement file
	- “To Last (S) File”: Go to the last Source file
	- “To Last File (R)”: Go to the last Replacement file
#### EXTRACT button
-	This button is always enabled. Choose a .uexp file(s) to extract the HCA header offsets from. You can create .hca files from the header offsets, print out the information in the program, or create a .txt file that logs the information.
-	The header offsets to search for and log are determined by the “Audio Start Header Search String” and the “Audio End Header Search String” options in the options menu.
-	The user will be notified if the program cannot find the “Audio Start Header Search String” in the selected .uexp file.
-	If the user selects multiple .uexp files and at least one of them fails to extract, a window will appear displaying the .uexp files that failed and which ones succeeded.
#### COMPARE button
-	This button is only enabled when both HCA File containers have an equal number of files. Compares the files in both the Source HCA Files container and Replacement HCA Files container. Files with the same index have their file sizes compared (1-1, 2-2, 3-3, etc.).
-	Afterwards, the files will have its text and color change based on if the Replacement file has a lower file size than its corresponding Source file of the same index.
-	Fillable Replacement files, denoted with “O”, are files that have a file size that is smaller or equal to its Source counterpart. The default color is green with black text.
-	Non-fillable Replacement files, denoted with “X”, are files that have a file size that is larger than its Source counterpart and cannot be filled. The default color is red with white text.
#### FILL button
-	This button is enabled only after the files are compared and there are replacement files that can be filled. Fills the files in the Replacement HCA Files container with 00 bytes until it matches its Source counterpart (matched by the file’s index position).
-	After pressing the button, a prompt is given for the user to select a file directory to place the filled replacement files. If the user chooses to keep the replacement files in the same directory, then those files will not move and just have its file size match its source counterpart. After the fillable replacement files are filled with 00 bytes, the files are moved to the chosen directory and the replacement file along with its source file counterpart are removed from both HCA File containers.
-	Any Replacement files that are non-fillable (its file size is larger than its source counterpart) will not move to the “Filled files” directory and will not be removed from the HCA File containers.
#### REPLACE button
-	This button is always enabled. Takes the selected .uexp file by the user and the selected .hca files to replace the HCA header offsets data with the data from your selected .hca files.
-	The header offsets to search for and to replace its data are determined by the “Audio Start Header Search String” and the “Audio End Header Search String” options in the options menu.
-	If the “Automatically Replace the .uexp File(s)?” option is checked, the program will automatically use the numbers in the file name of your chosen .hca files and replace the data in that header’s offset. The numbers in the file name must be at the start of the file and be separated by a space in the following way: 

	-	“(number) (file name).(file extension)” 
	-	Ex: “01 Ryu LP 3.hca” – “(01) (Ryu LP 3).(hca)”
		- The “01” is the only thing that will be read as the program will ignore every character after the space.
		- Doing: “01Ryu LP 3” will cause the program to read “01Ryu” and skip over that file.
-	If the numbers in the file name causes an error or the corresponding header offset’s data size is lower than the .hca file’s file size, then a window will appear notifying you the files that failed to replace and the reason for its failure.
-	If the option is unchecked, you will be given a prompt to manually input the offset of the HCA Header in the input field. The prompt will present you the name of the file and how many files you have left to replace. If the header offset data is smaller than your .hca file size, then the prompt will notify you that your file is larger than the header offset data in the .uexp file. You will have the option to try again and use a different number or the skip that chosen file and move on to the next one (or finish in the case of it being the file).
<br/>
<br/>

### Edit Menu:
#### Options - General tab
-	**Automatically Sort Added Files?**
	-	If the option is checked, any files that are added to a HCA File container will be sorted with natural/human sorting. If unchecked, any files added will be added in the order that they were selected in the file explorer.
		-	Default: Checked
-	**Set Byte Unit:**
	-	Sets the unit of bytes that will be displayed for the file size of the files. The selectable units are Bytes, KB (Kilobytes), MB (Megabytes), GB (Gigabytes), and TB (Terabytes).
		-	Default: KB (Kilobytes)
-	**File Size Decimal Position to Round to:**
	-	Determines the decimal position to round the file size of the files. An input field will appear where the user can choose the decimal position to round to. The user can also choose to have no rounding. If the Byte Unit is Bytes, this option will not apply (as bytes are whole numbers).
		-	Default: Two decimal places (1.00)
-	**Change File Scroll Buttons Increment:**
	-	Changes the number of files that the Source Up/Down or Replace Up/Down buttons scroll by. You can change the increment for each section separately or change both. Ex: You can have the Source section scroll by 5 files and the Replacement section scroll by 3 files in its container.
	-	There are also the options on how the “Both” scroll buttons will operate. “Use the lower of the Two” will use the lower increment of the two sections. Following the previous example, when pressing the “Both Up” or “Both Down” scroll buttons, the files will be scrolled by 3. “Use the higher of the Two” will use the higher increment of the two sections (i.e., it will scroll by 5). “Use Each Section’s Respective Value” will be like pressing the Source Scroll button and the Replacement Scroll button at the same time (the Source section will scroll by 3 and the Replacement section will scroll by 5).
		-	Default: Both Sections: 10
-	**Set Number Base:**
	-	Sets the used number base to be Hexadecimal (Base 16), Decimal (Base 10), or Octal (Base 8).
	-	Effects the numbers used when Extracting and when Replacing. The Extraction Logs will have the header offsets and file size in the selected number base. When Replacing files (automatically or manually), the program will expect a number in the file name/number in the input field that matches the number base. Ex: Trying to input 0A when the number base is in Decimal or Octal will not work.
	-	The number 30 in decimal is 1E in hexadecimal and 36 in octal. It is important to understand and keep in mind which number base you are using.
		-	Default: Hexadecimal (Base 16)
-	**Automatically Replace the .uexp File(s)?**
	-	If checked, instead of manually having to input the Header offsets in the input field of the Replace .uexp window, you can put the header offsets you wish to change in the file name itself.
		-	Default: Unchecked
-	**Change Audio Start Header Search String:**
	-	You can change the Audio Start Header Search String to a different sequence of a byte characters. This string is used to search for the similar byte string in the .uexp file that is being Extracted or Replaced.
		-	Default: HCA\x00\x02 -> \x48\x43\x41\x00\x02
-	**Change Audio End Header Search String:**
	-	Like the “Change Audio Start Header Search String:” option. This string is used to search for the header offset that signifies the end of the audio data in the .uexp file
	-	You can choose to not search for the Audio End Header Search String by unchecking the option (which will disable the buttons and input field of the window). When the option is unchecked, the last header offset will be considered the end of the file.
		-	Default: @UTF\x00\x00 -> \x40\x55\x54\x46\x00\x00
### Options - Color tab
-	Select a button’s color option and change its color. Pressing “RGB” will change the color codes of each button’s color to “HEX” and vice-versa. Ex: (255, 0, 255) -> #FF00FF
-	For the “Both/To File buttons use the same color” options: 
	-	Having it checked will have those button options use the same color as the leftmost color option.
	-	Having it unchecked will have those buttons use their own color. 
	-	Whether it is checked or not, those buttons will still save their individual color options.
-	Preset Color buttons: There are three buttons (Preset 1-3). Hovering your mouse over the Preset buttons iterates through each of the color options. You can choose to overwrite the preset colors with the current color options or use the saved preset colors for each of the color options. If there are no saved preset colors, the color options will be saved automatically.
### Go To…
-	This option is enabled once there are more than two files in one of the HCA File Containers. Upon clicking it, a window appears with an input field, where you can go to the index you inputted number. If the index is larger than the amount of files, then it will go to the last file in the chosen container.
<br/>
<br/>

### Extras Menu:
#### Switch Placement of HCA File Containers
-	Switch the Source file container with the Replacement file container. The source and replacement scroll buttons will switch sides. Any files in the container will stay in its respective section.
#### Switch Placement of "Up" and "Down" Scroll Buttons
-	Invert the positions of the “Up” scroll buttons with the “Down” scroll buttons.
#### Create A New "config.ini" File
-	Creates a default config.ini file so you don’t have to delete the current config.ini file to make a new one.
#### About
-	Information about the program: The program version, the program's file directory, the link to the program’s GitHub page, and the creator’s contact info.
<br/>
If you any questions, contact me, the creator, at the link below:<br/>
https://www.reddit.com/user/Captian_Roy_Falco
<br/>
<br/>
<br/>
*For anyone looking at the .py files, the program was written with Python 2.7.15 in mind as that was what the [old music mod guide](https://docs.google.com/document/d/1Yle_VsMJ9xEuOkC2doPk0BmgHsloMa-B5F4502H_flk/edit?usp=sharing) used to work.*
<br/>
