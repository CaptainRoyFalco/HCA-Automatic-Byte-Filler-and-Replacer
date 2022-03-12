import os
import sys
from natsort import natsorted, ns   #Version 6.2.1 - # https://pypi.org/project/natsort/6.2.1/
import shutil
from decimal import Decimal

from Tkinter import Tk, Menu, Toplevel, Frame, LabelFrame, Label, Button, Entry, Text, Checkbutton, Menubutton, Radiobutton, Listbox, IntVar, BooleanVar, StringVar
import ttk
import tkFileDialog
import tkColorChooser # https://stackoverflow.com/questions/18903911/tkinter-color-chooser-window-focus
#import webbrowser

import ConfigParser
config_parser = ConfigParser.RawConfigParser()
config_parser.read('config.ini')

#------------------------------------------------------------- CONFIG FILE CHECKS ------------------------------------------------------------------#

config_file_general_section = 'General'
config_file_options_section = 'Options'
config_file_color_options_section = 'Color'
config_file_color_preset1_section = "Preset Color 1"
config_file_color_preset2_section = "Preset Color 2"
config_file_color_preset3_section = "Preset Color 3"

#If the config file doesn't exist or wasn't found for some reason, create a new one.
def CreateConfigFile():
    global config_parser
    config_file_name = 'config.ini'
    previous_parser_instance = None
    if os.path.exists(config_file_name) == True: #This is if the user decides to create a brand new config file.
        config_name_index_suffix = 0
        config_name_one_file = "(Default) - config.ini"

        if os.path.exists(config_name_one_file) == True:
            config_name_index_suffix = 1

        if config_name_index_suffix != 0:
            while os.path.exists("(Default) - config({}).ini".format(config_name_index_suffix) ):
                config_name_index_suffix += 1

        if config_name_index_suffix == 0:
            config_file_name = config_name_one_file
        else:
            config_file_name = "(Default) - config({}).ini".format(config_name_index_suffix)

        previous_parser_instance = config_parser #Remember the current instance so the program can continue functioning after creating a new default config.ini file
        config_parser = ConfigParser.RawConfigParser() #Set the variable to a different, new instance of RawConfigParser()


    #Add sections to config.ini file
    config_parser.add_section(config_file_general_section)
    config_parser.add_section(config_file_options_section)
    config_parser.add_section(config_file_color_options_section)
    config_parser.add_section(config_file_color_preset1_section)
    config_parser.add_section(config_file_color_preset2_section)
    config_parser.add_section(config_file_color_preset3_section)


    #General Section
    config_parser.set(config_file_general_section, 'source_files_directory', '')
    config_parser.set(config_file_general_section, 'replacement_files_directory', '')
    config_parser.set(config_file_general_section, 'filled_files_directory', '')
    config_parser.set(config_file_general_section, 'uexp_directory', '')
    config_parser.set(config_file_general_section, 'file_to_extract_from_directory', '')
    config_parser.set(config_file_general_section, 'extracted_files_directory', '')
    config_parser.set(config_file_general_section, 'switch_containers_placement', 'False')
    config_parser.set(config_file_general_section, 'switch_scroll_buttons_placement', 'False')

    #Options Section
    config_parser.set(config_file_options_section, 'automatically_sort_files', 'True')
    config_parser.set(config_file_options_section, 'set_byte_unit', '1')
    config_parser.set(config_file_options_section, 'round_to_decimal_position', '2')
    config_parser.set(config_file_options_section, 'source_scroll_increment', '10')
    config_parser.set(config_file_options_section, 'replace_scroll_increment', '10')
    config_parser.set(config_file_options_section, 'both_buttons_scroll_type', '2')
    config_parser.set(config_file_options_section, 'number_base', '1')
    config_parser.set(config_file_options_section, 'automatically_replace_using_filename', 'False')
    config_parser.set(config_file_options_section, 'replacing_search_string', '\x48\x43\x41\x00\x02')
    config_parser.set(config_file_options_section, 'search_string_used_manual_input', 'False')
    config_parser.set(config_file_options_section, 'replacing_finish_string', '\x40\x55\x54\x46\x00\x00')
    config_parser.set(config_file_options_section, 'search_for_finish_string', 'True')
    config_parser.set(config_file_options_section, 'finish_string_used_manual_input', 'False')


    #Color Options Section
    config_parser.set(config_file_color_options_section, 'use_rgb_color_code', 'True')

    config_parser.set(config_file_color_options_section, 'source_section_color', default_source_section_color)
    config_parser.set(config_file_color_options_section, 'replacement_section_color', default_replacement_section_color)
    config_parser.set(config_file_color_options_section, 'default_button_color', default_default_button_color)
    config_parser.set(config_file_color_options_section, 'button_highlight_color', default_button_highlight_color) #Highlight color


    config_parser.set(config_file_color_options_section, 'both_scroll_buttons_same_color', 'True')
    config_parser.set(config_file_color_options_section, 'both_up_scroll_button_color', default_both_scroll_buttons_color)
    config_parser.set(config_file_color_options_section, 'both_down_scroll_button_color', default_both_scroll_buttons_color)

    config_parser.set(config_file_color_options_section, 'to_file_buttons_same_color', 'True')
    config_parser.set(config_file_color_options_section, 'to_first_source_file_button_color', default_to_file_scroll_buttons_color)
    config_parser.set(config_file_color_options_section, 'to_first_replacement_file_button_color', default_to_file_scroll_buttons_color)
    config_parser.set(config_file_color_options_section, 'to_last_source_file_button_color', default_to_file_scroll_buttons_color)
    config_parser.set(config_file_color_options_section, 'to_last_replacement_file_button_color', default_to_file_scroll_buttons_color)


    config_parser.set(config_file_color_options_section, 'extract_button_color', default_source_section_color)
    config_parser.set(config_file_color_options_section, 'compare_button_color', default_compare_button_color)
    config_parser.set(config_file_color_options_section, 'compare_O_label_color', default_compare_O_label_color)
    config_parser.set(config_file_color_options_section, 'compare_X_label_color', default_compare_X_label_color)
    config_parser.set(config_file_color_options_section, 'fill_button_color', default_fill_button_color)
    config_parser.set(config_file_color_options_section, 'replace_button_color', default_replace_button_color)

    #Preset Colors Section (1-3)
    config_file_color_preset_section = ""
    preset_number_prefix = ""
    color_preset_section = 0
    while color_preset_section < 3:
        if color_preset_section == 0:
            config_file_color_preset_section = config_file_color_preset1_section
            preset_number_prefix = "preset1_"
            preset_defaults_source_section_color =                      "#0000FF"
            preset_defaults_replacement_section_color =                 "#FF0000"
            preset_defaults_default_button_color =                      "#FFA300"
            preset_defaults_button_highlight_color =                    "#A020F0"

            preset_defaults_both_scroll_buttons_same_color =            "True"
            preset_defaults_both_up_scroll_button_color =               "#8000FF"
            preset_defaults_both_down_scroll_button_color =             "#8000FF"

            preset_defaults_to_file_buttons_same_color =                "True"
            preset_defaults_to_first_source_file_button_color =         "#8000FF"
            preset_defaults_to_first_replacement_file_button_color =    "#8000FF"
            preset_defaults_to_last_source_file_button_color =          "#8000FF"
            preset_defaults_to_last_replacement_file_button_color =     "#8000FF"

            preset_defaults_extract_button_color =                      "#FFFF00"
            preset_defaults_compare_button_color =                      "#FFA300"
            preset_defaults_compare_O_label_color =                     "#FFFFFF"
            preset_defaults_compare_X_label_color =                     "#989898"
            preset_defaults_fill_button_color =                         "#FFA300"
            preset_defaults_replace_button_color =                      "#00FF00"
        elif color_preset_section == 1:
            config_file_color_preset_section = config_file_color_preset2_section
            preset_number_prefix = "preset2_"
            preset_defaults_source_section_color =                      "#00FF00"
            preset_defaults_replacement_section_color =                 "#BF6DC9"
            preset_defaults_default_button_color =                      "#FFA300"
            preset_defaults_button_highlight_color =                    "#A020F0"

            preset_defaults_both_scroll_buttons_same_color =            "True"
            preset_defaults_both_up_scroll_button_color =               "#FF8000"
            preset_defaults_both_down_scroll_button_color =             "#FF38FF"

            preset_defaults_to_file_buttons_same_color =                "False"
            preset_defaults_to_first_source_file_button_color =         "#FFFFFF"
            preset_defaults_to_first_replacement_file_button_color =    "#FFFFFF"
            preset_defaults_to_last_source_file_button_color =          "#FFFFFF"
            preset_defaults_to_last_replacement_file_button_color =     "#FFFFFF"

            preset_defaults_extract_button_color =                      "#2D96FF"
            preset_defaults_compare_button_color =                      "#FFFF00"
            preset_defaults_compare_O_label_color =                     "#40FF38"
            preset_defaults_compare_X_label_color =                     "#FF0000"
            preset_defaults_fill_button_color =                         "#00FF64"
            preset_defaults_replace_button_color =                      "#FF5EFF"
        elif color_preset_section == 2:
            config_file_color_preset_section = config_file_color_preset3_section
            preset_number_prefix = "preset3_"
            preset_defaults_source_section_color =                      ""          #CDEAFF
            preset_defaults_replacement_section_color =                 ""
            preset_defaults_default_button_color =                      ""
            preset_defaults_button_highlight_color =                    ""          #CDA3FF

            preset_defaults_both_scroll_buttons_same_color =            ""
            preset_defaults_both_up_scroll_button_color =               ""
            preset_defaults_both_down_scroll_button_color =             ""

            preset_defaults_to_file_buttons_same_color =                ""
            preset_defaults_to_first_source_file_button_color =         ""
            preset_defaults_to_first_replacement_file_button_color =    ""
            preset_defaults_to_last_source_file_button_color =          ""
            preset_defaults_to_last_replacement_file_button_color =     ""

            preset_defaults_extract_button_color =                      ""
            preset_defaults_compare_button_color =                      ""
            preset_defaults_compare_O_label_color =                     ""
            preset_defaults_compare_X_label_color =                     ""
            preset_defaults_fill_button_color =                         ""
            preset_defaults_replace_button_color =                      ""
        
        config_parser.set(config_file_color_preset_section, "{0}source_section_color".format(preset_number_prefix), preset_defaults_source_section_color)
        config_parser.set(config_file_color_preset_section, "{0}replacement_section_color".format(preset_number_prefix), preset_defaults_replacement_section_color)
        config_parser.set(config_file_color_preset_section, "{0}default_button_color".format(preset_number_prefix), preset_defaults_default_button_color)
        config_parser.set(config_file_color_preset_section, "{0}button_highlight_color".format(preset_number_prefix), preset_defaults_button_highlight_color)


        config_parser.set(config_file_color_preset_section, "{0}both_scroll_buttons_same_color".format(preset_number_prefix), preset_defaults_both_scroll_buttons_same_color)
        config_parser.set(config_file_color_preset_section, "{0}both_up_scroll_button_color".format(preset_number_prefix), preset_defaults_both_up_scroll_button_color)
        config_parser.set(config_file_color_preset_section, "{0}both_down_scroll_button_color".format(preset_number_prefix), preset_defaults_both_down_scroll_button_color)

        config_parser.set(config_file_color_preset_section, "{0}to_file_buttons_same_color".format(preset_number_prefix), preset_defaults_to_file_buttons_same_color)
        config_parser.set(config_file_color_preset_section, "{0}to_first_source_file_button_color".format(preset_number_prefix), preset_defaults_to_first_source_file_button_color)
        config_parser.set(config_file_color_preset_section, "{0}to_first_replacement_file_button_color".format(preset_number_prefix), preset_defaults_to_first_replacement_file_button_color)
        config_parser.set(config_file_color_preset_section, "{0}to_last_source_file_button_color".format(preset_number_prefix), preset_defaults_to_last_source_file_button_color)
        config_parser.set(config_file_color_preset_section, "{0}to_last_replacement_file_button_color".format(preset_number_prefix), preset_defaults_to_last_replacement_file_button_color)


        config_parser.set(config_file_color_preset_section, "{0}extract_button_color".format(preset_number_prefix), preset_defaults_extract_button_color)
        config_parser.set(config_file_color_preset_section, "{0}compare_button_color".format(preset_number_prefix), preset_defaults_compare_button_color)
        config_parser.set(config_file_color_preset_section, "{0}compare_O_label_color".format(preset_number_prefix), preset_defaults_compare_O_label_color)
        config_parser.set(config_file_color_preset_section, "{0}compare_X_label_color".format(preset_number_prefix), preset_defaults_compare_X_label_color)
        config_parser.set(config_file_color_preset_section, "{0}fill_button_color".format(preset_number_prefix), preset_defaults_fill_button_color)
        config_parser.set(config_file_color_preset_section, "{0}replace_button_color".format(preset_number_prefix), preset_defaults_replace_button_color)

        color_preset_section += 1


    with open(config_file_name, 'w') as config_file: #Create the config.ini file
        config_parser.write(config_file)

    if previous_parser_instance != None:
        config_parser = previous_parser_instance #Set config_parser back to the previous instance so the program can still be used
        text_display_string.set("A new config.ini file was created! Check the file explorer to see it.")

    pass


# https://stackoverflow.com/questions/11340765/default-window-colour-tkinter-and-hex-colour-codes
default_source_section_color = "#1188FF" #"#0080FF"
default_replacement_section_color = "#FF3838"
default_default_button_color = "#FFA300"
default_button_highlight_color = "#A020F0"
default_both_scroll_buttons_color = "#FF38FF"
default_to_file_scroll_buttons_color = "#FFFFFF"
default_extract_button_color = "#2D96FF"
default_compare_button_color = "#FFFF00"
default_compare_O_label_color = "#40FF38"
default_compare_X_label_color = "#FF0000"
default_fill_button_color = "#00FF64"
default_replace_button_color = "#FF5EFF"

if not config_parser.read('config.ini'): #If the file wasn't found
    CreateConfigFile()
    config_parser.read('config.ini')

#------------------------------------------------------------- CONFIG FILE CHECKS ------------------------------------------------------------------#





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Sets the TopLevel/Root window to be set at the middle of the root window/screen.
def WindowCenterPositioner(window, window_width, window_height, parent_window=None, bind_child_window=True):
    window.withdraw() #Hide the window
    if parent_window == None: # Putting "root_window" as the default parameter for parent_window instead of "None" causes an error
        parent_window=root_window
    scaled_width, scaled_height = ScaleByResolutionSize(window_width, window_height)

    if window == root_window:
        #Get the width and height of the screen's resolution size
        x = 0
        y = 0
        w = root_window.winfo_screenwidth()
        h = root_window.winfo_screenheight()
    else:
        if bind_child_window == True:
            window.lift()       #Raise the toplevel window to appear above the root window
            window.grab_set()   #Make the toplevel window the main focus

            #These two bindings make it so the user cannot use the previous window unless they close the current TopLevel window
            window.bind('<Destroy>', lambda e: OnWindowClose(e, window, parent_window))
            window.bind('<FocusIn>', lambda e: SetFocusToCurrentChildWindow(e, window, parent_window))

        #Get the x and y coordinates and the width and height of the parent window (usually the root window)
        x = parent_window.winfo_x()
        y = parent_window.winfo_y()
        w = parent_window.winfo_width()
        h = parent_window.winfo_height()

    halved_width = Decimal(w) / Decimal(2)                      #Halve the width and height to get the top-left corner (0,0) of the child/root window to be in the middle of the root window/screen
    halved_height = Decimal(h) / Decimal(2)
    window_half_width = Decimal(scaled_width) / Decimal(2)      #Get and halve the properly scaled width and height of the window
    window_half_height = Decimal(scaled_height) / Decimal(2)
    rx = int(round(halved_width - window_half_width))           #Subract the top-left corner position of the window from the half of its width and height to anchor the window at its center
    ry = int(round(halved_height - window_half_height))

    window.update_idletasks() #This makes sure the geometry is properly set for when the InitialWindowFontSize function is called.
    window.geometry("%dx%d+%d+%d" % (scaled_width, scaled_height, x + rx, y + ry)) # https://stackoverflow.com/questions/36050192/how-to-position-toplevel-widget-relative-to-root-window

    # https://stackoverflow.com/questions/23773825/how-can-change-the-logo-of-tkinter-gui-screen/23773857
    try:
        window.wm_iconbitmap('HCA Byte Filler and Replacer Icon.ico') #This MUST go after window.geometry or the window will not be positioned properly
    except:
        pass
    #Show the window on screen
    window.deiconify()


#Change the number of pixles to be used for the given window's width and height based on the screen's resolution size.
def ScaleByResolutionSize(given_width, given_height):
    developer_monitor_width = Decimal(1920)
    developer_monitor_height = Decimal(1080)
    user_screen_resolution_width = Decimal(root_window.winfo_screenwidth())
    user_screen_resolution_height = Decimal(root_window.winfo_screenheight() )

    #Window's scaled width and height Equals: User's Screen Resolution divided by (Developer's Resolution (my monitor's screen size) divided by the base width and height of the window)
    width_to_scale = developer_monitor_width / Decimal(given_width)         #Developer's Resolution Width over Window's Base Width
    height_to_scale = developer_monitor_height / Decimal(given_height)
    scaled_width = user_screen_resolution_width / width_to_scale            #Current Screen Resolution Width over w
    scaled_height = user_screen_resolution_height / height_to_scale
    rounded_scaled_width = int(round(scaled_width))                         #Round scaled_with and convert it to be an integer (So using this to calculate the Minimum window size can also work)
    rounded_scaled_height = int(round(scaled_height))

    #It is fine to divide by the variables since they are considered Decimal objects and not int variables.    #Why dividing gives int numbers # https://docs.python.org/2.7/library/decimal.html#:~:text=getcontext().prec%20%3D%206%0A%3E%3E%3E-,Decimal(1)%20/%20Decimal(7),-Decimal(%270.142857%27)%0A%3E%3E%3E%20getcontext
    #Dividing the normal way is a hassle for me to properly do and figure out, so that is why basically every number variable is converted to a Decimal Object.

    return rounded_scaled_width, rounded_scaled_height # https://note.nkmk.me/en/python-function-return-multiple-values/


#Shifts the current window's focus to its child window.
def SetFocusToCurrentChildWindow(event, current_window, parent_window): # https://stackoverflow.com/questions/58328686/destroy-events-executes-the-binded-function-5-times
    if event.widget == current_window:
        #When the user clicks on the program on the taskbar, each window of this program will appear above other applications
        parent_window.lift() 
        current_window.lift()
        current_window.grab_set()
    pass


#Sets the focus back to the parent window when its child window is closed.
def OnWindowClose(e, window_parameter, parent_window_parameter):
    if e.widget == window_parameter: #Only do this code if the event widget is the current Toplevel() instance  # https://stackoverflow.com/questions/58328686/destroy-events-executes-the-binded-function-5-times
        window_parameter.grab_release() #Remove focus from the current window that is to be destroyed
        if parent_window_parameter != root_window: #Root window will regain focus when none of its child windows have been created
            parent_window_parameter.grab_set()
    pass


#Calculates what a widget's font size should be based on its owner window's size.
def InitialWindowFontSize(base_font_size, scaled_window_width, scaled_window_height, base_window_width, base_window_height, return_font=True):
    if scaled_window_width == base_window_width and scaled_window_height == base_window_height: #Don't do calculations if the width and height variable parameters are the same
        window_scaled_font_size = int(round(base_font_size))
    else:
        window_width_ratio = Decimal(scaled_window_width) / Decimal(base_window_width)
        window_height_ratio = Decimal(scaled_window_height) / Decimal(base_window_height)
        window_area_average = (window_width_ratio + window_height_ratio) / Decimal(2)
        window_scaled_font_size = int(round( base_font_size * window_area_average ))

    if return_font == True: #Return a Helvetica font with the calcuated font size instead.
        return ("Helvetica", window_scaled_font_size)

    return window_scaled_font_size




#Creates a window where the user chooses which section they want to add files to.
def ConfirmFileSection():
    confirm_section_box = Toplevel()
    confirm_section_box.resizable(width=False, height=False)
    confirm_box_base_width = 300
    confirm_box_base_height = 75
    WindowCenterPositioner(confirm_section_box, confirm_box_base_width, confirm_box_base_height)
    confirm_section_box.wm_title('Select A Section')

    confirm_box_font = InitialWindowFontSize(17, confirm_section_box.winfo_width(), confirm_section_box.winfo_height(), confirm_box_base_width, confirm_box_base_height)

    confirm_source = Button(confirm_section_box, text='SOURCE', font=confirm_box_font, command=lambda:[confirm_section_box.destroy(), ChosenFileSection(directory_type=source_section_dir, label_number=0)], bg=source_section_color, fg=source_section_text_color )
    confirm_replacement = Button(confirm_section_box, text='REPLACE', font=confirm_box_font, command=lambda:[confirm_section_box.destroy(), ChosenFileSection(directory_type=replacement_section_dir, label_number=1)], bg=replacement_section_color, fg=replacement_section_text_color)

    if switch_containers_placement == True:
        confirm_replacement.place(relwidth=0.5, relheight=1)
        confirm_source.place(relwidth=0.5, relheight=1, relx=0.5)
    else:
        confirm_source.place(relwidth=0.5, relheight=1)
        confirm_replacement.place(relwidth=0.5, relheight=1, relx=0.5)

    confirm_source.bind("<Enter>", HoveringOverWidget)
    confirm_source.bind("<Leave>", NotHoveringOverWidget)
    confirm_replacement.bind("<Enter>", HoveringOverWidget)
    confirm_replacement.bind("<Leave>", NotHoveringOverWidget)


#Finds the correct directory for the files and calls a function to add any selected files.
def ChosenFileSection(directory_type, label_number):
    selected_files = PickedFiles(CheckForSavedDirectory(directory_type), False)
    if len(selected_files) == 0: #If no files were chosen, return.
        return

    CreateNewLabels(selected_files, label_number)

    global comparing_labels_on
    if label_number == 0:
        move_position = source_section_scroll_position
        if comparing_labels_on == True:
            other_section_position = replacement_section_scroll_position
            other_section_label_list = label_replacement_list
            other_section_files = replacement_files
            other_section_color = replacement_section_color
            other_section_text_color = replacement_section_text_color
    elif label_number == 1:
        move_position = replacement_section_scroll_position
        if comparing_labels_on == True:
            other_section_position = source_section_scroll_position
            other_section_label_list = label_source_list
            other_section_files = source_files
            other_section_color = source_section_color
            other_section_text_color = source_section_text_color 

    #If a file(s) is added after the both section's files have been compared, this will make the other label section revert back to its section's color and naming
    if comparing_labels_on == True:
        other_section_file_index = other_section_position
        for label in other_section_label_list:
            other_section_name = os.path.basename(other_section_files[other_section_file_index])
            other_section_file_size = os.path.getsize(other_section_files[other_section_file_index])
            label.config(bg=other_section_color, fg=other_section_text_color, text=u'{2} | {0} | {1}'.format(other_section_name, ByteUnitConversion(other_section_file_size), (other_section_file_index + 1)), relief="raised")
            other_section_file_index += 1
        comparing_labels_on = False

    #This makes the label(s) appear in the correct position of their file index
    UpdateLabels(move_position, label_number)

    OverwriteDirectoryData(directory_type, selected_files[-1])


#Checks the config.ini file for any saved directories, so the user does not have to find the previously used directory multiple times.
def CheckForSavedDirectory(config_general_option):
    directory = os.path.split(os.getcwd())[0] #This gets the directory above the current directory of the program   # https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory/67509536#67509536
    saved_directory = config_parser.get(config_file_general_section, config_general_option)
    saved_directory = saved_directory.decode("utf-8") #Convert saved directory byte string into a unicode string

    if os.path.exists(saved_directory) == True: #Check if the given parameter's directory in the config.ini file exists
        directory = saved_directory
    else:
        if saved_directory != "": #Only display message if a directory was saved to the config.ini file
            text_display_string.set('File path does not/no longer exists.')

    return directory
    
    
#Returns a list of the file(s) or the directory the user selected.
def PickedFiles(chosen_directory, special_condition, extract_title=False):
    if special_condition == True:
        if extract_title == True:
            title_text = "Select a diretory to store the folder(s) that will house the extracted .hca files."
        else:
            title_text = 'Select a folder to store your replacement files. Your files will be filled with 00 bytes until its file size matches its source counterpart.'
        chosen_files = tkFileDialog.askdirectory(initialdir=chosen_directory, title=title_text)
    elif special_condition == 'UEXP':
        if extract_title == True:
            #This is a tuple - askopenfilenames
            chosen_files = tkFileDialog.askopenfilenames(initialdir=chosen_directory, title="Select a .uexp file", filetypes=(("UEXP File", "*.uexp"), ("All Files", "*.*")))
        else:
            #This is a unicode string - askopenfilename
            chosen_files = tkFileDialog.askopenfilename(initialdir=chosen_directory, title="Select a .uexp file", filetypes=(("UEXP File", "*.uexp"), ("All Files", "*.*")))
    else:
        chosen_files = tkFileDialog.askopenfilenames(initialdir=chosen_directory, title='Select the .hca file(s)', filetypes=(('HCA File', '*.hca'), ('All Files', '*.*')))
    return chosen_files


label_source_list = []
label_replacement_list = []
source_files = []
replacement_files = []
maximum_number_of_viewable_labels = 26
#Creates a new label for each file that was selected by the user.
def CreateNewLabels(files_to_add_list, id_number):
    if id_number == 0: #Source Section
        section_files = source_files
        section_label_list = label_source_list
        section_container = source_container
        section_title = source_container_title
    elif id_number == 1: #Replacement Section
        section_files = replacement_files
        section_label_list = label_replacement_list
        section_container = replacement_container
        section_title = replacement_container_title

    if automatically_sort_files == True:
        added_files = []
    else:
        added_files = section_files #These become attached, so anything that happens to added_files also happens to section_files, which also happens to source_files or replacement_files

    file_was_added = False
    for file in files_to_add_list:
        if file not in section_files: #This makes sure duplicate files aren't added and duplicate labels aren't created.
            file_was_added = True
            added_files.append(file)
            if len(section_label_list) < maximum_number_of_viewable_labels: #This makes sure that any labels that can't be seen won't be created
                section_label_list.append(Label(section_container, anchor='w', justify="right", padx=4, pady = 2, relief="raised"))
                section_label_list[-1].pack(fill="x") #Displays the just created label to the screen.
    if file_was_added == False:
        return


    if automatically_sort_files == True:
        added_files = natsorted(added_files, alg=ns.GROUPLETTERS) # https://natsort.readthedocs.io/en/master/examples.html#controlling-case-when-sorting
        section_files.extend(added_files) #Adds the sorted files to the already existing list    # https://www.kite.com/python/answers/how-to-append-one-list-to-another-list-in-python


    #Change the section's text based on the number of files added to it
    if len(section_files) == 1:
        section_container.config(text='{} - 1 File'.format(section_title) )
    else:
        section_container.config(text='{} - {} Files'.format(section_title, len(section_files)) )

    #Enables/Disables the bottom frame buttons of the root window
    remove_button.config(state="normal", bg=default_button_color, fg=default_button_text_color, relief="raised")
    if len(section_files) > 1:
        sort_button.config(state="normal", bg=default_button_color, fg=default_button_text_color, relief="raised")
        edit_menu.entryconfig(edit_menu_go_to_command_name, state="normal")
    if len(source_files) > 0 and len(replacement_files) > 0 and len(source_files) == len(replacement_files):
        compare_button.config(state="normal", bg=compare_button_color, fg=compare_button_text_color, relief="raised")
    else:
        compare_button.config(state="disabled", bg="gray", relief="sunken")
    fill_button.config(state="disabled", bg='gray', relief="sunken")

    #Resize the newly created labels to match the other resized labels (if resized at all)
    ResizeLabels(root_window.winfo_width(), root_window.winfo_height())


comparing_labels_on = False
#Updates every label's text information. The labels contain the index position of the section's file, the name of that file, as well as its file size.
def UpdateLabels(offset, id_number): #The "offset" parameter offsets the index that the label will display the files from
    if id_number == 0: #Source Section
        if len(source_files) == 0:
            return
        section_label_list = label_source_list
        section_displayed_files = source_files
        container = source_container
        color = source_section_color
        text_color = source_section_text_color 
        scroll_up_button = source_scroll_up_button
        scroll_down_button = source_scroll_down_button
    elif id_number == 1: #Replacement Section
        if len(replacement_files) == 0:
            return
        section_label_list = label_replacement_list
        section_displayed_files = replacement_files
        container = replacement_container
        color = replacement_section_color
        text_color = replacement_section_text_color
        scroll_up_button = replacement_scroll_up_button
        scroll_down_button = replacement_scroll_down_button

    update_file_index = offset
    label_index = 0
    newly_created_labels = []
    while label_index < len(section_label_list):
        #Moving Towards End of List
        if update_file_index >= len(section_displayed_files):
            if len(section_label_list) > 1:
                #Delete items in list
                section_label_list[label_index].destroy()
                section_label_list.pop(label_index)
            #Moved Down To End of List
            if (len(section_label_list) == 1):
                MoveArrowsActivation('Down', False, scroll_down_button)
                update_file_index = len(section_displayed_files) - 1 #There is 1 file that is shown but update_file_index = 0 because that is its index position in the list; the 1st file has an index of 0
            continue
        #Moving Up From End of List     (move_up_check must be at the end to not cause an error!)
        elif (update_file_index < len(section_displayed_files)-1) and (len(section_label_list) < maximum_number_of_viewable_labels) and (len(section_label_list) < len(section_displayed_files) and ( (direct_increment == True) or (move_up_check < 0) ) ) : #if (update_file_index < number of files (starting from index 0)) and (number of labels is < max number of labels to be shown) and (number of labels is < the number of files) and (increment is a negative number (pressed the up arrow))
            if comparing_labels_on == True: #Don't give text and color info since the CompareFiles() function will do that already.
                section_label_list.append(Label(container, anchor='w', justify="right", padx=4, pady = 2 ))
            else:
                file_name = os.path.basename(section_displayed_files[update_file_index])
                index_size = os.path.getsize(section_displayed_files[update_file_index])
                section_label_list.append(Label(container, bg=color, fg=text_color, anchor='w', justify="right", padx=4, pady = 2, relief="raised", text=u'{2} | {0} | {1}'.format(file_name , ByteUnitConversion(index_size), (update_file_index+1) ) ))

            section_label_list[-1].pack(fill="x")
            newly_created_labels.append(section_label_list[-1])
            continue
        #Moving Up or Down
        if comparing_labels_on == False: #Color and text string get changed anyways if comparing_labels_on == True
            #Update the labels with the corresponding file informaiton
            file_name = os.path.basename(section_displayed_files[update_file_index])
            index_size = os.path.getsize(section_displayed_files[update_file_index])
            section_label_list[label_index].config(bg=color, fg=text_color, text=u'{2} | {0} | {1}'.format(file_name, ByteUnitConversion(index_size), (update_file_index+1) ), relief="raised") #Label text is a unicode string so it can display unicode characters
        update_file_index += 1
        label_index += 1


    #Update the section's scroll position.
    def SetMovePosition(section_id, new_move_position):
        if section_id == 0:
            global source_section_scroll_position
            source_section_scroll_position = new_move_position
        elif section_id == 1:
            global replacement_section_scroll_position
            replacement_section_scroll_position = new_move_position


    new_pos = offset
    if new_pos >= len(section_displayed_files):
        new_pos = len(section_displayed_files) - 1
    
    if len(section_label_list) > 1:
        MoveArrowsActivation('Down', True, scroll_down_button, color, text_color)
    elif len(section_displayed_files) <= 1:
        MoveArrowsActivation('Up', False, scroll_up_button)
    SetMovePosition(id_number, new_pos)

    #Anytime Update labels is called, set the text box to be empty
    text_display_string.set("")

    if comparing_labels_on == True:
        ComparingFiles()

    if len(newly_created_labels) > 0: #If labels are created in this function, resize those created labels.
        used_created_labels = []
        for x in section_label_list: #The lower of the lists (in size) since newly_created_labels will be added until it reaches -> maximum_number_of_viewable_labels
            if x in newly_created_labels:
                used_created_labels.append(x)
            pass
        ResizeLabels(root_window.winfo_width(), root_window.winfo_height(), True, used_created_labels)
  
    pass


#Converts bytes from a file's file size to be KB, MB, GB, or TB. If the conversion variable is considered to be 0, then scientific notation is used.
def ByteUnitConversion(file_byte_size):
    if set_byte_unit == 1: #KB
        unit_string = 'KB'
    elif set_byte_unit == 2: #MB
        unit_string = 'MB'
    elif set_byte_unit == 3: #GB
        unit_string = 'GB'
    elif set_byte_unit == 4: #TB
        unit_string = 'TB'
    else: #Bytes
        unit_string = 'Bytes'

    divide_to_larger_unit = Decimal(1024 ** set_byte_unit) # 1024 ** 0 == 1
    conversion = Decimal(file_byte_size) / divide_to_larger_unit #file_byte_size / 1 == file_byte_size

    if round_to_decimal_position < 0 or set_byte_unit == 0:
        rounded_number = conversion #No rounding
    else:
        rounded_number = '{:.{}f}'.format(conversion, round_to_decimal_position) #jurajb's comment - https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places/6149115#6149115

    if Decimal(rounded_number) == 0 and conversion != 0:
        #Scientific Notation
        scientific_notation = '{:.{}e}'.format(conversion, round_to_decimal_position) # https://www.kite.com/python/answers/how-to-print-a-number-in-scientific-notation-in-python
        rounded_number = scientific_notation

    result = '{0} {1}'.format(rounded_number, unit_string)
    return result


#Overwrites the previously saved directory if the user selected the last chosen file from a different directory.
def OverwriteDirectoryData(overwrite_dir, directory_to_save):
    if overwrite_dir == finished_dir or overwrite_dir == extract_location_dir:
        saving_dir = os.path.join(os.path.dirname(directory_to_save), os.path.basename(directory_to_save))
    else:
        saving_dir = os.path.dirname(directory_to_save)
    saving_dir = saving_dir.encode("utf-8") #Convert the directory unicode string to a byte string
    
    if saving_dir != config_parser.get(config_file_general_section, overwrite_dir):
        config_parser.set(config_file_general_section, overwrite_dir, saving_dir)
        with open('config.ini', 'w') as outfile:
            config_parser.write(outfile)
    pass




source_section_scroll_position = 0
replacement_section_scroll_position = 0
#Uses the increment parameter to set the index position that the labels will be updated to.
def MoveFilesInSection(increment, id, set_increment_directly=False):
    move_position = 0
    if id == 0:
        move_position = source_section_scroll_position
        scroll_up_button = source_scroll_up_button
        scroll_color = source_section_color
        scroll_text_color = source_section_text_color 
        scroll_down_button = source_scroll_down_button
    elif id == 1:
        move_position = replacement_section_scroll_position
        scroll_up_button = replacement_scroll_up_button
        scroll_color = replacement_section_color
        scroll_text_color = replacement_section_text_color
        scroll_down_button = replacement_scroll_down_button
    #The return statements make sure the function doesn't proceed when it doesn't need to
    if (set_increment_directly == False) and ((increment <= 0 and scroll_up_button.cget('state') == 'disabled') or (increment > 0 and scroll_down_button.cget('state') == 'disabled')):
        return

    if set_increment_directly == True: #This is when using the "Go To" option under "Edit" in the menubar
        move_position = increment
    else:
        move_position += increment

    if move_position <= 0:
        move_position = 0
        MoveArrowsActivation('Up', False, scroll_up_button)
    else:
        MoveArrowsActivation('Up', True, scroll_up_button, scroll_color, scroll_text_color)

    global move_up_check
    move_up_check = increment
    global direct_increment
    direct_increment = set_increment_directly
    UpdateLabels(move_position, id)


