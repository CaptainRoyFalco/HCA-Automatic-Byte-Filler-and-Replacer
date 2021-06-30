import os
import sys
import re
import shutil
from decimal import *

from Tkinter import *
import ttk
import tkFileDialog
import tkColorChooser #https://stackoverflow.com/questions/18903911/tkinter-color-chooser-window-focus

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.ini')

#---------------------------------------------------------------------------------------------------------------------------------------------------#

config_general_section = 'General'
#Checks a config file for any saved directories, so the user does not have to find the previously used directory multiple times.
def CheckForSavedDirectory(config_general_option):
    directory = ''
    try:
        if os.path.exists(config.get(config_general_section, config_general_option)) == True:
            directory = config.get(config_general_section, config_general_option)
        else:
            text_display_string.set('File path does not/no longer exists.')
    except:
        text_display_string.set('An error occured while checking for a saved directory. Does "config.ini" not exist?')
    return directory
    
    
#Returns a list of the file(s) or the directory the user selected.
def PickedFiles(chosen_directory, special_condition):
    if special_condition == True:
    	chosen_files = tkFileDialog.askdirectory(initialdir=chosen_directory, title='Select a folder to store the finished files')
    elif special_condition == 'UEXP':
    	chosen_files = tkFileDialog.askopenfilename(initialdir=chosen_directory, title="Select a .uexp file", filetypes=(("UEXP File", "*.uexp"), ("All Files", "*.*")))
    else:
    	chosen_files = sorted( tkFileDialog.askopenfilenames(initialdir=chosen_directory, title='Select the .hca file(s)', filetypes=(('HCA File', '*.hca'), ('All Files', '*.*'))) )	
    return chosen_files


#Overwrites the previously saved directory if the user selected the last file from a different directory.
def OverwriteDirectoryData(config_general_option, para_directory):
    try:
        if config_general_option == 'finished_hca_directory':
            directory =	os.path.join(os.path.dirname(para_directory), os.path.basename(para_directory))
        else:
            directory = os.path.dirname(para_directory)
        
        if directory != config.get(config_general_section, config_general_option):
            config.set(config_general_section, config_general_option, directory)
            with open('config.ini', 'w') as outfile:
                config.write(outfile)
    except:
        text_display_string.set('An error occured while trying to overwrite saved directory data in "config.ini"')
    pass


#Sets the Root Window to be set at the middle of the computer screen.
def RootWindowCenterPositioner():
    x = root_window.winfo_x()
    y = root_window.winfo_y()
    w = root_window.winfo_screenwidth()             #Get the width and height of the screen
    h = root_window.winfo_screenheight()
    halved_witdh = (w/2)                            #Halve the width and height to get the (0,0) of the root window to be in the middle of the screen
    halved_height = (h/2)
    quarter_width = (halved_witdh/2)                #Halve the width and height again (to center the root window when subtracting in the next step)
    quarter_height = (halved_height/2)
    rx = halved_witdh - quarter_width               #Subract the upper corner position of the root window from the halved position to center the window
    ry = halved_height - quarter_height
    #https://stackoverflow.com/questions/36050192/how-to-position-toplevel-widget-relative-to-root-window
    root_window.geometry('+%d+%d' % (x + rx, y + ry)) 


#Sets a TopLevel Window to be set in the middle of root window. Used in the following functions (def): OptionsWindow()
def WindowCenterPositioner(window): 
    window.update_idletasks()                            #Allows for the correct width and height of the toplevel window to be obtained. Without this line, the width and height are set to 1.

    x = root_window.winfo_x()
    y = root_window.winfo_y()
    w = root_window.winfo_width()                        #Get the width and height of the root window
    h = root_window.winfo_height()
    halved_witdh = (w/2)                                 #Halve the width and height to get the (0,0) of the toplevel window to be in the middle of the root window
    halved_height = (h/2)
    window_half_width = (window.winfo_width() / 2)       #Get and halve the width and height of the toplevel window
    window_half_height = (window.winfo_height() / 2)
    rx = halved_witdh - window_half_width                #Subract the upper corner position of the toplevel window from the half its width and height to anchor the window at its center
    ry = halved_height - window_half_height

    window.geometry('+%d+%d' % (x + rx, y + ry))
    window.lift()                                       #Raise the toplevel window to appear above the root window
    window.grab_set()                                   #Makes it so the user cannot use the root window unless they close the toplevel window


config_options_section = 'Options'
#Converts bytes from a file's file size to be KB, MB, GB, or TB. If the conversion variable is equal to 0, then scientific notation is used.
def ByteOperation(byte_size):
    set_byte_conversion = int(config.get(config_options_section, 'set_byte_conversion'))
    round_to_decimal_position = int(config.get(config_options_section, 'round_to_decimal_position'))

    if set_byte_conversion == 1: #KB
        conversion = Decimal(byte_size) / Decimal(1024)
        unit_string = 'KB'
    elif set_byte_conversion == 2: #MB
        conversion = Decimal(byte_size) / Decimal(1024**2)
        unit_string = 'MB'
    elif set_byte_conversion == 3: #GB
        conversion = Decimal(byte_size) / Decimal(1024**3)
        unit_string = 'GB'
    elif set_byte_conversion == 4: #TB
        conversion = Decimal(byte_size) / Decimal(1024**4)
        unit_string = 'TB'
    else: #Bytes
        conversion = byte_size
        unit_string = ' Bytes'

    if round_to_decimal_position < 0:
        no_rounding = '{0}{1}'.format(conversion, unit_string)
        return no_rounding

    rounded_number = '{:.{}f}'.format(conversion, round_to_decimal_position)   #jurajib's comment - https://stackoverflow.com/questions/6149006/display-a-float-with-two-decimal-places-in-python

    if Decimal(rounded_number) == 0 and conversion != 0:
        #Sceintific Notation
        sceintific_notation = '{:.{}e} '.format(conversion, round_to_decimal_position) #https://www.kite.com/python/answers/how-to-print-a-number-in-scientific-notation-in-python
        rounded_number = sceintific_notation

    result = '{0}{1}'.format(rounded_number, unit_string)
    return result


label_source_list = []
label_replacement_list = []
displayed_source_files = []
displayed_replacement_files = []
#Creates a new label for each file that was selected by the user. Any files that the user picks which already have a label will update their information. Labels contain the index position of the file, the name of the file, as well as its file size.
def CreateNewLabel(list_to_check, id_number):
    if id_number == 0: #Source Section
        temp_display = displayed_source_files
        temp_label_list = label_source_list
        location = source_container
        color = config.get(config_options_section, 'source_color')
    elif id_number == 1: #Replacement Section
        temp_display = displayed_replacement_files
        temp_label_list = label_replacement_list
        location = replace_container
        color = config.get(config_options_section, 'replace_color')

    item_in_label_list = 0
    stop = False
    for element in list_to_check:
        if element in temp_display: #This updates the file sizes and makes sure duplicate labels aren't created (and at the same time deleted immediately within the UpdateLabels() function)
            pass
        else:
            temp_label_list.append(Label(location, bg=color, anchor='w', wraplength=322, justify="right", padx=4, pady = 3, relief=RAISED, width=40, text='{2} | {0} | {1}'.format(os.path.basename(element), ByteOperation(os.path.getsize(element)), (item_in_label_list + 1) ), font='Helvetica 10'))

        item_in_label_list += 1

        if item_in_label_list >= 30: #This makes sure that any labels that can't be seen (at full screen) won't be created.
            break

    #Displaying files to screen
    for label in temp_label_list:
        label.pack()

    fill_button.config(state=DISABLED, bg='gray')


