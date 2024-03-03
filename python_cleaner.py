import os
import PySimpleGUI as sg # pip install pysimplegui
import time
# If you want to send to trashcan insted
# import send2trash / 
# Pyinstaller if you want a .exe file / pip install pyinstaller

def get_downloads_dir():

    # Change the current directory to the download folder
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    os.chdir(download_dir)
    return os.listdir(download_dir)

def sort_downloads_by_date(date):
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    os.chdir(download_dir)

    all_files = filter(os.path.isfile, os.listdir(download_dir))
    all_files = [os.path.join(download_dir, f) for f in all_files]

    now=time.time()
    option_date = now - date
    recent_files=[i for i in all_files if os.path.getmtime(i) >option_date]
    recent_files.sort(key=os.path.getmtime, reverse=True)  
    return recent_files


def main_window():
    layout = [[sg.Text("Hello and welcome!")],
       [sg.Button("Show Downloads")],
       [sg.Button("Organise downloads by last seven days")],
       [sg.Button("Organise downloads by last month")],
       [sg.Button('Browse folder to clean')]]    
    window = sg.Window('Disk cleaner', layout)

    while True:
        event,values= window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event =="Show Downloads":
            window.close()
            show_all_downloads()
        elif event =="Organise downloads by last seven days": 
            window.close()
            one_week = 60*60*24*7
            list_downloads(one_week)
        elif event =="Organise downloads by last month":  
            window.close()
            one_month = 60*60*24*30
            list_downloads(one_month)
        elif event == 'Browse folder to clean':
            window.close()
            browse_dir_window()

    window.close()

#Option 1
def show_all_downloads():
            downloads =get_downloads_dir()
            download_layout = [[sg.Text(download)] for download in downloads]

            scrollable_download_layout=[[sg.Column(download_layout,scrollable=True,vertical_scroll_only=True,size=(450,450))]]
            scrollable_download_layout.append([sg.Button("Leave")])

            download_window = sg.Window('Your downloads', scrollable_download_layout,size=(500,500))

            # Event loop for the new window
            while True:
                event, values = download_window.read()
                if event == sg.WINDOW_CLOSED or event == "Leave":
                    download_window.close()
                    main_window()
                    break
            download_window.close()

#Option 2
def list_downloads(date):
 
        sorted_files=sort_downloads_by_date(date)
        download_dir = get_downloads_dir()
        
        download_layout = [[sg.Text(download)] for download in sorted_files]
        scrollable_download_layout=[[sg.Column(download_layout,scrollable=True,vertical_scroll_only=True,size=(450,450))]]
        scrollable_download_layout.append([sg.Button("Leave"), sg.Button("Delete files")])
        
        download_window = sg.Window('Files', scrollable_download_layout,size=(500,500))
        
        while True:
                event, values = download_window.read()
                if event == sg.WINDOW_CLOSED or event == "Leave":
                    download_window.close()
                    main_window()
                    break
                elif event == "Delete files":
                    download_window.close()
                    confirm_operation(delete_files,sorted_files,download_dir)
                    break
        download_window.close()

def browse_dir_window():

    layout = [[sg.Input(), sg.FolderBrowse(key='-IN-')],
          [sg.Button('Show Contents')]]    
    window = sg.Window('Folder cleaner', layout)

    while True:
        event,values=window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Show Contents":
            folder_path = values['-IN-']
            print(f'Folder path: {folder_path}')
            files=os.listdir(folder_path)
            window.close()
            list_browser_files(files,folder_path)
        window.close()


def list_browser_files(text_files,folder_path):

    browser_layout = [[sg.Text(file)] for file in text_files]
    scrollable_browser_layout=[[sg.Column(browser_layout,scrollable=True,vertical_scroll_only=True,size=(450,450))]]
    scrollable_browser_layout.append([sg.Button("Return"), sg.Button("Delete empty folders"),sg.Button("Delete empty folders and txt files")])
    browse_window = sg.Window('Files', scrollable_browser_layout,size=(500,500))
    while True:
        event,values=browse_window.read()
        if event==sg.WINDOW_CLOSED:
            break
        elif event=="Leave":
            browse_window.close()
            main_window()

        elif event=="Delete empty folders":
            browse_window.close()
            confirm_operation(delete_empty_folders,text_files,folder_path)
        elif event=="Delete empty folders and txt files":
             browse_window.close()
             confirm_operation(delete_folders_and_text,text_files,folder_path)
        browse_window.close()

def confirm_operation(operation, text_files, folder_path):
    layout = [[sg.Text("Are you sure about this operation?")],
              [sg.Button("Yes, proceed")],
              [sg.Button("No, wait a moment")]]
    window = sg.Window('Confirmation', layout)     

    while True:
        event, values = window.read()
        if event == "Yes, proceed":
            window.close()
            operation(text_files, folder_path)
            break
        elif event == "No, wait a moment":
            window.close()
            main_window()
            break
    

def delete_files(files,folder_path):
    amount_removed=0
    folder_path= os.path.join(os.path.expanduser('~'), 'Downloads')
    try:
        for i in files:
            full_path=os.path.join(folder_path,i)
            os.remove(full_path)
            amount_removed+=1
        success_operation(amount_removed)
    except (OSError,FileNotFoundError,PermissionError) as e:
        return f"Something went wrong: {str(e)}"


def delete_empty_folders(files,folder_path):
    amount_removed=0
    try:
        for i in files:
            full_path=os.path.join(folder_path,i)

            if os.path.isdir(full_path):
                if not os.listdir(full_path):
                    # os.chmod(full_path, 0o777) gives full access to remove/write/read files. 
                    os.rmdir(full_path)
                    amount_removed+=1
        success_operation(amount_removed)
    except (OSError,FileNotFoundError,PermissionError) as e:
        return f"Something went wrong: {str(e)}"

def delete_folders_and_text(files,folder_path):
    amount_of_files=0
    try: 
        for i in files:
            full_path=os.path.join(folder_path,i)
            if os.path.isfile(full_path):
                if full_path.endswith(".txt"):
                    # send2trash.send2trash(full_path)
                    os.remove(full_path)
                    amount_of_files+=1 
            elif os.path.isdir(full_path):
                if not os.listdir(full_path):
                    os.rmdir(full_path)
                    amount_of_files+=1 
                #Checks for txt files inside folders and deletes the folder if its empty afterwards
                else:
                    for root,dirs,files in os.walk(full_path):
                        for file in files:
                            if file.endswith(".txt"):
                            # send2trash.send2trash(full_path)
                                os.remove(os.path.join(root,file))
                                amount_of_files+=1 
                                if os.path.isdir(root):
                                    if not os.listdir(root):
                                        os.rmdir(root)
                                        amount_of_files+=1 

        success_operation(amount_of_files)
    except (OSError, FileNotFoundError, PermissionError) as e:     
        return f"Something went wrong: {str(e)}"

def success_operation(amount):
    layout = [[sg.Text(f"Success! {amount} of files removed!")],
       [sg.Button("Ok!")]]
    window = sg.Window('Window Title', layout)     
    
    while True:
        event,values=window.read()
        if event=="Ok!" or event==sg.WINDOW_CLOSED:
            window.close()     
            break

def start():
     main_window()

start()