#Sets the move buttons to be enabled or disabled depending on the inputed parameters.
def MoveArrowsActivation(arrow_direction, set_active_state, arrow_section, arrow_section_color='black', arrow_section_text_color="yellow"): # https://www.geeksforgeeks.org/default-arguments-in-python/
    #If the button is already active or is already disabled, return
    if ( (arrow_section.cget('state') == 'normal' and set_active_state == True) or (arrow_section.cget('state') == 'disabled' and set_active_state == False) ):
        return
    
    if arrow_direction.lower() == 'up':
        arrow2 = both_sections_up_arrow_button
        if both_scroll_buttons_same_color == True:
            if switch_scroll_buttons_placement == True:
                arrow2_color = both_down_scroll_button_color
                arrow2_text_color = both_down_scroll_button_text_color
            else:
                arrow2_color = both_up_scroll_button_color
                arrow2_text_color = both_up_scroll_button_text_color
        else:
            arrow2_color = both_up_scroll_button_color
            arrow2_text_color = both_up_scroll_button_text_color


        if arrow_section == source_scroll_up_button:
            arrow3 = to_first_source_file_button
        elif arrow_section == replacement_scroll_up_button:
            arrow3 = to_first_replacement_file_button

        if to_file_buttons_same_color == True:
            if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                arrow3_color = to_last_replacement_file_button_color
                arrow3_text_color = to_last_replacement_file_button_text_color
            elif switch_containers_placement == True:
                arrow3_color = to_first_replacement_file_button_color
                arrow3_text_color = to_first_replacement_file_button_text_color
            elif switch_scroll_buttons_placement == True:
                arrow3_color = to_last_source_file_button_color
                arrow3_text_color = to_last_source_file_button_text_color
            else:
                arrow3_color = to_first_source_file_button_color
                arrow3_text_color = to_first_source_file_button_text_color
            pass
        else:
            if arrow_section == source_scroll_up_button:
                arrow3_color = to_first_source_file_button_color
                arrow3_text_color = to_first_source_file_button_text_color
            elif arrow_section == replacement_scroll_up_button:
                arrow3_color = to_first_replacement_file_button_color
                arrow3_text_color = to_first_replacement_file_button_text_color

        up_condition = True
    elif arrow_direction.lower() == 'down':
        arrow2 = both_sections_down_arrow_button
        if both_scroll_buttons_same_color == True:
            if switch_scroll_buttons_placement == True:
                arrow2_color = both_down_scroll_button_color
                arrow2_text_color = both_down_scroll_button_text_color
            else:
                arrow2_color = both_up_scroll_button_color
                arrow2_text_color = both_up_scroll_button_text_color
        else:
            arrow2_color = both_down_scroll_button_color
            arrow2_text_color = both_down_scroll_button_text_color


        if arrow_section == source_scroll_down_button:
            arrow3 = to_last_source_file_button
        elif arrow_section == replacement_scroll_down_button:
            arrow3 = to_last_replacement_file_button

        if to_file_buttons_same_color == True:
            if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                arrow3_color = to_last_replacement_file_button_color
                arrow3_text_color = to_last_replacement_file_button_text_color
            elif switch_containers_placement == True:
                arrow3_color = to_first_replacement_file_button_color
                arrow3_text_color = to_first_replacement_file_button_text_color
            elif switch_scroll_buttons_placement == True:
                arrow3_color = to_last_source_file_button_color
                arrow3_text_color = to_last_source_file_button_text_color
            else:
                arrow3_color = to_first_source_file_button_color
                arrow3_text_color = to_first_source_file_button_text_color
            pass
        else:
            if arrow_section == source_scroll_down_button:
                arrow3_color = to_last_source_file_button_color
                arrow3_text_color = to_last_source_file_button_text_color

            elif arrow_section == replacement_scroll_down_button:
                arrow3_color = to_last_replacement_file_button_color
                arrow3_text_color = to_last_replacement_file_button_text_color

        up_condition = False


    if set_active_state == True:
        arrow_section.config(bg=arrow_section_color, fg=arrow_section_text_color, state="normal", relief="raised")
        arrow2.config(bg=arrow2_color, fg=arrow2_text_color, state="normal", relief="raised")
        arrow3.config(bg=arrow3_color, fg=arrow3_text_color, state="normal", relief="raised")
    else:
        arrow_section.config(bg='gray', state="disabled", relief="sunken")
        arrow3.config(bg='gray', state="disabled", relief="sunken")
        if ( (up_condition == True and source_scroll_up_button.cget('state') == 'disabled' and replacement_scroll_up_button.cget('state') == 'disabled') or (up_condition == False and source_scroll_down_button.cget('state') == 'disabled' and replacement_scroll_down_button.cget('state') == 'disabled') ):
            arrow2.config(bg='gray', state="disabled", relief="sunken")

    pass




#Creates a window where the user can choose which section's files to sort.
def SortFiles():
    global sorting_source_files
    global sorting_replacement_files
    global sort_listbox_used
    global sorting_files_list_used

    sorting_window = Toplevel()
    sorting_window_base_width = Decimal(600)
    sorting_window_base_height = Decimal(400)
    sorting_window.minsize( sorting_window_base_width / Decimal(2), sorting_window_base_height / Decimal(2) )
    WindowCenterPositioner(sorting_window, sorting_window_base_width, sorting_window_base_height)
    sorting_window.wm_title('Select Files To Sort   (Press "-" or "+" to get the last index)')

    sorting_window_listbox_font_size = int(round( Decimal(9) *( Decimal(sorting_window.winfo_width()) / Decimal(sorting_window_base_width) )  ))
    sorting_window_listbox_font = ("Helvetica", sorting_window_listbox_font_size)

    sorting_window_10_font = InitialWindowFontSize(10, sorting_window.winfo_width(), sorting_window.winfo_height(), sorting_window_base_width, sorting_window_base_height)
    sorting_window_12_font = InitialWindowFontSize(12, sorting_window.winfo_width(), sorting_window.winfo_height(), sorting_window_base_width, sorting_window_base_height)
    sorting_window_16_font = InitialWindowFontSize(16, sorting_window.winfo_width(), sorting_window.winfo_height(), sorting_window_base_width, sorting_window_base_height)

    remove_listbox_file_display_frame = Frame(sorting_window)
    remove_listbox_file_display_frame.place(relwidth=1, relheight=0.7)

    sorting_files_buttons_frame = Frame(sorting_window)
    sorting_files_buttons_frame.place(relwidth=1, relheight=0.3, rely=0.7)


    #Use the natural/human sorting from the natsort module and apply it to every file in the chosen section.
    def AutomaticallySortFiles(section):
        global sorting_files_list_used
        if section == 0:
            global sorting_source_files
            sorting_files_list_used = sorting_source_files = list(source_natural_sort)

            source_sort_listbox_is_disabled = False
            if source_sort_listbox.cget("state") == "disabled":
                source_sort_listbox.config(state="normal")
                source_sort_listbox_is_disabled = True

            ApplySort()

            if source_sort_listbox_is_disabled == True:
                source_sort_listbox.config(state="disabled")
        else:
            global sorting_replacement_files
            sorting_files_list_used = sorting_replacement_files = list(replacement_natural_sort)

            replacement_sort_listbox_is_disabled = False
            if replacement_sort_listbox.cget("state") == "disabled":
                replacement_sort_listbox.config(state="normal")
                replacement_sort_listbox_is_disabled = True

            ApplySort()

            if replacement_sort_listbox_is_disabled == True:
                replacement_sort_listbox.config(state="disabled")

        text_display_string.set("Files have been automatically sorted!")
        pass


    if len(source_files) > 1:
        sorting_source_frame = LabelFrame(remove_listbox_file_display_frame, text='{} - {} Files'.format(source_container_title, len(source_files)), font=sorting_window_12_font, bg=source_section_color, fg=source_section_text_color )
        source_sort_listbox = Listbox(sorting_source_frame, bg=source_section_color, fg=source_section_text_color , selectmode="extended", font=sorting_window_listbox_font)
        number_index = 1
        for item in source_files:
            source_sort_listbox.insert("end", u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), number_index)) #If a listbox is disabled, nothing will be inserted. It has to be disable afterwards.
            number_index += 1

        source_sort_scrollbar = ttk.Scrollbar(sorting_source_frame, command=source_sort_listbox.yview)
        source_sort_x_axis_scrollbar = ttk.Scrollbar(sorting_source_frame, orient = "horizontal", command=source_sort_listbox.xview)
        source_sort_scrollbar.pack(side="right", fill="y")
        source_sort_x_axis_scrollbar.pack(side="bottom", fill="x")
        source_sort_listbox.config(yscrollcommand = source_sort_scrollbar.set, xscrollcommand = source_sort_x_axis_scrollbar.set, state='disabled')
        source_sort_listbox.pack(fill="both", expand="y")
        
        source_natural_sort = natsorted(source_files, alg=ns.GROUPLETTERS)
        auto_sort_source_files_button = Button(sorting_files_buttons_frame, command=lambda: AutomaticallySortFiles(0), text='Auto Sort\nSource Files', font=sorting_window_12_font, bg=source_section_color, fg=source_section_text_color )
        if source_natural_sort == source_files:
            auto_sort_source_files_button.config(state="disabled", bg="gray", fg="black")
        sorting_source_files = list(source_files)
    if len(replacement_files) > 1:
        sorting_replacement_frame = LabelFrame(remove_listbox_file_display_frame, text='{} - {} Files'.format(replacement_container_title, len(replacement_files)), font=sorting_window_12_font, bg = replacement_section_color, fg=replacement_section_text_color)
        replacement_sort_listbox = Listbox(sorting_replacement_frame, bg=replacement_section_color, fg=replacement_section_text_color, selectmode="extended", font=sorting_window_listbox_font)
        number_index = 1
        for item in replacement_files:
            replacement_sort_listbox.insert("end", u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), number_index))
            number_index += 1

        replacement_sort_scrollbar = ttk.Scrollbar(sorting_replacement_frame, command=replacement_sort_listbox.yview)
        replacement_sort_x_axis_scrollbar = ttk.Scrollbar(sorting_replacement_frame, orient = "horizontal", command=replacement_sort_listbox.xview)
        replacement_sort_scrollbar.pack(side="right", fill="y")
        replacement_sort_x_axis_scrollbar.pack(side="bottom", fill="x")
        replacement_sort_listbox.config(yscrollcommand = replacement_sort_scrollbar.set, xscrollcommand = replacement_sort_x_axis_scrollbar.set, state='disabled')
        replacement_sort_listbox.pack(fill="both", expand="y")
        
        replacement_natural_sort = natsorted(replacement_files, alg=ns.GROUPLETTERS)
        auto_sort_replacement_files_button = Button(sorting_files_buttons_frame, command=lambda: AutomaticallySortFiles(1), text='Auto Sort\nReplacement Files', font=sorting_window_10_font, bg=replacement_section_color, fg=replacement_section_text_color)
        if replacement_natural_sort == replacement_files:
            auto_sort_replacement_files_button.config(state="disabled", bg="gray", fg="black")
        sorting_replacement_files = list(replacement_files)
        
    

    sort_listbox_used = None
    #Determines which listbox will have it's files be sorted.
    def ChangeSortListboxUsed(event):
        global sort_listbox_used
        if manual_sort_files_button.cget("state") == "disabled":
            if event.widget.cget("state") == "normal" and len(event.widget.curselection()) > 0:
                manual_sort_files_button.config(state="normal")
                if sort_listbox_used == None: #If true, continue on
                    pass
                elif sort_listbox_used == replacement_sort_listbox:
                    manual_sort_files_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
                else:
                    manual_sort_files_button.config(bg=source_section_color, fg=source_section_text_color )
            else:
                return

        if sort_listbox_used != event.widget:
            sort_listbox_used = event.widget
        else:
            return


        global sorting_source_files
        global sorting_replacement_files
        global sorting_files_list_used

        if sort_listbox_used == replacement_sort_listbox:
            sorting_files_list_used = sorting_replacement_files
            manual_sort_files_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
        else:
            sorting_files_list_used = sorting_source_files
            manual_sort_files_button.config(bg=source_section_color, fg=source_section_text_color )

        pass


    if len(source_files) > 1 and len(replacement_files) > 1:
        if switch_containers_placement == True:
            sorting_replacement_frame.place(relwidth=0.5, relheight=1)
            sorting_source_frame.place(relwidth=0.5, relheight=1, relx=0.5)
        else:
            sorting_source_frame.place(relwidth=0.5, relheight=1)
            sorting_replacement_frame.place(relwidth=0.5, relheight=1, relx=0.5)

        auto_sort_source_files_button.place(relwidth=0.2, relheight=0.5, relx=0.8)
        auto_sort_replacement_files_button.place(relwidth=0.2, relheight=0.5, relx=0.8, rely=0.5)

        sorting_list_used_id = 3
        source_sort_listbox.bind("<<ListboxSelect>>", ChangeSortListboxUsed) # https://tk-tutorial.readthedocs.io/en/latest/listbox/listbox.html#listboxselect-callback-function
        replacement_sort_listbox.bind("<<ListboxSelect>>", ChangeSortListboxUsed)
    elif len(source_files) > 1:
        sorting_source_frame.place(relwidth=1, relheight=1)
        auto_sort_source_files_button.place(relwidth=0.2, relheight=1, relx=0.8)
        sort_listbox_used = source_sort_listbox
        sorting_list_used_id = 1
        sorting_files_list_used = sorting_source_files
    elif len(replacement_files) > 1:
        sorting_replacement_frame.place(relwidth=1, relheight=1)
        auto_sort_replacement_files_button.place(relwidth=0.2, relheight=1, relx=0.8)
        sort_listbox_used = replacement_sort_listbox
        sorting_list_used_id = 2
        sorting_files_list_used = sorting_replacement_files


    global manual_sort_files_button
    manual_sort_files_button = Button(sorting_files_buttons_frame, command=lambda:MoveFilesToNewIndex(sort_listbox_used, sort_files_user_input, sorting_files_list_used, sorting_list_used_id), text='Move File(s)', font=sorting_window_12_font, bg="gray", fg="black", state="disabled")
    manual_sort_files_button.place(relwidth=0.3, relheight=0.5)
    manual_sort_files_button.bind("<Enter>", HoveringOverWidget)
    manual_sort_files_button.bind("<Leave>", NotHoveringOverWidget)


    #Apply and use the manually sorted files.
    def ApplySort():
        global source_files
        global replacement_files
        global comparing_labels_on

        if len(source_files) > 1:
            if source_files != sorting_source_files:
                comparing_labels_on = False
                source_files = list(sorting_source_files) #This - "list()" - is important, otherwise sorting_source_files and source_files become attached, so when the MoveFilesToNewIndex fucntion happens, source_files gets its values changed as well when it should not.
                if source_natural_sort == source_files:
                    auto_sort_source_files_button.config(state="disabled", bg="gray", fg="black")
                else:
                    auto_sort_source_files_button.config(state="normal", bg=source_section_color, fg=source_section_text_color)
                source_sort_listbox.delete(0, 'end')
                number_index = 1
                for item in source_files:
                    source_sort_listbox.insert("end", u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), number_index)) #If a listbox is disabled, nothing will be inserted. It has to be disable afterwards.
                    number_index += 1
                UpdateLabels(source_section_scroll_position, 0)
                comparing_labels_on = True
            elif comparing_labels_on == True:
                comparing_labels_on = False
                UpdateLabels(source_section_scroll_position, 0)
                comparing_labels_on = True
            pass

        if len(replacement_files) > 1:
            if replacement_files != sorting_replacement_files:
                comparing_labels_on = False
                replacement_files = list(sorting_replacement_files)
                if replacement_natural_sort == replacement_files:
                    auto_sort_replacement_files_button.config(state="disabled", bg="gray", fg="black")
                else:
                    auto_sort_replacement_files_button.config(state="normal", bg=replacement_section_color, fg=replacement_section_text_color)
                replacement_sort_listbox.delete(0, 'end')
                number_index = 1
                for item in replacement_files:
                    replacement_sort_listbox.insert("end", u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), number_index))
                    number_index += 1
                UpdateLabels(replacement_section_scroll_position, 1)
            elif comparing_labels_on == True:
                comparing_labels_on = False
                UpdateLabels(replacement_section_scroll_position, 1)
            pass

        if len(source_files) > 0 and len(replacement_files) > 0:
            compare_button.config(state="normal", bg=compare_button_color, fg=compare_button_text_color, relief="raised")
            fill_button.config(state="disabled", bg='gray', relief="sunken")
            
        comparing_labels_on = False
        sort_files_user_input.delete(0, 'end')
        save_sort_changes_button.config(bg="gray", fg="black", state="disabled")
        text_display_string.set("Files have been manually sorted!")
        pass


    global save_sort_changes_button
    save_sort_changes_button = Button(sorting_files_buttons_frame, command=ApplySort, text='Apply Changes', font=sorting_window_12_font, bg="gray", fg="black", state="disabled")
    save_sort_changes_button.place(relwidth=0.3, relheight=0.5, rely=0.5)
    save_sort_changes_button.bind("<Enter>", HoveringOverWidget)
    save_sort_changes_button.bind("<Leave>", NotHoveringOverWidget)


    sort_files_user_input = Entry(sorting_files_buttons_frame, justify="center", font=sorting_window_16_font, relief="ridge", bd=5)
    #Allow only decimal numbers to be inputed into the Entry widget. Pressing the - or + keys will give the length of the section that is the largest of the two.
    def DecimalNumberInputedInEntryWidget(action_code, inputed_string_character, text_change_allowed, text_before_change):
        if action_code == "1": #Inputing
            try:
                if inputed_string_character == "-" or inputed_string_character == "+":
                    if len(replacement_files) > len(source_files):
                        use_lentgh = len(replacement_files)
                    else:
                        use_lentgh = len(source_files)

                    if text_before_change == str(use_lentgh):
                        return False
                    sort_files_user_input.delete(0, "end")
                    sort_files_user_input.insert(0, use_lentgh)
                    sort_files_user_input.after_idle(lambda: sort_files_user_input.config(validate='key') )
                else:
                    int(inputed_string_character)
            except:
                return False

            if len(source_files) > 1:
                source_sort_listbox.config(state='normal')
            if len(replacement_files) > 1:
                replacement_sort_listbox.config(state='normal')

            if False == ( len(source_files) > 1 and len(replacement_files) > 1 ):
                manual_sort_files_button.config(state="normal")
                if len(source_files) > 1:
                    manual_sort_files_button.config(bg=source_section_color, fg=source_section_text_color )
                elif len(replacement_files) > 1:
                    manual_sort_files_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
            else:
                if sort_listbox_used != None and len(sort_listbox_used.curselection()) > 0:
                    manual_sort_files_button.config(state="normal")
                    if sort_listbox_used == replacement_sort_listbox:
                        manual_sort_files_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
                    else:
                        manual_sort_files_button.config(bg=source_section_color, fg=source_section_text_color )
                pass

        elif action_code == "0": #Deleting
            if text_change_allowed == "":
                manual_sort_files_button.config(state="disabled", bg="gray", fg="black")
                if len(source_files) > 1:
                    source_sort_listbox.config(state='disabled')
                if len(replacement_files) > 1:
                    replacement_sort_listbox.config(state='disabled')

        return True
    decimal_number_input_check = (sort_files_user_input.register(DecimalNumberInputedInEntryWidget),'%d', '%S', '%P', '%s')
    sort_files_user_input.config(validate='key', validatecommand=decimal_number_input_check)
    sort_files_user_input.place(relwidth=0.5, relheight=1, relx=0.3)
    sort_files_user_input.focus_set() #Set focus to the sort window's entry widget


    #Resize the text in the Sort Window
    def ResizeSortWindowText(event):
        if (event.widget == sorting_window):
            global sorting_window_previous_width
            global sorting_window_previous_height
            if (event.width != sorting_window_previous_width) or (event.height != sorting_window_previous_height): # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
                sorting_window_previous_width = event.width
                sorting_window_previous_height = event.height
    
                listbox_filename_font_size = int(round( Decimal(9) *( Decimal(event.width) / Decimal(sorting_window_base_width) )  ))

                sort_window_width_ratio = Decimal(event.width) / Decimal(sorting_window_base_width)
                sort_window_height_ratio = Decimal(event.height) / Decimal(sorting_window_base_height)
                sort_window_area_average = (sort_window_width_ratio + sort_window_height_ratio) / Decimal(2)

                sort_window_buttons_12_font = ("Helvetica", int(round(Decimal(12) * sort_window_area_average)) )
                sort_window_entry_16_font = ("Helvetica", int(round(Decimal(16) * sort_window_area_average)) )
    
                manual_sort_files_button.config(font=sort_window_buttons_12_font)
                save_sort_changes_button.config(font=sort_window_buttons_12_font)
                sort_files_user_input.config(font=sort_window_entry_16_font)

                if len(source_files) > 0:
                    sorting_source_frame.config(font=sort_window_buttons_12_font)
                    source_sort_listbox.config(font=("Helvetica", listbox_filename_font_size))
                    auto_sort_source_files_button.config(font=sort_window_buttons_12_font)
    
                if len(replacement_files) > 0:
                    sorting_replacement_frame.config(font=sort_window_buttons_12_font)
                    replacement_sort_listbox.config(font=("Helvetica", listbox_filename_font_size ))
                    sort_window_sort_replacement_button_10_font = ("Helvetica", int(round(Decimal(10) * sort_window_area_average)) )
                    auto_sort_replacement_files_button.config(font=sort_window_sort_replacement_button_10_font)    
                pass
        pass
    
    
    global sorting_window_previous_width
    sorting_window_previous_width = sorting_window.winfo_width()
    global sorting_window_previous_height
    sorting_window_previous_height = sorting_window.winfo_height()
    sorting_window.bind('<Configure>', ResizeSortWindowText)

    sorting_window.mainloop()


#Sorts listbox containing the filename's of its section's files to present to the user what the new, sorted positions of the files will be.
def MoveFilesToNewIndex(sort_listbox, input_widget, files_sorting_list, sorting_list_id):
    try:
        files_to_sort_at_index = int(input_widget.get()) - 1
    except:
        text_display_string.set("No index inputed to move file(s) to.")
        return

    if sort_listbox == None or len(sort_listbox.curselection()) == 0:
        text_display_string.set("No file(s) selected to sort.")
        return
    else:
        text_display_string.set("")

    if files_sorting_list == None:
        return

    temp_displayed_files = list(files_sorting_list)
    if files_to_sort_at_index < 0:
        files_to_sort_at_index = 0
    elif files_to_sort_at_index >= len(temp_displayed_files):
        files_to_sort_at_index = len(temp_displayed_files)-1
        pass

    input_widget.delete(0, "end")
    input_widget.insert(0, files_to_sort_at_index+1)

    if len(sort_listbox.curselection()) == 1:
        file_currently_selected_to_sort = (sort_listbox.curselection())[0]
        if temp_displayed_files[file_currently_selected_to_sort] == temp_displayed_files[files_to_sort_at_index]:
            return

    for x in reversed(sort_listbox.curselection()):
        jindex = 0
        for y in files_sorting_list:
            if y == temp_displayed_files[x]:
                files_sorting_list.pop(jindex)
                break
            jindex += 1
        files_sorting_list.insert(files_to_sort_at_index, temp_displayed_files[x])


    if files_sorting_list == temp_displayed_files:
        return

    original_text_from_listbox = sort_listbox.get(0, "end")
    global sorting_source_files
    global sorting_replacement_files
    if sorting_list_id == 3:
        if files_sorting_list == sorting_replacement_files:
            unsorted_list = replacement_files
        else:
            unsorted_list = source_files
        pass
    elif sorting_list_id == 1:
        unsorted_list = source_files
    elif sorting_list_id == 2:
        unsorted_list = replacement_files

    sort_listbox.delete(0, "end")
    list_box_add_index = 1
    for new_item in files_sorting_list:
        old_item_index = 0
        for old_item in unsorted_list:
            if old_item == new_item:
                get_number = int(Decimal.log10(Decimal(old_item_index+1)) ) + 1 # https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
                original_index = (original_text_from_listbox[old_item_index])[:get_number]
                break
            old_item_index += 1

        if int(list_box_add_index) == int(original_index):
            sort_listbox.insert("end",u'{2} | {0} | {1}'.format(os.path.basename(new_item), ByteUnitConversion(os.path.getsize(new_item)), original_index))
        else:
            sort_listbox.insert("end",u'{2} <- {3} | {0} | {1}'.format(os.path.basename(new_item), ByteUnitConversion(os.path.getsize(new_item)), list_box_add_index, original_index))
        list_box_add_index += 1


    if len(source_files) > 1 and len(replacement_files) > 1:
        if sorting_source_files == source_files and sorting_replacement_files == replacement_files:
            save_sort_changes_button.config(state="disabled", bg="gray", fg="black")
            return
    elif len(source_files) > 1:
        if sorting_source_files == source_files:
            save_sort_changes_button.config(state="disabled", bg="gray", fg="black")
            return
    elif len(replacement_files) > 1:
        if sorting_replacement_files == replacement_files:
            save_sort_changes_button.config(state="disabled", bg="gray", fg="black")
            return

    save_sort_changes_button.config(state="normal", bg=default_button_color, fg=default_button_text_color)




#Compares the file sizes between the two sections. If the replacement file size is good to go, then both files at the same index are colored green. If not, they are colored red.
def ComparingFiles():
    global comparing_labels_on
    comparing_labels_on = False
    #If there isn't an equal amount of files in both sections, this lets the user know.
    if len(source_files) != len(replacement_files):
        text_box_string = "You didn't choose an equal amount of files!\nSource: {0} | Replace: {1}".format(len(source_files), len(replacement_files))
    else:
        comparing_labels_on = True
        file_index=0
        amount_of_fillable_files=0
        source_label_stop = False
        replacement_label_stop = False
        
        while file_index < len(source_files):
            #Instead of having another while loop to add amount_of_fillable_files, this will all be done in one while loop.
            if os.path.getsize(source_files[file_index]) >= os.path.getsize(replacement_files[file_index]):
                amount_of_fillable_files += 1
            if source_label_stop == True and replacement_label_stop == True:
                file_index+=1
                continue

            #These if and elses are to make sure an error does not occur if the user compares the files when the label lists are less than the displayed files lists ( Ex: len(label_source_list) < len(source_files) )
            if file_index >= len(label_source_list):
                source_label_stop = True
            else:
                source_element = label_source_list[file_index]
                s_index = source_section_scroll_position + file_index
                s_name = os.path.basename(source_files[s_index])
                s_file = os.path.getsize(source_files[s_index])
                r_compare = os.path.getsize(replacement_files[s_index])   #This makes sure the source file size is accurately comparing itself to its replacement counterpart
                
            if file_index >= len(label_replacement_list):
                replacement_label_stop = True
            else:
                replacement_element = label_replacement_list[file_index]
                r_index = replacement_section_scroll_position + file_index
                r_name = os.path.basename(replacement_files[r_index])
                r_file = os.path.getsize(replacement_files[r_index])
                s_compare = os.path.getsize(source_files[r_index])        #This makes sure the replacement file size is accurately comparing itself to its source counterpart
                
            #Source Section
            if source_label_stop == False:
                if s_file >= r_compare:
                    source_element.config(bg=compare_O_label_color, fg=compare_O_label_text_color, text=u'O | {2} | {0} | {1}'.format(s_name, ByteUnitConversion(s_file), (s_index + 1)), relief="raised" )
                elif s_file < r_compare:
                    source_element.config(bg=compare_X_label_color, fg=compare_X_label_text_color, text=u'X | {2} | {0} | {1}'.format(s_name, ByteUnitConversion(s_file), (s_index + 1)), relief="sunken" )

            #Replacement Section
            if replacement_label_stop == False:
                if r_file <= s_compare:
                    replacement_element.config(bg=compare_O_label_color, fg=compare_O_label_text_color, text=u'O | {2} | {0} | {1}'.format(r_name, ByteUnitConversion(r_file), (r_index + 1)), relief="raised"  )
                elif r_file > s_compare:
                    replacement_element.config(bg=compare_X_label_color, fg=compare_X_label_text_color, text=u'X | {2} | {0} | {1}'.format(r_name, ByteUnitConversion(r_file), (r_index + 1)), relief="sunken" )
            file_index+=1
        
        if amount_of_fillable_files > 0:
            if amount_of_fillable_files == len(source_files):
                compare_message = 'All files are ready to be filled!'
            else:
                compare_message = '{0} out of the {1} files are ready to be filled!'.format(amount_of_fillable_files, len(source_files))
            fill_button.config(state="normal", bg=fill_button_color, fg=fill_button_text_color, relief="raised")
            compare_button.config(bg='gray', state="disabled", relief="sunken")
            text_box_string =  compare_message
        else:
            fill_button.config(state="disabled", bg='gray', relief="sunken")
            text_box_string = 'All {0} replacement files are bigger than their source counterpart!'.format(len(source_files))
    
    text_display_string.set(text_box_string)


#Gets a directory chosen by the user where the filled replacement files will be and calls a function that fills the replacement files.
def FinishedDirectory():
    finished_hca_files = PickedFiles(CheckForSavedDirectory(finished_dir), True)
    if not finished_hca_files: #If no directory was chosen
        text_box_string = 'Canceled. File section_container not chosen.'
    else:
        OverwriteDirectoryData(finished_dir, finished_hca_files)
        FillingFiles(finished_hca_files, CheckForSavedDirectory(replacement_section_dir))
        text_box_string = 'Replacement files are filled!'
        root_window.bell()

    text_display_string.set(text_box_string)


#Fills good to go replacement files with "\x00" bytes to match its corresponding Source File file size and moves all filled files to the "finished" directory. Replacement files that are larger than their source counterpart do not get filled nor moved.
def FillingFiles(filled_files_directory, replacement_files_directory):
    if filled_files_directory != replacement_files_directory: #This is here so it is only called once and doesn't check everytime in the loop if the files are equal to each other (I think using a bool is better for this sistaution, but it may just be uncessary).
        move_filled_files = True
    else:
        move_filled_files = False

    index = 0
    while index < len(source_files):
        source_size = os.path.getsize(source_files[index])
        replacement_size = os.path.getsize(replacement_files[index])      
        if replacement_size < source_size:
            #Fill Bytes
            with open(replacement_files[index], 'ab+') as fill_replacement_file:
                fill_replacement_file.write('\x00'*(source_size - replacement_size))
        elif replacement_size == source_size:
            pass
        else:
            index += 1
            continue

        #Only move the files if the replacement files directory and filling directory is different, else just replace the files already there.
        if move_filled_files == True:
            #Moves filled files to the "finished" directory
            move_to = os.path.abspath( os.path.join(filled_files_directory, os.path.basename(replacement_files[index])) )
            shutil.move(os.path.abspath(replacement_files[index]), move_to)    

        #Filled files are then removed from the lists
        source_files.pop(index)
        replacement_files.pop(index)

    global comparing_labels_on
    comparing_labels_on = False
    if len(source_files) == 0: #Same length as replacement_files since both get removed
        DeleteAllLabels(2)
    else:
        UpdateLabels(source_section_scroll_position, 0)
        UpdateLabels(replacement_section_scroll_position, 1)

    DisableRootButtons()



#Determines if the buttons of the root window should be disabled.
def DisableRootButtons():
    source_files_length = len(source_files)
    replacement_files_length = len(replacement_files)
    #DEL button
    if source_files_length == 0 and replacement_files_length == 0:
        remove_button.config(state="disabled", bg='gray', relief="sunken")
    #COMPARE button
    if source_files_length != replacement_files_length or (source_files_length == 0 or replacement_files_length == 0):
        compare_button.config(state="disabled", bg='gray', relief="sunken")
    else:
        compare_button.config(state="normal", bg=compare_button_color, fg=compare_button_text_color, relief="raised")
    #SORT button
    if source_files_length <= 1 and replacement_files_length <= 1:
        edit_menu.entryconfig(edit_menu_go_to_command_name, state="disabled")
        sort_button.config(state="disabled", bg='gray', relief="sunken")
    #FILL button
    fill_button.config(state="disabled", bg='gray', relief="sunken")



#Creates a window containing listboxes for each section where the user can choose which files to delete.
def RemoveSelection():
    global remove_box
    remove_box = Toplevel()
    remove_box_base_width = Decimal(600)
    remove_box_base_height = Decimal(400)
    remove_box.minsize( remove_box_base_width / Decimal(2), remove_box_base_height / Decimal(2) )

    WindowCenterPositioner(remove_box, remove_box_base_width, remove_box_base_height)
    remove_box_listbox_font_size = int(round( Decimal(9) *( Decimal(remove_box.winfo_width()) / Decimal(remove_box_base_width) )  ))
    remove_box_listbox_font = ("Helvetica", remove_box_listbox_font_size)
    remove_box_9_font = InitialWindowFontSize(9, remove_box.winfo_width(), remove_box.winfo_height(), remove_box_base_width, remove_box_base_height)
    remove_box_12_font = InitialWindowFontSize(12, remove_box.winfo_width(), remove_box.winfo_height(), remove_box_base_width, remove_box_base_height)
    remove_box.wm_title('Select Files To Remove')

    
    remove_listbox_file_display_frame = Frame(remove_box)
    remove_listbox_file_display_frame.place(relwidth=1, relheight=0.7)

    remove_buttons_frame = Frame(remove_box)
    remove_buttons_frame.place(relwidth=1, relheight=0.3, rely=0.7)


    global removal_source_frame
    global removal_source_listbox
    if len(source_files) > 0:
        removal_source_frame = LabelFrame(remove_listbox_file_display_frame, font=remove_box_12_font, bg=source_section_color, fg=source_section_text_color )
        if len(source_files) == 1:
            removal_source_frame.config(text='{} - 1 File'.format(source_container_title) )
        else:
            removal_source_frame.config(text='{} - {} Files'.format(source_container_title, len(source_files)) )
        removal_source_listbox = Listbox(removal_source_frame, bg=source_section_color, fg=source_section_text_color , selectmode="extended", font=remove_box_listbox_font)
        si = 1
        for item in source_files:
            removal_source_listbox.insert("end",u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), si ))
            si += 1

        # https://www.geeksforgeeks.org/how-to-make-a-proper-double-scrollbar-frame-in-tkinter/
        removal_source_scrollbar = ttk.Scrollbar(removal_source_frame, command=removal_source_listbox.yview)
        removal_source_x_axis_scrollbar = ttk.Scrollbar(removal_source_frame, orient = "horizontal", command=removal_source_listbox.xview)
        removal_source_scrollbar.pack(side="right", fill="y")
        removal_source_x_axis_scrollbar.pack(side="bottom", fill="x")
        removal_source_listbox.config(yscrollcommand = removal_source_scrollbar.set, xscrollcommand = removal_source_x_axis_scrollbar.set)

        removal_source_listbox.pack(fill="both", expand="y")

        removal_source_delete_button = Button(remove_buttons_frame, command=lambda:DeleteFunction(0), bg=source_section_color, fg=source_section_text_color , text='Delete Selected\nSource File(s)', font=remove_box_12_font)
        removal_source_delete_all_button = Button(remove_buttons_frame, command=lambda:DeleteAllListboxItems(0), bg=default_button_color, fg=default_button_text_color, text='Delete All Source Files', font=remove_box_9_font)

        removal_source_delete_button.bind("<Enter>", HoveringOverWidget)
        removal_source_delete_button.bind("<Leave>", NotHoveringOverWidget)
        removal_source_delete_all_button.bind("<Enter>", HoveringOverWidget)
        removal_source_delete_all_button.bind("<Leave>", NotHoveringOverWidget)


    global removal_replacement_frame
    global removal_replacement_listbox
    if len(replacement_files) > 0:
        removal_replacement_frame = LabelFrame(remove_listbox_file_display_frame, font=remove_box_12_font, bg = replacement_section_color, fg=replacement_section_text_color)
        if len(replacement_files) == 1:
            removal_replacement_frame.config(text='{} - 1 File'.format(replacement_container_title) )
        else:
            removal_replacement_frame.config(text='{} - {} Files'.format(replacement_container_title, len(replacement_files)) )
        removal_replacement_listbox = Listbox(removal_replacement_frame, bg=replacement_section_color, fg=replacement_section_text_color, selectmode="extended", font=remove_box_listbox_font)
        ri=1
        for item in replacement_files:
            removal_replacement_listbox.insert("end",u'{2} | {0} | {1}'.format(os.path.basename(item), ByteUnitConversion(os.path.getsize(item)), ri ))
            ri += 1

        removal_replacement_scrollbar = ttk.Scrollbar(removal_replacement_frame, command=removal_replacement_listbox.yview)
        removal_replacement_scrollbar.pack(side="right", fill="y")
        removal_replacement_x_axis_scrollbar = ttk.Scrollbar(removal_replacement_frame, orient = "horizontal", command=removal_replacement_listbox.xview)
        removal_replacement_x_axis_scrollbar.pack(side="bottom", fill="x")
        removal_replacement_listbox.config(yscrollcommand=removal_replacement_scrollbar.set, xscrollcommand=removal_replacement_x_axis_scrollbar.set)

        removal_replacement_listbox.pack(fill="both", expand="y")

        removal_replacement_delete_button = Button(remove_buttons_frame, command=lambda:DeleteFunction(1), bg=replacement_section_color, fg=replacement_section_text_color, text='Delete Selected\nReplacement File(s)', font=remove_box_12_font)
        removal_replacement_delete_all_button = Button(remove_buttons_frame, command=lambda:DeleteAllListboxItems(1), bg=default_button_color, fg=default_button_text_color, text='Delete All Replacment Files', font=remove_box_9_font)

        removal_replacement_delete_button.bind("<Enter>", HoveringOverWidget)
        removal_replacement_delete_button.bind("<Leave>", NotHoveringOverWidget)
        removal_replacement_delete_all_button.bind("<Enter>", HoveringOverWidget)
        removal_replacement_delete_all_button.bind("<Leave>", NotHoveringOverWidget)


    if len(source_files) != 0 and len(replacement_files) != 0:
        if switch_containers_placement == True:
            removal_replacement_frame.place(relwidth=0.5, relheight=1)
            removal_source_frame.place(relwidth=0.5, relheight=1, relx=0.5)
            
            removal_replacement_delete_button.place(relwidth=0.5, relheight=0.8)
            removal_replacement_delete_all_button.place(relwidth=0.5, relheight=0.2, rely=0.8)
            removal_source_delete_button.place(relwidth=0.5, relheight=0.8, relx=0.5)
            removal_source_delete_all_button.place(relwidth=0.5, relheight=0.2, relx=0.5, rely=0.8)
        else:
            removal_source_frame.place(relwidth=0.5, relheight=1)
            removal_replacement_frame.place(relwidth=0.5, relheight=1, relx=0.5)
            
            removal_source_delete_button.place(relwidth=0.5, relheight=0.8)
            removal_source_delete_all_button.place(relwidth=0.5, relheight=0.2, rely=0.8)
            removal_replacement_delete_button.place(relwidth=0.5, relheight=0.8, relx=0.5)
            removal_replacement_delete_all_button.place(relwidth=0.5, relheight=0.2, relx=0.5, rely=0.8)

    elif len(source_files) != 0:
        removal_source_frame.place(relwidth=1, relheight=1)

        removal_source_delete_button.place(relwidth=1, relheight=0.8)
        removal_source_delete_all_button.place(relwidth=1, relheight=0.2, rely=0.8)

    elif len(replacement_files) != 0:
        removal_replacement_frame.place(relwidth=1, relheight=1)

        removal_replacement_delete_button.place(relwidth=1, relheight=0.8)
        removal_replacement_delete_all_button.place(relwidth=1, relheight=0.2, rely=0.8)


    #Resize the text in the Remove box
    def ResizeRemoveBoxText(event):
        if (event.widget == remove_box):
            global remove_box_previous_width
            global remove_box_previous_height
            if (event.width != remove_box_previous_width) or (event.height != remove_box_previous_height): # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
                remove_box_previous_width = event.width
                remove_box_previous_height = event.height

                listbox_filename_font_size = int(round( Decimal(9) *( Decimal(event.width) / Decimal(remove_box_base_width) )  ))

                remove_box_width_ratio = Decimal(event.width) / Decimal(remove_box_base_width)
                remove_box_height_ratio = Decimal(event.height) / Decimal(remove_box_base_height)
                remove_box_font_size_calculation = (remove_box_width_ratio + remove_box_height_ratio) / Decimal(2)

                delete_buttons_font_size = int(round( Decimal(9) * remove_box_font_size_calculation ))
                remove_box_label_frame_font_size = int(round( Decimal(12) * remove_box_font_size_calculation ))

                if len(source_files) != 0:
                    removal_source_frame.config(font=("Helvetica", remove_box_label_frame_font_size ))
                    removal_source_listbox.config(font=("Helvetica", listbox_filename_font_size))
                    removal_source_delete_button.config(font=("Helvetica", remove_box_label_frame_font_size ))
                    removal_source_delete_all_button.config(font=("Helvetica", delete_buttons_font_size ))

                if len(replacement_files) != 0:
                    removal_replacement_frame.config(font=("Helvetica", remove_box_label_frame_font_size ))
                    removal_replacement_listbox.config(font=("Helvetica", listbox_filename_font_size ))
                    removal_replacement_delete_button.config(font=("Helvetica", remove_box_label_frame_font_size ))
                    removal_replacement_delete_all_button.config(font=("Helvetica", delete_buttons_font_size ))
    
                pass
        pass

    
    global remove_box_previous_width
    remove_box_previous_width = remove_box.winfo_width()
    global remove_box_previous_height
    remove_box_previous_height = remove_box.winfo_height()
    remove_box.bind('<Configure>', ResizeRemoveBoxText)

    remove_box.mainloop()


