from Vocabulary import Vocabulary
import tkinter,random
import time
import pyperclip,time
from pynput import keyboard
import multiprocessing as mp
from multiprocessing import Queue


class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        f = open("vocabulary.txt","r")
        f = f.read()
        self.quiz = f.split("\n")
        self.modeFlag = 0
        self.flag = 0
        self.r = 0
        self.geometry("800x400")
        self.title("GUI")
        self.readprofile(False,False)
        self.set()
        self.queue = Queue()
        self.myButton = tkinter.Button(self, text="抽考",height=1,width=10,command=self.test)
        self.myButton.place(x = 600, y = 200)

        self.myButton2 = tkinter.Button(self, text="ON",height=1,width=10,command=self.mode)
        self.myButton2.place(x = 700, y = 200)

        self.myButton3 = tkinter.Button(self, text="Search",height=1,width=10,command=self.search)
        self.myButton3.place(x = 600, y = 150)
        self.myButton3["state"] = "disable"

        self.myButton4 = tkinter.Button(self, text="Save",height=1,width=10,command=self.save)
        self.myButton4.place(x = 700, y = 150)

        self.myButton5 = tkinter.Button(self, text="Play",height=1,width=10,command=self.play)
        self.myButton5.place(x = 650, y = 100)
        
        self.word = tkinter.StringVar()
        self.input = tkinter.Entry(textvariable=self.word,bd=10).place(x = 600, y = 50)#.grid(column=2,row=1)

        self.v = Vocabulary.Vocabulary("")

    def search(self):
        self.v.word = self.word.get()
        self.v.lookUp()
        self.text.delete('1.0','end')
        self.v.insert(self.text)

    def save(self):
        self.v.save()

    def set(self):
        self.text = tkinter.Text(self,width=80,height=27)
        self.text.place(x=10,y=10)#.grid(row=3,column=1,padx=10,pady=10)
        self.text.tag_config('tag_1',font=('Arial',12))
        self.text.tag_config('tag_2',font=('Arial',18))
    
    def run(self):
        self.runProcess()
        self.mainloop()
    
    def runProcess(self):
        self.p1 = mp.Process(target=monitoring, args=(self.queue, ), daemon=True)
        self.p1.start()

    def stopProcess(self):
        self.p1.terminate()
        self.p1.join()
        
    def mode(self):
        if self.modeFlag == 0:
            self.stopProcess()
            self.modeFlag = 1
            self.myButton2['text'] = "OFF"
            self.myButton3["state"] = "normal"
              
        else:
            self.runProcess()
            self.modeFlag = 0
            self.myButton2['text'] = "ON"
            self.myButton3["state"] = "disable"
                   
    def change(self):
        if self.queue.empty():
            self.after(500,self.change)
        else:
            self.v.word = self.queue.get()
            self.v.lookUp()
            self.text.delete('1.0','end')
            self.v.insert(self.text)
            self.after(500,self.change)
    
    def test(self):
        if self.flag == 0:
            self.flag = 1
            self.text.delete('1.0','end')
            self.r = int(random.random()*(len(self.quiz)-1))
            self.text.insert('insert',self.quiz[self.r],"tag_2")
            self.myButton['text'] = "解答"
        else:
            self.flag = 0
            self.text.delete('1.0','end')
            self.v.word = self.quiz[self.r]
            self.v.lookUp()
            self.v.insert(self.text)
            self.myButton['text'] = "抽考"
    def play(self):
        self.v.playSound()
        
def monitoring(queue):
         
    ctr = keyboard.Controller()
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.KeyCode.from_char("z") and isinstance(event, keyboard.Events.Press):
                
                ctr.press(keyboard.Key.ctrl)
                ctr.press('c')
                ctr.release(keyboard.Key.ctrl)
                ctr.release('c')
                time.sleep(0.5)          
                v = pyperclip.paste()
                v = v.replace("-\r\n","")
                queue.put(v)
                
            elif event.key == keyboard.KeyCode.from_char("q"):
                break
            elif event.key == keyboard.KeyCode.from_char("s") and isinstance(event, keyboard.Events.Press):
                v = pyperclip.paste()
                v = Vocabulary.Vocabulary(v)
                v.save()