#Sorts added files by the base number set in the options menu.
def BaseNumberSort(list_element): #https://www.programiz.com/python-programming/methods/built-in/sorted
    element_name = os.path.basename(list_element)
    string_number_in_filemane = element_name.partition(' ')[0]
    base_number = int(config.get(config_options_section, 'number_base'))

    global remove_duplicate_id_number
    global filename_number_error
    if remove_duplicate_id_number == 0:
        end_string_number = element_name[0:-4].rpartition('_')[-1] #https://mylyfmycode.wordpress.com/2018/08/15/split-v-s-rsplit-partition-v-s-rpartition/#:~:text=But%20what%20is%20partiton()%3F,delimiter%2C%20and%20the%20right%20part.
        try:
            if base_number == 1: #Hex
                number_in_element_name = int(end_string_number, 16)
            elif base_number == 2: #Dec
                number_in_element_name = int(end_string_number)
            elif base_number == 3: #Oct
                number_in_element_name = int(end_string_number, 8)
        except:
            text_display_string.set('Sorting based on the first 3 characters in file name.')
            try:
                if base_number == 1: #Hex
                    number_in_element_name = int(string_number_in_filemane, 16)
                elif base_number == 2: #Dec
                    number_in_element_name = int(string_number_in_filemane)
                elif base_number == 3: #Oct
                    number_in_element_name = int(string_number_in_filemane, 8)
            except ValueError:
                filename_number_error = True
                text_display_string.set('Invalid value ( {0} ) obtained from filename {1}. Set Base Number = {2}'.format(string_number_in_filemane, element_name, base_number))
                return

    elif remove_duplicate_id_number == 1:
        try:
            if base_number == 1: #Hex
                number_in_element_name = int(string_number_in_filemane, 16)
            elif base_number == 2: #Dec
                number_in_element_name = int(string_number_in_filemane)
            elif base_number == 3: #Oct
                number_in_element_name = int(string_number_in_filemane, 8)
        except ValueError:
            filename_number_error = True
            text_display_string.set('Invalid value ( {0} ) obtained from filename {1}. Set Base Number = {2}'.format(string_number_in_filemane, element_name, base_number))
            return
    return number_in_element_name


#Removes duplicate files in a list and (if set) automatically sorts the files.
def RemoveDuplicates(checked_list, id_number):
    temp_list = list(set(checked_list))
    automatically_sort_files = config.get(config_options_section, 'automatically_sort_files')
    if automatically_sort_files == True:
        global remove_duplicate_id_number
        remove_duplicate_id_number = id_number
        returned_list = sorted(temp_list, key=BaseNumberSort)

        global filename_number_error
        filename_number_error = False
        if filename_number_error == True:
            text_display_string.set('An error occured while sorting the files. The files may not be sorted properly.')
    else: 
        returned_list = temp_list
    return returned_list


#Finds the correct directory for the files and calls a function to add any selected files.
def ChosenFileSection(directory_type, label_number):
    selected_files = PickedFiles(CheckForSavedDirectory(directory_type), False)
    if len(selected_files) == 0:
        return

    CreateNewLabel(selected_files, label_number)

    global source_move_position #https://www.programiz.com/python-programming/global-keyword
    global replace_move_position
    if label_number == 0:
        global displayed_source_files
        for i in selected_files:
            displayed_source_files.append(i)

        displayed_source_files = RemoveDuplicates(displayed_source_files, label_number) #If I do stored_source_files = displayed_source_files, then stored_source_files is tied to displayed_source_files. What I do to one list, happens to the other. So, I have to make it a new list.
        move_position = source_move_position
        alt_position = replace_move_position
        alt_id = 1
    elif label_number == 1:
        global displayed_replacement_files
        for i in selected_files:
            displayed_replacement_files.append(i)

        displayed_replacement_files = RemoveDuplicates(displayed_replacement_files, label_number)
        move_position = replace_move_position
        alt_position = source_move_position
        alt_id = 0

    global comparing_labels_on
    if comparing_labels_on == True:
        UpdateLabels(alt_position, alt_id)

    #To make sure added items appear in the correct position
    UpdateLabels(move_position, label_number)

    OverwriteDirectoryData(directory_type, selected_files[-1])
    RemoveCheck()


#Creates a window where the user chooses which section they want to add files to.
def ConfirmFileSection():
    confirm_box = Toplevel()
    confirm_box.geometry('300x75')
    confirm_box.resizable(width=False, height=False)
    WindowCenterPositioner(confirm_box)

    source_color = config.get(config_options_section, 'source_color')
    confirm_source = Button(confirm_box, text='SOURCE', font='Helvetica 12', command=lambda:[confirm_box.destroy(), ChosenFileSection(directory_type=source_dir, label_number=0)], bg=source_color)
    confirm_source.pack(side='left', fill='both', expand='yes')

    replace_color = config.get(config_options_section, 'replace_color')
    confirm_replace = Button(confirm_box, text='REPLACE', font='Helvetica 12', command=lambda:[confirm_box.destroy(), ChosenFileSection(directory_type=replace_dir, label_number=1)], bg=replace_color)
    confirm_replace.pack(side='right', fill='both', expand='yes')

    confirm_cancel = Button(confirm_box, text='CANCEL', font='Helvetica 12', command=confirm_box.destroy, bg='gray')
    confirm_cancel.pack(side='left', fill='both', expand='yes')


#Gets a directory chosen by the user where the filled replacement files will be and calls a function that fills the replacement files.
def FinishedDirectory():
    finished_hca_files = PickedFiles(CheckForSavedDirectory(finished_dir), True)
    if not finished_hca_files: #If no directory was chosen
        text_box_string = 'Canceled. File location not chosen.'
    else:
        OverwriteDirectoryData(finished_dir, finished_hca_files)
        FillingFiles(finished_hca_files)
        text_box_string = 'Replacement files are filled!'

    text_display_string.set(text_box_string)


#Fills good to go replacement files with "\x00" bytes to match its corresponding Source File file size and moves all filled files to the "finished" directory. Replacement files that are larger than their source counterpart do not get filled nor moved.
def FillingFiles(parameter):
    finished_hca_files = parameter
    index = 0
    while index < len(displayed_source_files):
        source_size = os.path.getsize(displayed_source_files[index])
        replace_size = os.path.getsize(displayed_replacement_files[index])
        if replace_size == source_size:
            pass
        elif replace_size <= source_size:
            #Fill Bytes
            with open (displayed_source_files[index], 'rb') as source_file, open (displayed_replacement_files[index], 'ab+') as replace_file:
                source_file.seek(0,2) #Seeks the end of the file
                end_of_source = source_file.tell()
                replace_file.seek(0,2)
                end_of_replace = replace_file.tell()
                while end_of_replace < end_of_source:
                    replace_file.write('\x00')
                    end_of_replace = replace_file.tell()
        else:
            index += 1
            continue

        #Moves filled files to the "finished" directory
        move_to = os.path.abspath( os.path.join(finished_hca_files, os.path.basename(displayed_replacement_files[index])) )
        shutil.move(os.path.abspath(displayed_replacement_files[index]), move_to)

        #Filled files are then removed from the lists
        displayed_source_files.pop(index)
        displayed_replacement_files.pop(index)

    global comparing_labels_on
    comparing_labels_on = False
    UpdateLabels(source_move_position, 0)
    UpdateLabels(replace_move_position, 1)

    if len(displayed_source_files) == 0 and len(displayed_replacement_files) == 0:
        fill_button.config(state=DISABLED, bg='gray')
    pass