#Deletes files in each section's respective list and updates/deletes the labels accordingly.
def DeleteFunction(listbox_id):
    if listbox_id == 0:
        selection_to_delete = removal_source_listbox.curselection()
        if not selection_to_delete: #If no files were chosen to be deleted
            text_display_string.set("No files were chosen to be deleted.")
            return
        global source_files
        global source_section_scroll_position

        files_to_delete = source_files
        listbox_to_delete_from = removal_source_listbox
        move_pos = source_section_scroll_position
        down_arrow_is_disabled = source_scroll_down_button
        section_container = source_container
        remove_container = removal_source_frame
        section_title = source_container_title
    elif listbox_id == 1:
        selection_to_delete = removal_replacement_listbox.curselection()
        if not selection_to_delete:
            text_display_string.set("No files were chosen to be deleted.")
            return
        global replacement_files
        global replacement_section_scroll_position

        files_to_delete = replacement_files
        listbox_to_delete_from = removal_replacement_listbox
        move_pos = replacement_section_scroll_position
        down_arrow_is_disabled = replacement_scroll_down_button
        section_container = replacement_container
        remove_container = removal_replacement_frame
        section_title = replacement_container_title


    number_of_files_deleted = 0
    for item in reversed(selection_to_delete):
        i=0
        while i < len(files_to_delete):
            if (i == int(item)):
                files_to_delete.pop(i)
                number_of_files_deleted +=1
                break
            i+=1

    for item in reversed(selection_to_delete):
    	listbox_to_delete_from.delete(item)

    other_pos = move_pos #This is so the other section's label positioning does not get altered when the files are currently being compared.
    #If the section's down arrow button is disabled (meaning if the user is at the end of the list)
    if down_arrow_is_disabled.cget('state') == 'disabled': # https://stackoverflow.com/questions/58648760/how-to-check-the-state-enabled-disabled-of-a-checkbox-in-python-tkinter
        move_pos = (move_pos - number_of_files_deleted) #This makes the label position match with the single label displayed

    global comparing_labels_on
    if len(files_to_delete) > 0:
        if len(files_to_delete) == 1:
            after_removal_container_titles = "{} - 1 File".format(source_container_title)
        else:
            after_removal_container_titles = "{} - {} Files".format(section_title, len(files_to_delete))
        section_container.config(text=after_removal_container_titles)
        remove_container.config(text=after_removal_container_titles)

        if comparing_labels_on == True: 
            comparing_labels_on = False
            UpdateLabels(other_pos, int(not listbox_id)) # https://stackoverflow.com/questions/47661242/how-to-switch-true-to-false-in-python
        UpdateLabels(move_pos, listbox_id) #This deletes excess labels and updates the labels that remain.
        listbox_to_delete_from.delete(0, 'end')
        remaining_index = 1
        for remaining_item in files_to_delete:
            listbox_to_delete_from.insert("end",u'{2} | {0} | {1}'.format(os.path.basename(remaining_item), ByteUnitConversion(os.path.getsize(remaining_item)), remaining_index))
            remaining_index += 1
    else:
        section_container.config(text=section_title)
        remove_container.config(text=section_title)
        comparing_labels_on = False #There is certainly a file that is going to be deleted or else it this function would have been returned. It is fine to call it here.
        DeleteAllLabels(listbox_id)
    

    #if the user deleted the files from both sections, remove the window.
    if not source_files and not replacement_files:
        global remove_box
        remove_box.destroy()
        remove_button.config(state="disabled", bg='gray', relief="sunken")

    DisableRootButtons()


#Automatically deletes all the files in the choosen section.
def DeleteAllListboxItems(label_section_id):
    if label_section_id == 0:
        delete_files = source_files
        listbox_section = removal_source_listbox
        section_container = source_container
        remove_frame = removal_source_frame
        section_title = source_container_title
    elif label_section_id == 1:
        delete_files = replacement_files
        listbox_section = removal_replacement_listbox
        section_container = replacement_container
        remove_frame = removal_replacement_frame
        section_title = replacement_container_title

    global comparing_labels_on #Not sure if global statement is needed
    comparing_labels_on = False

    i = 0
    while i < listbox_section.size():
        listbox_section.delete(i)
        delete_files.pop(i)
    DeleteAllLabels(label_section_id)

    section_container.config(text=section_title)

    global remove_box
    remove_box.bell()
    if not source_files and not replacement_files:
        remove_box.destroy()
        remove_button.config(bg='gray', state="disabled", relief="sunken")
    else:
        remove_frame.config(text=section_title)

    DisableRootButtons()


#Deletes all the labels in the chosen section and removes them from the appopriate list.
def DeleteAllLabels(id):
    global label_source_list
    global label_replacement_list
    global source_section_scroll_position
    global replacement_section_scroll_position

    if id == 0:
        #Destroy every label and remove their data from the list
        while len(label_source_list) > 0:
            label_source_list[-1].destroy()
            label_source_list.pop(-1)
        if len(label_replacement_list) > 0: #UpdateLabels returns and calls this function (DeleteAllLabels) if displayed_()_files are 0. This causes a loop between UpdateLabels and DeleteAllLabels that should not happen. This is why this if statement is here, to prevent that loop.
            UpdateLabels(replacement_section_scroll_position, 1)

        source_section_scroll_position = 0
        scroll_up_button = source_scroll_up_button
        scroll_down_button = source_scroll_down_button
    elif id==1:
        while len(label_replacement_list) > 0:
            label_replacement_list[-1].destroy()
            label_replacement_list.pop(-1)
        if len(label_source_list) > 0:
            UpdateLabels(source_section_scroll_position, 0)

        replacement_section_scroll_position = 0
        scroll_up_button = replacement_scroll_up_button
        scroll_down_button = replacement_scroll_down_button
    elif id == 2: #For when filling files
        while len(label_source_list) > 0:
            label_source_list[-1].destroy()
            label_source_list.pop(-1)
        source_container.config(text=source_container_title)
        MoveArrowsActivation('Up', False, source_scroll_up_button)
        MoveArrowsActivation('Down', False, source_scroll_down_button)
        
        while len(label_replacement_list) > 0:
            label_replacement_list[-1].destroy()
            label_replacement_list.pop(-1)
        replacement_container.config(text=replacement_container_title)
        MoveArrowsActivation('Up', False, replacement_scroll_up_button)
        MoveArrowsActivation('Down', False, replacement_scroll_down_button)
        return
        
    MoveArrowsActivation('Up', False, scroll_up_button)
    MoveArrowsActivation('Down', False, scroll_down_button)

   



#--------------------------------------------------------- AUTOMATIC REPLACER SECTION --------------------------------------------------------------#

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
    hca_replacement_files = PickedFiles(CheckForSavedDirectory(finished_dir), False)
    if len(hca_replacement_files) == 0:
        text_display_string.set('Canceled. No .hca files selected.')
        return
    OverwriteDirectoryData(finished_dir, os.path.dirname(hca_replacement_files[-1]))

    offset_of_headers_list = {}
    with open(uexp_file_to_replace, 'rb') as open_file:
        if LoopThroughFileForSearchStrings(open_file, offset_of_headers_list, uexp_file_to_replace) == True:
            return
        pass


    global chosen_number
    global number_input
    number_input = IntVar() # https://www.kite.com/python/docs/tkinter.Button.wait_variable

    DisplayReplacingInfo()


    if number_base == 1: #Hex
        uexp_message_label.config(text='Give the hexadecimal number that this file corresponds to:' )
    elif number_base == 2: #Dec
        uexp_message_label.config(text='Give the number that this file corresponds to:' )
    elif number_base == 3: #Oct
        uexp_message_label.config(text='Give the octal number that this file corresponds to:' )

    global terting
    terting = IntVar()
    #Determines if the replacement file's file size is larger than the data found in the .uexp file
    def CanReplaceDataCheck(replacement_file_size, header_length_offset_size):
        if replacement_file_size > header_length_offset_size:
            global try_again_button
            global cancel_current_file_button

            terting.set(-1)
            def function(parameter_number):
                terting.set(parameter_number)
                
                if number_base == 1: #Hex
                    uexp_message_label.config(text='Give the hexadecimal number that this file corresponds to:' )
                elif number_base == 2: #Dec
                    uexp_message_label.config(text='Give the number that this file corresponds to:' )
                elif number_base == 3: #Oct
                    uexp_message_label.config(text='Give the octal number that this file corresponds to:' )
                uexp_hca_file_label.config(text="Input")

                try_again_button.place_forget()
                cancel_current_file_button.place_forget()

                uexp_hca_file_label.place(relwidth=hca_file_label_relwidth, relheight=bottom_relheight, rely=bottom_rely)
                uexp_input_hex_number.place(relwidth=input_relwidth, relx=hca_file_label_relwidth, relheight=bottom_relheight, rely=bottom_rely)
                if parameter_number == 1:
                    return
                global chosen_number
                chosen_number = None
                return
        

            uexp_message_label.config(text="Error! Replacement file's file size is larger than it should be!")
            uexp_file_label.config(text="Length of Data in .uexp File:\n{}\nReplacement File:\n{}".format(ByteUnitConversion(header_length_offset_size), ByteUnitConversion(replacement_file_size)))
            uexp_hca_file_label.place_forget()
            uexp_input_hex_number.place_forget()

            try_again_button.config(text="Try Again", command=lambda:(function(1)))
            try_again_button.place(relwidth=0.5, relx=0.0, relheight=bottom_relheight, rely=bottom_rely)

            cancel_current_file_button.config(text="Skip", command=lambda:(function(0)) )
            cancel_current_file_button.place(relwidth=0.5, relx=0.5, relheight=bottom_relheight, rely=bottom_rely)

            try_again_button.wait_variable(terting)
            if terting.get() == -2: #This makes sure that the python function does not continue existing after the root_window has been closed.
                number_input.set(-2)
                return
        
            if terting.get() == 0:
                return False
            else:
                return True

        pass


    if automatically_replace_using_filename == True:
        read_number_in_filename_failed_size_check_list = []

    with open(uexp_file_to_replace, 'rb+') as uexp_file:
        remaining = 1
        for single_hca_file in hca_replacement_files:
            hca_filename = os.path.basename(single_hca_file)
            replacement_file_size = os.path.getsize(single_hca_file)
            with open(single_hca_file, 'rb') as hca_file:
                if automatically_replace_using_filename == True:
                    string_number_in_filename = hca_filename.partition(' ')[0]
                    uexp_message_label.config(text=string_number_in_filename)
                    try:
                        if number_base == 1: #Hex
                            chosen_number = int(string_number_in_filename, 16)
                        elif number_base == 2: #Dec
                            chosen_number = int(string_number_in_filename)
                        elif number_base == 3: #Oct
                            chosen_number = int(string_number_in_filename, 8)

                        header_length_offset_size = offset_of_headers_list[chosen_number+1] - offset_of_headers_list[chosen_number]
                        if replacement_file_size > header_length_offset_size:
                            #Add to failed size check list
                            read_number_in_filename_failed_size_check_list.append(tuple((hca_filename, replacement_file_size, header_length_offset_size, string_number_in_filename)) ) #https://www.w3schools.com/python/python_tuples.asp
                            continue
                    except ValueError:
                         read_number_in_filename_failed_size_check_list.append(tuple((hca_filename, string_number_in_filename, "ValueError")) )
                         continue
                    
                    uexp_file_label.config(text=(hca_filename))
                else:
                    try_again = True
                    while try_again == True:
                        uexp_file_label.config(text = u'{0}\n\n{1} out of {2}'.format(hca_filename, remaining, len(hca_replacement_files)))
                        number_input.set(-1)
                        uexp_hca_file_label.wait_variable(number_input) # https://stackoverflow.com/questions/44790449/making-tkinter-wait-untill-button-is-pressed
                        if number_input.get() == -2: #This makes sure that the python function does not continue existing after the root_window has been closed.
                            return

                        try:
                            header_length_offset_size = offset_of_headers_list[chosen_number+1] - offset_of_headers_list[chosen_number]
                        except:
                            uexp_input_hex_number.delete(0, 'end')
                            text_display_string.set("Invalid value. Try again")
                            continue
                        
                        try_again = CanReplaceDataCheck(replacement_file_size, header_length_offset_size)
                        if number_input.get() == -2: #This makes sure that the python function does not continue existing after the root_window has been closed.
                            return

                    uexp_input_hex_number.delete(0, 'end')
                    remaining += 1
                    text_display_string.set("")
                    if chosen_number == None:
                        continue


                uexp_file.seek(offset)
                replace = hca_file.read()
                uexp_file.writelines(replace)
        pass
    

    if automatically_replace_using_filename == True and len(read_number_in_filename_failed_size_check_list) > 0:
        uexp_replacing_files_window.destroy()
        present_failed_files_window = Toplevel(root_window)
        present_failed_files_base_width = Decimal(400)
        present_failed_files_base_height = Decimal(500)
        WindowCenterPositioner(present_failed_files_window, present_failed_files_base_width, present_failed_files_base_height)
    
        present_failed_files_window_12_font = InitialWindowFontSize(12, present_failed_files_window.winfo_width(), present_failed_files_window.winfo_height(), present_failed_files_base_width, present_failed_files_base_height)
        present_failed_files_window_14_font = InitialWindowFontSize(14, present_failed_files_window.winfo_width(), present_failed_files_window.winfo_height(), present_failed_files_base_width, present_failed_files_base_height)
        present_failed_files_window.wm_title('')
    
        present_failed_files_frame = LabelFrame(present_failed_files_window, text="Files That Failed To Replace Data", font=present_failed_files_window_14_font, bg="black", fg="white")
        present_failed_files_frame.pack(fill="both", expand="y")
    
        present_failed_files_listbox = Listbox(present_failed_files_frame, font=present_failed_files_window_12_font, bg="black", fg="white")
        present_failed_files_scrollbar = ttk.Scrollbar(present_failed_files_frame, command=present_failed_files_listbox.yview)
        present_failed_files_x_axis_scrollbar = ttk.Scrollbar(present_failed_files_frame, orient = "horizontal", command=present_failed_files_listbox.xview)
        present_failed_files_scrollbar.pack(side="right", fill="y")
        present_failed_files_x_axis_scrollbar.pack(side="bottom", fill="x")
        present_failed_files_listbox.config(yscrollcommand = present_failed_files_scrollbar.set, xscrollcommand = present_failed_files_x_axis_scrollbar.set)
    
        for failed_file in read_number_in_filename_failed_size_check_list:
            if failed_file[2] == "ValueError":
                failed_file_info = u'Invalid value ( {0} ) obtained from filename: "{1}"'.format(failed_file[1], failed_file[0])
            else:
                failed_file_info = u'{3}) "{0}"      {1} > {2}'.format(failed_file[0], ByteUnitConversion(failed_file[1]), ByteUnitConversion(failed_file[2]), failed_file[3] )
            present_failed_files_listbox.insert(0, failed_file_info)

        present_failed_files_listbox.insert(0, "")
        present_failed_files_listbox.insert(0, 'Number read from filename) "Filename":     File size of chosen file(s) > Size of Header offset length in .uexp file')
        present_failed_files_listbox.selection_set(0) # https://stackoverflow.com/questions/49695346/tkinter-listboxs-selection-set-and-activate-temporarily-disable-extended-se
    
        if number_base == 1: #Hex
            text_for_base_number = "Hex (Base 16)"
        elif number_base == 2: #Dec
            text_for_base_number = "Dec (Base 10)"
        elif number_base == 3: #Oct
            text_for_base_number = "Oct (Base 8)"
        present_failed_files_listbox.insert(0, "{0} out of {1} chosen files failed to replace | Base Number Used: {2}".format(len(read_number_in_filename_failed_size_check_list), len(hca_replacement_files), text_for_base_number) )
        present_failed_files_listbox.pack(fill="both", expand="y")

        del read_number_in_filename_failed_size_check_list[:]

    else:
        uexp_message_label.config(text='Finished!' )
        uexp_file_label.config(text="You can close this window now.")
        if automatically_replace_using_filename == False:
            uexp_hca_file_label.config(state="disabled", bg='gray')
            uexp_input_hex_number.config(state="disabled")
        pass

    pass


#Displays the window that appears when the user goes to replace the HCA code blocks in their character's .uexp file.
def DisplayReplacingInfo():
    global uexp_replacing_files_window
    global uexp_message_label
    global uexp_file_label
    
    uexp_replacing_files_window = Toplevel(root_window)

    global uexp_replacing_files_window_base_width
    global uexp_replacing_files_window_base_height
    uexp_replacing_files_window_base_width = Decimal(200)
    uexp_replacing_files_window_base_height = Decimal(200)
    uexp_replacing_files_window.minsize(150, 150)

    WindowCenterPositioner(uexp_replacing_files_window, uexp_replacing_files_window_base_width, uexp_replacing_files_window_base_height)

    uexp_replacing_files_window_10_font = InitialWindowFontSize(10, uexp_replacing_files_window.winfo_width(), uexp_replacing_files_window.winfo_height(), uexp_replacing_files_window_base_width, uexp_replacing_files_window_base_height)
    uexp_replacing_files_window.wm_title('')
    
    uexp_replacing_files_window_wrap_length = uexp_replacing_files_window.winfo_width() * (Decimal(175) / uexp_replacing_files_window_base_width)
    uexp_message_label = Label(uexp_replacing_files_window, text='Message here', font=uexp_replacing_files_window_10_font, bg='gray', wraplength=uexp_replacing_files_window_wrap_length) # https://stackoverflow.com/questions/55241150/tkinter-wraplength-units-is-pixels
    uexp_file_label = Label(uexp_replacing_files_window, text='File name here', font=uexp_replacing_files_window_10_font, bg='gray', wraplength=uexp_replacing_files_window_wrap_length) #175
    
    if automatically_replace_using_filename == False:
        message_label_relheight = Decimal(75) / (uexp_replacing_files_window_base_height - Decimal(20)) #To account for bar at top of window #Decimal(180)
        uexp_message_label.place(relwidth=1,relheight=message_label_relheight)
        uexp_file_label.place(relwidth=1,relheight=message_label_relheight, rely=message_label_relheight)

        global uexp_hca_file_label
        global uexp_input_hex_number

        global hca_file_label_relwidth
        global input_relwidth
        global bottom_relheight
        global bottom_rely

        global try_again_button
        global cancel_current_file_button

        hca_file_label_relwidth = Decimal(70) / uexp_replacing_files_window_base_width
        input_relwidth = Decimal(130) / uexp_replacing_files_window_base_width
        bottom_relheight = Decimal(30) / (uexp_replacing_files_window_base_height - Decimal(20))
        bottom_rely = Decimal(150) / (uexp_replacing_files_window_base_height - Decimal(20))

        uexp_replacing_files_window_9_font = InitialWindowFontSize(9, uexp_replacing_files_window.winfo_width(), uexp_replacing_files_window.winfo_height(), uexp_replacing_files_window_base_width, uexp_replacing_files_window_base_height)

        uexp_hca_file_label = Button(uexp_replacing_files_window, text='Input', font=uexp_replacing_files_window_9_font, bg=default_button_color, fg=default_button_text_color, command=lambda:ChosenNumber(None))
        uexp_hca_file_label.place(relwidth=hca_file_label_relwidth, relheight=bottom_relheight, rely=bottom_rely)

        uexp_input_hex_number = Entry(uexp_replacing_files_window, bd=5)
        uexp_input_hex_number.place(relwidth=input_relwidth, relx=hca_file_label_relwidth, relheight=bottom_relheight, rely=bottom_rely)
        uexp_input_hex_number.bind('<Return>', lambda e: ChosenNumber(e))


        #Based on the number base, only accept numbers and letters to be inputed in the Entry widget.
        def DecimalNumberInputedInReplaceEntryWidget(action_code, inputed_string_character):
            if action_code == "1": #Inputing
                try:
                    if number_base == 1: #Hex
                        int(inputed_string_character, 16)
                    elif number_base == 2: #Dec
                        int(inputed_string_character)
                    elif number_base == 3: #Oct
                        int(inputed_string_character, 8)
                except:
                    return False

            return True
        uexp_replace_decimal_number_input_check = (uexp_input_hex_number.register(DecimalNumberInputedInReplaceEntryWidget),'%d', '%S')
        uexp_input_hex_number.config(validate='key', validatecommand=uexp_replace_decimal_number_input_check)


        try_again_button = Button(uexp_replacing_files_window)
        cancel_current_file_button = Button(uexp_replacing_files_window)
    else:
        uexp_message_label.place(relwidth=1,relheight=0.5)
        uexp_file_label.place(relwidth=1,relheight=0.5, rely=0.5)
        

    #Resize the text of the replacing files window
    def ResizeReplacingInfoText(event):
        if event.widget == uexp_replacing_files_window:
            global uexp_replacing_files_window_previous_width
            global uexp_replacing_files_window_previous_height
    
            if (event.width != uexp_replacing_files_window_previous_width) or (event.height != uexp_replacing_files_window_previous_height):
                uexp_replacing_files_window_previous_width = event.width
                uexp_replacing_files_window_previous_height = event.height
    

                replacing_info_window_width_ratio = Decimal(event.width) / uexp_replacing_files_window_base_width
                replacing_info_window_height_ratio = Decimal(event.height) / uexp_replacing_files_window_base_height
                replacing_info_window_area_average = (replacing_info_window_width_ratio + replacing_info_window_height_ratio) / Decimal(2)

                replacing_info_text_font_size = int(round(Decimal(10) * replacing_info_window_area_average))
                replacing_info_text_wrap_length = Decimal(175) * ( Decimal(event.width) / Decimal(uexp_replacing_files_window_base_width) )
    
                uexp_message_label.config(font=('Helvetica', replacing_info_text_font_size), wraplength=int(replacing_info_text_wrap_length) )
                uexp_file_label.config(font=('Helvetica', replacing_info_text_font_size), wraplength=int(replacing_info_text_wrap_length) )
    
                if automatically_replace_using_filename == False:
                    replacing_info_button_text_font_size = int(round(Decimal(9) * font_scale_multiplier))
                    
                    uexp_input_hex_number.config(font=('Helvetica', replacing_info_button_text_font_size) ) # https://stackoverflow.com/questions/24501606/tkinter-python-entry-height
                    uexp_hca_file_label.config(font=('Helvetica', replacing_info_button_text_font_size) )
            pass
    
        pass


    global uexp_replacing_files_window_previous_width
    global uexp_replacing_files_window_previous_height
    uexp_replacing_files_window_previous_width = uexp_replacing_files_window.winfo_width()
    uexp_replacing_files_window_previous_height = uexp_replacing_files_window.winfo_height()

    uexp_replacing_files_window.bind('<Configure>', ResizeReplacingInfoText)
    uexp_replacing_files_window.bind('<Destroy>', StopAutoReplacerFunction)


#Obtains the inputed number from the user.
def ChosenNumber(e):
    try:
        if number_base == 1: #Hex
            number_input.set( int(uexp_input_hex_number.get(), 16) )
        elif number_base == 2: #Dec
            number_input.set( int(uexp_input_hex_number.get() ) )
        elif number_base == 3: #Oct
            number_input.set( int(uexp_input_hex_number.get(), 8) )

        global chosen_number
        chosen_number = number_input.get()
    except:
        uexp_message_label.config(text='Inputed number is invalid.\nGive the correct number that this file corresponds to.' )

    pass


#Stops the AutomaticReplacer() function if the user closes the "uexp_replacing_files_window" while it is waiting for an input from the user.
def StopAutoReplacerFunction(bind_event_parameter):
    if bind_event_parameter.widget == uexp_replacing_files_window: # https://stackoverflow.com/questions/58328686/destroy-events-executes-the-binded-function-5-times
        global number_input
        number_input.set(-2)
        global terting
        terting.set(-2)
    pass

#--------------------------------------------------------- AUTOMATIC REPLACER SECTION --------------------------------------------------------------#


#Uses the Search String to find the Header offsets in the given file.
def LoopThroughFileForSearchStrings(open_file, offset_header_positions, file):
    read_file = open_file.read()

    searchString = replacing_search_string #"\x48\x43\x41\x00\x02\x00\x00\x60\x66\x6D\x74" This entire hex string doesn't work for 000_CMN.uexp because it has a slightly different hex sequence for some reason.
    if search_for_finish_string == False:
        finishString = None
    else:
        finishString = replacing_finish_string

    end_of_hca_headers = False
    index_start = 0
    number_index = -1
    while True:
        number_index += 1
        if end_of_hca_headers == False:
            position_start = read_file.find(searchString, index_start)              #Read the file at the current offset position (index_start) until it finds a HCA hex string (Search String). Then, get the offset position of the "H" in HCA
            if position_start < 0:
                end_of_hca_headers = True
                continue
            open_file.seek(position_start)                                          #Set up the file so it reads the next offset position       #Go to that position
            index_start = 1 + open_file.tell()                                      #Read the current position and add 1 (so it doesn't read the current postion again)
            if position_start >= 0: #If [error] occured, start position = -1
                if isinstance(offset_header_positions, list):
                    offset_header_positions.append(position_start)                  #Add the offset position to the list
                else:
                    offset_header_positions.update({number_index: position_start})  #Add the offset position to the dictonary
            continue
        else:
            if number_index == 1:
                text_display_string.set("No Audio Start Header(s) was found in the file.\n{}".format(repr(replacing_search_string)[1:-1]) )
                return True
            
            if finishString == None:
                position_final = os.path.getsize(file)                              #Get the index at the end of the file
            else:
                position_final = read_file.find(finishString, index_start) - 1      #Read the file at the current offset position (index_start) until it finds the @UTF hex string (Finish String). Then, get the offset position right before @UTF
                if position_final < 0:
                    text_display_string.set("The Audio End Header was not found in the file.\n{}".format(repr(replacing_finish_string)[1:-1]))
                    return True
            if isinstance(offset_header_positions, list):
                offset_header_positions.append(position_final)                      #Add the final offset position to the list
            else:
                offset_header_positions.update({number_index: position_final})      #Add the final offset position to the dictonary
            break
    
        break #Just in case

    return False


#--------------------------------------------------------- CREATING HCA FILES SECTION --------------------------------------------------------------#

#Creates a window that lets the user decide how they want to extract the file information from their chosen file.
def ExtractHCAFiles():
    extract_hca_window = Toplevel()
    extract_hca_window.resizable(width=False, height=False)
    extract_hca_window_base_width = Decimal(300)
    extract_hca_window_base_height = Decimal(75)

    WindowCenterPositioner(extract_hca_window, extract_hca_window_base_width, extract_hca_window_base_height)
    extract_hca_window_12_font = InitialWindowFontSize(12, extract_hca_window.winfo_width(), extract_hca_window.winfo_height(), extract_hca_window_base_width, extract_hca_window_base_height)
    extract_hca_window.wm_title('')
    
    extract_hca_window_calculation = Decimal(1) / Decimal(3)
    create_files_button = Button(extract_hca_window, text='Create\nFiles', font=extract_hca_window_12_font, command=lambda:[extract_hca_window.destroy(), ProceedToExtraction(False)], bg=source_section_color, fg=source_section_text_color )
    create_files_button.place(relwidth=extract_hca_window_calculation, relheight=1, relx=extract_hca_window_calculation)

    print_files_button = Button(extract_hca_window, text='Print\nExtract Info\nHere', font=extract_hca_window_12_font, command=lambda:[extract_hca_window.destroy(), ProceedToExtraction(True)], bg=default_button_color, fg=default_button_text_color)
    print_files_button.place(relwidth=extract_hca_window_calculation, relheight=1, relx=Decimal(2) * extract_hca_window_calculation)

    create_only_txt_file_button = Button(extract_hca_window, text='Only Create\nA .txt File', font=extract_hca_window_12_font, command=lambda:[extract_hca_window.destroy(), ProceedToExtraction(False, True)], bg='gray')
    create_only_txt_file_button.place(relwidth=extract_hca_window_calculation, relheight=1)

    extract_hca_window_button_list = [create_files_button, print_files_button, create_only_txt_file_button]
    for extract_window_button in extract_hca_window_button_list:
        extract_window_button.bind("<Enter>", HoveringOverWidget)
        extract_window_button.bind("<Leave>", NotHoveringOverWidget)
    pass

#Prompts the user to select the file(s) he/she wants to extract from and which file directory he/she wants the extracted files to be in (if not printing info in program).
def ProceedToExtraction(print_files, only_text=False):
    selected_uexp_files = PickedFiles(CheckForSavedDirectory(extract_uexp_dir), 'UEXP', extract_title=True)
    if len(selected_uexp_files) == 0:
        text_display_string.set("No .uexp file was selected.")
        return
    OverwriteDirectoryData(extract_uexp_dir, selected_uexp_files[-1])

    if print_files == True:
        file_directory_chosen = None
    else:
        file_directory_chosen = PickedFiles(CheckForSavedDirectory(extract_location_dir), True, extract_title=True)
        if not file_directory_chosen:
            text_display_string.set("No directory was chosen.")
            return
        OverwriteDirectoryData(extract_location_dir, file_directory_chosen)

    FindingHCAHeaders(selected_uexp_files, file_directory_chosen, print_files, only_text)


