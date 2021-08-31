import face_recognition as fr
import cv2 
from tkinter import *
from tkinter.filedialog import  askopenfilename
import os
import datetime
from datetime import date
import numpy
import pyautogui
import time
import pandas as pd
import csv

def btnf2():
    def createFolder(directory): 
        try: 
            if not os.path.exists(directory): 
                os.makedirs(directory) 
        except OSError: 
            print ('Error: Creating directory. ' + directory) 
    createFolder('./tempu/')# Creates a folder in the current directory called data
    folder_name = 'tempu'
    #folder_name = 'temp'
    global total_students
    total_students = ent1.get()
    print(total_students)
    global grid_no
    grid_no = ent2.get()
    print(grid_no)
    total_students = pd.to_numeric(total_students)
    grid_no = pd.to_numeric(grid_no)
    nameList = []
    #To create a folder and save all the screenshot 
    attendent = []
    def printList():
        df=pd.read_csv('MarkAttendance.csv')
        letters = df.Name.to_list()
        print(letters)
        

    def put_Attendance(name):
        with open('MarkAttendance.csv','r+') as f:
                myDataList = f.readlines()
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    #attendent.append(name)
                    now = datetime.datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f' \n{name},{dtString}')
                    
        printList()

    def create_frame(location,label,target_image):
        top,right,bottom,left = location
        #print(label)
        name = label.split('.')[0].upper()
        put_Attendance(name)
        cv2.rectangle(target_image,(left,top),(right,bottom),(255,0,0),2)
        cv2.rectangle(target_image,(left,bottom+20),(right,bottom),(255,0,0),cv2.FILLED)
        cv2.putText(target_image,label,(left+3,bottom+14),cv2.FONT_HERSHEY_DUPLEX,0.4,(255,255,255),1)
        #print(target_image)



    def find_target_face(target_image,target_encoding):
        face_location = fr.face_locations(target_image)
        for person in encode_faces('known/'):
            encoded_face = person[0]
            filename = person[1]
            #print(filename) 
            is_target_face = fr.compare_faces(encoded_face,target_encoding,tolerance = 0.55)
            #print(f'{is_target_face} {filename}')
            #faceDis = fr.face_distance(encodeListKnown,encodeFace)
            #matchIndex = np.argmin(faceDis)
            
            if face_location:
                face_number = 0
                for location in face_location:
                    if is_target_face[face_number]:
                        label = filename
                        #print("label:"+label)
                        create_frame(location,label,target_image)
                        #name  = classNames[face_number].upper()
                        #print(name)
                    face_number += 1 
                    
    def render_image(target_image):
        rgb_img = cv2.cvtColor(target_image,cv2.COLOR_BGR2RGB)
        cv2.imshow('Face Reccognition',rgb_img)
        cv2.waitKey(0)
     

    def call_by_folder():
        #for i in range(totalss):
            target_image = fr.load_image_file(folder_name+r'/srn_shot'+str(i)+'.png')
            #target_image = fr.load_image_file("image6.png") 
            target_encoding = fr.face_encodings(target_image)
            find_target_face(target_image,target_encoding)
            render_image(target_image)

    #print(target_encoding)
    def encode_faces(folder):
        list_people_encoding = []
        for filename in os.listdir(folder):
            known_image = fr.load_image_file(f'{folder}{filename}')
            know_encoding = fr.face_encodings(known_image)[0]
            
            list_people_encoding.append((know_encoding,filename))
            
        return list_people_encoding
        
      


    def take_Shot(i):
        
        #delete_Shot()
        take_Time()

        myScreenshot = pyautogui.screenshot()
        temp_string = folder_name+r'/srn_shot'+str(i)+'.png'
        myScreenshot.save(temp_string)
        call_by_folder()


    def delete_Shot(i):
        if os.path.exists(folder_name+"/srn_shot"+str(i)+".png"):
            os.remove(folder_name+"/srn_shot"+str(i)+".png")
            
    def take_Time():
        time.sleep(5)

    totalss = total_students//grid_no
    print(totalss)
    for i in range(totalss):
        take_Shot(i)
          


    path = 'known'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0].upper())
    print(classNames)
    Tk().withdraw()
    #path1 = 'image3.png'
    #load_image = cv2.imread("image3.png", cv2.IMREAD_COLOR)

    #load_image = cv2.imread("image3.png", cv2.IMREAD_COLOR)


     
    def putAttendance():
        f1 = pd.read_csv('MarkAttendance.csv')
        f2 = pd.read_csv('Students.csv')
        x = date.today()
        for entry in f1['Name']:

            index =f2[f2['Name']==entry].index
            #print(index)
            f2.loc[index,x] = '1'
            f2.to_csv('Students.csv',index = False)
            index = next(iter(index),'no match')   
            
     

    def reset():
        os.remove('MarkAttendance.csv')
        with open('MarkAttendance.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Time"]) 
        for i in range(totalss):
            delete_Shot(i)
        print("data removed")
        
    putAttendance()
    print(attendent)
#put_Attendance()
    reset()
    ent1.delete(0,END)
    ent2.delete(0,END)

'''
def btnf1():
    b1win = tkr.Tk()
    b1win.title('Add new student')
    b1win.geometry('400x400+100+120')
    mylabel2=tkr.Label(b1win,text='second window',fg='green').pack()
'''

import tkinter as tkr
root = tkr.Tk()
root.title('Attendence:-')
root.geometry('400x500+400+150')
mylabel1=tkr.Label(text='Online Attendence',fg='Blue').pack()
lbl1 = Label(root,text = "Number of \n students")
lbl1.pack(pady = 20)
ent1 = Entry(root,bd = 5)
ent1.pack(pady = 5)

lbl2 = Label(root,text = "Number of \n grids")
lbl2.pack(pady = 20)
ent2 = Entry(root,bd = 5)
ent2.pack(pady = 5)
#Btn1=tkr.Button(text='New class',fg='White',bg='Black',command=btnf1).pack()
Btn2=tkr.Button(text='To record and put attendance:',fg='Blue',bg='White',command=btnf2).pack(pady = 10)               
#def remove_folder():
root.mainloop()  
    
#find_target_face()
#render_image()

#remove_folder()