#Compares the file sizes between the two sections. If the replacement file size is good to go, then both files at the same index are colored green. If not, they are colored red.
def ComparingFiles():
    global comparing_labels_on
    comparing_labels_on = False
    #Does some checks before the program compares the files. If something is wrong, this lets the user know.
    if len(displayed_source_files) != len(displayed_replacement_files):
        text_box_string = "You didn't choose an equal amount of files! - Source: {0} | Replace: {1}".format(len(displayed_source_files), len(displayed_replacement_files))
    elif len(displayed_source_files) == 0 and len(displayed_replacement_files) == 0:
        text_box_string = 'There are no files to compare'
    else:
        comparing_labels_on = True
        file_index=0
        fillable_files=0
        
        while file_index < len(displayed_source_files):
            sfile = os.path.getsize(displayed_source_files[file_index])
            rfile = os.path.getsize(displayed_replacement_files[file_index])

            #These if and elses are to make sure an error does not occur if the user compares the files when the label lists are less than the displayed files lists ( Ex: len(label_source_list) < len(displayed_source_files) )
            if file_index >= len(label_source_list):
                pass
            else:
                source_element = label_source_list[file_index]
            if file_index >= len(label_replacement_list):
                pass
            else:
                replace_element = label_replacement_list[file_index]
    
            if rfile <= sfile:
                source_element.config(bg='green', text='OK | {2} | {0} | {1}'.format(os.path.basename(displayed_source_files[file_index]), ByteOperation(sfile), (file_index + 1) ))
                replace_element.config(bg='green', text='OK | {2} | {0} | {1}'.format(os.path.basename(displayed_replacement_files[file_index]), ByteOperation(rfile), (file_index + 1) ))
                fillable_files += 1
            elif rfile > sfile:
                source_element.config(bg='red', text='NOPE | {2} | {0} | {1}'.format(os.path.basename(displayed_source_files[file_index]), ByteOperation(sfile), (file_index + 1)) )
                replace_element.config(bg='red', text='NOPE | {2} | {0} | {1}'.format(os.path.basename(displayed_replacement_files[file_index]), ByteOperation(rfile), (file_index + 1) ))
            file_index+=1
        
        if fillable_files > 0:
            if fillable_files == len(displayed_source_files):
                message = 'All files are ready to be filled!'
            else:
                message = '{0} out of the {1} files are ready to be filled!'.format(fillable_files, len(displayed_source_files))
            fill_button.config(state=NORMAL, bg='green', activebackground='yellow')
            text_box_string =  message
        else:
            fill_button.config(state=DISABLED, bg='gray')
            text_box_string = 'All {0} replacement files are bigger than their source counterpart!'.format(len(displayed_source_files))
    
    text_display_string.set(text_box_string)


#Deletes all the labels in the chosen section and removes them from the appopriate list.
def DeleteAllLabels(id):
    if id == 0:
        global label_source_list
        global source_move_position

        #Destroy every label and remove their data from the list
        while len(label_source_list) > 0:
            label_source_list[-1].destroy()
            label_source_list.pop(-1)
        source_move_position = 0
        down_arrow = source_down_arrow_button
    elif id==1:
        global label_replacement_list
        global replace_move_position

        while len(label_replacement_list) > 0:
            label_replacement_list[-1].destroy()
            label_replacement_list.pop(-1)
        replace_move_position = 0
        down_arrow = replace_down_arrow_button

    down_arrow.config(state = DISABLED, bg = 'gray')
    down_arrow_color_update = False


#Deletes files in each section's respective list and updates/deletes the labels accordingly.
def DeleteFunction(listbox_section):
    temp_display = []

    if listbox_section == source_listbox:
        selection_to_delete = source_listbox.curselection()
        global displayed_source_files
        global source_move_position

        temp_display = displayed_source_files
        section_id = 0
        other_section_id = 1
        listbox_to_delete_from = source_listbox
        move_pos = source_move_position
    elif listbox_section == replace_listbox:
        selection_to_delete = replace_listbox.curselection()
        global displayed_replacement_files
        global replace_move_position

        temp_display = displayed_replacement_files
        section_id = 1
        other_section_id = 0
        listbox_to_delete_from = replace_listbox
        move_pos = replace_move_position

    #If no files were chosen to be deleted
    if not selection_to_delete:
        return

    number_of_files_deleted = 0
    for item in reversed(selection_to_delete):
        i=0
        while i < len(temp_display):
            if (i == int(item)):
                temp_display.pop(i)
                number_of_files_deleted +=1
                break
            i+=1

    for item in reversed(selection_to_delete):
    	listbox_to_delete_from.delete(item)

    other_pos = move_pos #This is so the other section's label positioning does not get altered when the files are currently being compared.
    #If the down arrow button is disabled
    if down_arrow_color_update == False:
        move_pos = (move_pos - number_of_files_deleted) #This makes the label position match with the single label displayed

    if len(temp_display) > 0:
        global comparing_labels_on
        if comparing_labels_on == True:
            comparing_labels_on = False
            UpdateLabels(other_pos, other_section_id)
        UpdateLabels(move_pos, section_id) #This deletes excess labels and updates the labels that remain.
        if section_id == 0:
            source_move_position = move_pos
        elif section_id == 1:
            replace_move_position = move_pos
    else:
        DeleteAllLabels(section_id)

    #if the user deleted the files from both sections, remove the window.
    if not displayed_source_files and not displayed_replacement_files:
        global remove_box
        remove_box.destroy()	
    fill_button.config(state=DISABLED, bg='gray')
    RemoveCheck()

    