#Goes through the chosen .uexp file(s) and using the Search String and (if user wants to use it, the) Finish String, finds the start of each Audio Header in the file and the Header that denotes the end of the Audio data (Finish String), and then calculates the length of beteween the found Headers. A log of the data is put into a .txt file and/or the data of each header is then extracted out into its own .hca file OR the log data is just printed out to a window in the program.
def FindingHCAHeaders(selected_uexp_files, file_directory_chosen, print_files, only_text):
    global header_offsets_list
    global list_of_hca_filenames
    global list_of_hca_offsets
    global list_of_offset_lengths
    global hca_log_file_lines

    header_offsets_list = []
    list_of_hca_filenames = []
    list_of_hca_offsets = []
    list_of_offset_lengths = []
    hca_log_file_lines = []
    offset_size = []

    hca_header_search_string = replacing_search_string
    if search_for_finish_string == False:
        utf_header_search_string = None
    else:
        utf_header_search_string = replacing_finish_string

    selected_uexp_files_that_failed = []
    if print_files == True:
        print_out_logs_list = []
        print_out_logs_tab_filenames = []

    #Details on encoding and decoding for making sure file names work with unicode characters   # https://stackoverflow.com/a/11596746 # https://stackoverflow.com/a/55228566
    # .encode("utf-8") converts a unicode string to a byte string
    # .decode("utf-8") converts a byte string to a unicode string

    for uexp_file in selected_uexp_files:
        uexp_filename = (os.path.splitext(os.path.basename(uexp_file))[0]).encode("utf-8") #This is to remove the ".uexp" part of the filename   # https://www.geeksforgeeks.org/python-os-path-splitext-method/

        del header_offsets_list[:]   # https://stackoverflow.com/questions/14465279/delete-all-objects-in-a-list

        if print_files == False:
            if only_text == True:
                hca_folder_directory = file_directory_chosen
            else:
                folder_name = "{} - HCA Files Extraction".format(uexp_filename)
                hca_folder_directory = os.path.abspath( os.path.join(file_directory_chosen, folder_name.decode("utf-8")) )
                CreateFolder(hca_folder_directory)

        move_to_next_selected_uexp_file = False
        
        with open(uexp_file, 'rb') as opened_uexp_file:
            ### --- Find Seach String and Finish String Headers --- ###
            if LoopThroughFileForSearchStrings(opened_uexp_file, header_offsets_list, uexp_file) == True:
                if len(selected_uexp_files) == 1:
                    return
                selected_uexp_files_that_failed.append(os.path.basename(uexp_file))
                continue

            ### --- Get Offset Positions of Headers --- ###
            if number_base == 1: #Hex
                extract_file_number_format = "X"
                extract_file_index_prefix = "x"
                extract_file_number_base_type = "Hexadecimal (Base 16)"
            elif number_base == 2: #Dec
                extract_file_number_format = "n"
                extract_file_index_prefix = ""
                extract_file_number_base_type = "Decimal (Base 10)"
            elif number_base == 3: #Oct
                extract_file_number_format = "o"
                extract_file_index_prefix = "o"
                extract_file_number_base_type = "Octal (Base 8)"

            header_offset_index=0
            for offset_position in header_offsets_list:
                if header_offset_index < len(header_offsets_list)-1:
                    header_offset_length = header_offsets_list[header_offset_index+1] - offset_position

                    list_of_hca_offsets.append(format(offset_position, extract_file_number_format))
                    list_of_offset_lengths.append(format(header_offset_length, extract_file_number_format) )
                    offset_size.append(ByteUnitConversion(header_offset_length))

                    if print_files == False:
                        if len(header_offsets_list) == 2: #If there is only one HCA header found (remember, the @UTF Header gets included at the end)
                            filename_of_hca_header_section = "{}.hca".format(uexp_filename)
                        else:
                            filename_of_hca_header_section = "{0} - {1} ( {3}{2} ).hca".format(uexp_filename, header_offset_index, format(header_offset_index, extract_file_number_format).zfill(2), extract_file_index_prefix ) # https://www.kite.com/python/answers/how-to-add-leading-zeros-to-a-number-in-python
                        list_of_hca_filenames.append(filename_of_hca_header_section)


                        #Create the .hca files cointaining the data from the Header offset
                        if only_text == False:
                            opened_uexp_file.seek(offset_position)
                            data = opened_uexp_file.read(header_offset_length) #From the starting position read the bytes until the offset length as been reached
                            hca_header_section_file_directory = os.path.abspath( os.path.join(hca_folder_directory, filename_of_hca_header_section.decode("utf-8")) ) # https://www.w3schools.com/python/python_file_open.asp
                            with open(hca_header_section_file_directory, 'wb') as new_hca_file:
                                new_hca_file.writelines(data)
                    else:
                        printing_index_name = "{0} | ({2}{1})".format(header_offset_index, format(header_offset_index, extract_file_number_format).zfill(2), extract_file_index_prefix )
                        list_of_hca_filenames.append(printing_index_name)

                header_offset_index += 1
            pass

        ### --- Text Document Formating --- ###
        max_filename_length = len(max(list_of_hca_filenames)) #Get the length of the filename that has the longest characters
        #if max_filename_length < 25:
        #    max_filename_length = 25
        if max_filename_length < 10:
            max_filename_length = 10
        max_offset_length = len(max(list_of_hca_offsets))
        if max_offset_length < 8:
            max_offset_length = 8
        max_length_of_offset_lengths = len(max(list_of_offset_lengths))
        if max_length_of_offset_lengths < 15:
            max_length_of_offset_lengths = 15

        k=0
        for hca_filename in list_of_hca_filenames: # https://stackoverflow.com/questions/16796709/align-columns-in-a-text-file  # https://www.geeksforgeeks.org/string-alignment-in-python-f-string/    # https://stackabuse.com/formatting-strings-with-python/
            #offset_size = int(list_of_hca_offsets[k]) - int(list_of_offset_lengths[k])
            if print_files == True:
                hca_info = "{0:{fileLength}}\t\t{1:{hcaLength}}\t{2:{hcalengthLength}}\t\t{3}\n".format(hca_filename, list_of_hca_offsets[k], list_of_offset_lengths[k], offset_size[k], fileLength=max_filename_length, hcaLength=max_offset_length, hcalengthLength=max_length_of_offset_lengths)
            else:
                hca_info = "{0:{fileLength}}\t{1:{hcaLength}}\t{2:{hcalengthLength}}\t{3}\n".format(hca_filename, list_of_hca_offsets[k], list_of_offset_lengths[k], offset_size[k], fileLength=max_filename_length+3, hcaLength=max_offset_length, hcalengthLength=max_length_of_offset_lengths)
            hca_log_file_lines.append(hca_info)
            k+=1

        utf_offset = format(header_offsets_list[-1], extract_file_number_format) #"X"
        if utf_header_search_string == None:
            utf_info = "\nEnd of File: {}".format(utf_offset)
        else:
            utf_info = "\nEnd of Audio Data: {}".format(utf_offset)
        hca_log_file_lines.append(utf_info)

        if utf_header_search_string == None:
            utf_hex_characters = "End of Audio Data Header Not Used"
        else:
            utf_hex_characters = "".join(r"\x{:02X}".format(ord(c)) for c in utf_header_search_string)
        hca_hex_characters = "".join(r"\x{:02X}".format(ord(c)) for c in hca_header_search_string)

        if print_files == True:
            hca_log_file_lines.insert(0,"{0:{fileLength}}\t\t{1:{hcaLength}}\t{2:{hcalengthLength}}\t\t{3}\n".format("Index:", "Offset:", "Offset Length:", "Data Size:", fileLength=max_filename_length, hcaLength=max_offset_length, hcalengthLength=max_length_of_offset_lengths))
            if utf_header_search_string == None:
                utf_header_string_representation = "None"
            else:
                utf_header_string_representation = repr(utf_header_search_string)[1:-1]
            hca_header_string_representation = repr(hca_header_search_string)[1:-1]
        else:
            hca_log_file_lines.insert(0,"{0:{fileLength}}\t\t{1:{hcaLength}}\t{2:{hcalengthLength}}\t{3}\n".format("Filename:", "Offset:", "Offset Length:", "Filesize:", fileLength=max_filename_length+10, hcaLength=max_offset_length+5, hcalengthLength=max_length_of_offset_lengths))
            utf_header_string_representation = utf_header_search_string
            hca_header_string_representation = hca_header_search_string
            
        hca_log_file_lines.insert(0, "Offset Base: {0}\n\n\n".format(extract_file_number_base_type))
        hca_log_file_lines.insert(0, "End Search String: {0}\n{1}\n\n".format(utf_header_string_representation, utf_hex_characters))
        hca_log_file_lines.insert(0, "Search String: {0}\n{1}\n\n".format(hca_header_string_representation, hca_hex_characters))
        hca_log_file_lines.insert(0, "{0}\n\n".format(os.path.basename(uexp_file).encode("utf-8") ))

        ### --- Create File/Window to Hold Log Information --- ###

        #Displays windows with debug information. This will display info about each HCA code string that was found and will display the numbers used in the filename versus what the program read those numbers as (they should be the same).
        if print_files == True: #Only one .uexp file can be selected when print_files is True, so this being here is fine
            print_out_logs_list.append(list(hca_log_file_lines)) #A list of lists.  #Since del hca_log_file_lines[:] happens, it for some reason deletes the info in print_out_logs_list as well, so it as to be a new list.
            print_out_logs_tab_filenames.append(os.path.basename(uexp_file))
        else:
            hca_log_file_lines.insert(0, "Created Directory: {}\n\n\n".format(hca_folder_directory.encode("utf-8") ))
            extraction_log_filename = u"{} - Extraction Log.txt".format(uexp_filename.decode("utf-8"))
            extraction_log_file_directory = os.path.abspath( os.path.join(hca_folder_directory, extraction_log_filename) )
            with open(extraction_log_file_directory, 'wb') as extraction_log:
                extraction_log.writelines(hca_log_file_lines)

        del list_of_hca_filenames[:]
        del list_of_hca_offsets[:]
        del list_of_offset_lengths[:]
        del hca_log_file_lines[:]
        del offset_size[:]
        
        pass #end of uexp for loop


    
    if len(selected_uexp_files_that_failed) == len(selected_uexp_files):
        extract_fail_text = "Extraction Failed. Failed to find any Audio Headers in chosen file(s)\n"
        if search_for_finish_string == False:
            text_display_string.set("{1}Search String: {0}".format(repr(replacing_search_string)[1:-1], extract_fail_text))
        else:
            text_display_string.set("{2}Search String: {0}  |  Finish String: {1}".format(repr(replacing_search_string)[1:-1], repr(replacing_finish_string)[1:-1], extract_fail_text))
        return

    if print_files == True:
        print_out_extracted_files_window = Toplevel(root_window)
        print_out_extracted_files_window_base_width = Decimal(800)
        print_out_extracted_files_window_base_height = Decimal(800)
        print_out_extracted_files_window.minsize(200, 200)

        WindowCenterPositioner(print_out_extracted_files_window, print_out_extracted_files_window_base_width, print_out_extracted_files_window_base_height, bind_child_window=False)

        extracted_files_window_font_size = InitialWindowFontSize(12, print_out_extracted_files_window.winfo_width(), print_out_extracted_files_window.winfo_height(), print_out_extracted_files_window_base_width, print_out_extracted_files_window_base_height, False)
        print_out_extracted_files_window_12_font = ("Courier", extracted_files_window_font_size)
        print_out_extracted_files_window.wm_title('Files that were extracted from the file')

        print_files_tab_control = ttk.Notebook(print_out_extracted_files_window)#, width=800, height=800, style='Custom.TNotebook')
        print_files_tab_control.place(relwidth=1, relheight=1)

        for saved_log_info_index in range(0, len(print_out_logs_list)):
            file_log_filename = u"{}".format(print_out_logs_tab_filenames[saved_log_info_index])

            print_out_extraction_tab_instance = Frame(print_files_tab_control)
            print_files_tab_control.add(print_out_extraction_tab_instance, text=file_log_filename)
            print_out_extraction_frame = Frame(print_out_extraction_tab_instance)

            printed_out_extraction_log = Text(print_out_extraction_frame, font=print_out_extracted_files_window_12_font, wrap="none") # https://coderslegacy.com/python/tkinter-text-widget/
            
            print_out_extraction_scrollbar = ttk.Scrollbar(print_out_extraction_frame, command=printed_out_extraction_log.yview)
            print_out_extraction_x_axis_scrollbar = ttk.Scrollbar(print_out_extraction_frame, orient = "horizontal", command=printed_out_extraction_log.xview)
            print_out_extraction_scrollbar.pack(side="right", fill="y")
            print_out_extraction_x_axis_scrollbar.pack(side="bottom", fill="x")
            printed_out_extraction_log.config(yscrollcommand = print_out_extraction_scrollbar.set, xscrollcommand = print_out_extraction_x_axis_scrollbar.set)
            
            print_out_extraction_frame.pack(fill="both", expand="y")
            
            for log in print_out_logs_list[saved_log_info_index]:
                printed_out_extraction_log.insert("current lineend", log)   # https://stackoverflow.com/questions/59313660/tkinter-how-to-fix-label-and-check-button-not-lining-up
            
            printed_out_extraction_log.config(state="disabled")
            printed_out_extraction_log.pack(fill="both", expand="y")

        del print_out_logs_list[:]
        del print_out_logs_tab_filenames[:]
    else:
        text_display_string.set("Finished extracting .hca files from the .uexp file(s)!")

    if len(selected_uexp_files_that_failed) > 0:
        failed_files_filenames = ", ".join([i for i in selected_uexp_files_that_failed])
        text_display_string.set("Failed to extract {} out of {} files".format(len(selected_uexp_files_that_failed), len(selected_uexp_files) ))

        failed_files_extraction_window = Toplevel(root_window)
        failed_files_extraction_window_base_width = Decimal(400)
        failed_files_extraction_window_base_height = Decimal(400)
        WindowCenterPositioner(failed_files_extraction_window, failed_files_extraction_window_base_width, failed_files_extraction_window_base_height)
    
        failed_files_extraction_window_12_font = InitialWindowFontSize(12, failed_files_extraction_window.winfo_width(), failed_files_extraction_window.winfo_height(), failed_files_extraction_window_base_width, failed_files_extraction_window_base_height)
        failed_files_extraction_window_14_font = InitialWindowFontSize(14, failed_files_extraction_window.winfo_width(), failed_files_extraction_window.winfo_height(), failed_files_extraction_window_base_width, failed_files_extraction_window_base_height)
        failed_files_extraction_window.wm_title('')
    
        failed_files_extraction_frame = LabelFrame(failed_files_extraction_window, text="Files Where Extraction Failed", font=failed_files_extraction_window_14_font, bg="SystemButtonFace")
        failed_files_extraction_frame.pack(fill="both", expand="y")
    
        failed_files_extraction_listbox = Listbox(failed_files_extraction_frame, font=failed_files_extraction_window_12_font, bg="SystemButtonFace")
        failed_files_extraction_scrollbar = ttk.Scrollbar(failed_files_extraction_frame, command=failed_files_extraction_listbox.yview)
        failed_files_extraction_x_axis_scrollbar = ttk.Scrollbar(failed_files_extraction_frame, orient="horizontal", command=failed_files_extraction_listbox.xview)
        failed_files_extraction_scrollbar.pack(side="right", fill="y")
        failed_files_extraction_x_axis_scrollbar.pack(side="bottom", fill="x")
        failed_files_extraction_listbox.config(yscrollcommand = failed_files_extraction_scrollbar.set, xscrollcommand = failed_files_extraction_x_axis_scrollbar.set)
    
        extraction_fail_index = len(selected_uexp_files) - len(selected_uexp_files_that_failed)
        for file_selected in reversed(selected_uexp_files):
            file_selected_file_name = os.path.basename(file_selected)
            if file_selected_file_name not in selected_uexp_files_that_failed:
                failed_files_extraction_listbox.insert(0, u'{1}) {0}'.format(file_selected_file_name, extraction_fail_index) )
                extraction_fail_index -= 1
            pass

        failed_files_extraction_listbox.insert(0, "Files That Were Successfully Extracted:")
        failed_files_extraction_listbox.insert(0, "")
        failed_files_extraction_listbox.insert(0, "")

        extraction_fail_index = len(selected_uexp_files_that_failed)
        for failed_extract_file in reversed(selected_uexp_files_that_failed):
            failed_extract_info = u'{1}) {0}'.format(failed_extract_file, extraction_fail_index)
            failed_files_extraction_listbox.insert(0, failed_extract_info)

            extraction_fail_index -= 1

        failed_files_extraction_listbox.insert(0, "")
    
        failed_files_extraction_listbox.insert(0, "Failed to extract {0} out of the {1} chosen files:".format(len(selected_uexp_files_that_failed), len(selected_uexp_files)) )
        failed_files_extraction_listbox.pack(fill="both", expand="y")

    root_window.bell()
    pass


#Create a folder to hold the extracted .hca files from a .uexp file.
def CreateFolder(created_hca_files_directory): # https://gist.github.com/keithweaver/562d3caa8650eefe7f84fa074e9ca949
    try:
        if os.path.exists(created_hca_files_directory) == False:
            os.makedirs(created_hca_files_directory)
    except OSError:
        text_display_string.set("Error in creating directory: {}".format(created_hca_files_directory))

    pass


#--------------------------------------------------------- CREATING HCA FILES SECTION --------------------------------------------------------------#





#------------------------------------------------------------------------------------------ OPTIONS MENU SECTION -----------------------------------------------------------------------------------------------#

# General Option Variables spaced out by the type of .get the config_parser (.getint, .getboolean, .get). 
# These distinctions are important as doing config_parser.get on a variable ment to be a boolean will set the varialbe with a string. Instead of False, it is "False"

#General Options
automatically_sort_files = config_parser.getboolean(config_file_options_section, 'automatically_sort_files') # https://linuxhint.com/read_write_ini_conf_python/

set_byte_unit = config_parser.getint(config_file_options_section, 'set_byte_unit')
round_to_decimal_position = config_parser.getint(config_file_options_section, 'round_to_decimal_position')
source_scroll_increment = config_parser.getint(config_file_options_section, 'source_scroll_increment')
replace_scroll_increment = config_parser.getint(config_file_options_section, 'replace_scroll_increment')
both_buttons_scroll_type = config_parser.getint(config_file_options_section, 'both_buttons_scroll_type')
number_base = config_parser.getint(config_file_options_section, 'number_base')

automatically_replace_using_filename = config_parser.getboolean(config_file_options_section, 'automatically_replace_using_filename')

replacing_search_string = config_parser.get(config_file_options_section, 'replacing_search_string')

search_string_used_manual_input = config_parser.getboolean(config_file_options_section, 'search_string_used_manual_input')

replacing_finish_string = config_parser.get(config_file_options_section, 'replacing_finish_string')

search_for_finish_string = config_parser.getboolean(config_file_options_section, 'search_for_finish_string')
finish_string_used_manual_input = config_parser.getboolean(config_file_options_section, 'finish_string_used_manual_input')


#Color Options
use_rgb_color_code = config_parser.getboolean(config_file_color_options_section, 'use_rgb_color_code')

source_section_color = config_parser.get(config_file_color_options_section, 'source_section_color')
replacement_section_color = config_parser.get(config_file_color_options_section, 'replacement_section_color')
default_button_color = config_parser.get(config_file_color_options_section, 'default_button_color')
button_highlight_color = config_parser.get(config_file_color_options_section, 'button_highlight_color')

both_scroll_buttons_same_color = config_parser.getboolean(config_file_color_options_section, 'both_scroll_buttons_same_color')
both_up_scroll_button_color = config_parser.get(config_file_color_options_section, 'both_up_scroll_button_color')
both_down_scroll_button_color = config_parser.get(config_file_color_options_section, 'both_down_scroll_button_color')

to_file_buttons_same_color = config_parser.getboolean(config_file_color_options_section, 'to_file_buttons_same_color')
to_first_source_file_button_color = config_parser.get(config_file_color_options_section, 'to_first_source_file_button_color')
to_first_replacement_file_button_color = config_parser.get(config_file_color_options_section, 'to_first_replacement_file_button_color')
to_last_source_file_button_color = config_parser.get(config_file_color_options_section, 'to_last_source_file_button_color')
to_last_replacement_file_button_color = config_parser.get(config_file_color_options_section, 'to_last_replacement_file_button_color')

extract_button_color = config_parser.get(config_file_color_options_section, 'extract_button_color')
compare_button_color = config_parser.get(config_file_color_options_section, 'compare_button_color')
compare_O_label_color = config_parser.get(config_file_color_options_section, 'compare_O_label_color')
compare_X_label_color = config_parser.get(config_file_color_options_section, 'compare_X_label_color')
fill_button_color = config_parser.get(config_file_color_options_section, 'fill_button_color')
replace_button_color = config_parser.get(config_file_color_options_section, 'replace_button_color')


widget_background_colors_with_text_list = [source_section_color, replacement_section_color,
                                           default_button_color,
                                           button_highlight_color,
                                           both_up_scroll_button_color, both_down_scroll_button_color,
                                           to_first_source_file_button_color, to_first_replacement_file_button_color, to_last_source_file_button_color, to_last_replacement_file_button_color,
                                           extract_button_color,
                                           compare_button_color, compare_O_label_color, compare_X_label_color,
                                           fill_button_color, replace_button_color]


