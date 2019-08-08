'''This program 'folders.py' creates folders for different classes on the
desktop. To run the program, launch from the command line with the command
'pyton folders.py' with no arguments. The program will prompt and ask how
many classes to make folders for and then ask for the names of the folders.
The program creates one folder for each class, and then within each class
folder it creates folders for ten sets and an additional folder for 
lecture slides. This program should be placed in the desktop of the
computer. If this program is called and a folder with the requested name
already exists, the program will print a warning message and not override
the folder'''

import os

def directory_names():
    '''This function loops asking the user for the name of directories
    to make'''
    
    num_classes = int(input("Enter number of classes: "))
    class_list = num_classes * ['']
    for i in range(num_classes):
        #loop asking for name of courses
        course = input("Enter class #%d name: " %(i+1))
        #add course name to list
        class_list[i] = course
        
    return class_list

def create_dirs(class_list):
    '''This function creates the directories from the list of
    classes. Each class has its own directory, located on the desktop.'''
    
    dpath = '/Users/Timothy/Desktop/'
    
    for course in class_list:
        fpath = os.path.join(dpath, course)
        if not os.path.isdir(fpath):
            os.makedirs(fpath)
            create_subdir(fpath)
        else:
            print("Directory already exists!")
            print(class_list[i])
            
    return

def create_subdir(classpath):
    '''This function creates ten folders for sets, and one folder for
    lecture slides inside of a directory for a single class.'''
    
    for i in range(10):
        fpath = os.path.join(classpath, "Set%d" %(i+1))
        if not os.path.isdir(fpath):
            os.makedirs(fpath)
    lecpath = os.path.join(classpath, "LectureSlides")
    if not os.path.isdir(lecpath):
        os.makedirs(lecpath)
        
    return

if __name__ == "__main__":
    class_list = directory_names()
    create_dirs(class_list)
    exit()