#Creates a window containing listboxes for each section where the user can choose which files to delete.
def RemoveSelection():
    global remove_box
    remove_box = Toplevel()
    remove_box.geometry('400x400')
    WindowCenterPositioner(remove_box)
    
    list_box_canvas = Canvas(remove_box)
    list_box_canvas.pack(fill='both', expand='yes')

    remove_buttons_frame = Frame(remove_box)
    remove_buttons_frame.pack(side='bottom',fill='both', expand='yes')

    if len(displayed_source_files) != 0:
        source_color = config.get(config_options_section, 'source_color')
        source_frame = Frame(list_box_canvas)
        source_frame.pack(side='left',fill='both', expand='yes')

        global source_listbox
        source_listbox = Listbox(source_frame, bg=source_color, selectmode=EXTENDED, font='Helvetica 9')
        for item in displayed_source_files:
        	source_listbox.insert(END,'{0} | {1}'.format(os.path.basename(item), ByteOperation(os.path.getsize(item)) ))
        source_listbox.pack(side='left',fill='both', expand='yes')

        source_scrollbar = ttk.Scrollbar(source_listbox)
        source_scrollbar.pack(side=RIGHT, fill=Y)
        source_listbox.config(yscrollcommand = source_scrollbar.set)
        source_scrollbar.config(command=source_listbox.yview)
        source_delete_button = Button(remove_buttons_frame, command=lambda:DeleteFunction(source_listbox), bg=source_color, text='Select A Source Item To Remove', font='Helvetica 9')
        source_delete_button.pack(side='left',fill='both', expand='yes')

    if len(displayed_replacement_files) != 0:
        replace_color = config.get(config_options_section, 'replace_color')
        remove_frame = Frame(list_box_canvas)
        remove_frame.pack(side='right',fill='both', expand='yes')

        global replace_listbox
        replace_listbox = Listbox(remove_frame, bg=replace_color, selectmode=EXTENDED, font='Helvetica 9')
        for item in displayed_replacement_files:
            replace_listbox.insert(END,'{0} | {1}'.format(os.path.basename(item), ByteOperation(os.path.getsize(item)) ))
        replace_listbox.pack(side='right',fill='both', expand='yes')

        replace_scrollbar = ttk.Scrollbar(replace_listbox)
        replace_scrollbar.pack(side=RIGHT, fill=Y)
        replace_listbox.config(yscrollcommand=replace_scrollbar.set)
        replace_scrollbar.config(command=replace_listbox.yview)
        replace_delete_button = Button(remove_buttons_frame,command=lambda:DeleteFunction(replace_listbox), bg=replace_color, text='Select A Replace Item To Remove', font='Helvetica 9')
        replace_delete_button.pack(side='right',fill='both', expand='yes')
    
    remove_box.mainloop()
  
    
#Checks to see if the remove button can be clicked or not.
def RemoveCheck():
	if len(displayed_source_files) != 0 or len(displayed_replacement_files) != 0:
		remove_button.config(bg='orange', activebackground='purple', state=NORMAL)
	else:
		remove_button.config(bg='gray', state=DISABLED)


comparing_labels_on = False
#Updates all label information. The "offset" parameter offsets the index that the label will display the files from.
def UpdateLabels(offset, id_number):
    global source_move_position
    global replace_move_position
    if id_number == 0: #Source Section
        if len(displayed_source_files) == 0:
            DeleteAllLabels(id_number)
            return
        section_label_list = label_source_list
        section_displayed_files = displayed_source_files
        container = source_container
        color = config.get(config_options_section, 'source_color')
        down_arrow = source_down_arrow_button
        section = source_move_position
    elif id_number == 1: #Replacement Section
        if len(displayed_replacement_files) == 0:
            DeleteAllLabels(id_number)
            return
        section_label_list = label_replacement_list
        section_displayed_files = displayed_replacement_files
        container = replace_container
        color = config.get(config_options_section, 'replace_color')
        down_arrow = replace_down_arrow_button
        section = replace_move_position

    global down_arrow_color_update
    i = offset
    label_index = 0
    while label_index < len(section_label_list):
        #Moving Down From End of List
        if (i >= len(section_displayed_files) and len(section_label_list) > 1):
            #Delete items in list
            section_label_list[label_index].destroy()
            section_label_list.pop(label_index)
            if (len(section_label_list) == 1):
                down_arrow.config(state = DISABLED, bg = 'gray')
                down_arrow_color_update = False

                section = len(section_displayed_files) - 1
                i = section
                break
            continue  
        #Moving Up From End of List
        elif (i < len(section_displayed_files) and len(section_label_list) < 30 and len(section_label_list) < len(section_displayed_files)):
            section_label_list.append(Label(container, bg=color, anchor='w', wraplength=322, justify="right", padx=4, pady = 3, relief=RAISED, width=40, text='{2} | {0} | {1}'.format(os.path.basename(section_displayed_files[i]), ByteOperation(os.path.getsize(section_displayed_files[i])), (i + 1) ), font='Helvetica 10' ))
            section_label_list[-1].pack()
            continue
        #Moving Up or Down
        index_size = os.path.getsize(section_displayed_files[i])
        section_label_list[label_index].config(bg=color, fg='black', relief=RAISED, width=40, text='{2} | {0} | {1}'.format(os.path.basename(section_displayed_files[i]), ByteOperation(index_size), (i+1) ))
        i += 1
        label_index += 1

    if len(section_label_list) > 1:
        down_arrow.config(bg=color, activebackground='purple', state=NORMAL)
        down_arrow_color_update = True
    else:
        if id_number == 0:
            source_move_position = section
        elif id_number == 1:
            replace_move_position = section
    if comparing_labels_on == True:
        ComparingFiles()
    pass


source_move_position = 0
replace_move_position = 0
up_arrow_color_update = False
down_arrow_color_update = False
#Uses the increment parameter to set the index position that the labels will be updated to.
def MoveFilesInSection(increment, id):
    if len(displayed_source_files) == 0 and len(displayed_replacement_files) == 0:
        return

    if id == 0:
        global source_move_position

        move_position = source_move_position
        up_arrow = source_up_arrow_button
        color = config.get(config_options_section, 'source_color')#source_color

    elif id == 1:
        global replace_move_position

        move_position = replace_move_position
        up_arrow = replace_up_arrow_button
        color = config.get(config_options_section, 'replace_color') #replace_color

    global up_arrow_color_update
    move_position += increment
    if move_position <= 0:
        move_position = 0
        up_arrow_color_update = False
        up_arrow.config(bg='gray', state=DISABLED)    
    else:
        up_arrow_color_update = True
        up_arrow.config(bg=color, activebackground='purple', state=NORMAL)

    
    UpdateLabels(move_position, id)
    global down_arrow_color_update
    if down_arrow_color_update == True:
        if id == 0:
            source_move_position = move_position
        elif id == 1:
            replace_move_position = move_position
    pass



#--------------------------------------------------------- AUTOMATIC REPLACER SECTION --------------------------------------------------------------#

#Obtains the inputed number from the user.
def ChosenNumber():
    try:
        base_number = int(config.get(config_options_section, 'number_base'))
        if base_number == 1: #Hex
            number_input.set( int(uexp_input_hex_number.get(), 16) )
        elif base_number == 2: #Dec
            number_input.set( int(uexp_input_hex_number.get() ) )
        elif base_number == 3: #Oct
            number_input.set( int(uexp_input_hex_number.get(), 8) )

        global chosen_number
        chosen_number = number_input.get()
    except:
        uexp_message_label.config(text='Inputed hex is invalid.\nGive the correct hex number that this file corresponds to.' )

    pass