#Displays a window with various tabs that contain all of the available options the user can choose from.
def OptionsWindow():
    global options_window
    options_window = Toplevel()
    global options_window_base_width
    global options_window_base_height
    options_window_base_width = Decimal(600) #1.25 ratio for width against height
    options_window_base_height = Decimal(480)
    options_window.minsize(options_window_base_width / Decimal(2), options_window_base_height / Decimal(2))
    WindowCenterPositioner(options_window, options_window_base_width, options_window_base_height)

    options_window_7_font = InitialWindowFontSize(7, options_window.winfo_width(), options_window.winfo_height(), options_window_base_width, options_window_base_height)
    options_window_8_font = InitialWindowFontSize(8, options_window.winfo_width(), options_window.winfo_height(), options_window_base_width, options_window_base_height)
    options_window_9_font = InitialWindowFontSize(9, options_window.winfo_width(), options_window.winfo_height(), options_window_base_width, options_window_base_height)
    options_window_11_font = InitialWindowFontSize(11, options_window.winfo_width(), options_window.winfo_height(), options_window_base_width, options_window_base_height)

    options_window.wm_title('Select The Options You Wish To Change')


    global tabControl
    tabControl = ttk.Notebook(options_window)
    tabControl.place(relwidth=1, relheight=0.95) # Set All to default and Presets for All options

    options_text_box = Label(options_window, bg="black", fg="white", textvariable=text_display_string, font="{} {} bold".format(options_window_9_font[0], options_window_9_font[1]), wraplength=Decimal(options_window.winfo_width()), justify="left")
    options_text_box.place(relwidth=1, relheight=0.05, rely=0.95) #Text box of the options window

    general_tab = Frame(tabControl)
    color_tab = Frame(tabControl)
    tabControl.add(general_tab, text='General')
    tabControl.add(color_tab, text='Color')

    options_frame = Frame(general_tab)
    options_frame.pack(fill='both', expand='yes')

    color_presets_frame = Frame(color_tab)
    color_options_frame = Frame(color_tab)
    color_presets_frame.place(relwidth=1, relheight=0.1)
    color_options_frame.place(relwidth=1, relheight=0.9, rely=Decimal(color_tab.winfo_height()) * Decimal(0.1)  )


    #Sets up the options in the General Tab for the user to choose from.
    def CreatingGeneralOptionsTab():
        global automatically_sort_files_check_bool
        automatically_sort_files_check_bool = BooleanVar()
        automatically_sort_files_check_bool.set(automatically_sort_files)
        automatically_sort_files_checkbox = Checkbutton(options_frame, variable=automatically_sort_files_check_bool, fg="black", text='Automatically Sort Added Files?', command=SetAutomaticFileSort)
        
        
        global byte_conversion_check
        byte_conversion_check = Menubutton(options_frame)
        SetByteUnit(set_byte_unit, True)
        
        byte_conversion_check.menu = Menu(byte_conversion_check, tearoff=0)
        byte_conversion_check.config(menu=byte_conversion_check.menu)
        byte_conversion_check.menu.add_command (label="Bytes", command=lambda : SetByteUnit(0))
        byte_conversion_check.menu.add_command (label="KB", command=lambda : SetByteUnit(1))
        byte_conversion_check.menu.add_command (label="MB", command=lambda : SetByteUnit(2))
        byte_conversion_check.menu.add_command (label="GB", command=lambda : SetByteUnit(3))
        byte_conversion_check.menu.add_command (label="TB", command=lambda : SetByteUnit(4))
        
        
        #Creates the child window where the user can change the Decimal Positon option.
        def ChangeDecimalPosition():
            decimal_position_input_window = Toplevel()
            decimal_position_input_window.resizable(False, False)

            decimal_position_input_window_base_width = Decimal(200)
            decimal_position_input_window_base_height = Decimal(200)
            options_window.minsize(decimal_position_input_window_base_width / Decimal(2), decimal_position_input_window_base_height / Decimal(2))
            WindowCenterPositioner(decimal_position_input_window, decimal_position_input_window_base_width, decimal_position_input_window_base_height, options_window)

            decimal_position_rounding_type_frame = Frame(decimal_position_input_window)
            decimal_position_rounding_type_frame.place(relwidth=1, relheight=0.7)

            use_rounding = IntVar()
            if round_to_decimal_position < 0:
                use_rounding.set(2)
            else:
                use_rounding.set(1)

            def DetermineRoundingUsed():
                if use_rounding.get() == 2:
                    decimal_position_user_input.delete(0,"end")
                    decimal_position_user_input.insert(0, "No Rounding!")
                    decimal_position_user_input.config(state="disabled")
                else:
                    decimal_position_user_input.config(state="normal")
                    decimal_position_user_input.delete(0,"end")
                    if round_to_decimal_position < 0:
                        decimal_position_user_input.insert(0, 2)
                    else:
                        decimal_position_user_input.insert(0, round_to_decimal_position)
                pass

            #Font Calculations
            dp_width_scale = Decimal(decimal_position_input_window.winfo_width()) / decimal_position_input_window_base_width
            dp_height_scale = Decimal(decimal_position_input_window.winfo_height()) / decimal_position_input_window_base_height
            decimal_position_input_window_font_size = Decimal(12) * ((dp_width_scale+dp_height_scale)/Decimal(2))
            dp_font = ("Helvetica", int(round(decimal_position_input_window_font_size)) )

            yes_rounding_type = Radiobutton(decimal_position_rounding_type_frame, variable=use_rounding, value=1, command=DetermineRoundingUsed, font=dp_font, text="Use Rounding")
            no_rounding_type =  Radiobutton(decimal_position_rounding_type_frame, variable=use_rounding, value=2, command=DetermineRoundingUsed, font=dp_font, text=" No Rounding ")
            yes_rounding_type.place(relwidth=1, relheight=0.15, rely=0.30)
            no_rounding_type.place(relwidth=1, relheight=0.15, rely=0.50)


            decimal_position_input_frame = Frame(decimal_position_input_window)
            decimal_position_input_frame.place(relwidth=1, relheight=0.3, rely=0.7)

            decimal_position_affirm_button = Button(decimal_position_input_frame, text="Use", font=dp_font, bg=default_button_color, fg=default_button_text_color, command=lambda : SetDecimalPosition(None, False, use_rounding.get()) )
            decimal_position_affirm_button.place(relwidth=0.3, relheight=1)
            decimal_position_affirm_button.bind("<Enter>", HoveringOverWidget)
            decimal_position_affirm_button.bind("<Leave>", NotHoveringOverWidget)

            global decimal_position_user_input
            decimal_position_user_input = Entry(decimal_position_input_frame, justify="center", font=dp_font, relief = "ridge", bd=5)
            decimal_position_user_input.place(relwidth=0.7, relheight=1, relx=0.3)
            DetermineRoundingUsed()
            decimal_position_user_input.bind('<Return>', lambda e: SetDecimalPosition(e, False, use_rounding.get()) ) # https://stackoverflow.com/questions/16996432/how-do-i-bind-the-enter-key-to-a-function-in-tkinter

            #Only allow number inputs from the user into the Entry widget and allow the "No Rounding!" string if the user selects to not use any rounding.
            def InputInDeicmalPositionEntryWidgetCheck(action_code, inputed_string_character):
                if action_code == "1": #Inputing
                    if inputed_string_character == "No Rounding!":
                        return True

                    try:
                        int(inputed_string_character)
                    except:
                        return False

                return True
            decimal_number_input_check = (decimal_position_user_input.register(InputInDeicmalPositionEntryWidgetCheck),'%d', '%S')
            decimal_position_user_input.config(validate='key', validatecommand=decimal_number_input_check)

            decimal_position_input_window.mainloop()
        
        global decimal_position_button
        decimal_position_button = Button(options_frame, command=ChangeDecimalPosition)
        SetDecimalPositionText()


        #Creates the child window where the user can change the Scroll Increment option.
        def ChangeScrollingIncrement():
            index_move_by_input_window = Toplevel()
            index_move_by_input_window.resizable(False, False)
            index_move_by_input_window.wm_title("Select A Section's Increment To Change")

            index_move_by_input_window_base_width = Decimal(400)
            index_move_by_input_window_base_height = Decimal(200)

            WindowCenterPositioner(index_move_by_input_window, index_move_by_input_window_base_width, index_move_by_input_window_base_height, options_window)

            ibm_font = InitialWindowFontSize(12, index_move_by_input_window.winfo_width(), index_move_by_input_window.winfo_height(), index_move_by_input_window_base_width, index_move_by_input_window_base_height)
            ibm_change_button_font = InitialWindowFontSize(10, index_move_by_input_window.winfo_width(), index_move_by_input_window.winfo_height(), index_move_by_input_window_base_width, index_move_by_input_window_base_height)
            ibm_both_buttons_use_type_font = InitialWindowFontSize(9, index_move_by_input_window.winfo_width(), index_move_by_input_window.winfo_height(), index_move_by_input_window_base_width, index_move_by_input_window_base_height)


            change_index_move_by_option_type = IntVar()
            change_index_move_by_option_type.set(1)
            def ShowCurrentScrollingIncrement():
                index_move_by_user_input.delete(0, 'end')
                background_frame_color = "SystemButtonFace"
                background_frame_text_color = "black"
                background_frame_select_color = "white"
                selected_option_type = change_index_move_by_option_type.get()
                if selected_option_type == 1:
                    if source_scroll_increment == replace_scroll_increment:
                        index_move_by_user_input.insert(0, source_scroll_increment)
                    index_move_by_input_change_button.config(text="Change\nBoth")

                    background_frame_color = both_up_scroll_button_color
                    background_frame_text_color = both_up_scroll_button_text_color
                elif selected_option_type == 2:
                    index_move_by_user_input.insert(0, source_scroll_increment)
                    index_move_by_input_change_button.config(text="Change\nSource")

                    background_frame_color = source_section_color
                    background_frame_text_color = source_section_text_color 
                elif selected_option_type == 3:
                    index_move_by_user_input.insert(0, replace_scroll_increment)
                    index_move_by_input_change_button.config(text="Change\nReplacement")

                    background_frame_color = replacement_section_color
                    background_frame_text_color = replacement_section_text_color

                background_frame_select_color = CalculateTextColor(background_frame_text_color)

                index_move_by_option_types_frame.config(bg=background_frame_color)
                change_both_indexes.config(bg=background_frame_color, fg=background_frame_text_color, activebackground=background_frame_color, selectcolor=background_frame_select_color)
                change_source_index.config(bg=background_frame_color, fg=background_frame_text_color, activebackground=background_frame_color, selectcolor=background_frame_select_color)
                change_replace_index.config(bg=background_frame_color, fg=background_frame_text_color, activebackground=background_frame_color, selectcolor=background_frame_select_color)
                pass


            both_buttons_index_type = IntVar()
            both_buttons_index_type.set(both_buttons_scroll_type)
            #Calls the functions to change and save the type of scrolling used with the "Both" scroll buttons.
            def BothScrollButtonsIncrementTypeUsed():
                global both_buttons_scroll_type
                both_buttons_scroll_type = both_buttons_index_type.get()
                SetBothScrollButtonsIncrement()
                OverwriteOptionsData("both_buttons_scroll_type", both_buttons_scroll_type)


            index_move_by_option_types_frame = Frame(index_move_by_input_window)
            index_move_by_option_types_frame.place(relwidth=1, relheight=0.8)

            both_button_index_move_by_option_type_frame = LabelFrame(index_move_by_option_types_frame, text='For scrolling with "Both" buttons', font=ibm_both_buttons_use_type_font, bd=4, relief="ridge")
            both_button_index_move_by_option_type_frame.place(relwidth=0.98, relheight=0.40, relx=0.01, rely=0.0)

            both_buttons_lower_index_type = Radiobutton(both_button_index_move_by_option_type_frame, variable=both_buttons_index_type, value=1, command=BothScrollButtonsIncrementTypeUsed, font=ibm_both_buttons_use_type_font, text="Use Lower\nof the Two") #Use Lower of the Two
            both_buttons_higher_index_type = Radiobutton(both_button_index_move_by_option_type_frame, variable=both_buttons_index_type, value=2, command=BothScrollButtonsIncrementTypeUsed, font=ibm_both_buttons_use_type_font, text="Use Higher\nof the Two") #Use Higher of the Two
            both_buttons_seperate_indexes_type = Radiobutton(both_button_index_move_by_option_type_frame, variable=both_buttons_index_type, value=3, command=BothScrollButtonsIncrementTypeUsed, font=ibm_both_buttons_use_type_font, text="Use Each Section's\nRespective Value") #Use Each Section's Respective Value

            f1_div_3 = Decimal(1) / Decimal(3)
            both_buttons_lower_index_type.place(relwidth=f1_div_3, relheight=1, rely = 0.0)
            both_buttons_higher_index_type.place(relwidth=f1_div_3, relheight=1, relx=f1_div_3, rely = 0.00)
            both_buttons_seperate_indexes_type.place(relwidth=f1_div_3, relheight=1, relx=2 * f1_div_3, rely = 0.0)

           
            change_both_indexes =  Radiobutton(index_move_by_option_types_frame, variable=change_index_move_by_option_type, value=1, command=ShowCurrentScrollingIncrement, font=ibm_font, text="Both")
            change_source_index =  Radiobutton(index_move_by_option_types_frame, variable=change_index_move_by_option_type, value=2, command=ShowCurrentScrollingIncrement, font=ibm_font, text="Source")
            change_replace_index = Radiobutton(index_move_by_option_types_frame, variable=change_index_move_by_option_type, value=3, command=ShowCurrentScrollingIncrement, font=ibm_font, text="Replacement")

            change_both_indexes.place(relwidth=1, relheight=0.15, rely = 0.45)
            change_source_index.place(relwidth=1, relheight=0.15, rely = 0.60)
            change_replace_index.place(relwidth=1, relheight=0.15, rely = 0.75)


            index_move_by_input_window_input_frame = Frame(index_move_by_input_window)
            index_move_by_input_window_input_frame.place(relwidth=1, relheight=0.2, rely=0.8)

            index_move_by_input_change_button = Button(index_move_by_input_window_input_frame, font=ibm_change_button_font, bg=default_button_color, fg=default_button_text_color, command=lambda: SetScrollingIncrement(None, False, change_index_move_by_option_type.get()) ) # text="Change",
            index_move_by_input_change_button.place(relwidth=0.3, relheight=1)
            index_move_by_input_change_button.bind("<Enter>", HoveringOverWidget)
            index_move_by_input_change_button.bind("<Leave>", NotHoveringOverWidget)

            global index_move_by_user_input
            index_move_by_user_input = Entry(index_move_by_input_window_input_frame, justify="center", font=ibm_font, relief="ridge", bd=5)
            index_move_by_user_input.place(relwidth=0.7, relheight=1, relx=0.3)
            index_move_by_user_input.bind('<Return>', lambda e: SetScrollingIncrement(e, False, change_index_move_by_option_type.get()) )

            def DecimalNumberInputedInEntryWidget(action_code, inputed_string_character):
                if action_code == "1": #Inputing
                    try:
                        int(inputed_string_character)
                    except:
                        return False

                return True
            decimal_number_input_check = (index_move_by_user_input.register(DecimalNumberInputedInEntryWidget),'%d', '%S')
            index_move_by_user_input.config(validate='key', validatecommand=decimal_number_input_check)

            ShowCurrentScrollingIncrement()

            pass

        global index_move_by_button
        index_move_by_button = Button(options_frame, command=ChangeScrollingIncrement)
        SetScrollingIncrementOptionText()
        
        
        global number_base_button
        number_base_button = Menubutton(options_frame)
        SetBaseNumber(number_base, True) #This sets the button text
        
        number_base_button.menu = Menu(number_base_button, tearoff=0)
        number_base_button.config(menu=number_base_button.menu)
        number_base_button.menu.add_command (label="Hexadecimal (Base 16)", command=lambda : SetBaseNumber(1))
        number_base_button.menu.add_command (label="Decimal (Base 10)", command=lambda : SetBaseNumber(2))
        number_base_button.menu.add_command (label="Octal (Base 8)", command=lambda : SetBaseNumber(3))
        
        
        global number_in_filename_check_bool
        number_in_filename_check_bool = BooleanVar()
        number_in_filename_check_bool.set(automatically_replace_using_filename)
        number_in_filename_checkbox = Checkbutton(options_frame, variable=number_in_filename_check_bool, fg="black", text='Automatically Replace the .uexp File(s)?\n(Number and a space MUST be in\nfront of your Replacement file\'s file name)\nEx: "05 Ryu Light Kick 2.hca"', command=UseNumberInFileName)
        
        
        #Creates the child window where the user can change the Search String and Finish String options.
        def ChangeSearchString(search_string_to_change):
            search_string_input_window = Toplevel()
            search_string_input_window.resizable(False, False)
            search_string_input_window_base_width = Decimal(200)
            search_string_input_window_base_height = Decimal(200)
            options_window.minsize(search_string_input_window_base_width / Decimal(2), search_string_input_window_base_height / Decimal(2))
            WindowCenterPositioner(search_string_input_window, search_string_input_window_base_width, search_string_input_window_base_height, options_window)

            search_string_types_frame = Frame(search_string_input_window)
            search_string_types_frame.place(relwidth=1, relheight=0.7)

            set_search_string_type = IntVar()
            set_search_string_type.set(1)
            
            #To make the entry widget no longer have focus.  # https://stackoverflow.com/questions/4299432/in-tkinter-how-do-i-remove-focus-from-a-widget
            def RemoveFocusFromEntryWidget():
                type_hex_codes.focus_set() # This is so if you go to the type_manual button and back to type_hex_codes, the replacing_search_string won't still be there (because the entry widget has lost focus and can be selected again).


            #Font Calculations
            ss_width_scale = Decimal(search_string_input_window.winfo_width()) / search_string_input_window_base_width
            ss_height_scale = Decimal(search_string_input_window.winfo_height()) / search_string_input_window_base_height
            search_string_input_window_font_size = Decimal(12) * ((ss_width_scale+ss_height_scale)/Decimal(2))
            ss_font = ("Helvetica", int(round(search_string_input_window_font_size)) )

            type_hex_codes =  Radiobutton(search_string_types_frame, variable=set_search_string_type, value=1, command=RemoveFocusFromEntryWidget, font=ss_font, text="Input Hex Offset")
            type_manual =  Radiobutton(search_string_types_frame, variable=set_search_string_type, value=3, font=ss_font, text="Input Manual String")
            type_hex_codes.place(relwidth=1, relheight=0.15, rely=0.35)
            type_manual.place(relwidth=1, relheight=0.15, rely=0.55)


            search_string_input_frame = Frame(search_string_input_window)
            search_string_input_frame.place(relwidth=1, relheight=0.3, rely=0.7)

            search_string_set_button = Button(search_string_input_frame, text="Set", font=ss_font, bg=default_button_color, fg=default_button_text_color, command=lambda : SetSearchString(None, False, search_string_to_change, set_search_string_type.get()) )
            search_string_set_button.place(relwidth=1, relheight=0.4, rely=0.6)
            search_string_set_button.bind("<Enter>", HoveringOverWidget)
            search_string_set_button.bind("<Leave>", NotHoveringOverWidget)

            global search_string_user_input
            search_string_user_input = Entry(search_string_input_frame, justify="center", font=ss_font, relief = "ridge", bd=5)
            search_string_user_input.place(relwidth=1, relheight=0.6)

            if search_string_to_change == 1:
                #Enables/Disables the other widgets in the window based on if the user wants to use the Finish Search String or not.
                def SetSearchForSeachFinishSearchStringBoolean():
                    global search_for_finish_string
                    if search_for_finish_string == True:
                        search_for_finish_string = False
                        search_string_user_input.config(state="disabled")
                        type_hex_codes.config(state="disabled")
                        type_manual.config(state="disabled")
                        search_string_set_button.config(state="disabled", bg="gray", fg="black")
                        pass
                    else:
                        search_for_finish_string = True
                        search_string_user_input.config(state="normal")
                        type_hex_codes.config(state="normal")
                        type_manual.config(state="normal")
                        search_string_set_button.config(state="normal", bg=default_button_color, fg=default_button_text_color)

                    OverwriteOptionsData("search_for_finish_string", str(search_for_finish_string))
                    pass


                final_string_font_size = Decimal(8) * ((ss_width_scale+ss_height_scale)/Decimal(2))
                fs_font = ("Helvetica", int(round(final_string_font_size)) )

                use_finish_string = BooleanVar()
                use_finish_string.set(search_for_finish_string)
                use_finish_string_checkbutton = Checkbutton(search_string_types_frame, variable=use_finish_string, font=fs_font, text="Search for the End Header?", command=SetSearchForSeachFinishSearchStringBoolean)
                use_finish_string_checkbutton.place(relwidth=1, relheight=0.15, rely=0.10)

                search_string_using = replacing_finish_string
                manaul_input_using = finish_string_used_manual_input
            else:
                search_string_using = replacing_search_string
                manaul_input_using = search_string_used_manual_input


            if manaul_input_using == True:
                hex_character = search_string_using
            else:
                hex_character = "".join(r"\x{:02x}".format(ord(c)) for c in search_string_using)
            search_string_user_input.insert(0, hex_character)
            search_string_user_input.bind('<Return>', lambda e: SetSearchString(e, False, search_string_to_change, set_search_string_type.get()))

            #Remove the contents of the Entry widget and make it empty upon clicking it.
            def DeleteSearchStringUponClicking(event): # Based on this but using '<FocusIn> instead' # https://stackoverflow.com/questions/34744768/entry-window-in-tkinter-is-not-deleting
                if search_string_user_input.get().encode("utf-8") == hex_character and set_search_string_type.get() == 1:
                    search_string_user_input.delete(0, "end") # https://coderslegacy.com/python/tkinter-clear-entry/
                pass
            search_string_user_input.bind('<FocusIn>', DeleteSearchStringUponClicking )


            deletion_type = IntVar()
            #Determines if the user is deleting with the "BackSpace" key or "Delete" key on their keyboard.
            def SetDeleteType(key_pressed_event):
                if key_pressed_event.keysym == "BackSpace":
                    deletion_type.set(1)
                elif key_pressed_event.keysym == "Delete":
                    deletion_type.set(2)
                pass
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
            search_string_user_input.bind('<BackSpace>', SetDeleteType)
            search_string_user_input.bind('<Delete>', SetDeleteType)
            


            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
            # http://tcl.tk/man/tcl8.5/TkCmd/entry.htm#M7
            #Spaces out the inputed hex numbers so each hex number has 2-digits so the numbers from inputed by the user can then properly be converted into a string.
            def RepositionInputedHexNumbers(action_code, text_change_value, text_remove_index, inputed_text_string, current_text_string): # https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/35554720#35554720
                if set_search_string_type.get() != 1 or text_change_value == "": #Note: (text_change_value == "") is for when the Entry widget gets deleted by code (entrywidget.delete(0, "end")) and not by the user.
                    return True

                #Function Iterates through each character in the string list that was taken from the text in the entry widget (that is what is passed as the parameter).
                def EntryStringSorter(sort_through_string):
                    if sort_through_string[0] == " ":
                        sort_through_string.pop(0)

                    if len(sort_through_string) <= 2:
                        return "".join(sort_through_string) #Return the combination of each character in the list into a string

                    stay_in_while_loop = True
                    exit_while_loop = True
                    saftey_precaution = 0
                    
                    entry_string_index = 0

                    while stay_in_while_loop == True:
                        saftey_precaution += 1
                        exit_while_loop = True
                        digit = entry_string_index + 1
                        for string_character in sort_through_string: #This for loop works on the fact that the "sort_through_string" is a list of each character from the "text_change_value" string                            
                            #This for loop iterates through each character that will be in the entry string, including blank spaces(" ").
                            #The string characters are grouped up as a set of 3. The for loop checks the characters in the set match what the entry string should be presented as:
                            # Characters 1 and 2 should not be a blank space, but the 3rd character should be).
                            #If the character in its position does not match, there are if statements to check

                            if digit % 3 == 1 and string_character == " ": #1st offset in set #Remainder is 1/3
                                current_set_3rd_digit = entry_string_index + 2
                                previous_2nd_set_digit = entry_string_index - 2

                                #If the current hex character is not the 1st two of the list and the current index is less than the final two of the list and
                                # (01 23 45 67 89) -> (01 23 5 67 89) -> (01 23  67 89) -> (01 23 67 89)
                                #If the user deletes two hex offsets in the middle of the entry string (after the 1st two and before the last two), delete the leftover empty space

                                if digit > 2 and entry_string_index < len(sort_through_string)-2 and (sort_through_string[current_set_3rd_digit] != " ") and sort_through_string[previous_2nd_set_digit] != " ":
                                    sort_through_string.pop(entry_string_index)
                                    exit_while_loop = False
                                pass
                            elif digit % 3 == 2 and string_character == " ": #2nd offset in set #Remainder is 2/3
                                current_set_1st_digit = entry_string_index - 1 # current_set_1st_digit should never be an empty space, since the "digit % 3 == 1" if statement would go off and take care of it
                                next_1st_set_digit = entry_string_index + 2 #Next 1st set digit; If empty, then that digit is taking the 3rd position of the this set
                 
                                if (entry_string_index >= len(sort_through_string)-2 or sort_through_string[next_1st_set_digit] == " "): # (01 23 45 67 89) -> (0 23 45 67 89) -> (0 2 45 67 89) -> (02 45 67 89)
                                    sort_through_string.pop(entry_string_index)
                                    exit_while_loop = False
                                else: #If the user is just deleting a single hex offset, skip past and ignore: (01 23 45 67 89) -> (0 23 45 67 89) or also (0 23 4 67 89)
                                    digit += 1
                                pass
                            elif digit % 3 == 0 and string_character != " ": #3rd offset in set #Remainder is 0 (3/3 = 1) #If the 3rd string character in the set is not a blank space, insert a blank space before that character.
                                sort_through_string.insert(entry_string_index, " ")
                                exit_while_loop = False


                            if exit_while_loop == False: #If the while loop is not being exited, prepare to restart the for loop and begin from the start.
                                entry_string_index = 0
                                break

                            entry_string_index += 1
                            digit += 1
                            #End of for loop
                            

                        if sort_through_string[len(sort_through_string)-1] == " ": #If the character at the end of the string is a blank space, remove it.
                            entry_string_list.pop()


                        if exit_while_loop == False:
                            stay_in_while_loop = True
                        else:
                            stay_in_while_loop = False


                        if saftey_precaution >= len(text_change_value):
                            text_display_string.set("Error! The code function to sort the hex offsets had its while loop try to go on forever!")
                            break

                        pass #End of while loop
                        
                    return "".join(sort_through_string) #Return the combination of each character in the list into a string


                if action_code == "0": # Deleting
                    # https://www.kite.com/python/answers/how-to-split-a-string-at-every-nth-character-in-python
                    entry_string_list = []

                    if inputed_text_string == " ":
                        delete_string_list = search_string_user_input.get()
                    else:
                        delete_string_list = text_change_value

                    for index in delete_string_list:
                        entry_string_list.append(index)

                    if inputed_text_string == " ":                       
                        if deletion_type.get() == 1 and int(text_remove_index) >= 2: #Backspace Key
                            entry_string_list.pop(int(text_remove_index)-1)
                            
                        elif deletion_type.get() == 2 and int(text_remove_index) <= len(entry_string_list)-2: #Delete Key
                            entry_string_list.pop(int(text_remove_index)+1)      
                        pass

                    entry_string_list = EntryStringSorter(entry_string_list)
                    search_string_user_input.delete(0, "end")
                    search_string_user_input.insert(0, "".join(entry_string_list))

                    if inputed_text_string == " ": #This is needed because I delete the string and put a new one in the entry widget.
                        if deletion_type.get() == 1: #Backspace Key
                            search_string_user_input.icursor(int(text_remove_index)-1)
                        elif deletion_type.get() == 2: #Delete Key
                            search_string_user_input.icursor(int(text_remove_index)+1)
                    else:
                        search_string_user_input.icursor(int(text_remove_index))

                    pass
                elif action_code == "1": #Inserting
                    more_than_one_input = False
                    try: # https://newbedev.com/check-if-a-string-is-hexadecimal
                        if len(inputed_text_string) > 1: #If user copy-pasted their string into the Entry widget
                            more_than_one_input = True
                            combined_no_spaces_string_characters = "".join(inputed_text_string.split())
                            int(combined_no_spaces_string_characters, 16)
                        else:
                            int(inputed_text_string, 16)
                    except:
                        return False
                    
                    text_change_characters_list = []
                    for x in text_change_value:
                        text_change_characters_list.append(x)

                    inserted_hex_offset_characters = list(text_change_characters_list) # Make a new list, not make the two lists the same where a deletion can effect the other
                    
                    if more_than_one_input == True:
                        last_index = len(text_change_characters_list)-1
                        for xd in reversed(text_change_characters_list): #Remove any blank spaces after the end of the last hex offset
                            try:
                                int(xd, 16)
                                break
                            except:
                                inserted_hex_offset_characters.pop(last_index)
                            last_index -= 1
                        
                        intteeger = 0
                        for x in text_change_characters_list: #Remove any blank spaces before the start of the first hex offset
                            try:
                                int(x, 16)
                                break
                            except:
                                inserted_hex_offset_characters.pop(intteeger)
                                intteeger -= 1
                            intteeger += 1
                        pass
                    

                    finish_string = EntryStringSorter(inserted_hex_offset_characters)
                    search_string_user_input.delete(0, "end")
                    search_string_user_input.insert(int(text_remove_index), finish_string)
                    search_string_user_input.icursor("insert")



                # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/universal.html
                search_string_user_input.after_idle(lambda: search_string_user_input.config(validate='key') ) #Makes sure this function doesn't stop after altering the Entry widget directly in code  # https://stackoverflow.com/questions/33582211/entry-validation-stop-working-when-triggered-in-specific-situations
                return True #End of function
                
            typetype = (search_string_user_input.register(RepositionInputedHexNumbers),'%d', '%P', '%i', '%S', '%s')
            search_string_user_input.config( validate='key', validatecommand=typetype )


            if search_string_to_change == 1 and search_for_finish_string == False:
                search_string_user_input.config(state="disabled")
                type_hex_codes.config(state="disabled")
                type_manual.config(state="disabled")
                search_string_set_button.config(state="disabled", bg="gray", fg="black")
            else:
                search_string_user_input.config(state="normal")
                type_hex_codes.config(state="normal")
                type_manual.config(state="normal")
                search_string_set_button.config(state="normal", bg=default_button_color, fg=default_button_text_color)


            search_string_input_window.mainloop()


        global search_string_button
        search_string_button = Button(options_frame, command=lambda: ChangeSearchString(0))
        global start_string_button_title_text
        start_string_button_title_text = "Change Audio Start Header Serach String:\n"
        if search_string_used_manual_input == False:
            try:
                unicode_hex_offset_representation = "".join(r"\x{:02x}".format(ord(c)) for c in replacing_search_string) # https://stackoverflow.com/questions/12214801/print-a-string-as-hexadecimal-bytes/16882092#16882092
                search_string_button.config(text='{2}{1}\n{0}'.format(repr(replacing_search_string)[1:-1], unicode_hex_offset_representation, start_string_button_title_text) )
            except:
                search_string_button.config(text=u'{1}{0}'.format(replacing_search_string.decode("utf-8"), start_string_button_title_text) )
        else:
            search_string_button.config(text=u'{1}{0}'.format(replacing_search_string.decode("utf-8"), start_string_button_title_text) )
        
        global finish_string_button
        finish_string_button = Button(options_frame, command=lambda: ChangeSearchString(1))
        global end_string_button_title_text
        end_string_button_title_text = "Change Audio End Header Serach String:\n"
        if finish_string_used_manual_input == False:
            try:
                unicode_hex_offset_representation = "".join(r"\x{:02x}".format(ord(c)) for c in replacing_finish_string) # https://stackoverflow.com/questions/12214801/print-a-string-as-hexadecimal-bytes/16882092#16882092
                finish_string_button.config(text='{2}{1}\n{0}'.format(repr(replacing_finish_string)[1:-1], unicode_hex_offset_representation, end_string_button_title_text) )
            except:
                finish_string_button.config(text=u'{1}{0}'.format(replacing_finish_string.decode("utf-8"), end_string_button_title_text))
        else:
            finish_string_button.config(text=u'{1}{0}'.format(replacing_finish_string.decode("utf-8"), end_string_button_title_text) )
        

        
        #Set To Default functions
        automatically_sort_files_default_button = Button(options_frame, text='Set Default Automatic Sort Option')
        byte_conversion_default_button = Button(options_frame, text='Set Default File Size Unit Displayed')
        decimal_position_default_button = Button(options_frame, text='Set Default Rounded Decimal Position')
        index_move_by_default_button = Button(options_frame, text='Set Default File Scroll Increment') 
        number_base_default_button = Button(options_frame, text='Set Default Number Base')
        number_in_filename_default_button = Button(options_frame, text='Set Default Auto Replace Option')
        search_string_default_button = Button(options_frame, text='Set Default Start Search String')
        end_string_default_button = Button(options_frame, text='Set Default Stop Search String')
        
        global set_all_to_default_button
        set_all_to_default_button = Button(options_frame, text='Set All General Options To Default', bg='black', fg='white', font=options_window_9_font, relief="ridge", bd=5, command=lambda: SetToDefaultSettings(0))
        set_all_to_default_button.bind("<Enter>", HoveringOverWidget)
        set_all_to_default_button.bind("<Leave>", NotHoveringOverWidget)
        
        global list_of_option_menu_select_buttons
        list_of_option_menu_select_buttons =  [automatically_sort_files_checkbox, byte_conversion_check, decimal_position_button, index_move_by_button, number_base_button, number_in_filename_checkbox,
                                              search_string_button, finish_string_button]
        global list_of_option_menu_default_buttons
        list_of_option_menu_default_buttons = [automatically_sort_files_default_button, byte_conversion_default_button, decimal_position_default_button, index_move_by_default_button, number_base_default_button, number_in_filename_default_button, 
                                               search_string_default_button, end_string_default_button]


        odd_option_color = '#FFFFFF'
        even_option_color = '#CCCCCC'

        select_button_relwidth = Decimal(0.55)
        select_button_relheight = ( Decimal(options_frame.winfo_height()) / Decimal(len(list_of_option_menu_select_buttons) + Decimal(4.56) ) ) / Decimal(options_frame.winfo_height())
        select_button_rely = 0
        select_color_even_type = False
        for select_button in list_of_option_menu_select_buttons:
            if select_color_even_type == False: #Odd number
                select_button_color = odd_option_color
                select_color_even_type = True
            else:                               #Even number
                select_button_color = even_option_color
                select_color_even_type = False

            select_button.config(bg=select_button_color, font=options_window_9_font, bd=4, relief="ridge")

            if ( (select_button == index_move_by_button) or (select_button == decimal_position_button) ):
                drel_height = Decimal(0.64) * (Decimal(2) * select_button_relheight)
                select_button.place(relwidth=select_button_relwidth, relheight=drel_height, rely=select_button_rely)
                select_button_rely += drel_height
            elif select_button == number_in_filename_checkbox or (select_button == search_string_button) or (select_button == finish_string_button):
                select_button.place(relwidth=select_button_relwidth, relheight=Decimal(2) * select_button_relheight, rely=select_button_rely)
                select_button_rely += Decimal(2) * select_button_relheight
            else:
                select_button.place(relwidth=select_button_relwidth, relheight=select_button_relheight, rely=select_button_rely)
                select_button_rely += select_button_relheight
        
            select_button.bind("<Enter>", HoveringOverWidget)
            select_button.bind("<Leave>", NotHoveringOverWidget)


        set_all_to_default_button.place(relwidth=1, relheight=select_button_relheight, rely=select_button_rely)
        

        default_button_relwidth = Decimal(1) - select_button_relwidth
        default_button_relheight = select_button_relheight
        default_button_relx = select_button_relwidth
        default_button_rely = 0
        default_command_index = 1
        for default_button in list_of_option_menu_default_buttons:
            if default_command_index % 2 == 1:  #Odd number
                default_color_option_button_color = odd_option_color
            else:                               #Even number
                default_color_option_button_color = even_option_color

            default_button.config(bg=default_color_option_button_color, font=options_window_9_font, bd=4, relief="ridge", command=lambda iy=(default_command_index): SetToDefaultSettings(iy)) # https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments

            if (default_button == index_move_by_default_button) or (default_button == decimal_position_default_button):
                default_button_relheight = (select_button_relheight * Decimal(2) ) * Decimal(0.64)
            elif (default_button == number_in_filename_default_button) or (default_button == search_string_default_button) or (default_button == end_string_default_button):
                default_button_relheight = select_button_relheight * Decimal(2)
            else:
                default_button_relheight = select_button_relheight

            default_button.place(relwidth=default_button_relwidth, relheight=default_button_relheight, relx=default_button_relx, rely=default_button_rely)
            default_button_rely += default_button_relheight

            default_command_index += 1
        
            default_button.bind("<Enter>", HoveringOverWidget)
            default_button.bind("<Leave>", NotHoveringOverWidget)
        pass

    CreatingGeneralOptionsTab()

    #Sets up the options in the Color Tab for the user to choose from.
    def CreatingColorOptionsTab():
        preset_button_calc = Decimal(0.125) * Decimal(0.75)
        preset1_button = Button(color_presets_frame, text = "Preset 1", command =  lambda: ConfirmPresetUsage(1))
        preset1_button.place(relwidth=(preset_button_calc * Decimal(2)), relheight=1, relx=(preset_button_calc * Decimal(1)) ) #1/8
        preset2_button = Button(color_presets_frame, text = "Preset 2", command =  lambda: ConfirmPresetUsage(2))
        preset2_button.place(relwidth=(preset_button_calc * Decimal(2)), relheight=1, relx=(preset_button_calc * Decimal(3)) ) #3/8
        preset3_button = Button(color_presets_frame, text = "Preset 3", command = lambda: ConfirmPresetUsage(3))
        preset3_button.place(relwidth=(preset_button_calc * Decimal(2)), relheight=1, relx=(preset_button_calc * Decimal(5)) ) #5/8
        set_all_color_options_to_default_button = Button(color_presets_frame, text = "Set All Colors\nBack To Default", command = lambda a=("all"): SetColorsToDefaultSettings(a) )
        set_all_color_options_to_default_button.place(relwidth=0.25, relheight=1, relx=0.75)
        
        #Change the color code that will be used for color button text.
        def ConvertColorCodeWidgetText():
            global use_rgb_color_code
            if use_rgb_color_code == False:
                use_rgb_color_code = True
                color_code_conversion_button.config(text="RGB")
            else:
                use_rgb_color_code = False
                color_code_conversion_button.config(text="HEX")

            OverwriteOptionsData("use_rgb_color_code", str(use_rgb_color_code), tab=1)
            SetColorOptionsButtonNames()


        color_code_conversion_button = Button(color_presets_frame, command=ConvertColorCodeWidgetText)
        color_code_conversion_button.place(relwidth=preset_button_calc, relheight=1)
        if use_rgb_color_code == True:
            color_code_conversion_button.config(text="RGB")
        else:
            color_code_conversion_button.config(text="HEX")


        global color_options_button_names_list
        color_options_button_names_list = ["Source", "Replace",
                                             "Default Button",
                                             "Button Highlight",
                                             "Both Up", "Both Down",
                                             "To First (S) File", "To First File (R)", "To Last (S) File", "To Last File (R)",
                                             "Extract Button",
                                             "Compare Button", "Fillable Files", "Nonfillabe Files",
                                             "Fill Button",
                                             "Replace Button"]

        #Sets the colors that will iterated when the mouse is hovered over a Preset button that has saved colors in its section. If there is no saved colors, then the Preset button will be highlighted by the button highlight color.
        def HoveringOverPresetColorsWidget(event, preset_index):
            global original_preset_button_color
            global original_preset_button_text_color
            global original_preset_button_name_string
            global original_preset_button_font

            preset_button = event.widget
            original_preset_button_color = preset_button.cget('bg')
            original_preset_button_text_color = preset_button.cget('fg')
            original_preset_button_name_string = preset_button.cget('text')
            original_preset_button_font = preset_button.cget('font')

            global color_iterate
            color_iterate = None

            preset_section = ""
            preset_prefix = ""
            if preset_index == 1:
                preset_section = config_file_color_preset1_section
                preset_prefix = "preset1_"
            elif preset_index == 2:
                preset_section = config_file_color_preset2_section
                preset_prefix = "preset2_"
            elif preset_index == 3:
                preset_section = config_file_color_preset3_section
                preset_prefix = "preset3_"
            else:
                text_display_string.set('Error! "preset_index" not equal to corresponding button number! - HoveringOverPresetColorsWidget(event)')
                preset_button.config(bg=button_highlight_color)
                preset_button.config(fg=button_highlight_text_color)
                return

            if config_parser.get(preset_section, "{0}source_section_color".format(preset_prefix)) == "":
                preset_button.config(bg=button_highlight_color)
                preset_button.config(fg=button_highlight_text_color)
                return

            preset_button.config(font=options_window_8_font)

            preset_color_to_iterate_list = [
                config_parser.get(preset_section,            "{0}source_section_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}replacement_section_color".format(preset_prefix)),                        
                config_parser.get(preset_section,            "{0}default_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}button_highlight_color".format(preset_prefix)),
            
                config_parser.get(preset_section,            "{0}both_up_scroll_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}both_down_scroll_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}to_first_source_file_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}to_first_replacement_file_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}to_last_source_file_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}to_last_replacement_file_button_color".format(preset_prefix)),
                
                config_parser.get(preset_section,            "{0}extract_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}compare_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}compare_o_label_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}compare_x_label_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}fill_button_color".format(preset_prefix)),
                config_parser.get(preset_section,            "{0}replace_button_color".format(preset_prefix)) ]

            preset_button_text_hover_9_font = InitialWindowFontSize(9, options_window.winfo_width(), options_window.winfo_height(), options_window_base_width, options_window_base_height)

            color_index = 0
            global varboolvarailbey
            if switch_containers_placement == True or switch_scroll_buttons_placement == True:
                varboolvarailbey = False
            else:
                varboolvarailbey = None
            def IterateThroughPresetColorsSet(preset_color_list, preset_button, color_index):
                global varboolvarailbey
                if varboolvarailbey != None and color_index <= 10:
                    if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                        if varboolvarailbey == True:
                            varboolvarailbey = False
                            if color_index == 1: #Back to Replacement
                                color_index = 2 #set to default button
                        
                            elif color_index == 6: #"To First S"
                                color_index = 4#set to "Both Up"

                            elif color_index == 9: #Back to "To Last R" - previous was "To Last S"
                                color_index = 7#set to "To First R"
                        
                        elif color_index == 0: #Source
                            color_index = 1 #set to replacement

                        elif color_index == 2: #Default Button
                            color_index = 0 #set to source
                            varboolvarailbey = True


                        elif color_index == 4: #"Both Up"
                            color_index = 5 #set to "Both Down"
                            varboolvarailbey = True
                        elif color_index == 5: #Back to "Both Down"
                            color_index = 9 #set to "To Last R"
                        

                        elif color_index == 10: #Extract Button
                            color_index = 8 #set to "To Last S"
                            varboolvarailbey = True

                        elif color_index == 8: # Back to "To Last S"
                            color_index = 6#set to "To First S"

                        elif color_index == 7: # Back to "To Last R"
                            color_index = 10#set to Extract Button
                            #OVER
                        pass
                    elif switch_containers_placement == True:
                        if varboolvarailbey == True:
                            varboolvarailbey = False
                            if color_index == 1: #Back to Replacement
                                color_index = 2 #set to default button
                        
                            elif color_index == 7: #Back to "To First R" - previous was "To First S"
                                color_index = 9#set to #To Last R
                        
                        elif color_index == 0: #Source
                            color_index = 1 #set to replacement

                        elif color_index == 2: #Default Button
                            color_index = 0 #set to source
                            varboolvarailbey = True

                        
                        elif color_index == 6: #"To First S"
                            color_index = 7 #set to "To First R"
                        elif color_index == 8: #"To Last S"
                            color_index = 6 #set to "To First S"
                            varboolvarailbey = True

                        elif color_index == 10: # Extract Button
                            color_index = 8#set to "To Last S"

                        elif color_index == 9: # Back to "To Last R"
                            color_index = 10#set to Extract Button
                            #OVER
                        pass
                    elif switch_scroll_buttons_placement == True:
                        if varboolvarailbey == True:
                            varboolvarailbey = False
                            if color_index == 6: #"To First S"
                                color_index = 4#set to "Both Up"

                            elif color_index == 9: #Back to "To Last R" - previous was "To Last S"
                                color_index = 7#set to "To First R"
                        
                        elif color_index == 4: #"Both Up"
                            color_index = 5 #set to "Both Down"
                            varboolvarailbey = True
                        elif color_index == 5: #Back to "Both Down"
                            color_index = 8 #set to "To Last S"
                        
                        elif color_index == 10: #Extract Button
                            color_index = 6 #set to "To First S"
                        elif color_index == 8: # Back to "To Last S"
                            color_index = 10#set to Extract Button
                            #OVER
                        pass


                    pass

                preset_color = preset_color_list[color_index]
                preset_text_color = CalculateTextColor(preset_color)
                
                if use_rgb_color_code == True:
                    R = int(preset_color[1:3], 16)
                    G = int(preset_color[3:5], 16)
                    B = int(preset_color[5:7], 16)
                    preset_color_color_code = "({0},{1},{2})".format(R, G, B)
                else:
                    preset_color_color_code = preset_color
                preset_button.config(bg=preset_color, fg=preset_text_color, text= "{0}\n{1}".format(color_options_button_names_list[color_index], preset_color_color_code), font=preset_button_text_hover_9_font)
                color_index += 1
                if color_index >= len(preset_color_list):
                    color_index = 0
            
                global color_iterate
                color_iterate = preset_button.after(1000, lambda: IterateThroughPresetColorsSet(preset_color_list, preset_button, color_index)  )
            #preset_button.after_idle(lambda: IterateThroughPresetColorsSet(preset_color_to_iterate_list, preset_button, color_index)) # <- This (using .after_idle) caused a bug where the preset button keeps iterating through the colors despite the mouse not being over it.
            IterateThroughPresetColorsSet(preset_color_to_iterate_list, preset_button, color_index)
        def NotHoveringOverPresetColorsWidget(event):
            preset_button = event.widget
            preset_button.config(bg=original_preset_button_color, fg=original_preset_button_text_color, text=original_preset_button_name_string, font=original_preset_button_font)
            global color_iterate
            if color_iterate != None:
                preset_button.after_cancel(color_iterate)
                color_iterate = None
            pass



        global preset_frame_buttons_list
        preset_frame_buttons_list = [preset1_button, preset2_button, preset3_button, set_all_color_options_to_default_button, color_code_conversion_button]
        preset_button_bind_index = 0
        for preset_color_button in preset_frame_buttons_list:
            preset_color_button.config(fg="black", bd=3, relief="raised", font=options_window_9_font)
            if preset_color_button == set_all_color_options_to_default_button or preset_color_button == color_code_conversion_button:
                preset_color_button.bind("<Enter>", HoveringOverWidget)
                preset_color_button.bind("<Leave>", NotHoveringOverWidget)
            else:
                preset_button_bind_index += 1
                preset_color_button.bind("<Enter>", lambda e, y=(preset_button_bind_index): HoveringOverPresetColorsWidget(e, y))
                preset_color_button.bind("<Leave>", NotHoveringOverPresetColorsWidget)
            pass
        set_all_color_options_to_default_button.config(bg="black", fg="white")


        global source_color_options_button # https://python-forum.io/Thread-NameError-Global-Name-is-not-defined
        source_color_options_button = Button(color_options_frame, bg=source_section_color, fg=source_section_text_color )

        global replace_color_options_button
        replace_color_options_button = Button(color_options_frame, bg=replacement_section_color, fg=replacement_section_text_color)


        global default_button_color_options_button
        default_button_color_options_button = Button(color_options_frame, bg=default_button_color, fg=default_button_text_color)

        global middle_frame_color_options_button
        middle_frame_color_options_button = Button(color_options_frame, bg=button_highlight_color, fg=button_highlight_text_color)

        global both_arrow_buttons_same_color_bool
        both_arrow_buttons_same_color_bool = BooleanVar()
        both_arrow_buttons_same_color_bool.set(both_scroll_buttons_same_color)
        global both_arrow_buttons_same_color_checkbox
        both_arrow_buttons_same_color_checkbox = Checkbutton(color_options_frame, variable=both_arrow_buttons_same_color_bool, command=BothArrowButtonsAreTheSameColor)

        global both_up_color_options_button
        both_up_color_options_button = Button(color_options_frame, text='Change Both Up Color')

        global both_down_color_options_button
        both_down_color_options_button = Button(color_options_frame, text='Change Both Down Color')

        SetColorOfBothArrowColorCheckbutton()


        global top_n_bottom_section_buttons_same_color_bool
        top_n_bottom_section_buttons_same_color_bool = BooleanVar()
        top_n_bottom_section_buttons_same_color_bool.set(to_file_buttons_same_color)
        global top_n_bottom_section_buttons_same_color_checkbox
        top_n_bottom_section_buttons_same_color_checkbox = Checkbutton(color_options_frame, variable=top_n_bottom_section_buttons_same_color_bool, command=AllToIndexButtonsAreTheSameColor)


        global top_source_color_options_button
        top_source_color_options_button = Button(color_options_frame, text='Change To First\n(S) File Color')

        global top_replace_color_options_button
        top_replace_color_options_button = Button(color_options_frame, text='Change To First\nFile (R) Color')

        global bottom_source_color_options_button
        bottom_source_color_options_button = Button(color_options_frame, text='Change To Last\n(S) File Color')

        global bottom_replace_color_options_button
        bottom_replace_color_options_button = Button(color_options_frame, text='Change To Last\nFile (R) Color')

        SetColorOfToFileColorCheckbutton()


        global extract_button_color_options_button
        extract_button_color_options_button = Button(color_options_frame, bg=extract_button_color, fg=extract_button_text_color)


        global compare_button_color_options_button
        compare_button_color_options_button = Button(color_options_frame, bg=compare_button_color, fg=compare_button_text_color)

        global compare_O_label_color_options_button
        compare_O_label_color_options_button = Button(color_options_frame, text='Change Fillable Files Color:\n{0}'.format(compare_O_label_color), bg=compare_O_label_color, fg=compare_O_label_text_color)

        global compare_X_label_color_options_button
        compare_X_label_color_options_button = Button(color_options_frame, text='Change Nonfillable Files Color:\n{0}'.format(compare_X_label_color), bg=compare_X_label_color, fg=compare_X_label_text_color)


        global fill_button_color_options_button
        fill_button_color_options_button = Button(color_options_frame, bg=fill_button_color, fg=fill_button_text_color)


        global replace_button_color_options_button
        replace_button_color_options_button = Button(color_options_frame, bg=replace_button_color, fg=replace_button_text_color)
        


        #Default Color Button Options
        source_color_default_button = Button(color_options_frame, text="Source\n{0}".format(default_source_section_color), bg=default_source_section_color)
        replace_color_default_button = Button(color_options_frame, text="Replace\n{0}".format(default_replacement_section_color), bg=default_replacement_section_color)
        default_button_color_default_button = Button(color_options_frame, text="Default Button\n{0}".format(default_default_button_color), bg=default_default_button_color)
        middle_frame_color_default_button = Button(color_options_frame, text="Middle Frame\n{0}".format(default_button_highlight_color), bg=default_button_highlight_color, fg="white")
        both_arrow_buttons_same_color_default_button = Button(color_options_frame, text='"Both" Buttons\n{0}'.format(default_both_scroll_buttons_color), bg=default_both_scroll_buttons_color)
        top_n_bottom_section_buttons_same_color_default_button = Button(color_options_frame, text='All "To File" buttons\n{0}'.format(default_to_file_scroll_buttons_color), bg=default_to_file_scroll_buttons_color)
        extract_button_color_default_button = Button(color_options_frame, text="Compare Button\n{0}".format(default_extract_button_color), bg=default_extract_button_color)
        compare_button_color_default_button = Button(color_options_frame, text="Compare Button\n{0}".format(default_compare_button_color), bg=default_compare_button_color)
        compare_O_label_color_default_button = Button(color_options_frame, text="Fillable\n{0}".format(default_compare_O_label_color), bg=default_compare_O_label_color)
        compare_X_label_color_default_button = Button(color_options_frame, text="Nonfillable\n{0}".format(default_compare_X_label_color), bg=default_compare_X_label_color, fg="white")
        fill_button_color_default_button = Button(color_options_frame, text="Fill Button\n{0}".format(default_fill_button_color), bg=default_fill_button_color)
        replace_button_color_default_button = Button(color_options_frame, text="Replace Button\n{0}".format(default_replace_button_color), bg=default_replace_button_color)
        
        global color_options_default_button_names_list
        color_options_default_button_names_list = ["Source", "Replace",
                                             "Default Button",
                                             "Button Highlight",
                                             '"Both" Buttons',
                                             '"To File" Buttons',
                                             "Extract Button",
                                             "Compare Button", "Fillable", "Nonfillabe",
                                             "Fill Button",
                                             "Replace Button"]

        global color_options_button_list
        color_options_button_list = [source_color_options_button, replace_color_options_button,
                                     default_button_color_options_button,
                                     middle_frame_color_options_button,
                                     both_arrow_buttons_same_color_checkbox, both_up_color_options_button, both_down_color_options_button,
                                     top_n_bottom_section_buttons_same_color_checkbox, top_source_color_options_button, top_replace_color_options_button, bottom_source_color_options_button, bottom_replace_color_options_button,
                                     extract_button_color_options_button,
                                     compare_button_color_options_button, compare_O_label_color_options_button, compare_X_label_color_options_button,
                                     fill_button_color_options_button,
                                     replace_button_color_options_button]

        global color_options_default_button_list
        color_options_default_button_list = [source_color_default_button, replace_color_default_button,
                                             default_button_color_default_button,
                                             middle_frame_color_default_button,
                                             both_arrow_buttons_same_color_default_button,
                                             top_n_bottom_section_buttons_same_color_default_button,
                                             extract_button_color_default_button,
                                             compare_button_color_default_button, compare_O_label_color_default_button, compare_X_label_color_default_button,
                                             fill_button_color_default_button,
                                             replace_button_color_default_button]

        color_option_relwidth = Decimal(0.75)
        color_option_relx = Decimal(0)
        color_option_widget_height = Decimal(color_options_frame.winfo_height()) / Decimal(12) #11
        color_option_relheight = Decimal(color_option_widget_height) / Decimal(color_options_frame.winfo_height())
        color_option_rely = Decimal(0)
        pause_counting = False
        color_option_use_lower_font_bool = False

        color_option_picker_index = 0
        for color_option in color_options_button_list:

            if ( (color_option == source_color_options_button) or (color_option == both_up_color_options_button) or (color_option == top_source_color_options_button) or (color_option == compare_O_label_color_options_button) ):
                pause_counting = True
                if (color_option == top_source_color_options_button):
                    color_option_relwidth = color_option_relwidth / Decimal(4)
                    color_option_use_lower_font_bool = True
                else:
                    color_option_relwidth = color_option_relwidth / Decimal(2)
                    if use_rgb_color_code == True:
                        color_option_use_lower_font_bool = True
                    else:
                        color_option_use_lower_font_bool = False
                color_option_relx = Decimal(0)

            elif ( (color_option == default_button_color_options_button) or (color_option == top_n_bottom_section_buttons_same_color_checkbox) or (color_option == extract_button_color_options_button) or (color_option == fill_button_color_options_button) ): #middle_frame_color_options_button
                pause_counting = False
                color_option_rely += color_option_relheight
                color_option_relwidth = Decimal(0.75)


            if pause_counting == True:
                color_option.place(relwidth=color_option_relwidth, relx=color_option_relx, relheight=color_option_relheight, rely=color_option_rely)
                color_option_relx += color_option_relwidth
                if color_option_use_lower_font_bool == True:
                    color_option.config(font=options_window_8_font)
                else:
                    color_option.config(font=options_window_9_font)
            else:
                if (color_option == top_n_bottom_section_buttons_same_color_checkbox):
                    if (to_file_buttons_same_color == False and use_rgb_color_code == True):
                        color_option.config(font=options_window_7_font)
                    else:
                        color_option.config(font=options_window_8_font)
                else:
                    color_option.config(font=options_window_9_font)
                color_option.place(relwidth=color_option_relwidth, relheight=color_option_relheight, rely=color_option_rely)
                color_option_rely += color_option_relheight


            if isinstance(color_option, Button):
                color_option.config(command = lambda i=(color_option_picker_index): ColorPicker(i) )
                color_option_picker_index += 1
            elif isinstance(color_option, Checkbutton):
                color_option.config(selectcolor=CalculateTextColor(color_option.cget("fg")) )
                pass
            
            color_option.config(relief="raised", bd=3)

            color_option.bind("<Enter>", HoveringOverWidget)
            color_option.bind("<Leave>", NotHoveringOverWidget)

        SetColorOptionsButtonNames()


        color_set_default_index = 0
        color_default_relwidth = Decimal(1) - color_option_relwidth
        color_default_relx = color_option_relwidth
        color_default_relheight = color_option_relheight
        color_default_rely = 0
        color_default_wrap_length = Decimal(options_window.winfo_width()) * color_default_relwidth

        for color_default in color_options_default_button_list:
            if (color_default == both_arrow_buttons_same_color_default_button) or (color_default == top_n_bottom_section_buttons_same_color_default_button):
                color_default.place(relwidth=color_default_relwidth, relheight=Decimal(2)*color_default_relheight,  relx=color_default_relx, rely=color_default_rely)
                color_default_rely += color_default_relheight

            elif color_default == source_color_default_button or color_default == compare_O_label_color_default_button:
                color_default.place(relwidth=(color_default_relwidth / Decimal(2)), relheight=color_default_relheight,  relx=color_default_relx, rely=color_default_rely)
                color_default_rely -= color_default_relheight

            elif color_default == replace_color_default_button or color_default == compare_X_label_color_default_button:
                color_default.place(relwidth=(color_default_relwidth / Decimal(2)), relheight=color_default_relheight,  relx=(color_default_relx+(color_default_relwidth / Decimal(2)) ), rely=color_default_rely)

            else:
                color_default.place(relwidth=color_default_relwidth, relheight=color_default_relheight,  relx=color_default_relx, rely=color_default_rely)
                
            color_default_rely += color_default_relheight

            
            if ( (color_default == compare_O_label_color_default_button) or (color_default == compare_X_label_color_default_button) ):
                color_default.config(font=options_window_8_font)
            elif ( (color_default == both_arrow_buttons_same_color_default_button) or (color_default == top_n_bottom_section_buttons_same_color_default_button) ):
                color_default.config(font=options_window_11_font)
            else:
                color_default.config(font=options_window_9_font)

            color_default.config(bd=3, command = lambda d=(color_set_default_index): SetColorsToDefaultSettings(d))
            color_set_default_index += 1

            color_default.bind("<Enter>", HoveringOverWidget)
            color_default.bind("<Leave>", NotHoveringOverWidget)


        color_options_half_relwidth = Decimal(0.75)/Decimal(2)
        if switch_containers_placement == True:
            replace_color_options_button.place(relwidth=color_options_half_relwidth, relheight=color_option_widget_height, relx=0, rely=0) #source_color_options_button
            source_color_options_button.place(relwidth=color_options_half_relwidth, relheight=color_option_widget_height, relx=color_options_half_relwidth, rely=0) #replace_color_options_button

            replace_color_default_button.place(relwidth=color_default_relwidth / Decimal(2), relheight=color_default_relheight, relx=color_default_relx, rely=0) #source_color_default_button
            source_color_default_button.place(relwidth=color_default_relwidth / Decimal(2), relheight=color_default_relheight, relx=color_default_relx+(color_default_relwidth / Decimal(2)), rely=0) #replace_color_default_button
        if switch_scroll_buttons_placement == True:
            both_down_color_options_button.place(relwidth=color_options_half_relwidth, relheight=color_option_widget_height, relx=0, rely=color_default_relheight*4)
            both_up_color_options_button.place(relwidth=color_options_half_relwidth, relheight=color_option_widget_height, relx=color_options_half_relwidth, rely=color_default_relheight*4)


        color_options_quarter_relwidth = Decimal(0.75)/Decimal(4)
        if switch_containers_placement == True and switch_scroll_buttons_placement == True:
            bottom_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=0, rely=(color_option_relheight*6))
            bottom_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=color_options_quarter_relwidth, rely=(color_option_relheight*6))
            top_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=2*color_options_quarter_relwidth, rely=(color_option_relheight*6))
            top_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=3*color_options_quarter_relwidth, rely=(color_option_relheight*6))

        elif switch_containers_placement == True:
            top_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=0, rely=(color_option_relheight*6)) #top_source_color_options_button
            top_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=color_options_quarter_relwidth, rely=(color_option_relheight*6)) #top_replace_color_options_button
            bottom_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=2*color_options_quarter_relwidth, rely=(color_option_relheight*6)) #bottom_source_color_options_button
            bottom_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=3*color_options_quarter_relwidth, rely=(color_option_relheight*6)) #bottom_replace_color_options_button

        elif switch_scroll_buttons_placement == True:
            bottom_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=0, rely=(color_option_relheight*6)) #top_source_color_options_button
            bottom_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=color_options_quarter_relwidth, rely=(color_option_relheight*6)) #top_replace_color_options_button
            top_source_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=2*color_options_quarter_relwidth, rely=(color_option_relheight*6)) #bottom_source_color_options_button
            top_replace_color_options_button.place(relwidth=color_options_quarter_relwidth, relheight=color_option_widget_height, relx=3*color_options_quarter_relwidth, rely=(color_option_relheight*6)) #bottom_replace_color_options_button


        pass

    CreatingColorOptionsTab()

    

    #Resize the font size based on option window size and resize the font is the user goes to a previous tab with a different window size than before.
    def ResizeOptionsText(e, change_previous_tab_font_size=False):
        if e.widget == options_window or change_previous_tab_font_size == True: # https://stackoverflow.com/questions/58328686/destroy-events-executes-the-binded-function-5-times#:~:text=def%20on_destroy(self%2C%20event)%3A%0A%20%20%20%20if%20event.widget%20%3D%3D%20self.master%3A%0A%20%20%20%20%20%20%20%20print(%22%7B%7D%3A%20OK%22.format(event.widget))%0A%0Aself.master.bind(%22%3CDestroy%3E%22%2C%20self.on_destroy)
            global options_window_previous_width2
            global options_window_previous_height2
            if change_previous_tab_font_size == True or (e.width != options_window_previous_width2) or (e.height != options_window_previous_height2): # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
                if change_previous_tab_font_size == True:
                    varw=options_window.winfo_width()
                    varh=options_window.winfo_height()
                else:
                    varw=e.width
                    varh=e.height
                    pass
                options_window_previous_width2 = varw
                options_window_previous_height2 = varh

                base_font_size = Decimal(9)


                current_color_width = Decimal(varw) / options_window_base_width
                current_color_height = Decimal(varh) / options_window_base_height
                if current_color_width > current_color_height:
                    used_side = current_color_height
                else:
                    used_side = current_color_width
                size = base_font_size * used_side

                options_text_box.config(font=("Helvetica", int(round(size)), "bold" ) )


                global tabControl
                if tabControl.index("current") == 0:
                    for select_buttons in list_of_option_menu_select_buttons:
                        select_buttons.config(font=("Helvetica", int(round(size)) ) )
                    for default_buttons in list_of_option_menu_default_buttons:
                        default_buttons.config(font=("Helvetica", int(round(size)) ) )
                    set_all_to_default_button.config(font=("Helvetica", int(round(size)) ) )

                    return
                elif tabControl.index("current") == 1: #How to know which tab you are in # https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook/47994363
                    lower_font_size= Decimal(8)
                    low_because_of_rgb_color_code_font_size = Decimal(7)
                    
                    color_option_use_lower_font_bool_e = False
                    for color_options_button in color_options_button_list:
                        if (color_options_button == top_n_bottom_section_buttons_same_color_checkbox):
                            color_option_use_lower_font_bool_e = True
                        elif color_options_button == extract_button_color_options_button:
                            color_option_use_lower_font_bool_e = False
                    
                        if color_option_use_lower_font_bool_e == True:
                            if use_rgb_color_code == True:
                                font_size = low_because_of_rgb_color_code_font_size
                            else:
                                font_size = lower_font_size
                        else:
                            if color_options_button == source_color_options_button or color_options_button == replace_color_options_button:
                                if use_rgb_color_code == True:
                                    font_size = lower_font_size
                                else:
                                    font_size = base_font_size
                            else:
                                font_size = base_font_size

                        size = font_size * used_side
                        color_options_button.config(font=("Helvetica", int(round(size)) ) )
                    

                    higher_font_size = Decimal(11)
                    for color_defaults_button in color_options_default_button_list:

                        if ( (color_defaults_button == color_options_default_button_list[4]) or (color_defaults_button == color_options_default_button_list[5]) ):
                            font_size = higher_font_size
                        elif ( (color_defaults_button == color_options_default_button_list[8]) or (color_defaults_button == color_options_default_button_list[9]) ):
                            font_size = lower_font_size
                        else:
                            font_size = base_font_size
                        
                        size = font_size * used_side
                        color_defaults_button.config(font=("Helvetica", int(round(size)) ) )

                    for x in preset_frame_buttons_list:
                        size = base_font_size * used_side
                        x.config(font=("Helvetica", int(round(size)) ) )
        pass


    global options_window_previous_width2
    global options_window_previous_height2
    options_window_previous_width2 = options_window.winfo_width()
    options_window_previous_height2 = options_window.winfo_height()
    options_window.bind('<<NotebookTabChanged>>', lambda e: ResizeOptionsText(e, change_previous_tab_font_size=True)) # https://stackoverflow.com/questions/49976353/python-tk-notebook-tab-change-check
    options_window.bind('<Configure>', ResizeOptionsText)

    options_window.mainloop()


