"""  
  Project : To build an IR model based on a vector space model                  
  Course No : CS F469 Information Retrieval

  GUI for the Vector space model implementation
    
"""

from tkinter import *
from load_pickle import *
import tkinter.messagebox
import speech_recognition as sr
import os

def makeListbox():
	'''
		function to display results on the screen
	'''
	#to clear all items of the last query	
	items.clear()	
	
	#get Text query entered in the Textbox
	query=queryText.get()	
	
	#throw an error if no text is entered
	if query=="":	
		tkinter.messagebox.showinfo('PyTunes', 'Input Missing :/')
		listbox.delete(0, END)
		return
	
	#place listbox on the grid
	listbox.grid(row=20,column=20)	
	
	#delete all existing items on the screen
	listbox.delete(0, END)
	
	#get all song IDs matching the input query		
	songs=input_query(query)	
	
	#append all the song IDs and their names as tuples to a list 
	for x in songs:
		items.append((x,answer[str(x)][1]))	
	
	#clear the song IDs
	songs.clear()	
	
	#insert all these items in the listbox on the GUI
	for x,item in items:
	    listbox.insert(END, item)	
	
	#place the getLyrics button on the screen
	getButton.grid(row=80,column=20,padx=10,pady=10,sticky=S)	
	return

def saveLyrics(x):
	'''
		To save lyrics to a file in a default directory
	'''
	path= os.getcwd()+os.path.sep+"Saved Songs"+os.path.sep
	if not os.path.exists(path):
		os.makedirs(path)
	
	with open(path+answer[str(x)][1]+".txt","w+") as f:
		try:
			f.write("Song:"+answer[str(x)][1]+"\n")
			f.write("Singer:"+answer[str(x)][0]+"\n\n")
			f.write(answer[str(x)][2])
			f.close()
			
			#message pop-up after successful file write
			tkinter.messagebox.showinfo('PyTunes', 'Saved Successfully :)')
		except:
			tkinter.messagebox.showinfo('PyTunes', 'Error :/')
	return

def getDetails():	
	'''
		GUI for displaying the lyrics of the selected song
	'''
	#gets the selected item
	item=(list)(listbox.curselection())[0]	
	x,name=items[item]
	
	#creates a new window to display lyrics	
	popUp=Tk()	
	popUp.title(answer[str(x)][1])
	
	#menu to have an option to save lyrics or quit
	menu1=Menu(popUp)	
	popUp.config(menu=menu1)
	
	#cascading submenu
	submenu=Menu(menu1)	
	menu1.add_cascade(label="Options",menu=submenu)
	
	#option to save lyrics
	submenu.add_command(label="Save Lyrics",command=lambda:saveLyrics(x))	
	
	#option to quit and close the current window
	submenu.add_command(label="Quit",command=popUp.destroy)			
	
	#text area to insert lyrics
	box=Text(popUp)	
	box.pack()
	box.insert(INSERT,answer[str(x)][2])

	#status bar to show the singer's name
	status = Label(popUp, text="Singer:"+answer[str(x)][0], bd=1, relief=SUNKEN, anchor=W)	
	status.pack(side=BOTTOM, fill=X,padx=5)
	
	popUp.mainloop()
	return

 
def speechInput():	
	'''
		To take input from microphone
	'''
	start=time.time()
	r=sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening Now:")
		audio = r.listen(source)
		if time.time()-start >5:
			print("Seems like I am not a good ear after all!")
	try:
		print(r.recognize_google(audio))
		inp=input("If you meant this, please press Y else N\t")
		if inp.lower() =='y':
			query =  r.recognize_google(audio)
		else:
			query = input("Sorry! Can you please enter the query.Seems like I am having a bad day!\n")
	except sr.UnknownValueError:
		query = input("Sorry.Can you please enter the query.Seems like I am having a bad day!\n")
	except sr.RequestError as e:
		query = input("Sorry!! Can you please enter the query.Seems like I am having a bad day!\n")
	return
	

#main window
root=Tk()
root.title("PyTunes")	

items=[]

#main window frame
frame=Frame(root,width=480,height=360)	
frame.pack()

queryLabel=Label(frame,text="Enter Query:")			
queryLabel.grid(row=10,column=10,padx=10,pady=20,sticky=W)

#textbox to enter the query
queryText=Entry(frame)						
queryText.grid(row=10,column=20,padx=10,pady=10,sticky=E)

searchButton=Button(frame,text="Search",fg="black",command=makeListbox)
searchButton.grid(row=10,column=50,padx=10,pady=10,sticky=E)

'''
singButton=Button(frame,text="Speech Input",fg="black",command=speechInput)
singButton.grid(row=10,column=80,padx=10,pady=10,sticky=E)
'''

#listbox to show results
listbox = Listbox(frame) 							
listbox.grid(row=20,column=20)

#button to get lyrics of selected song	
getButton=Button(frame,text="Get Song's Lyrics",fg="black",command=getDetails)
getButton.grid(row=80,column=20,padx=10,pady=10,sticky=S)

root.mainloop()