#Displays the window that appears when the user goes to replace the HCA code blocks in their character's .uexp file.
def DisplayReplacingInfo():
    global uexp_replacing_files_window
    global uexp_message_label
    global uexp_file_label
    global uexp_input_hex_number
    global uexp_hca_file_label

    uexp_replacing_files_window = Toplevel(root_window)
    uexp_replacing_files_window.geometry('200x200')
    WindowCenterPositioner(uexp_replacing_files_window)
    
    uexp_message_label = Label(uexp_replacing_files_window, text='Message here', font='Helvetica 10', bg='gray', wraplength=175) #https://stackoverflow.com/questions/55241150/tkinter-wraplength-units-is-pixels
    uexp_message_label.pack(side='top', fill='both', expand='yes')

    uexp_file_label = Label(uexp_replacing_files_window, text='File name here', font='Helvetica 10', bg='gray', wraplength=175)
    uexp_file_label.pack(anchor='n', side='top', fill='both', expand='yes')
    
    global number_in_filename_used
    number_in_filename_used = config.get(config_options_section, 'number_in_filename_used')
    if number_in_filename_used == False:
        uexp_input_hex_number = Entry(uexp_replacing_files_window, bd=5)
        uexp_input_hex_number.pack(anchor = "s", side = "right")
        
        uexp_hca_file_label = Button(uexp_replacing_files_window, text='Input', font='Helvetica 9', bg='orange', command=ChosenNumber)
        uexp_hca_file_label.pack(side = "left", fill='both', expand='yes')

    pass


#Displays windows with debug information. This will display info about each HCA code string that was found and will display the numbers used in the filename versus what the program read those numbers as (they should be the same).
def DisplayDebugInfo(parameter):
    debug_mode = config.get(config_options_section, 'debug_mode')
    if debug_mode == False:
        return
    base_number = int(config.get(config_options_section, 'number_base'))

    if parameter == 0:
        global debug_window
        debug_window = Toplevel(root_window)
        debug_window.geometry('200x800')
        WindowCenterPositioner(debug_window)

        global debug_listbox
        debug_listbox = Listbox(debug_window, state=NORMAL)
        
        if base_number == 1: #Hex
            debug_listbox.insert(END, 'Hex Offset -     # | Hex #')
        elif base_number == 2: #Dec
            debug_listbox.insert(END, 'Dec Offset -     # | Dec #')
        elif base_number == 3: #Oct
            debug_listbox.insert(END, 'Oct Offset -     # | Oct #')
        
        debug_listbox.insert(END, '')
        debug_listbox.pack(fill='both', expand='yes')

        debug_scrollbar = ttk.Scrollbar(debug_listbox)
        debug_scrollbar.pack(side=RIGHT, fill=Y)
        debug_listbox.config(yscrollcommand = debug_scrollbar.set)
        debug_scrollbar.config(command=debug_listbox.yview)
    elif parameter == 1:
        global receipt_window
        receipt_window = Toplevel(root_window)
        receipt_window.geometry('250x500')
        WindowCenterPositioner(receipt_window)

        global receipt_listbox
        receipt_listbox = Listbox(receipt_window, state=NORMAL)
        receipt_listbox.pack(fill='both', expand='yes')
        if base_number == 1: #Hex
            receipt_listbox.insert(END, 'Hex # In File Name - Hex # Found')
        elif base_number == 2: #Dec
            receipt_listbox.insert(END, 'Dec # In File Name - Dec # Found')
        elif base_number == 3: #Oct
            receipt_listbox.insert(END, 'Oct # In File Name - Oct # Found')
        
        receipt_scrollbar = ttk.Scrollbar(receipt_listbox)
        receipt_scrollbar.pack(side=RIGHT, fill=Y)
        receipt_listbox.config(yscrollcommand = receipt_scrollbar.set)
        receipt_scrollbar.config(command=receipt_listbox.yview)

    debug_window.update_idletasks()

#The code section that goes about automatically replacing the HCA code blocks within a .uexp file.
def AutomaticReplacer():
    global uexp_message_label
    global uexp_file_label
    global uexp_input_hex_number
    global uexp_hca_file_label    

    uexp_file_to_replace = PickedFiles(CheckForSavedDirectory(uexp_dir), 'UEXP')
    if len(uexp_file_to_replace) == 0:
        text_display_string.set('Canceled. No .uexp file selected.')
        return
    OverwriteDirectoryData(uexp_dir, uexp_file_to_replace)

    debug_mode = config.get(config_options_section, 'debug_mode')
    base_number = int(config.get(config_options_section, 'number_base'))
    DisplayDebugInfo(0)

    dictionary = {}
    with open(uexp_file_to_replace, 'rb') as open_file:
        searchString = config.get(config_options_section, 'replacing_search_string') #"\x48\x43\x41\x00\x02\x00\x00\x60\x66\x6D\x74" This entire hex string doesn't work for 000_CMN.uexp because it has a slightly different hex sequence for some reason.
        read_file = open_file.read()
        number = 0
        comparing = 'string'
        for m in re.finditer(searchString, read_file):
            if base_number == 1: #Hex
                position = format(m.start(), 'x')
            elif base_number == 2: #Dec
                position = str(m.start())
            elif base_number == 3: #Oct
                position = format(m.start(), 'o')
            
            if debug_mode == True:
                global debug_listbox
                if base_number == 1: #Hex
                    comparing = format( number, 'x')  #https://stackoverflow.com/questions/38451592/unknown-format-code-x
                elif base_number == 2: #Dec
                    comparing = str(number)
                elif base_number == 3: #Oct
                    comparing = format(number, 'o')
                debug_listbox.insert(END, '{0} -        {1} | {2}'.format(position.upper(), str(number), comparing).upper() )
            dictionary.update({number: position})
            number += 1

    hca_replacement_files = PickedFiles(CheckForSavedDirectory(finished_dir), False)
    if len(hca_replacement_files) == 0:
        text_display_string.set('Canceled. No .hca files selected.')
        return
    OverwriteDirectoryData(finished_dir, os.path.dirname(hca_replacement_files[-1]))

    global chosen_number
    global number_input
    number_input = IntVar() #https://www.kite.com/python/docs/tkinter.Button.wait_variable
        
    DisplayDebugInfo(1)
    DisplayReplacingInfo()

    with open(uexp_file_to_replace, 'rb+') as uexp_file:
        for single_hca_file in hca_replacement_files:
            hca_filename = os.path.basename(single_hca_file)
            with open(single_hca_file, 'rb') as hca_file:
                if number_in_filename_used == True:
                    string_number_in_filename = hca_filename.partition(' ')[0]
                    uexp_message_label.config(text=string_number_in_filename)
                    try:
                        if base_number == 1: #Hex
                            chosen_number = int(string_number_in_filename, 16)
                        elif base_number == 2: #Dec
                            chosen_number = int(string_number_in_filename)
                        elif base_number == 3: #Oct
                            chosen_number = int(string_number_in_filename, 8)
                    except ValueError:
                         text_display_string.set('Invalid value ( {0} ) obtained from filename {1}. Set Number Base = {2}.'.format(string_number_in_filename, hca_filename, base_number))
                         return
                    
                    uexp_file_label.config(text=(hca_filename))
                    uexp_replacing_files_window.update_idletasks()

                    if debug_mode == True:
                        if base_number == 1: #Hex
                            found_value = format(chosen_number, 'x')
                        elif base_number == 2: #Dec
                            found_value = str(chosen_number)
                        elif base_number == 3: #Oct
                            found_value = format(chosen_number, 'o')
                        global receipt_listbox
                        receipt_listbox.insert(END, '{0} - {1}'.format(string_number_in_filename, found_value).upper() )

                else:
                    if base_number == 1: #Hex
                        uexp_message_label.config(text='Give the hexadecimal number that this file corresponds to:' )
                    elif base_number == 2: #Dec
                        uexp_message_label.config(text='Give the number that this file corresponds to:' )
                    elif base_number == 3: #Oct
                        uexp_message_label.config(text='Give the octal number that this file corresponds to:' )
                    uexp_file_label.config(text = hca_filename)
                
                    uexp_replacing_files_window.update_idletasks()
                    number_input.set(-1)
                    uexp_hca_file_label.wait_variable(number_input) #https://stackoverflow.com/questions/44790449/making-tkinter-wait-untill-button-is-pressed
                    uexp_input_hex_number.delete(0, 'end')
                    uexp_replacing_files_window.update_idletasks()
                
                offset = int(dictionary[chosen_number], 16)
                uexp_file.seek(offset)
                replace = hca_file.read()
                uexp_file.writelines(replace)

    uexp_message_label.config(text='Finished!' )
    uexp_file_label.config(text="You can close this window now.")
    if number_in_filename_used == False:
        uexp_hca_file_label.config(state=DISABLED, bg='gray')
        uexp_input_hex_number.config(state=DISABLED)

    pass