#------------------------------------------------------------ General Options ------------------------------------------------------------#

#---- Option 1 ---- #
#Sets if the program should automatically sort the files added to the source and replace sections.
def SetAutomaticFileSort():
    global automatically_sort_files
    if automatically_sort_files == automatically_sort_files_check_bool.get():
        return
    automatically_sort_files = automatically_sort_files_check_bool.get()
    OverwriteOptionsData('automatically_sort_files', str(automatically_sort_files) )


#---- Option 2 ---- #
#Sets the unit that the file size will be converted to.
def SetByteUnit(unit_number, set_only_text=False):
    global set_byte_unit
    if set_only_text == False:
        if set_byte_unit == unit_number:
            return
        set_byte_unit = unit_number
        OverwriteOptionsData('set_byte_unit', unit_number)

        UpdateLabels(source_section_scroll_position, 0)
        UpdateLabels(replacement_section_scroll_position, 1)

    if set_byte_unit == 1:
        byte_conversion_check_text = "KB"
    elif set_byte_unit == 2:
        byte_conversion_check_text = "MB"
    elif set_byte_unit == 3:
        byte_conversion_check_text = "GB"
    elif set_byte_unit == 4:
        byte_conversion_check_text = "TB"
    else:
        byte_conversion_check_text = "Bytes"
    byte_conversion_check.config(text='Set Byte Unit: {0}'.format(byte_conversion_check_text))


#---- Option 3 ---- #
#Sets the text of the Decimal Position Option in the Options Window.
def SetDecimalPositionText():
    decimal_position_button_title = "File Size Decimal Position to Round to:\n"
    if round_to_decimal_position < 0:
        decimal_position_button.config(text='{}No Rounding!'.format(decimal_position_button_title))
    else:
        decimal_position_button.config(text='{}{} | {:.{}f}'.format(decimal_position_button_title, round_to_decimal_position, 1, round_to_decimal_position))
    pass
#Sets the decimal position the file size will be rounded to.
def SetDecimalPosition(e, use_default, use_rounding=0):
    try:
        global round_to_decimal_position
        if use_default == True:
            if round_to_decimal_position == 2:
                return
            round_to_decimal_position = 2
        else:
            if (use_rounding != 2 and round_to_decimal_position == int(decimal_position_user_input.get()) ) or (use_rounding == 2 and round_to_decimal_position < 0):
                return
            
        if use_rounding == 2:
            round_to_decimal_position = -1
        elif use_default == True:
            pass
        else:
            round_to_decimal_position = int(decimal_position_user_input.get())
            decimal_position_user_input.delete(0, 'end') # https://coderslegacy.com/python/tkinter-clear-entry/

            decimal_position_user_input.insert(0, round_to_decimal_position)
        SetDecimalPositionText()
        OverwriteOptionsData('round_to_decimal_position', round_to_decimal_position)

        UpdateLabels(source_section_scroll_position, 0)
        UpdateLabels(replacement_section_scroll_position, 1)
    except ValueError: # https://www.youtube.com/watch?v=IbpInH4q4Sg    #This shouldn't occur because of the vaildate command function for this option's Entry widget
        text_display_string.set('Invalid input. Type the number position you wish to round to. Ex: Type "3" for 1.000')
    pass


#---- Option 4 ---- #
#Sets the text of the Scrolling Increment Option in the Options Window.
def SetScrollingIncrementOptionText():
    scrolling_increment_option_title = "Change File Scroll Buttons Increment\n"
    if source_scroll_increment == replace_scroll_increment:
        index_move_by_button.config(text='{1}Both Sections: {0}'.format(source_scroll_increment, scrolling_increment_option_title) )
    else:
        if switch_containers_placement == True:
            index_move_by_button.config(text='{2}R: {1} | S: {0}'.format(source_scroll_increment, replace_scroll_increment, scrolling_increment_option_title) )
        else:
            index_move_by_button.config(text='{2}S: {0} | R: {1}'.format(source_scroll_increment, replace_scroll_increment, scrolling_increment_option_title) )
    pass
#Sets the scrolling increment that the scroll buttons will increment by.
def SetScrollingIncrement(e, using_default, change_index_move_in_section=0):
    global source_scroll_increment
    global replace_scroll_increment
    if using_default == True:
        default_index_move_by = 10
        if (source_scroll_increment == default_index_move_by) and (replace_scroll_increment == default_index_move_by):
            return
        if source_scroll_increment != default_index_move_by:
            source_scroll_increment = default_index_move_by
            OverwriteOptionsData('source_scroll_increment', source_scroll_increment)
        if replace_scroll_increment != default_index_move_by:
            replace_scroll_increment = default_index_move_by
            OverwriteOptionsData('replace_scroll_increment', replace_scroll_increment)
        pass
    else:
        if index_move_by_user_input.get() == "":
            return
        inputed_index_move_by = int(index_move_by_user_input.get() )
        if inputed_index_move_by == 0:
            text_display_string.set("Number cannot be 0 as the arrow buttons will not move the files when pressed.")
            return

        if change_index_move_in_section == 1: #Both Sections
            if (source_scroll_increment == inputed_index_move_by) and (replace_scroll_increment == inputed_index_move_by):
                return

            if source_scroll_increment != inputed_index_move_by:
                source_scroll_increment = inputed_index_move_by
                OverwriteOptionsData('source_scroll_increment', source_scroll_increment)

            if replace_scroll_increment != inputed_index_move_by:
                replace_scroll_increment = inputed_index_move_by
                OverwriteOptionsData('replace_scroll_increment', replace_scroll_increment)
            pass
        elif change_index_move_in_section == 2: #Source Section
            if source_scroll_increment == inputed_index_move_by:
                return
            source_scroll_increment = inputed_index_move_by
            OverwriteOptionsData('source_scroll_increment', source_scroll_increment)
        elif change_index_move_in_section == 3: #Replacement Section
            if replace_scroll_increment == inputed_index_move_by:
                return
            replace_scroll_increment = inputed_index_move_by
            OverwriteOptionsData('replace_scroll_increment', replace_scroll_increment)

        pass
    SetScrollingIncrementOptionText()
    SetBothScrollButtonsIncrement()

#Sets what the values that will be used when the user presses the "Both Up" and "Both Down" scroll buttons.
def SetBothScrollButtonsIncrement():
    global both_scroll_buttons_source_increment
    global both_scroll_buttons_replacement_increment
    both_index_type = both_buttons_scroll_type
    if both_index_type == 1: #Use Lower of the two
        if source_scroll_increment > replace_scroll_increment:
            both_scroll_buttons_source_increment = replace_scroll_increment
            both_scroll_buttons_replacement_increment = replace_scroll_increment
        else:
            both_scroll_buttons_source_increment = source_scroll_increment
            both_scroll_buttons_replacement_increment = source_scroll_increment  
    elif both_index_type == 2: #Use Higher of the two
        if source_scroll_increment > replace_scroll_increment:
            both_scroll_buttons_source_increment = source_scroll_increment
            both_scroll_buttons_replacement_increment = source_scroll_increment
        else:
            both_scroll_buttons_source_increment = replace_scroll_increment
            both_scroll_buttons_replacement_increment = replace_scroll_increment
    else: #Use Each Section's Respective Value
        both_scroll_buttons_source_increment = source_scroll_increment
        both_scroll_buttons_replacement_increment = replace_scroll_increment

    pass


#---- Option 5 ---- #
#Sets what number base will be used when replacing the HCA code blocks in the .uexp file.
def SetBaseNumber(set_number_base, set_only_text=False):
    global number_base
    if set_only_text == False:
        if number_base == set_number_base:
            return
        number_base = set_number_base
        OverwriteOptionsData('number_base', number_base)

    if number_base == 1: #Hex
        number_base_button_text = "Hex (Base 16)"
    elif number_base == 2: #Dec
        number_base_button_text = "Dec (Base 10)"
    elif number_base == 3: #Oct
        number_base_button_text = "Oct (Base 8)"
    number_base_button.config(text='Set Number Base: {0}'.format(number_base_button_text))


#---- Option 6 ---- #
#Sets whether numbers at the start of the name of a file should be read.
def UseNumberInFileName():
    global automatically_replace_using_filename
    if automatically_replace_using_filename == number_in_filename_check_bool.get():
        return
    automatically_replace_using_filename = number_in_filename_check_bool.get()
    OverwriteOptionsData('automatically_replace_using_filename', str(automatically_replace_using_filename) )


#---- Option 7/8 ---- #
#Sets the string that is to be found while reading the .uexp file.
def SetSearchString(e, set_default, search_string_to_change, search_type_used=0):
    global replacing_search_string
    global replacing_finish_string
    global search_string_used_manual_input
    global finish_string_used_manual_input

    if search_string_to_change == 1: #End Search String
        used_search_string = replacing_finish_string
        button_search_string = finish_string_button
        manual_input_used = finish_string_used_manual_input
        default_hex_offsets = '\x40\x55\x54\x46\x00\x00'
        button_string_title = end_string_button_title_text
    else: #Start Search String
        used_search_string = replacing_search_string
        button_search_string = search_string_button
        manual_input_used = search_string_used_manual_input
        default_hex_offsets = '\x48\x43\x41\x00\x02'
        button_string_title = start_string_button_title_text


    if set_default == True:
        if search_string_to_change == 1:
            global search_for_finish_string
            if search_for_finish_string != True:
                search_for_finish_string = True
                OverwriteOptionsData('search_for_finish_string', search_for_finish_string)
        if used_search_string == default_hex_offsets:
            return
        used_search_string = default_hex_offsets # https://www.askpython.com/python/string/python-raw-strings
        default_hex_offsets_string = "".join(r"\x{:02x}".format(ord(c)) for c in used_search_string) # https://stackoverflow.com/questions/12214801/print-a-string-as-hexadecimal-bytes/16882092#16882092
        button_search_string.config(text='{2}{1}\n{0}'.format(repr(used_search_string)[1:-1], default_hex_offsets_string, button_string_title) )
        manual_input_used = False
    else:
        if search_type_used == 1:
            # https://stackoverflow.com/questions/41420622/converting-unicode-string-to-hexadecimal-representation
            # https://stackoverflow.com/questions/9475241/split-string-every-nth-character
            # https://stackoverflow.com/questions/50474645/how-to-prefix-with-0x-and-separate-by-a-list-of-numbers-in-python/50474724

            entry_string = "".join(search_string_user_input.get().upper().split()) # https://www.journaldev.com/23763/python-remove-spaces-from-string
            if len(entry_string) % 2 != 0:
                text_display_string.set("A hex number is missing a digit.")
                return

            try:
                get_text_proper = "".join(search_string_user_input.get().split())

                n = 2
                hex_offsets_list = [entry_string[i:i+n] for i in range(0, len(get_text_proper), n)]
                hex_characters=[]
                for x in hex_offsets_list:
                    hex_characters.append('{:c}'.format(int(x,16)) ) #Not exactly the answer given but I changed it to work.  # https://stackoverflow.com/questions/47497536/python-string-format-and-invalid-x-escape

                character_offset_string = "".join(hex_characters)
                if used_search_string == character_offset_string:
                    return
            except:
                if len(entry_string) % 2 == 0: #Even number
                    text_display_string.set("An inputed hex number(s) is not a valid hex offset (00 - FF).")
                else:
                    text_display_string.set("The total length of the hex numbers are not even.")
                return

            used_search_string = character_offset_string
            hexinto = "".join(r"\x{:02x}".format(ord(c) ) for c in used_search_string)
            button_search_string.config(text='{2}{1}\n{0}'.format(repr(used_search_string)[1:-1], hexinto, button_string_title) )
            manual_input_used = False
        else:
            character_offset_string = search_string_user_input.get().encode("utf-8")
            if used_search_string == character_offset_string:
                return
            used_search_string = character_offset_string

            button_search_string.config(text=u'{1}{0}'.format(search_string_user_input.get(), button_string_title))
            manual_input_used = True

    if search_string_to_change == 1:
        replacing_finish_string = used_search_string
        finish_string_used_manual_input = manual_input_used
        OverwriteOptionsData('replacing_finish_string', replacing_finish_string)
        OverwriteOptionsData('finish_string_used_manual_input', finish_string_used_manual_input)
    else:
        replacing_search_string = used_search_string
        search_string_used_manual_input = manual_input_used
        OverwriteOptionsData('replacing_search_string', replacing_search_string)
        OverwriteOptionsData('search_string_used_manual_input', search_string_used_manual_input)

    pass


#Sets an option to its default setting. The option chosen is based on the given number pass as the parameter.
def SetToDefaultSettings(number):
    all_default = 0
    if number == all_default or number == 1: #Automatically Sort Files Default
        automatically_sort_files_check_bool.set(True)
        SetAutomaticFileSort()
    if number == all_default or number == 2: #Byte Unit Default
        SetByteUnit(1)
    if number == all_default or number == 3: #Round To Decimal Position Default
        SetDecimalPosition(None, True)
    if number == all_default or number == 4: #File Scroll Increment Default
        SetScrollingIncrement(None, True)
    if number == all_default or number == 5: #Base Number Default
        SetBaseNumber(1)
    if number == all_default or number == 6: # Automatically Replace .uexp File Default
        number_in_filename_check_bool.set(False)
        UseNumberInFileName()
    if number == all_default or number == 7: #Search String Default
        SetSearchString(None, True, 0)
    if number == all_default or number == 8: #Finish String Default
        SetSearchString(None, True, 1)

    pass

#------------------------------------------------------------ General Options ------------------------------------------------------------#



#------------------------------------------------------------- Color Options -------------------------------------------------------------#

#Opens a window where the user can choose the new color for the chosen Color Option button.
def ColorPicker(id_number):
    starting_color = widget_background_colors_with_text_list[id_number]
    color_picked = tkColorChooser.askcolor(parent=options_window, title='Choose A Color', initialcolor=starting_color) # https://www.youtube.com/watch?v=NDCirUTTrhg  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tkColorChooser.html #for how I found initalcolor - # https://www.programcreek.com/python/example/64776/tkColorChooser.askcolor
    if color_picked[1] != None: #hex_code
        global source_section_color
        global replacement_section_color
        global default_button_color
        global button_highlight_color
        global both_arrow_buttons_same_color_bool
        global both_up_scroll_button_color
        global both_down_scroll_button_color
        global top_n_bottom_section_buttons_same_color_bool
        global to_first_source_file_button_color
        global to_first_replacement_file_button_color
        global to_last_source_file_button_color
        global to_last_replacement_file_button_color
        global extract_button_color
        global compare_button_color
        global compare_O_label_color
        global compare_X_label_color
        global fill_button_color
        global replace_button_color

        
        hex_color = color_picked[1].upper()

        RGB_color = color_picked[0]
        L = Decimal.sqrt(  (RY * Decimal(RGB_color[0] * RGB_color[0]) ) + (GY * Decimal(RGB_color[1] * RGB_color[1]) ) + (BY * Decimal(RGB_color[2] * RGB_color[2]) )  )
        brightness_value = L / denominator
        if round(brightness_value, 2) < 0.5:
            widget_text_color = "#FFFFFF" #white
        else:
            widget_text_color = "#000000" #black


        if id_number == 0: # Source
            if source_section_color == hex_color:
                return
            source_section_color = hex_color
            option_name = "source_section_color"

        elif id_number == 1: # Replace
            if replacement_section_color == hex_color:
                return
            replacement_section_color = hex_color
            option_name = "replacement_section_color"

        elif id_number == 2: # Default
            if default_button_color == hex_color:
                return
            default_button_color = hex_color
            option_name = "default_button_color"

        elif id_number == 3: # Button Highlight
            if button_highlight_color == hex_color:
                return
            button_highlight_color = hex_color
            option_name = "button_highlight_color"

        elif id_number == 4: # Both Up
            if both_scroll_buttons_same_color == True:
                if switch_scroll_buttons_placement == True:
                    both_down_scroll_button_color = hex_color
                else:
                    both_up_scroll_button_color = hex_color
                id_number = "both_scroll"
            else:
                both_up_scroll_button_color = hex_color
            option_name = "both_up_scroll_button_color"

        elif id_number == 5: # Both Down
            if both_scroll_buttons_same_color == True:
                if switch_scroll_buttons_placement == True:
                    both_down_scroll_button_color = hex_color
                else:
                    both_up_scroll_button_color = hex_color
                id_number = "both_scroll"  
            else:
                both_down_scroll_button_color = hex_color
            option_name = "both_down_scroll_button_color"

        elif id_number == 6: # To First Source
            if to_file_buttons_same_color == True:
                if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                    to_last_replacement_file_button_color = hex_color
                elif switch_containers_placement == True:
                    to_first_replacement_file_button_color = hex_color
                elif switch_scroll_buttons_placement == True:
                    to_last_source_file_button_color = hex_color
                else:
                    to_first_source_file_button_color = hex_color
                id_number = "four_scroll"
            else:
                to_first_source_file_button_color = hex_color
            option_name = "to_first_source_file_button_color"

        elif id_number == 7: # To First Replace
            if to_file_buttons_same_color == True:
                if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                    to_last_replacement_file_button_color = hex_color
                elif switch_containers_placement == True:
                    to_first_replacement_file_button_color = hex_color
                elif switch_scroll_buttons_placement == True:
                    to_last_source_file_button_color = hex_color
                else:
                    to_first_source_file_button_color = hex_color
                id_number = "four_scroll"
            else:
                to_first_replacement_file_button_color = hex_color

            option_name = "to_first_replacement_file_button_color"

        elif id_number == 8: # To Last Source
            if to_file_buttons_same_color == True:
                if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                    to_last_replacement_file_button_color = hex_color
                elif switch_containers_placement == True:
                    to_first_replacement_file_button_color = hex_color
                elif switch_scroll_buttons_placement == True:
                    to_last_source_file_button_color = hex_color
                else:
                    to_first_source_file_button_color = hex_color
                id_number = "four_scroll"
            else:
                to_last_source_file_button_color = hex_color
            option_name = "to_last_source_file_button_color"

        elif id_number == 9: # To Last Replace
            if to_file_buttons_same_color == True:
                if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                    to_last_replacement_file_button_color = hex_color
                elif switch_containers_placement == True:
                    to_first_replacement_file_button_color = hex_color
                elif switch_scroll_buttons_placement == True:
                    to_last_source_file_button_color = hex_color
                else:
                    to_first_source_file_button_color = hex_color
                id_number = "four_scroll"
            else:
                to_last_replacement_file_button_color = hex_color
            option_name = "to_last_replacement_file_button_color"

        elif id_number == 10: # Extract Button
            if extract_button_color == hex_color:
                return
            extract_button_color = hex_color
            option_name = "extract_button_color"

        elif id_number == 11: # Compare Button
            if compare_button_color == hex_color:
                return
            compare_button_color = hex_color
            option_name = "compare_button_color"

        elif id_number == 12: # Comapre Fillable
            if compare_O_label_color == hex_color:
                return
            compare_O_label_color = hex_color
            option_name = "compare_O_label_color"

        elif id_number == 13: # Comapre Nonfillable
            if compare_X_label_color == hex_color:
                return
            compare_X_label_color = hex_color
            option_name = "compare_X_label_color"

        elif id_number == 14: # Fill Button
            if fill_button_color == hex_color:
                return
            fill_button_color = hex_color
            option_name = "fill_button_color"

        elif id_number == 15: # Replace Button
            if replace_button_color == hex_color:
                return
            replace_button_color = hex_color
            option_name = "replace_button_color"


        UpdateWidgetColor(id_number, widget_text_color)
        OverwriteOptionsData(option_name, hex_color, tab=1)
    else:
        text_display_string.set("No Color Chosen.")

    pass

#Updates a widget's color whoses section has changed. Only widgets that are enabled and can be presently seen are effected.
def UpdateWidgetColor(color_picker_id, color_picker_text_color="Default"): #color_picker_text_color parameter is for default color option buttons
    #I only have to update the buttons in the options window and the root window as these two windows can be seen.

    set_default_white_text = False
    if color_picker_text_color == "Default":
        color_picker_text_color = "#000000"
        set_default_white_text = True

    change_all = "all"
    if color_picker_id == 0 or color_picker_id == change_all: # Update Source Section Color
        global source_section_text_color 
        if color_picker_text_color != None:
            source_section_text_color  = color_picker_text_color

        source_color_options_button.config(bg=source_section_color, fg=source_section_text_color )
        source_container.config(bg=source_section_color, fg=source_section_text_color )

        if source_scroll_up_button.cget('state') == 'normal':
            source_scroll_up_button.config(bg=source_section_color, fg=source_section_text_color )
        if source_scroll_down_button.cget('state') == 'normal':
            source_scroll_down_button.config(bg=source_section_color, fg=source_section_text_color )
        
        if comparing_labels_on == False:
            for label in label_source_list:
                label.config(bg=source_section_color, fg=source_section_text_color )
        pass
    if color_picker_id == 1 or color_picker_id == change_all: # Update Replacement Section Color
        global replacement_section_text_color
        if color_picker_text_color != None:
            replacement_section_text_color = color_picker_text_color

        replace_color_options_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
        replacement_container.config(bg=replacement_section_color, fg=replacement_section_text_color)
        
        if replacement_scroll_up_button.cget('state') == 'normal':
            replacement_scroll_up_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
        if replacement_scroll_down_button.cget('state') == 'normal':
            replacement_scroll_down_button.config(bg=replacement_section_color, fg=replacement_section_text_color)
        
        if comparing_labels_on == False:
            for label in label_replacement_list:
                label.config(bg=replacement_section_color, fg=replacement_section_text_color)
        pass
    if color_picker_id == 2 or color_picker_id == change_all: #Update Default Button Color
        global default_button_text_color
        if color_picker_text_color != None:
            default_button_text_color = color_picker_text_color

        default_button_color_options_button.config(bg=default_button_color, fg=default_button_text_color)
        add_button.config(bg=default_button_color, fg=default_button_text_color)
        if remove_button.cget("state") == "normal":
            remove_button.config(bg=default_button_color, fg=default_button_text_color)
        if sort_button.cget("state") == "normal":
            sort_button.config(bg=default_button_color, fg=default_button_text_color)
        pass
    if color_picker_id == 3 or color_picker_id == change_all: # Update Button Highlight Color
        global button_highlight_text_color
        if color_picker_text_color != None:
            if set_default_white_text == True:
                button_highlight_text_color = "white"
            else:
                button_highlight_text_color = color_picker_text_color
    
        middle_frame_color_options_button.config(bg=button_highlight_color, fg=button_highlight_text_color)
        middle_frame.config(bg=button_highlight_color)

    if (color_picker_id == 4) or (color_picker_id == 5) or (color_picker_id == change_all) or (color_picker_id == "both_scroll"): # Update "Both" Scroll Buttons Color
        global both_up_scroll_button_text_color
        global both_down_scroll_button_text_color

        if (color_picker_id == "both_scroll") or (color_picker_id == change_all and color_picker_text_color != None):
            if switch_scroll_buttons_placement == True:
                both_button_lead_color = both_down_scroll_button_color
                if color_picker_text_color != None:
                    both_down_scroll_button_text_color = color_picker_text_color
            else:
                both_button_lead_color = both_up_scroll_button_color
                if color_picker_text_color != None:
                    both_up_scroll_button_text_color = color_picker_text_color
            both_button_lead_text_color = color_picker_text_color

            both_arrow_buttons_same_color_checkbox.config(bg=both_button_lead_color, fg=both_button_lead_text_color, selectcolor=CalculateTextColor(both_button_lead_text_color))

            both_up_color_options_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)

            if both_sections_up_arrow_button.cget("state") == "normal":
                both_sections_up_arrow_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)

            both_down_color_options_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)

            if both_sections_down_arrow_button.cget("state") == "normal":
                both_sections_down_arrow_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)
            
        elif (color_picker_id == change_all and color_picker_text_color == None):
            if switch_scroll_buttons_placement == True:
                both_arrow_buttons_same_color_checkbox.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color, selectcolor=CalculateTextColor(both_down_scroll_button_text_color))
            else:
                both_arrow_buttons_same_color_checkbox.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color, selectcolor=CalculateTextColor(both_up_scroll_button_text_color))

            both_up_color_options_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)
            both_down_color_options_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)

            if both_sections_up_arrow_button.cget("state") == "normal":
                both_sections_up_arrow_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)

            if both_sections_down_arrow_button.cget("state") == "normal":
                both_sections_down_arrow_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)

            pass

        elif color_picker_id == 4: # Update Both Up Color
            if color_picker_text_color != None:
                both_up_scroll_button_text_color = color_picker_text_color

            if switch_scroll_buttons_placement == False:
                both_arrow_buttons_same_color_checkbox.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color, selectcolor=CalculateTextColor(both_up_scroll_button_text_color))

            both_up_color_options_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)

            if both_sections_up_arrow_button.cget("state") == "normal":
                both_sections_up_arrow_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)
            
            
        elif color_picker_id == 5: # Update Both Down Color
            if color_picker_text_color != None:
                both_down_scroll_button_text_color = color_picker_text_color

            if switch_scroll_buttons_placement == True:
                both_arrow_buttons_same_color_checkbox.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color, selectcolor=CalculateTextColor(both_down_scroll_button_text_color))

            both_down_color_options_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)

            if both_sections_down_arrow_button.cget("state") == "normal":
                both_sections_down_arrow_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)         
        pass   
    if (color_picker_id == 6) or (color_picker_id == 7) or (color_picker_id == 8) or (color_picker_id == 9) or (color_picker_id == change_all) or (color_picker_id == "four_scroll"): # Update "To File" Scroll Buttons Color
        global to_first_source_file_button_text_color
        global to_first_replacement_file_button_text_color
        global to_last_source_file_button_text_color
        global to_last_replacement_file_button_text_color
        
        if (color_picker_id == "four_scroll") or (color_picker_id == change_all and color_picker_text_color != None):
            if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                to_file_lead_color = to_last_replacement_file_button_color
                if color_picker_text_color != None:
                    to_last_replacement_file_button_text_color = color_picker_text_color
            elif switch_containers_placement == True:
                to_file_lead_color = to_first_replacement_file_button_color
                if color_picker_text_color != None:
                    to_first_replacement_file_button_text_color = color_picker_text_color
            elif switch_scroll_buttons_placement == True:
                to_file_lead_color = to_last_source_file_button_color
                if color_picker_text_color != None:
                    to_last_source_file_button_text_color = color_picker_text_color
            else:
                to_file_lead_color = to_first_source_file_button_color
                if color_picker_text_color != None:
                    to_first_source_file_button_text_color = color_picker_text_color

            to_file_lead_text_color = color_picker_text_color

            top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_file_lead_color, fg=to_file_lead_text_color, selectcolor=CalculateTextColor(to_file_lead_text_color))

            top_source_color_options_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            if to_first_source_file_button.cget("state") == "normal":
                to_first_source_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            top_replace_color_options_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            if to_first_replacement_file_button.cget("state") == "normal":
                to_first_replacement_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            bottom_source_color_options_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            if to_last_source_file_button.cget("state") == "normal":
                to_last_source_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            bottom_replace_color_options_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            if to_last_replacement_file_button.cget("state") == "normal":
                to_last_replacement_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)

            pass


        elif (color_picker_id == change_all and color_picker_text_color == None): #When you use preset colors?
            if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_last_replacement_file_button_text_color))
            elif switch_containers_placement == True:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_first_replacement_file_button_text_color))
            elif switch_scroll_buttons_placement == True:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color, selectcolor=CalculateTextColor(to_last_source_file_button_text_color))
            else:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color, selectcolor=CalculateTextColor(to_first_source_file_button_text_color))

            top_source_color_options_button.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color)
            top_replace_color_options_button.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color)
            bottom_source_color_options_button.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color)
            bottom_replace_color_options_button.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color)

            if to_first_source_file_button.cget("state") == "normal":
                to_first_source_file_button.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color)
            
            if to_first_replacement_file_button.cget("state") == "normal":
                to_first_replacement_file_button.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color)
            
            if to_last_source_file_button.cget("state") == "normal":
                to_last_source_file_button.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color)
            
            if to_last_replacement_file_button.cget("state") == "normal":
                to_last_replacement_file_button.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color)

            pass


        elif color_picker_id == 6: # Update To First Source Color
            if color_picker_text_color != None:
                to_first_source_file_button_text_color = color_picker_text_color

            if switch_containers_placement == False and switch_scroll_buttons_placement == False:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color, selectcolor=CalculateTextColor(to_first_source_file_button_text_color))

            top_source_color_options_button.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color)
            if to_first_source_file_button.cget("state") == "normal":
                to_first_source_file_button.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color)
            pass

            
        elif color_picker_id == 7: # Update To First Replace Color
            if color_picker_text_color != None:
                to_first_replacement_file_button_text_color = color_picker_text_color

            if switch_containers_placement == True and switch_scroll_buttons_placement == False:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_first_replacement_file_button_text_color))

            top_replace_color_options_button.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color)
            if to_first_replacement_file_button.cget("state") == "normal":
                to_first_replacement_file_button.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color)
            pass

    
        elif color_picker_id == 8: # Update To Last Source Color
            if color_picker_text_color != None:
                to_last_source_file_button_text_color = color_picker_text_color

            if switch_containers_placement == False and switch_scroll_buttons_placement == True:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color, selectcolor=CalculateTextColor(to_last_source_file_button_text_color))
            #top_n_bottom_section_buttons_same_color_checkbox.config(text='All arrows use the same color:\nF(S): {0} | F(R): {1} | L(S): {2} | L(R): {3}'.format(to_first_source_file_button_color, to_first_replacement_file_button_color, 
            #                                                                                                                                                    to_last_source_file_button_color, to_last_replacement_file_button_color))
            bottom_source_color_options_button.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color)
            if to_last_source_file_button.cget("state") == "normal":
                to_last_source_file_button.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color)
            pass

    
        elif color_picker_id == 9: # Update To Last Replace Color
            if color_picker_text_color != None:
                to_last_replacement_file_button_text_color = color_picker_text_color

            if switch_containers_placement == True and switch_scroll_buttons_placement == True:
                top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_last_replacement_file_button_text_color))

            bottom_replace_color_options_button.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color)
            if to_last_replacement_file_button.cget("state") == "normal":
                to_last_replacement_file_button.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color)
            pass

        pass

    if color_picker_id == 10 or color_picker_id == change_all: # Update Compare Button Color
        global extract_button_text_color
        if color_picker_text_color != None:
            extract_button_text_color = color_picker_text_color

        extract_button_color_options_button.config(bg=extract_button_color, fg=extract_button_text_color)
        extract_button.config(bg=extract_button_color, fg=extract_button_text_color)
    if color_picker_id == 11 or color_picker_id == change_all: # Update Compare Button Color
        global compare_button_text_color
        if color_picker_text_color != None:
            compare_button_text_color = color_picker_text_color

        compare_button_color_options_button.config(bg=compare_button_color, fg=compare_button_text_color)
        if compare_button.cget("state") == "normal":
            compare_button.config(bg=compare_button_color, fg=compare_button_text_color)
        pass
    if color_picker_id == 12 or color_picker_id == change_all: # Update Compare Fillable Color
        global compare_O_label_text_color
        if color_picker_text_color != None:
            compare_O_label_text_color = color_picker_text_color

        compare_O_label_color_options_button.config(bg=compare_O_label_color, fg=compare_O_label_text_color)
        if (comparing_labels_on == True) and (color_picker_id != change_all): #So Comparing Files does not get called twice if "all" is the input parameter
            ComparingFiles()
        pass
    if color_picker_id == 13 or color_picker_id == change_all: # Update Compare Nonfillable Color
        global compare_X_label_text_color
        if color_picker_text_color != None:
            if set_default_white_text == True:
                compare_X_label_text_color = "white"
            else:
                compare_X_label_text_color = color_picker_text_color
        
        compare_X_label_color_options_button.config(bg=compare_X_label_color, fg=compare_X_label_text_color)
        if comparing_labels_on == True:
            ComparingFiles()
        pass
    if color_picker_id == 14 or color_picker_id == change_all: # Update Fill Button Color
        global fill_button_text_color
        if color_picker_text_color != None:
            fill_button_text_color = color_picker_text_color

        fill_button_color_options_button.config(bg=fill_button_color, fg=fill_button_text_color)
        if fill_button.cget("state") == "normal":
            fill_button.config(bg=fill_button_color, fg=fill_button_text_color)
        pass
    if color_picker_id == 15 or color_picker_id == change_all: # Update Replace Button Color
        global replace_button_text_color
        if color_picker_text_color != None:
            replace_button_text_color = color_picker_text_color

        replace_button_color_options_button.config(bg=replace_button_color, fg=replace_button_text_color)
        replace_button.config(bg=replace_button_color, fg=replace_button_text_color)


    global widget_background_colors_with_text_list #This is for the color picker to have the correct initialcolor variable
    widget_background_colors_with_text_list = [source_section_color, replacement_section_color,
                                           default_button_color,
                                           button_highlight_color,
                                           both_up_scroll_button_color, both_down_scroll_button_color,
                                           to_first_source_file_button_color, to_first_replacement_file_button_color, to_last_source_file_button_color, to_last_replacement_file_button_color,
                                           extract_button_color,
                                           compare_button_color, compare_O_label_color, compare_X_label_color,
                                           fill_button_color, replace_button_color]
    SetColorOptionsButtonNames(set_default_color_button=False) #This changes the text of the color option.