#--------------------------------------------------------- AUTOMATIC REPLACER SECTION --------------------------------------------------------------#





#------------------------------------------------------------ OPTIONS MENU SECTION -----------------------------------------------------------------#

#Displays a window showing all the available options the user can choose from.
def OptionsWindow():
    global options_window
    options_window = Toplevel()
    options_window.geometry('525x450')
    options_window.resizable(width=FALSE, height=FALSE)
    WindowCenterPositioner(options_window)

    options_canvas = Canvas(options_window)
    options_canvas.pack(fill='both', expand='yes')

    options_frame = Frame(options_canvas)
    options_frame.pack(fill='both', expand='yes')


    source_color = config.get(config_options_section, 'source_color')
    replace_color = config.get(config_options_section, 'replace_color')

    global source_color_options_button #https://python-forum.io/Thread-NameError-Global-Name-is-not-defined
    source_color_options_button = Button(options_frame, text='Change Source Color: {0}'.format(source_color), font='Helvetica 9', bg=source_color, relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : ColorPicker(0))
    source_color_options_button.grid(row=0, column=0)
    
    global replace_color_options_button
    replace_color_options_button = Button(options_frame, text='Change Replace Color: {0}'.format(replace_color), font='Helvetica 9', bg=replace_color, relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : ColorPicker(1))
    replace_color_options_button.grid(row=1, column=0)


    set_byte_conversion = int(config.get(config_options_section, 'set_byte_conversion'))
    global byte_conversion_check
    byte_conversion_check = Menubutton(options_frame, text='Set Byte Unit: {0}'.format(set_byte_conversion), font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=36, bd=5, padx=0, pady = 3)
    byte_conversion_check.grid(row=2, column=0)

    byte_conversion_check.menu = Menu(byte_conversion_check, tearoff=0)
    byte_conversion_check.config(menu=byte_conversion_check.menu)
    byte_conversion_check.menu.add_command (label="0 - Bytes", command=lambda : SetByteUnit(0))
    byte_conversion_check.menu.add_command (label="1 - KB", command=lambda : SetByteUnit(1))
    byte_conversion_check.menu.add_command (label="2 - MB", command=lambda : SetByteUnit(2))
    byte_conversion_check.menu.add_command (label="3 - GB", command=lambda : SetByteUnit(3))
    byte_conversion_check.menu.add_command (label="4 - TB", command=lambda : SetByteUnit(4))


    round_to_decimal_position = int(config.get(config_options_section, 'round_to_decimal_position'))
    global decimal_position_button
    decimal_position_button = Button(options_frame, text='Decimal Position to Round to:\n{} - {:.{}f}'.format(round_to_decimal_position, 1, round_to_decimal_position), font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=35, bd=5, pady = 0, command=SetDecimalPosition)
    decimal_position_button.grid(row=3, column=0)
    
    global decimal_position_user_input
    decimal_position_user_input = Entry(options_frame, relief=RIDGE, width=41, bd=5, justify=CENTER)
    decimal_position_user_input.grid(row=4, column=0)
    decimal_position_user_input.insert(0, round_to_decimal_position)


    base_number = int(config.get(config_options_section, 'number_base'))
    global number_base_button
    number_base_button = Menubutton(options_frame, text='Set Number Base: {0}'.format(base_number), font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=36, bd=5, padx=0, pady = 3)
    number_base_button.grid(row=5, column=0)

    number_base_button.menu = Menu(number_base_button, tearoff=0)
    number_base_button.config(menu=number_base_button.menu)
    number_base_button.menu.add_command (label="1 - Hexadecimal (Base 16)", command=lambda : SetBaseNumber(1))
    number_base_button.menu.add_command (label="2 - Decimal (Base 10)", command=lambda : SetBaseNumber(2))
    number_base_button.menu.add_command (label="3 - Octal (Base 8)", command=lambda : SetBaseNumber(3))


    global number_in_filename_check_bool
    number_in_filename_check_bool = BooleanVar()
    number_in_filename_check_bool.set(config.get(config_options_section, 'number_in_filename_used') )
    number_in_filename_checkbox = Checkbutton(options_frame, variable=number_in_filename_check_bool, text='Read the first 3 characters in a file name?\n(Used when replacing HCA\ncode blocks in a .uexp file)', font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=33, bd=5, padx=0, pady = 0, command=UseNumberInFileName)
    number_in_filename_checkbox.grid(row=6, column=0)


    global automatically_sort_files_check_bool
    automatically_sort_files_check_bool = BooleanVar()
    automatically_sort_files_check_bool.set( config.get(config_options_section, 'automatically_sort_files') )
    automatically_sort_files = Checkbutton(options_frame, variable=automatically_sort_files_check_bool, text='Automatically sort added files?', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=33, bd=5, padx=0, pady = 0, command=SetAutomaticFileSort)
    automatically_sort_files.grid(row=7, column=0)


    replacing_search_string = config.get(config_options_section, 'replacing_search_string')
    global search_string_button
    search_string_button = Button(options_frame, text='Change Search String:\n{0}'.format(replacing_search_string), font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=35, bd=5, pady = 0, command=SetSearchString)
    search_string_button.grid(row=8, column=0)

    global search_string_user_input
    search_string_user_input = Entry(options_frame, relief=RIDGE, width=41, bd=5, justify=CENTER)
    search_string_user_input.grid(row=9, column=0)
    search_string_user_input.insert(0, replacing_search_string)


    global debug_mode_check_bool
    debug_mode_check_bool = BooleanVar()
    debug_mode_check_bool.set( config.get(config_options_section, 'debug_mode') )
    debug_mode_check_button = Checkbutton(options_frame, variable=debug_mode_check_bool, text='Use Debug Mode?', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=33, bd=5, padx=0, pady = 1, command=SetDebugMode)
    debug_mode_check_button.grid(row=10, column=0)



    #Set To Default functions
    source_color_default_button = Button(options_frame, text='Set Default Source Color', font='Helvetica 9', bg='#0080FF', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(1)) #'#80C1FF'
    source_color_default_button.grid(row=0, column=1)

    replace_color_default_button = Button(options_frame, text='Set Default Replace Color', font='Helvetica 9', bg='#E3242B', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(2))
    replace_color_default_button.grid(row=1, column=1)

    byte_conversion_default_button = Button(options_frame, text='Set Default File Size Units Displayed', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(3))
    byte_conversion_default_button.grid(row=2, column=1)

    decimal_position_default_button = Button(options_frame, text='Set Default Rounded Decimal Position', font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=35, bd=5, pady = 6, height=3, command=lambda : SetToDefaultSettings(4))
    decimal_position_default_button.grid(row=3, column=1, rowspan = 2)

    number_base_default_button = Button(options_frame, text='Set Default Base Number', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(5))
    number_base_default_button.grid(row=5, column=1)

    number_in_filename_default_button = Button(options_frame, text='Set Default Read Filename Option', font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=35, bd=5, pady = -1, height=3, command=lambda : SetToDefaultSettings(6))
    number_in_filename_default_button.grid(row=6, column=1)

    automatically_sort_files_default_button = Button(options_frame, text='Set Default Automatic Sort Option', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(7))
    automatically_sort_files_default_button.grid(row=7,column=1)

    search_string_default_button = Button(options_frame, text='Set Default Search String', font='Helvetica 9', bg='#FFFFFF', relief=RIDGE, width=35, bd=5, pady = 6, height=3, command=lambda : SetToDefaultSettings(8))
    search_string_default_button.grid(row=8, column=1, rowspan=2)

    debug_mode_default_button = Button(options_frame, text='Set Default Debug Mode Option', font='Helvetica 9', bg='#CCCCCC', relief=RIDGE, width=35, bd=5, pady = 0, command=lambda : SetToDefaultSettings(9))
    debug_mode_default_button.grid(row=10, column=1)


    set_all_to_default_button = Button(options_frame, text='Set All Options To Default', font='Helvetica 9 bold', bg='black', fg='white', relief=RIDGE, width=72, bd=5, pady = 2, height=3, command=lambda : SetToDefaultSettings(0))
    set_all_to_default_button.grid(row=100, column=0, columnspan = 3)

    options_window.mainloop()


#Opens a window where the user can choose the new color for the chosen section.
def ColorPicker(id_number):
    hex_code = tkColorChooser.askcolor()[1] #https://www.youtube.com/watch?v=NDCirUTTrhg   
    if hex_code != None:
        color = hex_code.upper()
        if id_number == 0:
            option_name = 'source_color'
            OverwriteOptionsData(option_name, color)
            UpdateSourceColor()
        elif id_number == 1:
            option_name = 'replace_color'
            OverwriteOptionsData(option_name, color)
            UpdateReplaceColor()
    pass


#Updates any widgets that use source_color to the new chosen color. This does not effect widgets created from TopLevel windows as those are not currently created.
def UpdateSourceColor(): #1
    source_color = config.get(config_options_section, 'source_color')
    source_color_options_button.config(bg=source_color, text='Change Source Color: {0}'.format(source_color))
    source_container.config(bg=source_color)

    global up_arrow_color_update
    global down_arrow_color_update
    if up_arrow_color_update == True:
        source_up_arrow_button.config(bg=source_color)
    if down_arrow_color_update == True:
        source_down_arrow_button.config(bg=source_color)

    global comparing_labels_on
    if comparing_labels_on == False:
        UpdateLabels(source_move_position, 0)
    pass

  
#Like UpdateSourceColor() but for the Replacement Files Section.
def UpdateReplaceColor(): #2
    replace_color = config.get(config_options_section, 'replace_color')
    replace_color_options_button.config(bg=replace_color, text='Change Replace Color: {0}'.format(replace_color))
    replace_container.config(bg=replace_color)

    global up_arrow_color_update
    if up_arrow_color_update == True:
        replace_up_arrow_button.config(bg=replace_color)

    global comparing_labels_on
    if comparing_labels_on == False:
        UpdateLabels(replace_move_position, 1)
    pass


#Sets the unit that the file size will be converted to.
def SetByteUnit(unit_number): #3
    OverwriteOptionsData('set_byte_conversion', unit_number)
    set_byte_conversion = int(config.get(config_options_section, 'set_byte_conversion'))
    byte_conversion_check.config(text='Set Byte Unit: {0}'.format(set_byte_conversion))

    UpdateLabels(source_move_position, 0)
    UpdateLabels(replace_move_position, 1)

    
#Sets the decimal position the file size will be rounded to.
def SetDecimalPosition(): #4
    try:
        round_to_decimal_position = int(decimal_position_user_input.get())
        decimal_position_user_input.delete(0, 'end') #https://coderslegacy.com/python/tkinter-clear-entry/
        decimal_position_button.config(text='Decimal Position to Round to:\n{} - {:.{}f}'.format(round_to_decimal_position, 1, round_to_decimal_position))
        OverwriteOptionsData('round_to_decimal_position', round_to_decimal_position)
    except ValueError: #https://www.youtube.com/watch?v=IbpInH4q4Sg
        text_display_string.set("Invalid input. Type the number position you wish to round to. Ex: 3 for #.000\nIf you want no rounding, input a negative number.")
    pass


#Sets whether numbers at the start of the name of a file should be read.
def UseNumberInFileName(): #5
    global number_in_filename_check_bool
    OverwriteOptionsData('number_in_filename_used', number_in_filename_check_bool.get() )
    number_in_filename_used = config.get(config_options_section, 'number_in_filename_used')


#Sets what number base will be used when replacing the HCA code blocks in the .uexp file.
def SetBaseNumber(base_number): #6
    OverwriteOptionsData('number_base', base_number)
    base_number = int(config.get(config_options_section, 'number_base'))
    number_base_button.config(text='Set Number Base: {0}'.format(base_number))


#Sets if the program should automatically sort the files added to the source and replace sections.
def SetAutomaticFileSort(): #7
    global automatically_sort_files_check_bool
    OverwriteOptionsData('automatically_sort_files', automatically_sort_files_check_bool.get() )
    automatically_sort_files = config.get(config_options_section, 'automatically_sort_files')


#Sets the string that is to be found while reading the .uexp file.
def SetSearchString(): #8
    replacing_search_string = search_string_user_input.get()
    search_string_user_input.delete(0, 'end') #https://coderslegacy.com/python/tkinter-clear-entry/
    search_string_button.config(text='Change Search String:\n{0}'.format(replacing_search_string))
    OverwriteOptionsData('replacing_search_string', replacing_search_string)


def SetDebugMode(): #9
    global debug_mode_check_bool
    OverwriteOptionsData('debug_mode', debug_mode_check_bool.get() )
    debug_mode = config.get(config_options_section, 'debug_mode')