#Sets the name and color code (HEX/RBG) of the Color Option buttons.
def SetColorOptionsButtonNames(set_default_color_button=True):
    current_color_width = Decimal(options_window.winfo_width()) / options_window_base_width
    current_color_height = Decimal(options_window.winfo_height()) / options_window_base_height
    if current_color_width > current_color_height:
        used_side = current_color_height
    else:
        used_side = current_color_width
    options_window_color_tab_7_font = ("Helvetica", int(round(7 * used_side)) )
    options_window_color_tab_8_font = ("Helvetica", int(round(8 * used_side)) )
    options_window_color_tab_9_font = ("Helvetica", int(round(9 * used_side)) )


    color_options_widget_index = 0
    for color_options_widget in color_options_button_list:
        if isinstance(color_options_widget, Button):
            color_option_name = color_options_button_names_list[color_options_widget_index]
            if (color_options_widget == top_source_color_options_button) or (color_options_widget == top_replace_color_options_button) or (color_options_widget == bottom_source_color_options_button) or (color_options_widget == bottom_replace_color_options_button):
                if (color_options_widget == top_source_color_options_button) or (color_options_widget == bottom_source_color_options_button):
                    new_string = color_option_name.replace(" (S)", "\n(S)")
                else:
                    new_string = color_option_name.replace(" File", "\nFile")
                color_option_change_text = "Change {} Color".format(new_string)
            else:
                color_option_change_text = "Change {} Color".format(color_option_name)

            hex_color_code = color_options_widget.cget("bg")
            if use_rgb_color_code == True:
                red_value =   int(hex_color_code[1:3], 16)
                green_value = int(hex_color_code[3:5], 16)
                blue_value =  int(hex_color_code[5:7], 16)
                rgb_color_code = "({0},{1},{2})".format(red_value, green_value, blue_value)
                color_code = rgb_color_code
            else:
                color_code = hex_color_code

            widget_text = ""
            if (color_options_widget == both_up_color_options_button) or (color_options_widget == both_down_color_options_button) or (color_options_widget == top_source_color_options_button) or (color_options_widget == top_replace_color_options_button) or (color_options_widget == bottom_source_color_options_button) or (color_options_widget == bottom_replace_color_options_button):
                widget_text = color_option_change_text
                pass
            elif (color_options_widget == compare_O_label_color_options_button) or (color_options_widget == compare_X_label_color_options_button):
                name_and_color_code_tuple = (color_option_change_text, color_code)
                widget_text = ":\n".join(name_and_color_code_tuple)
                pass
            else:
                name_and_color_code_tuple = (color_option_change_text, color_code)
                widget_text = ": ".join(name_and_color_code_tuple)
                pass

            color_options_widget.config(text=widget_text)
            if (color_options_widget == source_color_options_button) or (color_options_widget == replace_color_options_button):
                if use_rgb_color_code == True:
                    color_options_widget.config(font=options_window_color_tab_8_font)
                else:
                    color_options_widget.config(font=options_window_color_tab_9_font)
            color_options_widget_index += 1

        elif isinstance(color_options_widget, Checkbutton):
            if color_options_widget == both_arrow_buttons_same_color_checkbox:
                SetTextOfBothArrowColorCheckbutton()
            elif color_options_widget == top_n_bottom_section_buttons_same_color_checkbox:
                SetTextOfToFileColorCheckbutton()
                if to_file_buttons_same_color == True:
                    top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_8_font)
                else:
                    if use_rgb_color_code == True:
                        top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_7_font)
                    else:
                        top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_8_font)
            pass

        pass

    if set_default_color_button == False:
        return

    color_default_options_widget_index = 0
    for color_default_options_widget in color_options_default_button_list:
        color_default_option_name = color_options_default_button_names_list[color_default_options_widget_index]

        hex_color_code = color_default_options_widget.cget("bg")
        if use_rgb_color_code == True:
            red_value =   int(hex_color_code[1:3], 16)
            green_value = int(hex_color_code[3:5], 16)
            blue_value =  int(hex_color_code[5:7], 16)
            rgb_color_code = "({0},{1},{2})".format(red_value, green_value, blue_value)
            color_code = rgb_color_code
        else:
            color_code = hex_color_code

        name_and_color_code_tuple = (color_default_option_name, color_code)
        widget_text = "\n".join(name_and_color_code_tuple)

        color_default_options_widget.config(text=widget_text)
        color_default_options_widget_index += 1

    pass


#Rec.709 luma coefficients  # https://en.wikipedia.org/wiki/Luma_(video)
RY = Decimal(0.2126)
GY = Decimal(0.7152)
BY = Decimal(0.0722)
denominator = Decimal(255) * Decimal.sqrt( RY + GY + BY )
#Calculates the brightness of a given color. Can accept one color and return the variable OR accept a list and return a list.
def CalculateTextColor(background_color, using_list_of_colors=False, list_of_background_colors=None):
    #Method 7 - https://medium.com/random-noise/methods-for-measuring-color-lightness-in-python-84df593d0786  #Based on this -  http://alienryderflex.com/hsp.html

    #Calculates the brightness of the given color and returns what the text color should be.
    def CalculateBackgroundColorLightness(color): # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python#:~:text=The%20following%20function%20will%20convert%20hex%20string%20to%20rgb%20values%3A
        R = int(color[1:3], 16)
        G = int(color[3:5], 16)
        B = int(color[5:7], 16)
        
        L = Decimal.sqrt(  (RY * Decimal(R * R) ) + (GY * Decimal(G * G) ) + (BY * Decimal(B * B) )  ) #Use luma value to determine brightness  # https://medium.com/random-noise/methods-for-measuring-color-lightness-in-python-84df593d0786#:~:text=L%20%3D%20(0.212%20*%20R%20%2B%200.701%20*%20G%20%2B%200.087%20*%20B)%20/%20255
        brightness_value = L / denominator
        
        if round(brightness_value, 2) < 0.5:
            widget_text_color = "#FFFFFF" #white
        else:
            widget_text_color = "#000000" #black
        return widget_text_color


    if using_list_of_colors:
        widget_foreground_text_colors_list = []
        for color_in_list in list_of_background_colors:
            widget_foreground_text_colors_list.append(CalculateBackgroundColorLightness(color_in_list))
        return widget_foreground_text_colors_list

    return CalculateBackgroundColorLightness(background_color)


#Sets the Foreground colors for their corresponing Background color.
def SetWidgetsTextColors():
    global source_section_text_color 
    global replacement_section_text_color
    global default_button_text_color
    global button_highlight_text_color

    global both_up_scroll_button_text_color
    global both_down_scroll_button_text_color
    global to_first_source_file_button_text_color 
    global to_first_replacement_file_button_text_color
    global to_last_source_file_button_text_color
    global to_last_replacement_file_button_text_color
    
    global extract_button_text_color
    global compare_button_text_color
    global compare_O_label_text_color
    global compare_X_label_text_color
    global fill_button_text_color
    global replace_button_text_color


    widget_foreground_text_colors_list = CalculateTextColor(None, True, widget_background_colors_with_text_list)

    if len(widget_background_colors_with_text_list) != len(widget_foreground_text_colors_list):
        text_display_string.set('Hold it! - The length of "widget_background_colors_with_text_list" is not equal to the length of "widget_foreground_text_colors_list"!')
        return

    source_section_text_color  = widget_foreground_text_colors_list[0]
    replacement_section_text_color = widget_foreground_text_colors_list[1]
    default_button_text_color = widget_foreground_text_colors_list[2]
    button_highlight_text_color = widget_foreground_text_colors_list[3]
    both_up_scroll_button_text_color = widget_foreground_text_colors_list[4]
    both_down_scroll_button_text_color = widget_foreground_text_colors_list[5]
    to_first_source_file_button_text_color = widget_foreground_text_colors_list[6]
    to_first_replacement_file_button_text_color = widget_foreground_text_colors_list[7]
    to_last_source_file_button_text_color = widget_foreground_text_colors_list[8]
    to_last_replacement_file_button_text_color = widget_foreground_text_colors_list[9]
    extract_button_text_color = widget_foreground_text_colors_list[10]
    compare_button_text_color = widget_foreground_text_colors_list[11]
    compare_O_label_text_color = widget_foreground_text_colors_list[12]
    compare_X_label_text_color = widget_foreground_text_colors_list[13]
    fill_button_text_color = widget_foreground_text_colors_list[14]
    replace_button_text_color = widget_foreground_text_colors_list[15]

SetWidgetsTextColors()


#Sets the name and color code of the "Both" Scroll buttons.
def SetTextOfBothArrowColorCheckbutton():
    both_arrow_buttons_color_list = [both_up_scroll_button_color, both_down_scroll_button_color]
    if use_rgb_color_code == True:
        both_buttons_color_code = []
        for both_buttons_hex_color_code in both_arrow_buttons_color_list:
            red_value =   int(both_buttons_hex_color_code[1:3], 16)
            green_value = int(both_buttons_hex_color_code[3:5], 16)
            blue_value =  int(both_buttons_hex_color_code[5:7], 16)
            rgb_color_code = "({0},{1},{2})".format(red_value, green_value, blue_value)
            both_buttons_color_code.append(rgb_color_code)
    else:
        both_buttons_color_code = both_arrow_buttons_color_list

    both_buttons_checkbox_title_text = '"Both" Buttons use the same color'
    if both_scroll_buttons_same_color == True:
        if switch_scroll_buttons_placement == True:
            both_butoon_lead_color_used = 1
        else:
            both_butoon_lead_color_used = 0
        both_arrow_buttons_same_color_checkbox.config(text='{1}:\n{0}'.format(both_buttons_color_code[both_butoon_lead_color_used], both_buttons_checkbox_title_text) )
    else:
        if switch_scroll_buttons_placement == True:
            both_arrow_buttons_same_color_checkbox.config(text='{2}:\nDown: {1} | Up: {0}'.format(both_buttons_color_code[0], both_buttons_color_code[1], both_buttons_checkbox_title_text) )
        else:
            both_arrow_buttons_same_color_checkbox.config(text='{2}:\nUp: {0} | Down: {1}'.format(both_buttons_color_code[0], both_buttons_color_code[1], both_buttons_checkbox_title_text) )
        pass

    pass
#Sets the color of the "Both" Scroll buttons based on the layout of the buttons and if the Two buttons use the same color.
def SetColorOfBothArrowColorCheckbutton():
    if switch_scroll_buttons_placement == True:
        both_arrow_lead_color = both_down_scroll_button_color
        both_arrow_lead_text_color = both_down_scroll_button_text_color
    else:
        both_arrow_lead_color = both_up_scroll_button_color
        both_arrow_lead_text_color = both_up_scroll_button_text_color
        
    both_arrow_buttons_same_color_checkbox.config(bg=both_arrow_lead_color, fg=both_arrow_lead_text_color, selectcolor=CalculateTextColor(both_arrow_lead_text_color))

    if both_scroll_buttons_same_color == True:
        both_up_color_options_button.config(bg=both_arrow_lead_color, fg=both_arrow_lead_text_color)
        both_down_color_options_button.config(bg=both_arrow_lead_color, fg=both_arrow_lead_text_color)

        if both_sections_up_arrow_button.cget("state") == "normal":
            both_sections_up_arrow_button.config(bg=both_arrow_lead_color, fg=both_arrow_lead_text_color)
        if both_sections_down_arrow_button.cget("state") == "normal":
            both_sections_down_arrow_button.config(bg=both_arrow_lead_color, fg=both_arrow_lead_text_color)
    else:
        both_up_color_options_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)
        both_down_color_options_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)

        if both_sections_up_arrow_button.cget("state") == "normal":
            both_sections_up_arrow_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)
        if both_sections_down_arrow_button.cget("state") == "normal":
            both_sections_down_arrow_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)
        pass

    pass

#Changes the "Both" Scroll buttons to use the same color or not based on if the options is checked or unchecked.
def BothArrowButtonsAreTheSameColor():
    global both_scroll_buttons_same_color
    if both_scroll_buttons_same_color == both_arrow_buttons_same_color_bool.get():
        return
    both_scroll_buttons_same_color = both_arrow_buttons_same_color_bool.get()

    SetTextOfBothArrowColorCheckbutton()
    SetColorOfBothArrowColorCheckbutton()

    OverwriteOptionsData("both_scroll_buttons_same_color", str(both_scroll_buttons_same_color), tab=1 )


#Sets the name and color code of the "To File" Scroll buttons.
def SetTextOfToFileColorCheckbutton():
    to_file_buttons_color_list = [to_first_source_file_button_color, to_first_replacement_file_button_color, to_last_source_file_button_color, to_last_replacement_file_button_color]
    if use_rgb_color_code == True:
        to_file_color_code = []
        for to_file_hex_color_code in to_file_buttons_color_list:
            red_value =   int(to_file_hex_color_code[1:3], 16)
            green_value = int(to_file_hex_color_code[3:5], 16)
            blue_value =  int(to_file_hex_color_code[5:7], 16)
            rgb_color_code = "({0},{1},{2})".format(red_value, green_value, blue_value)
            to_file_color_code.append(rgb_color_code)
    else:
        to_file_color_code = to_file_buttons_color_list

    to_file_checkbox_title_text = 'All "To File" buttons use the same color'
    if to_file_buttons_same_color == True:
        if switch_containers_placement == True and switch_scroll_buttons_placement == True:
            color_var_pick = 3
        elif switch_containers_placement == True:
            color_var_pick = 1
        elif switch_scroll_buttons_placement == True:
            color_var_pick = 2
        else:
            color_var_pick = 0

        top_n_bottom_section_buttons_same_color_checkbox.config(text='{1}:\n{0}'.format(to_file_color_code[color_var_pick], to_file_checkbox_title_text) )
    else:
        if switch_containers_placement == True and switch_scroll_buttons_placement == True:
            top_n_bottom_section_buttons_same_color_checkbox.config(text='{4}:\nL(R): {3} - L(S): {2} - F(R): {1} - F(S): {0}'.format(to_file_color_code[0], to_file_color_code[1], to_file_color_code[2], to_file_color_code[3], to_file_checkbox_title_text) )
        elif switch_containers_placement == True:
            top_n_bottom_section_buttons_same_color_checkbox.config(text='{4}:\nF(R): {1} - F(S): {0} - L(R): {3} - L(S): {2}'.format(to_file_color_code[0], to_file_color_code[1], to_file_color_code[2], to_file_color_code[3], to_file_checkbox_title_text) )
        elif switch_scroll_buttons_placement == True:
            top_n_bottom_section_buttons_same_color_checkbox.config(text='{4}:\nL(S): {2} - L(R): {3} - F(S): {0} - F(R): {1}'.format(to_file_color_code[0], to_file_color_code[1], to_file_color_code[2], to_file_color_code[3], to_file_checkbox_title_text) )
        else:
            top_n_bottom_section_buttons_same_color_checkbox.config(text='{4}:\nF(S): {0} - F(R): {1} - L(S): {2} - L(R): {3}'.format(to_file_color_code[0], to_file_color_code[1], to_file_color_code[2], to_file_color_code[3], to_file_checkbox_title_text) )
        pass

    pass
#Sets the color of the "To File" Scroll buttons based on the layout of the buttons and if the Four buttons use the same color.
def SetColorOfToFileColorCheckbutton():
    if switch_containers_placement == True and switch_scroll_buttons_placement == True:
        top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_last_replacement_file_button_text_color))
    elif switch_containers_placement == True:
        top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color, selectcolor=CalculateTextColor(to_first_replacement_file_button_text_color))
    elif switch_scroll_buttons_placement == True:
        top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color, selectcolor=CalculateTextColor(to_last_source_file_button_text_color))
    else:
        top_n_bottom_section_buttons_same_color_checkbox.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color, selectcolor=CalculateTextColor(to_first_source_file_button_text_color))


    if to_file_buttons_same_color == True:
        if switch_containers_placement == True and switch_scroll_buttons_placement == True:
            to_file_buttons_lead_color = to_last_replacement_file_button_color
            to_file_buttons_lead_text_color = to_last_replacement_file_button_text_color
        elif switch_containers_placement == True:
            to_file_buttons_lead_color = to_first_replacement_file_button_color
            to_file_buttons_lead_text_color = to_first_replacement_file_button_text_color
        elif switch_scroll_buttons_placement == True:
            to_file_buttons_lead_color = to_last_source_file_button_color
            to_file_buttons_lead_text_color = to_last_source_file_button_text_color
        else:
            to_file_buttons_lead_color = to_first_source_file_button_color
            to_file_buttons_lead_text_color = to_first_source_file_button_text_color

        to_file_var_color1 = to_file_buttons_lead_color
        to_file_var_color2 = to_file_buttons_lead_color
        to_file_var_color3 = to_file_buttons_lead_color
        to_file_var_color4 = to_file_buttons_lead_color

        to_file_var_text_color1 = to_file_buttons_lead_text_color
        to_file_var_text_color2 = to_file_buttons_lead_text_color
        to_file_var_text_color3 = to_file_buttons_lead_text_color
        to_file_var_text_color4 = to_file_buttons_lead_text_color

    else:
        to_file_var_color1 = to_first_source_file_button_color
        to_file_var_color2 = to_first_replacement_file_button_color
        to_file_var_color3 = to_last_source_file_button_color
        to_file_var_color4 = to_last_replacement_file_button_color
        
        to_file_var_text_color1 = to_first_source_file_button_text_color
        to_file_var_text_color2 = to_first_replacement_file_button_text_color
        to_file_var_text_color3 = to_last_source_file_button_text_color
        to_file_var_text_color4 = to_last_replacement_file_button_text_color


    top_source_color_options_button.config(bg=to_file_var_color1, fg=to_file_var_text_color1)
    top_replace_color_options_button.config(bg=to_file_var_color2, fg=to_file_var_text_color2)
    bottom_source_color_options_button.config(bg=to_file_var_color3, fg=to_file_var_text_color3)
    bottom_replace_color_options_button.config(bg=to_file_var_color4, fg=to_file_var_text_color4)
    
    if to_first_source_file_button.cget("state") == "normal":
        to_first_source_file_button.config(bg=to_file_var_color1, fg=to_file_var_text_color1)
    
    if to_first_replacement_file_button.cget("state") == "normal":
        to_first_replacement_file_button.config(bg=to_file_var_color2, fg=to_file_var_text_color2)
    
    if to_last_source_file_button.cget("state") == "normal":
        to_last_source_file_button.config(bg=to_file_var_color3, fg=to_file_var_text_color3)
    
    if to_last_replacement_file_button.cget("state") == "normal":
        to_last_replacement_file_button.config(bg=to_file_var_color4, fg=to_file_var_text_color4)

    
    pass

#Changes the "To File" Scroll buttons to use the same color or not based on if the options is checked or unchecked.
def AllToIndexButtonsAreTheSameColor():
    global to_file_buttons_same_color
    if to_file_buttons_same_color == top_n_bottom_section_buttons_same_color_bool.get():
        return
    to_file_buttons_same_color = top_n_bottom_section_buttons_same_color_bool.get()


    current_color_width = Decimal(options_window.winfo_width()) / options_window_base_width
    current_color_height = Decimal(options_window.winfo_height()) / options_window_base_height
    if current_color_width > current_color_height:
        used_side = current_color_height
    else:
        used_side = current_color_width
    options_window_color_tab_to_file_checkbutton_7_font = ("Helvetica", int(round(7 * used_side)) )
    options_window_color_tab_to_file_checkbutton_8_font = ("Helvetica", int(round(8 * used_side)) )

    if to_file_buttons_same_color == True:
        top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_to_file_checkbutton_8_font)
    else:
        if use_rgb_color_code == True:
            top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_to_file_checkbutton_7_font)
        else:
            top_n_bottom_section_buttons_same_color_checkbox.config(font=options_window_color_tab_to_file_checkbutton_8_font)
        pass
    SetTextOfToFileColorCheckbutton()
    SetColorOfToFileColorCheckbutton()

    OverwriteOptionsData("to_file_buttons_same_color", str(to_file_buttons_same_color), tab=1 )


#Creates a window where the user chooses which action they want to choose for using preset colors
def ConfirmPresetUsage(button_number):
    preset_section = ""
    preset_prefix = ""
    if button_number == 1:
        preset_section = config_file_color_preset1_section
        preset_prefix = "preset1_"
    elif button_number == 2:
        preset_section = config_file_color_preset2_section
        preset_prefix = "preset2_"
    elif button_number == 3:
        preset_section = config_file_color_preset3_section
        preset_prefix = "preset3_"
    else:
        text_display_string.set('Error! "preset_index" not equal to corresponding button number! - ConfirmPresetUsage(button_number)')
        return
    
    if config_parser.get(preset_section, "{0}source_section_color".format(preset_prefix)) == "":
        text_display_string.set("No saved color changes found for {0}".format(preset_section))
        SavePresetColors(button_number)
        return

    preset_box = Toplevel()
    preset_box.resizable(width=False, height=False)
    preset_box_base_width = Decimal(315)
    preset_box_base_height = Decimal(75)
    WindowCenterPositioner(preset_box, preset_box_base_width, preset_box_base_height, options_window)
    preset_box_12_font = InitialWindowFontSize(12, preset_box.winfo_width(), preset_box.winfo_height(), preset_box_base_width, preset_box_base_height)
    preset_box.wm_title('Select An Option - Preset {}'.format(button_number))

    preset_buttons_relwidth = Decimal(1) / Decimal(3)
    preset_use_button = Button(preset_box, text='USE', font=preset_box_12_font, command=lambda:[preset_box.destroy(), UsePresetColors(preset_index=button_number)])
    preset_use_button.place(relwidth=preset_buttons_relwidth, relheight=1)

    preset_save_button = Button(preset_box, text='OVERWRITE', font=preset_box_12_font, command=lambda:[preset_box.destroy(), SavePresetColors(preset_index=button_number)])
    preset_save_button.place(relwidth=preset_buttons_relwidth, relheight=1, relx=preset_buttons_relwidth + preset_buttons_relwidth)

    preset_box_cancel = Button(preset_box, text='CANCEL', font=preset_box_12_font, command=preset_box.destroy, bg='gray')
    preset_box_cancel.place(relwidth=preset_buttons_relwidth, relheight=1, relx=preset_buttons_relwidth)


#Finds the preset colors in the config.ini file and calls SetWidgetsTextColors() to find the corresponding text color for each preset color. Then it calls UpdateWidgetColor() to update the colors accordingly and saves the preset colors as the used colors.
def UsePresetColors(preset_index):
    global source_section_color
    global replacement_section_color
    global default_button_color
    global button_highlight_color
    global both_scroll_buttons_same_color
    global both_up_scroll_button_color
    global both_down_scroll_button_color
    global to_file_buttons_same_color
    global to_first_source_file_button_color
    global to_first_replacement_file_button_color
    global to_last_source_file_button_color
    global to_last_replacement_file_button_color
    global extract_button_color
    global compare_button_color
    global compare_O_label_color
    global compare_X_label_color
    global fill_button_color
    global replace_button_color


    preset_section = ""
    preset_prefix = ""
    if preset_index == 1:
        preset_section = config_file_color_preset1_section
        preset_prefix = "preset1_"
    elif preset_index == 2:
        preset_section = config_file_color_preset2_section
        preset_prefix = "preset2_"
    elif preset_index == 3:
        preset_section = config_file_color_preset3_section
        preset_prefix = "preset3_"

    try:
        preset_color_hex = config_parser.get(preset_section, "{0}source_section_color".format(preset_prefix))
        preset_color_string = preset_color_hex.replace(" ", "") # https://www.journaldev.com/23763/python-remove-spaces-from-string
        if len(preset_color_string) != 7:
            text_display_string.set("Length of string not correct to be a hex color code".format(preset_section))
            return
        if preset_color_string[:1] != "#": #Check to see if the first index of the string is "#".
            text_display_string.set("String not hex color code".format(preset_section))
            return
        int(preset_color_string[1:], 16) #Remove the "#" at the start and check if string can be convereted to hex
    except ValueError:
        text_display_string.set("Invalid value in string".format(preset_section))
        return
    except:
        text_display_string.set("No saved color changes found for {0}".format(preset_section))
        return


    source_section_color =                      config_parser.get(preset_section,            "{0}source_section_color".format(preset_prefix))
    replacement_section_color =                 config_parser.get(preset_section,            "{0}replacement_section_color".format(preset_prefix))                         
    default_button_color =                      config_parser.get(preset_section,            "{0}default_button_color".format(preset_prefix))
    button_highlight_color =                    config_parser.get(preset_section,            "{0}button_highlight_color".format(preset_prefix))
    both_scroll_buttons_same_color =            config_parser.getboolean(preset_section,     "{0}both_scroll_buttons_same_color".format(preset_prefix))
    both_up_scroll_button_color =               config_parser.get(preset_section,            "{0}both_up_scroll_button_color".format(preset_prefix))
    both_down_scroll_button_color =             config_parser.get(preset_section,            "{0}both_down_scroll_button_color".format(preset_prefix))
    to_file_buttons_same_color =                config_parser.getboolean(preset_section,     "{0}to_file_buttons_same_color".format(preset_prefix))
    to_first_source_file_button_color =         config_parser.get(preset_section,            "{0}to_first_source_file_button_color".format(preset_prefix))
    to_first_replacement_file_button_color =    config_parser.get(preset_section,            "{0}to_first_replacement_file_button_color".format(preset_prefix))
    to_last_source_file_button_color =          config_parser.get(preset_section,            "{0}to_last_source_file_button_color".format(preset_prefix))
    to_last_replacement_file_button_color =     config_parser.get(preset_section,            "{0}to_last_replacement_file_button_color".format(preset_prefix))
    extract_button_color =                      config_parser.get(preset_section,            "{0}extract_button_color".format(preset_prefix))
    compare_button_color =                      config_parser.get(preset_section,            "{0}compare_button_color".format(preset_prefix))
    compare_O_label_color =                     config_parser.get(preset_section,            "{0}compare_o_label_color".format(preset_prefix))
    compare_X_label_color =                     config_parser.get(preset_section,            "{0}compare_x_label_color".format(preset_prefix))
    fill_button_color =                         config_parser.get(preset_section,            "{0}fill_button_color".format(preset_prefix))
    replace_button_color =                      config_parser.get(preset_section,            "{0}replace_button_color".format(preset_prefix))

    global both_arrow_buttons_same_color_bool
    both_arrow_buttons_same_color_bool.set(both_scroll_buttons_same_color)
    global top_n_bottom_section_buttons_same_color_bool
    top_n_bottom_section_buttons_same_color_bool.set(to_file_buttons_same_color)


    global widget_background_colors_with_text_list
    widget_background_colors_with_text_list = [source_section_color, replacement_section_color,
                                           default_button_color,
                                           button_highlight_color,
                                           both_up_scroll_button_color, both_down_scroll_button_color,
                                           to_first_source_file_button_color, to_first_replacement_file_button_color, to_last_source_file_button_color, to_last_replacement_file_button_color,
                                           extract_button_color,
                                           compare_button_color, compare_O_label_color, compare_X_label_color,
                                           fill_button_color, replace_button_color]
    
    SetWidgetsTextColors()


    UpdateWidgetColor("all", None)

    if both_scroll_buttons_same_color == True:
        SetTextOfBothArrowColorCheckbutton()
        SetColorOfBothArrowColorCheckbutton()

    if to_file_buttons_same_color == True:
        SetTextOfToFileColorCheckbutton()
        SetColorOfToFileColorCheckbutton()


    OverwriteOptionsData("source_section_color", source_section_color, tab=1)
    OverwriteOptionsData("replacement_section_color", replacement_section_color, tab=1)
    OverwriteOptionsData("default_button_color", default_button_color, tab=1)
    OverwriteOptionsData("button_highlight_color", button_highlight_color, tab=1)
    OverwriteOptionsData("both_scroll_buttons_same_color", both_scroll_buttons_same_color, tab=1)
    OverwriteOptionsData("both_up_scroll_button_color", both_up_scroll_button_color, tab=1)
    OverwriteOptionsData("both_down_scroll_button_color", both_down_scroll_button_color, tab=1)
    OverwriteOptionsData("to_file_buttons_same_color", to_file_buttons_same_color, tab=1)
    OverwriteOptionsData("to_first_source_file_button_color", to_first_source_file_button_color, tab=1)
    OverwriteOptionsData("to_first_replacement_file_button_color", to_first_replacement_file_button_color, tab=1)
    OverwriteOptionsData("to_last_source_file_button_color", to_last_source_file_button_color, tab=1)
    OverwriteOptionsData("to_last_replacement_file_button_color", to_last_replacement_file_button_color, tab=1)
    OverwriteOptionsData("extract_button_color", extract_button_color, tab=1)
    OverwriteOptionsData("compare_button_color", compare_button_color, tab=1)
    OverwriteOptionsData("compare_O_label_color", compare_O_label_color, tab=1)
    OverwriteOptionsData("compare_X_label_color", compare_X_label_color, tab=1)
    OverwriteOptionsData("fill_button_color", fill_button_color, tab=1)
    OverwriteOptionsData("replace_button_color", replace_button_color, tab=1)


#Save the colors chosen for each button in the Color Options tab to the selected Preset section.
def SavePresetColors(preset_index):
    preset_section = ""
    preset_prefix = ""
    if preset_index == 1:
        preset_section = config_file_color_preset1_section
        preset_prefix = "preset1_"
    elif preset_index == 2:
        preset_section = config_file_color_preset2_section
        preset_prefix = "preset2_"
    elif preset_index == 3:
        preset_section = config_file_color_preset3_section
        preset_prefix = "preset3_"
    else:
        text_display_string.set('Error! "preset_index" not equal to corresponding button number! - SavePresetColors')
        return

    if config_parser.get(preset_section, "{0}source_section_color".format(preset_prefix)) == "":
        saving_color_presets_text = "Current colors saved"
    else:
        saving_color_presets_text = "Overwritten previous preset colors. Current colors saved"

    config_parser.set(preset_section, "{0}source_section_color".format(preset_prefix),                      widget_background_colors_with_text_list[0])
    config_parser.set(preset_section, "{0}replacement_section_color".format(preset_prefix),                 widget_background_colors_with_text_list[1])
    config_parser.set(preset_section, "{0}default_button_color".format(preset_prefix),                      widget_background_colors_with_text_list[2])
    config_parser.set(preset_section, "{0}button_highlight_color".format(preset_prefix),                    widget_background_colors_with_text_list[3])
    config_parser.set(preset_section, "{0}both_scroll_buttons_same_color".format(preset_prefix),            str(both_scroll_buttons_same_color))
    config_parser.set(preset_section, "{0}both_up_scroll_button_color".format(preset_prefix),               widget_background_colors_with_text_list[4])
    config_parser.set(preset_section, "{0}both_down_scroll_button_color".format(preset_prefix),             widget_background_colors_with_text_list[5])
    config_parser.set(preset_section, "{0}to_file_buttons_same_color".format(preset_prefix),                str(to_file_buttons_same_color))
    config_parser.set(preset_section, "{0}to_first_source_file_button_color".format(preset_prefix),         widget_background_colors_with_text_list[6])
    config_parser.set(preset_section, "{0}to_first_replacement_file_button_color".format(preset_prefix),    widget_background_colors_with_text_list[7])
    config_parser.set(preset_section, "{0}to_last_source_file_button_color".format(preset_prefix),          widget_background_colors_with_text_list[8])
    config_parser.set(preset_section, "{0}to_last_replacement_file_button_color".format(preset_prefix),     widget_background_colors_with_text_list[9])
    config_parser.set(preset_section, "{0}extract_button_color".format(preset_prefix),                      widget_background_colors_with_text_list[10])
    config_parser.set(preset_section, "{0}compare_button_color".format(preset_prefix),                      widget_background_colors_with_text_list[11])
    config_parser.set(preset_section, "{0}compare_o_label_color".format(preset_prefix),                     widget_background_colors_with_text_list[12])
    config_parser.set(preset_section, "{0}compare_x_label_color".format(preset_prefix),                     widget_background_colors_with_text_list[13])
    config_parser.set(preset_section, "{0}fill_button_color".format(preset_prefix),                         widget_background_colors_with_text_list[14])
    config_parser.set(preset_section, "{0}replace_button_color".format(preset_prefix),                      widget_background_colors_with_text_list[15])
    with open('config.ini', 'w') as outfile:
        config_parser.write(outfile)

    text_display_string.set(saving_color_presets_text)


#Sets the Chosen Color Option to its default color.
def SetColorsToDefaultSettings(number):
    
    update_widget_color_index = 0
    set_all_colors_to_default_string = "all"
    if number == 0 or number == set_all_colors_to_default_string: #Source Color Default
        global source_section_color
        if source_section_color != default_source_section_color:
            source_section_color = default_source_section_color
            OverwriteOptionsData("source_section_color", source_section_color, tab=1)
        pass
    if number == 1 or number == set_all_colors_to_default_string: #Replace Color Default
        global replacement_section_color
        if replacement_section_color != default_replacement_section_color:
            replacement_section_color = default_replacement_section_color
            OverwriteOptionsData("replacement_section_color", replacement_section_color, tab=1)
            update_widget_color_index = 1
        pass
    if number == 2 or number == set_all_colors_to_default_string: #Default Button Default Color
        global default_button_color
        if default_button_color != default_default_button_color:
            default_button_color = default_default_button_color
            OverwriteOptionsData("default_button_color", default_button_color, tab=1)
            update_widget_color_index = 2
        pass
    if number == 3 or number == set_all_colors_to_default_string: #Button Highlight Default
        global button_highlight_color
        if button_highlight_color != default_button_highlight_color:
            button_highlight_color = default_button_highlight_color
            OverwriteOptionsData("button_highlight_color", button_highlight_color, tab=1)
            update_widget_color_index = 3
        pass
    if number == 4 or number == set_all_colors_to_default_string: #"Both" Scroll Buttons Default
        global both_scroll_buttons_same_color
        global both_arrow_buttons_same_color_bool
        global both_up_scroll_button_color
        global both_down_scroll_button_color
        global both_up_scroll_button_text_color
        global both_down_scroll_button_text_color

        both_buttons_color = default_both_scroll_buttons_color
        both_buttons_text_color = "#000000" #black

        if both_up_scroll_button_color != both_buttons_color:
            both_up_scroll_button_color = both_buttons_color
            OverwriteOptionsData("both_up_scroll_button_color", both_up_scroll_button_color, tab=1)
            both_up_scroll_button_text_color = both_buttons_text_color

        if both_down_scroll_button_color != both_buttons_color:
            both_down_scroll_button_color = both_buttons_color
            OverwriteOptionsData("both_down_scroll_button_color", both_down_scroll_button_color, tab=1)
            both_down_scroll_button_text_color = both_buttons_text_color


        both_arrow_buttons_same_color_bool.set(True)
        if both_scroll_buttons_same_color != True:
            both_scroll_buttons_same_color = True
            OverwriteOptionsData('both_scroll_buttons_same_color', str(both_scroll_buttons_same_color), tab=1)

        if number != set_all_colors_to_default_string:
            update_widget_color_index = "both_scroll"

        pass
    if number == 5 or number == set_all_colors_to_default_string: #"To File" Scroll Buttons Default
        global to_file_buttons_same_color
        global top_n_bottom_section_buttons_same_color_bool
        global to_first_source_file_button_color
        global to_first_replacement_file_button_color
        global to_last_source_file_button_color
        global to_last_replacement_file_button_color
        global to_first_source_file_button_text_color
        global to_first_replacement_file_button_text_color
        global to_last_source_file_button_text_color
        global to_last_replacement_file_button_text_color

        to_buttons_color = default_to_file_scroll_buttons_color #white
        to_buttons_text_color = "#000000" #black

        if to_first_source_file_button_color != to_buttons_color:
            to_first_source_file_button_color = to_buttons_color
            OverwriteOptionsData("to_first_source_file_button_color", to_first_source_file_button_color, tab=1)
            to_first_source_file_button_text_color = to_buttons_text_color

        if to_first_replacement_file_button_color != to_buttons_color:
            to_first_replacement_file_button_color = to_buttons_color
            OverwriteOptionsData("to_first_replacement_file_button_color", to_first_replacement_file_button_color, tab=1)
            to_first_replacement_file_button_text_color = to_buttons_text_color

        if to_last_source_file_button_color != to_buttons_color:
            to_last_source_file_button_color = to_buttons_color
            OverwriteOptionsData("to_last_source_file_button_color", to_last_source_file_button_color, tab=1)
            to_last_source_file_button_text_color = to_buttons_text_color

        if to_last_replacement_file_button_color != to_buttons_color:
            to_last_replacement_file_button_color = to_buttons_color
            OverwriteOptionsData("to_last_replacement_file_button_color", to_last_replacement_file_button_color, tab=1)
            to_last_replacement_file_button_text_color = to_buttons_text_color


        top_n_bottom_section_buttons_same_color_bool.set(True)
        if to_file_buttons_same_color != True:
            to_file_buttons_same_color = True
            OverwriteOptionsData("to_file_buttons_same_color", str(to_file_buttons_same_color), tab=1)

        if number != set_all_colors_to_default_string:
            update_widget_color_index = "four_scroll"

        pass
    if number == 6 or number == set_all_colors_to_default_string: #Extract Button Default
        global extract_button_color
        if extract_button_color != default_extract_button_color:
            extract_button_color = default_extract_button_color
            OverwriteOptionsData("extract_button_color", extract_button_color, tab=1)
            update_widget_color_index = 10
        pass
    if number == 7 or number == set_all_colors_to_default_string: #Compare Button Default
        global compare_button_color
        if compare_button_color != default_compare_button_color:
            compare_button_color = default_compare_button_color
            OverwriteOptionsData("compare_button_color", compare_button_color, tab=1)
            update_widget_color_index = 11
        pass
    if number == 8 or number == set_all_colors_to_default_string: #Compare Fillable Default
        global compare_O_label_color
        if compare_O_label_color != default_compare_O_label_color:
            compare_O_label_color = default_compare_O_label_color
            OverwriteOptionsData("compare_O_label_color", compare_O_label_color, tab=1)
            update_widget_color_index = 12
        pass
    if number == 9 or number == set_all_colors_to_default_string: #Compare Nonfillable Default
        global compare_X_label_color
        if compare_X_label_color != default_compare_X_label_color:
            compare_X_label_color = default_compare_X_label_color
            OverwriteOptionsData("compare_X_label_color", compare_X_label_color, tab=1)
            update_widget_color_index = 13
        pass
    if number == 10 or number == set_all_colors_to_default_string: #Fill Button Default
        global fill_button_color
        if fill_button_color != default_fill_button_color:
            fill_button_color = default_fill_button_color
            OverwriteOptionsData("fill_button_color", fill_button_color, tab=1)
            update_widget_color_index = 14
        pass
    if number == 11 or number == set_all_colors_to_default_string: #Replace Button Default
        global replace_button_color
        if replace_button_color != default_replace_button_color:
            replace_button_color = default_replace_button_color
            OverwriteOptionsData("replace_button_color", replace_button_color, tab=1)
            update_widget_color_index = 15
        pass


    if number == set_all_colors_to_default_string:
        update_widget_color_index = set_all_colors_to_default_string
    if update_widget_color_index != None:
        UpdateWidgetColor(update_widget_color_index)
    
    pass