#Sets an option to its default setting. The option chosen is based on the given number pass as the parameter.
def SetToDefaultSettings(number):
     #All - if number == 0
    if number == 0 or number == 1: #Source Color Default
        source_color='#0080FF' #'#80C1FF'
        source_color_options_button.config(bg=source_color)
        OverwriteOptionsData('source_color', source_color)
        UpdateSourceColor()

    if number == 0 or number == 2: #Replace Color Default
        replace_color='#E3242B'
        replace_color_options_button.config(bg=replace_color)
        OverwriteOptionsData('replace_color', replace_color)
        UpdateReplaceColor()

    if number == 0 or number == 3: #Byte Unit Default
        set_byte_conversion = 1
        byte_conversion_check.config(text='Set Byte Unit: {0}'.format(set_byte_conversion))
        OverwriteOptionsData('set_byte_conversion', set_byte_conversion)

    if number == 0 or number == 4: #Decimal Position Default
        round_to_decimal_position = 2
        decimal_position_button.config(text='Decimal Position to Round to:\n{} - {:.{}f}'.format(round_to_decimal_position, 1, round_to_decimal_position))
        OverwriteOptionsData('round_to_decimal_position', round_to_decimal_position)

    if number == 0 or number == 5: #Base Number Default
        base_number = 1
        number_base_button.config(text='Set Number Base: {0}'.format(base_number))
        OverwriteOptionsData('number_base', base_number)

    if number == 0 or number == 6: #Use Number in File Name Default
        global number_in_filename_check_bool
        number_in_filename_check_bool.set(True)
        OverwriteOptionsData('number_in_filename_used', number_in_filename_check_bool.get() )

    if number == 0 or number == 7: #Automatically Sort Files Default
        global automatically_sort_files_check_bool
        automatically_sort_files_check_bool.set(True)
        OverwriteOptionsData('automatically_sort_files', automatically_sort_files_check_bool.get() )

    if number == 0 or number == 8: #Search String Default
        replacing_search_string = (r'\x48\x43\x41\x00\x02') #https://www.askpython.com/python/string/python-raw-strings
        search_string_button.config(text='Change Search String:\n{0}'.format(replacing_search_string))
        search_string_user_input.delete(0, 'end')
        OverwriteOptionsData('replacing_search_string', replacing_search_string)

    if number == 0 or number == 9: #Debug Mode Default
        global debug_mode_check_bool
        debug_mode_check_bool.set(False)
        OverwriteOptionsData('debug_mode', debug_mode_check_bool.get() )

    pass


#Overwrites any option data that the user changed and saves it.
def OverwriteOptionsData(name_of_option, option):
    try:
        #If the data is not the exact same as in the config file
        if option != config.get(config_options_section, name_of_option):
            config.set(config_options_section, name_of_option, option)
            with open('config.ini', 'w') as outfile:
                config.write(outfile)
            debug_mode = config.get(config_options_section, 'debug_mode')

            if debug_mode == True:
                text_display_string.set('Saved "{0}" data as "{1}".'.format(name_of_option, option))
            else:
                text_display_string.set('')
    except:
        text_display_string.set('Error occured when trying to overwrite data in config.ini')
    pass

#------------------------------------------------------------ OPTIONS MENU SECTION -----------------------------------------------------------------#



#---------------------------------------------------------------------------------------------------------------------------------------------------#

#----- Main Canvas -----#
root_window = Tk()
RootWindowCenterPositioner()

canvas_width = 750
canvas_height = 500
program_canvas = Canvas(root_window, width=canvas_width, height=canvas_height)
program_canvas.pack()


#----- Menu Bar -----#
menubar = Menu(root_window)
root_window.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root_window.quit)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Options', command=OptionsWindow)



#----- Source Files Section-----#
source_dir = 'source_hca_directory'
source_color = config.get(config_options_section, 'source_color')

# Create A Main Frame #
source_frame = Frame(root_window)
source_frame.place(relwidth=0.45, relheight=0.8, relx=0.245, rely=0.05, anchor='n' )

source_container = LabelFrame(source_frame, text='Source HCA Files', font='Helvetica 9', bg=source_color)
source_container.pack(fill='both', expand='yes')



#----- Replacement Files Section-----#
replace_dir = 'replacement_hca_directory'
replace_color = config.get(config_options_section, 'replace_color')

replace_frame = Frame(root_window)
replace_frame.place(relwidth=0.449, relheight=0.8, relx=0.755, rely=0.05, anchor='n')

replace_container = LabelFrame(replace_frame, text='Replacement HCA Files', font='Helvetica 9', bg = replace_color)
replace_container.pack(fill='both', expand='yes')



#----- Middle Section -----#
middle_frame = Frame(root_window, bg='purple')
middle_frame.place(relwidth=0.055, relheight=0.8, relx=0.5, rely=0.05, anchor= 'n')

add_button = Button(middle_frame, bg='orange', text='ADD', font='Helvetica 10', activebackground='purple', command=ConfirmFileSection)
add_button.place(relwidth=1, relheight=0.1, rely=0.35, anchor='nw')

remove_button = Button(middle_frame, bg='gray', text='DEL', font='Helvetica 10', state=DISABLED, command=RemoveSelection)
remove_button.place(relwidth=1, relheight=0.1, rely=0.55, anchor='sw')

source_up_arrow_button = Button(middle_frame, bg='gray', text='Source\nUp', font='Helvetica 8', state=DISABLED, command=lambda : MoveFilesInSection(-10, 0)) #https://stackoverflow.com/questions/3704568/tkinter-button-command-activates-upon-running-program
source_up_arrow_button.place(relwidth=1, relheight=0.1, rely=0.20, anchor='nw')

replace_up_arrow_button = Button(middle_frame, bg='gray', text='Replace\nUp', font='Helvetica 8', state=DISABLED, command=lambda : MoveFilesInSection(-10, 1))
replace_up_arrow_button.place(relwidth=1, relheight=0.1, rely=0.10, anchor='nw')

source_down_arrow_button = Button(middle_frame, bg='gray', text='Source\nDown', font='Helvetica 8', state=DISABLED, command=lambda : MoveFilesInSection(10, 0))
source_down_arrow_button.place(relwidth=1, relheight=0.1, rely=0.70, anchor='sw')

replace_down_arrow_button = Button(middle_frame, bg='gray', text='Replace\nDown', font='Helvetica 8', state=DISABLED, command=lambda : MoveFilesInSection(10, 1))
replace_down_arrow_button.place(relwidth=1, relheight=0.1, rely=0.80, anchor='sw')



#----- Bottom Section -----#
text_frame = Frame(root_window, bg='black')
text_frame.place(relwidth=1, relheight=0.1, relx=0.5, rely=1, anchor='s')

text_box_string = ''
text_display_string=StringVar()
display_text = Label(text_frame, bg='black', fg='white', textvariable=text_display_string, font='Helvetica 10')
text_display_string.set(text_box_string)
display_text.pack(side=LEFT)

compare_button = Button(text_frame, bg='yellow', text='COMPARE', font='Helvetica 9', command=ComparingFiles)
compare_button.place(relwidth=0.1, relheight=1, relx=0.75, anchor='n')

finished_dir = 'finished_hca_directory'
fill_button = Button(text_frame, bg='grey', text='FILL', font='Helvetica 9', command=FinishedDirectory, state=DISABLED)
fill_button.place(relwidth=0.1, relheight=1, relx=0.85, anchor='n')

uexp_dir = 'uexp_directory'
replace_button = Button(text_frame, bg='red', text ='REPLACE', font='Helvetica 9', command=AutomaticReplacer)
replace_button.place(relwidth=0.1, relheight=1, relx=0.95, anchor='n')



root_window.mainloop()