#------------------------------------------------------------- Color Options -------------------------------------------------------------#


#Overwrites any option data that the user changed and saves it.
def OverwriteOptionsData(name_of_option, option, tab=0):
    #try:
    if tab == 0:
        config_file_tab_section = config_file_options_section
    elif tab == 1:
        config_file_tab_section = config_file_color_options_section
    elif tab == 2:
        config_file_tab_section = config_file_general_section

    #If the data is not the exact same as in the config file
    if option != config_parser.get(config_file_tab_section, name_of_option):
        config_parser.set(config_file_tab_section, name_of_option, option)
        with open('config.ini', 'w') as outfile:
            config_parser.write(outfile)
    #except:
    #    text_display_string.set('Error occured when trying to overwrite data in config.ini')
    pass


#------------------------------------------------------------------------------------------ OPTIONS MENU SECTION -----------------------------------------------------------------------------------------------#





#--------------------------------------------------------------- MENUBAR SECTION -------------------------------------------------------------------#

#Creates the window that allows the user to set the File index they want to go to.
def GoToFileIndexInSection():
    if len(replacement_files) == 0 and len(source_files) == 0:
        text_display_string.set("There are no files in both HCA Files sections.")
        return
    go_to_file_in_section_window = Toplevel()
    go_to_file_in_section_window_base_width = Decimal(200)
    go_to_file_in_section_window_base_height = Decimal(200)
    go_to_file_in_section_window.resizable(False, False)
    WindowCenterPositioner(go_to_file_in_section_window, go_to_file_in_section_window_base_width, go_to_file_in_section_window_base_height)

    go_to_file_in_section_window_12_font = InitialWindowFontSize(12, go_to_file_in_section_window.winfo_width(), go_to_file_in_section_window.winfo_height(), go_to_file_in_section_window_base_width, go_to_file_in_section_window_base_height)
    go_to_file_in_section_window_8_font = InitialWindowFontSize(8, go_to_file_in_section_window.winfo_width(), go_to_file_in_section_window.winfo_height(), go_to_file_in_section_window_base_width, go_to_file_in_section_window_base_height)

    go_to_file_in_section_option_types_frame = Frame(go_to_file_in_section_window)
    go_to_file_in_section_option_types_frame.place(relwidth=1, relheight=0.8)

    go_to_file_in_section_type = IntVar()

    #Sets the background color of the window.
    def SetGoToFileWindowColor():
        hero = go_to_file_in_section_type.get()
        if hero == 1:
            go_to_file_in_section_bg_color = source_section_color
            go_to_file_in_section_text_color = source_section_text_color 
        elif hero == 2:
            go_to_file_in_section_bg_color = replacement_section_color
            go_to_file_in_section_text_color = replacement_section_text_color
        else:
            if switch_scroll_buttons_placement == True:
                go_to_file_in_section_bg_color = both_down_scroll_button_color
                go_to_file_in_section_text_color = both_down_scroll_button_text_color
            else:
                go_to_file_in_section_bg_color = both_up_scroll_button_color
                go_to_file_in_section_text_color = both_up_scroll_button_text_color

        go_to_file_in_section_option_types_frame.config(bg=go_to_file_in_section_bg_color)
        if len(source_files) > 1 and len(replacement_files) > 1:
            go_to_file_in_both_containers.config(bg=go_to_file_in_section_bg_color, fg=go_to_file_in_section_text_color, activebackground=go_to_file_in_section_bg_color, selectcolor=CalculateTextColor(go_to_file_in_section_text_color))
        if len(source_files) > 1:
            go_to_file_in_source_container.config(bg=go_to_file_in_section_bg_color, fg=go_to_file_in_section_text_color, activebackground=go_to_file_in_section_bg_color, selectcolor=CalculateTextColor(go_to_file_in_section_text_color))
        if len(replacement_files) > 1:
            go_to_file_in_replacement_container.config(bg=go_to_file_in_section_bg_color, fg=go_to_file_in_section_text_color, activebackground=go_to_file_in_section_bg_color, selectcolor=CalculateTextColor(go_to_file_in_section_text_color))
        pass


    if len(source_files) > 1 and len(replacement_files) > 1:
        go_to_file_in_both_containers = Radiobutton(go_to_file_in_section_option_types_frame, variable=go_to_file_in_section_type, value=3, font=go_to_file_in_section_window_12_font, text="Both Sections", command=SetGoToFileWindowColor)
    if len(source_files) > 1:
        go_to_file_in_source_container = Radiobutton(go_to_file_in_section_option_types_frame, variable=go_to_file_in_section_type, value=1, font=go_to_file_in_section_window_12_font, text="Source HCA Files", command=SetGoToFileWindowColor)
    if len(replacement_files) > 1:
        go_to_file_in_replacement_container = Radiobutton(go_to_file_in_section_option_types_frame, variable=go_to_file_in_section_type, value=2, font=go_to_file_in_section_window_12_font, text="Replacement HCA Files", command=SetGoToFileWindowColor)


    if len(source_files) > 1 and len(replacement_files) > 1:
        go_to_file_in_section_type.set(3)
        go_to_file_in_both_containers.place(relwidth=1, relheight=0.15, rely=0.25)
        go_to_file_in_source_container.place(relwidth=1, relheight=0.15, rely=0.40)
        go_to_file_in_replacement_container.place(relwidth=1, relheight=0.15, rely=0.55)
    elif len(source_files) > 1:
        go_to_file_in_section_type.set(1)
        go_to_file_in_source_container.place(relwidth=1, relheight=0.15, rely=0.40)
    elif len(replacement_files) > 1:
        go_to_file_in_section_type.set(2)
        go_to_file_in_replacement_container.place(relwidth=1, relheight=0.15, rely=0.40)

    SetGoToFileWindowColor()


    #Resize the font size of the window.
    def GoToIndexInSelectedSection(event):
        try:
            inputed_info = int(go_to_file_in_section_user_input.get()) - 1
        except:
            return

        file_section_type = go_to_file_in_section_type.get()
        if file_section_type == 1:
            MoveFilesInSection(inputed_info, 0, True)
        elif file_section_type == 2:
            MoveFilesInSection(inputed_info, 1, True)
        else:
            MoveFilesInSection(inputed_info, 0, True)
            MoveFilesInSection(inputed_info, 1, True)

        if int(go_to_file_in_section_user_input.get()) <= 0:
            go_to_file_in_section_user_input.delete(0, "end")
            go_to_file_in_section_user_input.insert(0, 1)
            return

        if file_section_type == 1:
            largest_files_size = len(source_files)
            if largest_files_size == 0:
                text_display_string.set("There are no files in the Source HCA Files section.")
        elif file_section_type == 2:
            largest_files_size = len(replacement_files)
            if largest_files_size == 0:
                text_display_string.set("There are no files in the Replacement HCA Files section.")
        else:
            if len(replacement_files) > len(source_files):
                largest_files_size = len(replacement_files)
            else:
                largest_files_size = len(source_files)
            if largest_files_size == 0:
                text_display_string.set("There are no files in both HCA Files sections.")

        if int(go_to_file_in_section_user_input.get()) > largest_files_size:
            go_to_file_in_section_user_input.delete(0, "end")
            go_to_file_in_section_user_input.insert(0, largest_files_size)

        pass


    go_to_file_in_section_window_input_frame = Frame(go_to_file_in_section_window)
    go_to_file_in_section_window_input_frame.place(relwidth=1, relheight=0.2, rely=0.8)

    index_move_by_input_change_button = Button(go_to_file_in_section_window_input_frame, text="Go to File\nPosition", font=go_to_file_in_section_window_8_font, bg=default_button_color, fg=default_button_text_color, command=lambda: GoToIndexInSelectedSection(None) )
    index_move_by_input_change_button.place(relwidth=0.3, relheight=1)

    go_to_file_in_section_user_input = Entry(go_to_file_in_section_window_input_frame, justify="center", font=go_to_file_in_section_window_12_font, relief="ridge", bd=5)
    go_to_file_in_section_user_input.place(relwidth=0.7, relheight=1, relx=0.3)
    go_to_file_in_section_user_input.bind('<Return>', lambda e: GoToIndexInSelectedSection(e) )

    #Only accept decimal numbers to be inputed into the Entry widget.
    def OnlyDecimalNumbersInputedInEntryWidget(action_code, inputed_string_character):
        if action_code == "1": #Inputing
            try:
                int(inputed_string_character)
            except:
                return False

        return True
    only_decimal_number_input_check = (go_to_file_in_section_user_input.register(OnlyDecimalNumbersInputedInEntryWidget),'%d', '%S')
    go_to_file_in_section_user_input.config(validate='key', validatecommand=only_decimal_number_input_check)

    pass


switch_containers_placement = config_parser.getboolean(config_file_general_section, 'switch_containers_placement')
#Switch the positions of the Source Section and the Replacement Section.
def SwitchHCAFilesContainers():
    global switch_containers_placement
    if switch_containers_placement == True:
        switch_containers_placement = False #Set back to default

        source_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=source_container_relx, rely=top_section_rely)
        replacement_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=replace_container_relx, rely=top_section_rely)

        to_file_lead_color = to_first_source_file_button_color
        to_file_lead_text_color = to_first_source_file_button_text_color
    else:
        switch_containers_placement = True #Switch placements
        
        replacement_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=source_container_relx, rely=top_section_rely)
        source_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=replace_container_relx, rely=top_section_rely)

        to_file_lead_color = to_first_replacement_file_button_color
        to_file_lead_text_color = to_first_replacement_file_button_text_color

    SetScrollButtonLayout()

    switch_hca_files_containers_type.set(switch_containers_placement)
    OverwriteOptionsData("switch_containers_placement", str(switch_containers_placement), tab=2 )


switch_scroll_buttons_placement = config_parser.getboolean(config_file_general_section, 'switch_scroll_buttons_placement')
#Switch the Upwards Scroll Buttons and the Downards Scroll Buttons.
def SwitchPositionsOfScrollButtons():
    global switch_scroll_buttons_placement
    if switch_scroll_buttons_placement == True:
        switch_scroll_buttons_placement = False
    else:
        switch_scroll_buttons_placement = True
    SetScrollButtonLayout()
    switch_scroll_buttons_type.set(switch_scroll_buttons_placement)
    OverwriteOptionsData("switch_scroll_buttons_placement", str(switch_scroll_buttons_placement), tab=2 )


#Creates the About Window, which details information about the program, such as the Program Version, the creator (me; Captain Roy Falco), the directory of the program's .exe file, the page to download the proram, and the contact info for the creator.
def AboutWindow():
    about_window = Toplevel(root_window)
    about_window_base_width = Decimal(500)
    about_window_base_height = Decimal(375)
    about_window.resizable(False, False)
    WindowCenterPositioner(about_window, about_window_base_width, about_window_base_height)
    
    about_window_10_font = InitialWindowFontSize(10, about_window.winfo_width(), about_window.winfo_height(), about_window_base_width, about_window_base_height)
    about_window_12_font = InitialWindowFontSize(12, about_window.winfo_width(), about_window.winfo_height(), about_window_base_width, about_window_base_height)

    about_window_14_font = InitialWindowFontSize(15, about_window.winfo_width(), about_window.winfo_height(), about_window_base_width, about_window_base_height)
    about_window_18_font = InitialWindowFontSize(18, about_window.winfo_width(), about_window.winfo_height(), about_window_base_width, about_window_base_height)

    about_window_frame = Frame(about_window)
    about_window_frame.pack(fill="both", expand="y")

    program_name = Label(about_window_frame, text="HCA Automatic Byte Filler and Replacer", font=about_window_18_font)
    version_info = Label(about_window_frame, text="Version 1.4", font=about_window_18_font)
    credits_info = Label(about_window_frame, text="Created by Captain Roy Falco", font=about_window_14_font)

    file_location_info_label = Label(about_window_frame, text="Program Directory", font=about_window_12_font)
    file_location_info = Text(about_window_frame, font=about_window_10_font, wrap="none", bd=4, relief="ridge")
    file_location_info.insert("end", os.getcwd() )
    file_location_info_x_axis_scrollbar = ttk.Scrollbar(file_location_info, orient="horizontal", command=file_location_info.xview)
    file_location_info.config(xscrollcommand=file_location_info_x_axis_scrollbar.set, state="disabled")

    download_info_label = Label(about_window_frame, text="Download Page", font=about_window_12_font)
    download_info_link = "https://github.com/CaptainRoyFalco/HCA-Automatic-Byte-Filler-and-Replacer"
    download_info = Text(about_window_frame, font=about_window_10_font, wrap="none", bd=4, relief="ridge")
    download_info.insert("end", download_info_link)
    download_info.config(state="disabled")
    #download_info = Label(about_window_frame, text=download_info_link, font=about_window_10_font), fg="blue", cursor="hand2")
    #download_info.bind("<Button-1>", lambda e, d=webbrowser: [d.open_new_tab(download_info_link)]) # https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter

    contact_info_label = Label(about_window_frame, text="Contact me on Reddit", font=about_window_12_font)
    contact_info_link = "https://www.reddit.com/user/Captian_Roy_Falco"
    contact_info = Text(about_window_frame, font=about_window_10_font, wrap="none", bd=4, relief="ridge")
    contact_info.insert("end", contact_info_link)
    contact_info.config(state="disabled")
    #contact_info = Label(about_window_frame, text=contact_info_link, font=about_window_10_font), fg="blue", cursor="hand2")
    #contact_info.bind("<Button-1>", lambda e, c=webbrowser: c.open_new_tab(contact_info_link))


    program_name.place(relwidth=1, relheight=0.10, rely=0.01)
    version_info.place(relwidth=1, relheight=0.06, rely=0.11)
    credits_info.place(relwidth=1, relheight=0.10, rely=0.21)
    file_location_info_label.place(relwidth=1, relheight=0.1, rely=0.38)
    file_location_info_x_axis_scrollbar.place(relwidth=1, relheight=0.45, relx=0.0, rely=0.55) #.pack(side="bottom", fill="x")
    file_location_info.place(relwidth=1, relheight=0.13, rely=0.48)
    download_info_label.place(relwidth=1, relheight=0.10, rely=0.63)
    download_info.place(relwidth=1, relheight=0.08, rely=0.71) #download_info.place(relwidth=1, relheight=0.05, rely=0.71)
    contact_info_label.place(relwidth=1, relheight=0.10, rely=0.79)
    contact_info.place(relwidth=1, relheight=0.08, rely=0.87) #contact_info.place(relwidth=1, relheight=0.05, rely=0.87)

#--------------------------------------------------------------- MENUBAR SECTION -------------------------------------------------------------------#





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Set the positions of the Scroll Buttons based on the options selected by the user.
def SetScrollButtonLayout():
    global switch_containers_placement
    global switch_scroll_buttons_placement

    if switch_containers_placement == True and switch_scroll_buttons_placement == True:
        holdthis = [to_last_replacement_file_button, to_last_source_file_button, both_sections_down_arrow_button, replacement_scroll_down_button, source_scroll_down_button, replacement_scroll_up_button, source_scroll_up_button, both_sections_up_arrow_button, to_first_replacement_file_button, to_first_source_file_button]
        both_button_lead_color = both_down_scroll_button_color
        both_button_lead_text_color = both_down_scroll_button_text_color
        to_file_lead_color = to_last_replacement_file_button_color
        to_file_lead_text_color = to_last_replacement_file_button_text_color
        pass
    elif switch_containers_placement == True:
        holdthis = [to_first_replacement_file_button, to_first_source_file_button, both_sections_up_arrow_button, replacement_scroll_up_button, source_scroll_up_button, replacement_scroll_down_button, source_scroll_down_button, both_sections_down_arrow_button, to_last_replacement_file_button, to_last_source_file_button]
        both_button_lead_color = both_up_scroll_button_color
        both_button_lead_text_color = both_up_scroll_button_text_color
        to_file_lead_color = to_first_replacement_file_button_color
        to_file_lead_text_color = to_first_replacement_file_button_text_color
        pass
    elif switch_scroll_buttons_placement == True:
        holdthis = [to_last_source_file_button, to_last_replacement_file_button, both_sections_down_arrow_button, source_scroll_down_button, replacement_scroll_down_button, source_scroll_up_button, replacement_scroll_up_button, both_sections_up_arrow_button, to_first_source_file_button, to_first_replacement_file_button]
        both_button_lead_color = both_down_scroll_button_color
        both_button_lead_text_color = both_down_scroll_button_text_color
        to_file_lead_color = to_last_source_file_button_color
        to_file_lead_text_color = to_last_source_file_button_text_color
        pass
    else: #Default Positions
        holdthis = [to_first_source_file_button, to_first_replacement_file_button, both_sections_up_arrow_button, source_scroll_up_button, replacement_scroll_up_button, source_scroll_down_button, replacement_scroll_down_button, both_sections_down_arrow_button, to_last_source_file_button, to_last_replacement_file_button]
        both_button_lead_color = both_up_scroll_button_color
        both_button_lead_text_color = both_up_scroll_button_text_color
        to_file_lead_color = to_first_source_file_button_color
        to_file_lead_text_color = to_first_source_file_button_text_color
        pass

    integet = 0
    scroll_button_relwidth = 0.5
    scroll_button_relx = 0.0
    scroll_button_rely = 0.0
    for scroll_button in holdthis:
        if (scroll_button == both_sections_up_arrow_button) or (scroll_button == both_sections_down_arrow_button):
            scroll_button_relwidth = 1
        else:
            scroll_button_relwidth = 0.5

        if integet == 1 or integet == 4 or integet == 6 or integet == 9:
            scroll_button_relx = 0.5
        else:
            scroll_button_relx = 0.0

        if integet == 2:
            scroll_button_rely = 0.2
        elif integet == 3:
            scroll_button_rely = 0.3
        elif integet == 5:
            scroll_button_rely = 0.6
        elif integet == 7:
            scroll_button_rely = 0.7
        elif integet == 8:
            scroll_button_rely = 0.9

        scroll_button.place(relwidth=scroll_button_relwidth, relheight=0.1, relx=scroll_button_relx, rely=scroll_button_rely)

        integet += 1


    global both_scroll_buttons_same_color
    if both_scroll_buttons_same_color == True:
        if both_sections_up_arrow_button.cget("state") == "normal":
            both_sections_up_arrow_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)
        if both_sections_down_arrow_button.cget("state") == "normal":
            both_sections_down_arrow_button.config(bg=both_button_lead_color, fg=both_button_lead_text_color)
        pass
    else:
        if both_sections_up_arrow_button.cget("state") == "normal":
            both_sections_up_arrow_button.config(bg=both_up_scroll_button_color, fg=both_up_scroll_button_text_color)
        if both_sections_down_arrow_button.cget("state") == "normal":
            both_sections_down_arrow_button.config(bg=both_down_scroll_button_color, fg=both_down_scroll_button_text_color)
        pass

    global to_file_buttons_same_color
    if to_file_buttons_same_color == True:
        if to_first_source_file_button.cget("state") == "normal":
            to_first_source_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)
        if to_first_replacement_file_button.cget("state") == "normal":
            to_first_replacement_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)
        if to_last_source_file_button.cget("state") == "normal":
            to_last_source_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)
        if to_last_replacement_file_button.cget("state") == "normal":
            to_last_replacement_file_button.config(bg=to_file_lead_color, fg=to_file_lead_text_color)
        pass
    else:
        if to_first_source_file_button.cget("state") == "normal":
            to_first_source_file_button.config(bg=to_first_source_file_button_color, fg=to_first_source_file_button_text_color)
        if to_first_replacement_file_button.cget("state") == "normal":
            to_first_replacement_file_button.config(bg=to_first_replacement_file_button_color, fg=to_first_replacement_file_button_text_color)
        if to_last_source_file_button.cget("state") == "normal":
            to_last_source_file_button.config(bg=to_last_source_file_button_color, fg=to_last_source_file_button_text_color)
        if to_last_replacement_file_button.cget("state") == "normal":
            to_last_replacement_file_button.config(bg=to_last_replacement_file_button_color, fg=to_last_replacement_file_button_text_color)
        pass

    pass


#Sets the button highlight color when the mouse pointer is over an enabled button and sets the button's color back when it's not.
def HoveringOverWidget(event):
    button = event.widget
    if button.cget("state") == "disabled":
        return

    global original_button_color
    global original_button_text_color
    original_button_color = button.cget('background')
    original_button_text_color = button.cget('fg')

    if original_button_color == button_highlight_color:
        highlight_color="SystemButtonFace"
        highlight_text_color = "black"
    else:
        highlight_color = button_highlight_color
        highlight_text_color = button_highlight_text_color

    if isinstance(button, Menubutton): # https://stackoverflow.com/questions/34667710/pattern-matching-tkinter-child-widgets-winfo-children-to-determine-type
        button.config(activebackground=highlight_color, activeforeground=highlight_text_color)
    else:
        if isinstance(button, Checkbutton):
            if highlight_text_color == "#000000" or highlight_text_color == "black": # https://stackoverflow.com/questions/55311242/tkinter-checkbutton-wont-keep-its-check-mark-post-color-change
                button.config(selectcolor='white')
            else:
                button.config(selectcolor='black')
        button.config(bg=highlight_color, fg=highlight_text_color)
    pass
def NotHoveringOverWidget(event):
    button = event.widget
    if button.cget("state") == "disabled":
        return

    if isinstance(button, Menubutton):
        button.config(activeforeground='black')
    else:
        if isinstance(button, Checkbutton):
            if original_button_text_color == "#000000" or original_button_text_color == "black":
                button.config(selectcolor='white')
            else:
                button.config(selectcolor='black')           
        button.config(bg=original_button_color, fg=original_button_text_color)
    pass


#Resize the text size of the labels in the Source and Replacement containers.
def ResizeLabels(root_window_width, root_window_height, do_single_label=False, single_label_in_other_loop=None):
    label_font_size = int(round(  Decimal(10) * (( (Decimal(root_window_width) / root_window_base_width) + (Decimal(root_window_height) / root_window_base_height) ) / Decimal(2)) ))
    label_wrap_length = int( Decimal(300) * (Decimal(root_window_width) / root_window_base_width) )
    #Label width is uneccessary to calculate because the labels are packed with fill="x", meaning the labels autmatically fill all the way to the sides based on the size of the container

    #Only configure things that will change when the labels are resized. Don't configure "justify" for example, since that doesn't need to change after the label is created.
    if do_single_label == True:
        for single_label in single_label_in_other_loop:
            single_label.config(wraplength = label_wrap_length, font=("Helvetica", label_font_size) )
    else:
        if len(label_source_list) > 0:
            for source_label in label_source_list:
                source_label.config(wraplength = label_wrap_length, font=("Helvetica", label_font_size) )

        if len(label_replacement_list) > 0:
            for replace_label in label_replacement_list:
                replace_label.config(wraplength = label_wrap_length, font=("Helvetica", label_font_size) )
        pass

    pass


#Resize the text size of the buttons, containers, and text frame.
def ResizeFont(event):
    if event.widget == root_window:
        global root_window_previous_width
        global root_window_previous_height

        if (event.width != root_window_previous_width) or (event.height != root_window_previous_height): # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
            root_window_previous_width = event.width
            root_window_previous_height = event.height

            root_window_width_ratio = Decimal(event.width) / root_window_base_width
            root_window_height_ratio = Decimal(event.height) / root_window_base_height_without_menubar
            scale_by_size = (root_window_width_ratio + root_window_height_ratio) / Decimal(2)

            size_10 = int(round( Decimal(10) * scale_by_size ))
            root_resize_font_10 = ("Helvetica", size_10)
            size_9 = int(round( Decimal(9) * scale_by_size ))
            root_resize_font_9 = ("Helvetica", size_9)
            size_8 = int(round( Decimal(8) * scale_by_size ))
            root_resize_font_8 = ("Helvetica", size_8)

            source_container.config(font=root_resize_font_10)
            replacement_container.config(font=root_resize_font_10)
            add_button.config(font=root_resize_font_10)

            for disabled_button in initially_disabled_buttons_list:
                if disabled_button == sort_button or disabled_button == remove_button:
                    disabled_button.config(font=root_resize_font_10)
                elif disabled_button == fill_button or disabled_button == compare_button:
                    disabled_button.config(font=root_resize_font_9)
                else:
                    disabled_button.config(font=root_resize_font_8)

            extract_button.config(font=root_resize_font_9)
            replace_button.config(font=root_resize_font_9)

            new_wrap_length = Decimal(515) * ( Decimal(event.width) / root_window_base_width )
            display_text.config(wraplength = new_wrap_length, font=root_resize_font_10)

            if len(label_source_list) > 0 or len(label_replacement_list) > 0:
                ResizeLabels(event.width, event.height)

            pass
    pass


#----- Main Canvas -----#
root_window = Tk()
root_window_base_width = Decimal(750)
root_window_base_height = Decimal(500)

root_window.minsize( root_window_base_width / Decimal(2), root_window_base_height / Decimal(2) )
WindowCenterPositioner(root_window, root_window_base_width, root_window_base_height)

root_window_8_font = InitialWindowFontSize(8, root_window.winfo_width(), root_window.winfo_height(), root_window_base_width, root_window_base_height)
root_window_9_font = InitialWindowFontSize(9, root_window.winfo_width(), root_window.winfo_height(), root_window_base_width, root_window_base_height)
root_window_10_font = InitialWindowFontSize(10, root_window.winfo_width(), root_window.winfo_height(), root_window_base_width, root_window_base_height)

root_window.wm_title('HCA Automatic Byte Filler and Replacer')

#----- Menu Bar -----#
menubar = Menu(root_window)
root_window.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root_window.quit) #Even though you need to press the Exit button twice opening it from the command line window, this does not happen when the program is a .exe     # https://stackoverflow.com/questions/38442853/why-does-the-tkinter-quit2-widget-require-me-to-press-it-twice-for-it-to-activat#:~:text=you%20launch%20your%20script%20from%20the%20interpreter%20(implicit%20mainloop)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Options', command=OptionsWindow)
edit_menu_go_to_command_name = 'Go To...'
edit_menu.add_command(label=edit_menu_go_to_command_name, command=GoToFileIndexInSection, state="disabled")

about_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Extra', menu=about_menu)
switch_hca_files_containers_type = BooleanVar()
switch_hca_files_containers_type.set(switch_containers_placement)
about_menu.add_checkbutton(label='Switch Placement of HCA File Containers', command=SwitchHCAFilesContainers, variable=switch_hca_files_containers_type)
switch_scroll_buttons_type = BooleanVar()
switch_scroll_buttons_type.set(switch_scroll_buttons_placement)
about_menu.add_checkbutton(label='Switch Placement of "Up" and "Down" Scroll Buttons', command=SwitchPositionsOfScrollButtons, variable=switch_scroll_buttons_type)
about_menu.add_separator()
about_menu.add_command(label='Create A New "config.ini" File', command=CreateConfigFile)
about_menu.add_separator()
about_menu.add_command(label='About', command=AboutWindow)


#----- .place() calculations -----#
#Calculations based on the root window being 750 x 480 (480 instead of 500 because of the menu bar I think)
root_window_base_height_without_menubar = root_window_base_height - Decimal(20)


# root window width = left padding + source container width + middle frame width + replacement container width + right padding
#        750        =       15     +           310          +        100         +            310              +      15

s_and_r_containers_relwidth = Decimal(310) / root_window_base_width
source_container_relx = Decimal(15) / root_window_base_width
mid_frame_relwidth = Decimal(100) / root_window_base_width
mid_frame_relx = Decimal(325) / root_window_base_width #15+310=325
replace_container_relx = Decimal(425) / root_window_base_width #15+310+100=425


# root window height = top padding + top section height + text frame section height + bottom padding
#         480        =     15      +         400        +            50             +       15

top_section_relheight = Decimal(400) / root_window_base_height_without_menubar
top_section_rely = Decimal(15) / root_window_base_height_without_menubar
text_relheight = Decimal(50) / root_window_base_height_without_menubar



#----- Source Files Section-----#   #----- Replacement Files Section-----#
source_section_dir = 'source_files_directory'
source_container_title = "Source HCA Files"
source_container = LabelFrame(root_window, text=source_container_title, font=root_window_10_font, bg=source_section_color, fg=source_section_text_color)

replacement_section_dir = 'replacement_files_directory'
replacement_container_title = "Replacement HCA Files"
replacement_container = LabelFrame(root_window, text=replacement_container_title, font=root_window_10_font, bg = replacement_section_color, fg=replacement_section_text_color)

if switch_containers_placement == True:
    replacement_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=source_container_relx, rely=top_section_rely) #replacement_container uses source_container_relx
    source_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=replace_container_relx, rely=top_section_rely) #source_container uses replace_container_relx
else:
    source_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=source_container_relx, rely=top_section_rely)
    replacement_container.place(relwidth=s_and_r_containers_relwidth, relheight=top_section_relheight, relx=replace_container_relx, rely=top_section_rely)



#----- Middle Section -----#
middle_frame = Frame(root_window, bg=button_highlight_color)
middle_frame.place(relwidth=mid_frame_relwidth, relheight=top_section_relheight, relx=mid_frame_relx, rely=top_section_rely)

add_button = Button(middle_frame, bg=default_button_color, fg=default_button_text_color, text='ADD', font=root_window_10_font, command=ConfirmFileSection)
add_button.place(relwidth=0.5, relheight=0.1, rely=0.40)

sort_button = Button(middle_frame, text='SORT', command=SortFiles)
sort_button.place(relwidth=1, relheight=0.1, rely=0.50)

remove_button = Button(middle_frame, text='DEL', command=RemoveSelection)
remove_button.place(relwidth=0.5, relheight=0.1, rely=0.40, relx=0.5)


SetBothScrollButtonsIncrement()
source_scroll_up_button = Button(middle_frame, text='Source\nUp', command=lambda : MoveFilesInSection(-source_scroll_increment, 0)) # https://stackoverflow.com/questions/3704568/tkinter-button-command-activates-upon-running-program
replacement_scroll_up_button = Button(middle_frame, text='Replace\nUp', command=lambda : MoveFilesInSection(-replace_scroll_increment, 1))

both_sections_up_arrow_button = Button(middle_frame, text='Both\nUp', command=lambda : [MoveFilesInSection(-both_scroll_buttons_source_increment, 0), MoveFilesInSection(-both_scroll_buttons_replacement_increment, 1)])

to_first_source_file_button = Button(middle_frame, text='To First\n(S) File', command=lambda : MoveFilesInSection(-len(source_files), 0) )
to_first_replacement_file_button = Button(middle_frame, text='To First\nFile (R)', command=lambda : MoveFilesInSection(-len(replacement_files), 1) )

source_scroll_down_button = Button(middle_frame, text='Source\nDown', command=lambda : MoveFilesInSection(source_scroll_increment, 0))
replacement_scroll_down_button = Button(middle_frame, text='Replace\nDown', command=lambda : MoveFilesInSection(replace_scroll_increment, 1))

both_sections_down_arrow_button = Button(middle_frame, text='Both\nDown', command=lambda : [MoveFilesInSection(both_scroll_buttons_source_increment, 0), MoveFilesInSection(both_scroll_buttons_replacement_increment, 1)])

to_last_source_file_button = Button(middle_frame, text='To Last\n(S) File', command=lambda : MoveFilesInSection(len(source_files), 0) )
to_last_replacement_file_button = Button(middle_frame, text='To Last\nFile (R)', command=lambda : MoveFilesInSection(len(replacement_files), 1) )


SetScrollButtonLayout()



#----- Bottom Section -----#
text_frame = Frame(root_window, bg='black')
text_frame.place(relwidth=1, relheight=text_relheight, relx=0.5, rely=1, anchor='s')

extract_uexp_dir = "file_to_extract_from_directory"
extract_location_dir = "extracted_files_directory"
extract_button = Button(text_frame, bg=extract_button_color, fg=extract_button_text_color, text ='EXTRACT', font=root_window_9_font, command=ExtractHCAFiles)
extract_button.place(relwidth=0.1, relheight=1, relx=0.0)

text_display_string=StringVar()
display_text = Label(text_frame, bg='black', fg='white', textvariable=text_display_string, font=root_window_10_font, anchor="w", justify='left', wraplength=450)
text_display_string.set('')
display_text.place(relwidth=0.6, relheight=1, relx=0.1) # 750 * 0.1 = 75, 75 * 4 = 300, 750-300 = 450, 450 / 750 = 0.6 | relwidth = 0.6

compare_button = Button(text_frame, text='COMPARE', command=ComparingFiles)
compare_button.place(relwidth=0.1, relheight=1, relx=0.75, anchor='n')

finished_dir = 'filled_files_directory'
fill_button = Button(text_frame, text='FILL', command=FinishedDirectory)
fill_button.place(relwidth=0.1, relheight=1, relx=0.85, anchor='n')

uexp_dir = 'uexp_directory'
replace_button = Button(text_frame, bg=replace_button_color, fg=replace_button_text_color, text ='REPLACE', font=root_window_9_font, command=AutomaticReplacer)
replace_button.place(relwidth=0.1, relheight=1, relx=0.95, anchor='n')




initially_disabled_buttons_list = [sort_button, remove_button, source_scroll_up_button, replacement_scroll_up_button, both_sections_up_arrow_button, to_first_source_file_button, to_first_replacement_file_button, 
                        source_scroll_down_button, replacement_scroll_down_button, both_sections_down_arrow_button, to_last_source_file_button, to_last_replacement_file_button, compare_button, fill_button]

for button in initially_disabled_buttons_list:
    button.config(bg='gray', state="disabled", relief="sunken" )
    if button == sort_button or button == remove_button:
        button.config(font=root_window_10_font)
    elif button == fill_button or button == compare_button:
        button.config(font=root_window_9_font)
    else:
        button.config(font=root_window_8_font) #If button font is not being sized properly, check ResizeFont function

    button.bind("<Enter>", HoveringOverWidget)
    button.bind("<Leave>", NotHoveringOverWidget)
        
    pass


enabled_buttons = [add_button, replace_button, extract_button]
for button in enabled_buttons:
    button.bind("<Enter>", HoveringOverWidget) # https://stackoverflow.com/questions/16996432/how-do-i-bind-the-enter-key-to-a-function-in-tkinter
    button.bind("<Leave>", NotHoveringOverWidget) 


root_window_previous_width = root_window_base_width
root_window_previous_height = root_window_base_height_without_menubar
def BindConfigureRootWindow():
    root_window.bind('<Configure>', ResizeFont)
root_window.after(1000, BindConfigureRootWindow) #So the event function doesn't occur immediately when the program starts up.


root_window.mainloop()

#Good to know.   # https://www.kite.com/python/answers/how-to-check-if-a-variable-exists-in-python