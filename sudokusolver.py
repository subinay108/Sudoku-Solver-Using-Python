from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import time
select=''
class box:
    def __init__(self,x,y,coord):
        self.x=x
        self.y=y
        self.correct=1
        self.hover=1
        self.tag=str(coord).replace(' ','')
        self.cv=canvas.create_rectangle(x,y,x+34,y+34,activefill='beige',
        width=0,tag=self.tag)
        self.text=canvas.create_text(x+17,y+17,tag='t'+self.tag,font=('arial',15))
        canvas.tag_bind(self.cv,'<Button-1>',self.click)
        canvas.tag_bind(self.text,'<Button-1>',self.click)
        canvas.tag_bind(self.text,'<Enter>',self.hover_in)
        canvas.tag_bind(self.text,'<Leave>',self.hover_out)
    def click(self,event):
        global select
        if select!='':
            if select.correct:
                self.hover=0
                select.hover=1
                canvas.itemconfig(select.tag,fill='AntiqueWhite3')
                
        if self.correct==1:
            canvas.itemconfig(self.tag,fill='beige')
        select=self
    def hover_in(self,event):
        if self.hover!=0:
            self.hover=1
            canvas.itemconfig(self.tag,fill='beige')
    def hover_out(self,event):
        if self.hover==1:
            canvas.itemconfig(self.tag,fill='AntiqueWhite3')
        
    def right(self,event):
        global select
        if select!='':
            canvas.itemconfig(select,fill='AntiqueWhite3')


def cell_checker(l,j,x,y): 
    if j in l[x]:
        message.configure(state='normal')
        message.insert('end','\nMultiple %d in same row'%j)
        message.see('end')
        message.configure(state='disabled')
        return 1
    for a in range(9):
        if l[a][y]==j:
            message.configure(state='normal')
            message.insert('end','\nMultiple %d in same column'%j)
            message.see('end')
            message.configure(state='disabled')
            return 1
    gx=(x//3)*3
    gy=(y//3)*3
    for p in range(gx,gx+3):
        for q in range(gy,gy+3):
            if l[p][q]==j:
                message.configure(state='normal')
                message.insert('end','\nMultiple %d in same box'%j)
                message.see('end')
                message.configure(state='disabled')
                return 1
    else:
        return 0

tmpt=tmps=''
def call(event,t):
    global select,l
    canvas.itemconfig('middle',text='0')
    canvas.tag_unbind('left','<Button-1>',None)
    canvas.tag_unbind('right','<Button-1>',None)
    if t!='':
        it=int(t)
    else:
        it=0
    if select!='' and t!=canvas.itemcget('t'+select.tag,'text'):
        c=eval(select.tag)
        if it and cell_checker(l,it,c[0],c[1]):
            canvas.itemconfig(select.tag,fill='brown1',activefill='brown1')
            canvas.tag_unbind(select.text,'<Enter>',None)
            canvas.tag_unbind(select.text,'<Leave>',None)
            select.correct=0
        elif select.correct==0:
            canvas.itemconfig(select.tag,fill='beige',activefill='beige')
            canvas.tag_bind(select.text,'<Enter>',select.hover_in)
            canvas.tag_bind(select.text,'<Leave>',select.hover_out)
            select.correct=1
        l[c[0]][c[1]]=it
        canvas.itemconfig('t'+select.tag,text=t,fill='black')

        
def erase_all(event):
    global l,select,box_list
    canvas.itemconfig('middle',text='0')
    canvas.tag_unbind('left','<Button-1>',None)
    canvas.tag_unbind('right','<Button-1>',None)
    if select!='':
        canvas.itemconfig(select.tag,fill='AntiqueWhite3')
        for i in range(9):
            for j in range(9):
                if l[i][j]!=0:
                    l[i][j]=0
                    select=box_list[i][j]
                    select.correct=1
                    select.hover=1
                    canvas.tag_bind(select.text,'<Enter>',select.hover_in)
                    canvas.tag_bind(select.text,'<Leave>',select.hover_out)
                    canvas.itemconfig(select.tag,fill='AntiqueWhite3',activefill='beige')
                    canvas.itemconfig('t'+select.tag,text='')
        select=''
        
def number(x,t):
    a=canvas.create_rectangle(x,350,x+30,380,fill='white')
    b=canvas.create_text(x+15,365,text=t)
    canvas.tag_bind(a,'<Button-1>',lambda event,arg=t:call(event,arg))
    canvas.tag_bind(b,'<Button-1>',lambda event,arg=t:call(event,arg))
    
def unclick(event):
    global select
    if select!='':
        select.hover=0
        canvas.itemconfig(select.tag,fill='AntiqueWhite3')
        select=''
middle=1
def show(event,side):
    global middle,solutions,box_list,l
    if (middle==1 and side=='l')or(middle==len(solutions) and side=='r'):
        return None
    if side=='l':
        middle-=1
    else:
        middle+=1
    l=eval(solutions[middle-1])
    for i in range(9):
        for j in range(9):
            if temp_list[i][j]==0:
                select=box_list[i][j]
                canvas.itemconfig('t'+select.tag,text=str(l[i][j]),fill='blue')
    canvas.itemconfig('middle',text=str(middle))
    
    
    
chk=0
def start():
    global l,select,note,no,inter,solutions,chk,temp_list
    unclick('')
    solutions=[]
    canvas.config(state='disabled')
    if '0' not in str(l):
        message.configure(state='normal')
        message.insert('end','\nAlready solved')
        message.see('end')
        message.configure(state='disabled')
        canvas.config(state='normal')
        return None
    for i in range(9):
            for j in range(9):
                if l[i][j]!=0:
                    select=box_list[i][j]
                    canvas.itemconfig('t'+select.tag,fill='black')
    if str(l).count('0')>=60:
        message.configure(state='normal')
        message.insert('end','\nToo less input')
        message.see('end')
        message.configure(state='disabled')
        canvas.config(state='normal')
        return None
    temp_list=eval(str(l))
    message.configure(state='normal')
    message.insert('end','\nSolving by logic...')
    message.see('end')
    message.configure(state='disabled')
    solve(l)
    if chk==2:
        l=eval(solutions[0])
        if len(solutions)==1:
            chk=1
        else:
            canvas.tag_bind('left','<Button-1>',lambda event,arg='l':show(event,arg))
            canvas.tag_bind('right','<Button-1>',lambda event,arg='r':show(event,arg))
        
    if chk:
        canvas.config(state='normal')
        message.configure(state='normal')
        if chk==1:
            message.insert('end','\nThis Sudoku has unique solution\nSolved')
        else:
            message.insert('end','\nThis Sudoku has total %d solutions\nSolved'%len(solutions))
        message.see('end')
        message.configure(state='disabled')
        for i in range(9):
            for j in range(9):
                if temp_list[i][j]==0:
                    select=box_list[i][j]
                    canvas.itemconfig('t'+select.tag,text=str(l[i][j]),fill='blue')
        canvas.itemconfig('middle',text='1')
        
    else:
        canvas.config(state='normal')
    note={}
    no=0
    inter=0
    chk=0

    
    
l=[[0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0]]

note={}
no=0
inter=0
def create_note(l):
    for x in range(len(l)):
        for y in range(len(l[x])):
            if l[x][y]==0:
                note[str(x)+str(y)]=set()
    
    

def rule1(l):
    global note,inter,group
    for x in range(len(l)):
        for y in range(len(l[x])):
            if l[x][y]==0:
                blank=set()
                for i in range(1,10):
                    column=1
                    for z in range(9):
                        if i == l[z][y]:
                            column=0
                    if column and (i not in l[x]):
                        blank.add(i)
                if inter==0:
                    note[str(x)+str(y)]=note[str(x)+str(y)].union(blank)
                else:
                    note[str(x)+str(y)]=note[str(x)+str(y)].intersection(blank)
    inter=1
                
def rule2(l):
    global note
    for gx in [0,3,6]:
        for gy in [0,3,6]:
            blank=set()
            for i in range(1,10):
                f=0
                for x in range(gx,gx+3):
                    for y in range(gy,gy+3):
                        if l[x][y]==i:
                            f+=1
                            break
                    if f==1:
                        break
                else:
                    blank.add(i)
                    
            for x in range(gx,gx+3):
                for y in range(gy,gy+3):
                    if l[x][y]==0:
                        note[str(x)+str(y)]=note[str(x)+str(y)].intersection(blank)


def rule3(l):
    global note
    group={}
    for i in note:
        blank={}
        px=str(int(i[0])//3)
        py=str(int(i[1])//3)
        group[px+py]=blank
    for i in note:
        gx=str(int(i[0])//3)
        gy=str(int(i[1])//3)
        group[gx+gy][i]=note[i]
    for num in group:
        for i in range(1,10):
            f=0
            x=[]
            y=[]
            for ele in group[num]:
                if i in group[num][ele]:
                    x.append(ele[0])
                    y.append(ele[1])
                    f+=1
            if f==2:
                if x[0]==x[1]:
                    for j in note:
                        g=str(int(j[0])//3)+str(int(j[1])//3)
                        if j[0]==x[0] and num!=g:
                            note[j]=note[j].difference({i})
                if y[0]==y[1]:
                    for j in note:
                        g=str(int(j[0])//3)+str(int(j[1])//3)
                        if j[1]==y[0] and num!=g:
                            note[j]=note[j].difference({i})
                    
            elif f==3:
                if x[0]==x[1]==x[2]:
                    for j in note:
                        g=str(int(j[0])//3)+str(int(j[1])//3)
                        if j[0]==x[0] and num!=g:
                            note[j]=note[j].difference({i})
                if y[0]==y[1]==y[2]:
                    for j in note:
                        g=str(int(j[0])//3)+str(int(j[1])//3)
                        if j[1]==y[0] and num!=g:
                            note[j]=note[j].difference({i})
            
    
    

def check1(l):
    global note
    for i in range(1,10):
        for gx in [0,3,6]:
            for gy in [0,3,6]:
                f=0
                for x in range(gx,gx+3):
                    for y in range(gy,gy+3):
                        if l[x][y]==0 and (i in note[str(x)+str(y)]):
                            f+=1
                        if f==2:
                            break
                    if f==2:
                        break          
                else:
                    f=0
                    for x in range(gx,gx+3):
                        for y in range(gy,gy+3):
                            if l[x][y]==0 and (i in note[str(x)+str(y)]):
                                l[x][y]=i
                                del note[str(x)+str(y)]
                                f=1
                                break
                        if f==1:
                            break

                                
def check2(l):
    global note
    for x in range(len(l)):
        for y in range(len(l[x])):
            if l[x][y]==0 and len(note[str(x)+str(y)])==1:
                l[x][y]= list(note[str(x)+str(y)])[0]
                del note[str(x)+str(y)]


def sudoku_checker(l):            
    for i in range(1,10):
        for x in range(len(l)):
            if l[x].count(i)>1:
                return 0
    for i in range(9):
        s=[]
        for x in range(len(l)):
            if l[x][i] not in s:
                if l[x][i]!=0:
                    s.append(l[x][i])
            else:
                return 0               
    else:
        return 1
    
def input_checker(l,j,x,y):            
    if j in l[x]:
        return 0
    for a in range(9):
        if l[a][y]==j:
            return 0
    gx=(x//3)*3
    gy=(y//3)*3
    for p in range(gx,gx+3):
        for q in range(gy,gy+3):
            if l[p][q]==j:
                return 0
    else:
        return 1


solutions=[]
def back(l):
    global pos,keys,note,solutions,chk
    pos=0
    keys=list(note)
    keys.sort()
    zote=str(note)
    searching(str(l),zote)
    chk=2

def searching(l,zote):
    global keys,pos
    l=eval(l)
    zote=eval(zote)
    i=keys[pos]
    x=int(i[0])
    y=int(i[1])
    for j in zote[i]:
        if input_checker(l,j,x,y):
            l[x][y]=j
            if pos!=(len(keys)-1):                
                pos+=1
                searching(str(l),str(zote))
            else:
                if '0' not in str(l):
                    solutions.append(str(l))
                    #return None
                
    else:
        pos-=1
        return None

def solve(l):
    global no,note,chk
    s=str(l).count('0')
    if s==no:
        if sudoku_checker:
            message.configure(state='normal')
            message.insert('end',"\nIt's too hard\nSolving by Brute Force Searching... ")
            message.see('end')
            message.configure(state='disabled')
            back(l)
            return None
        else:
            message.configure(state='normal')
            message.insert('end','\nThis Sudoku has no solution')
            message.see('end')
            message.configure(state='disabled')
            return None

    if note=={}:
        create_note(l)
    no=str(l).count('0')
    rule1(l)
    rule2(l)
    rule3(l)
    check1(l)
    check2(l)                       
    if '0' in str(l):
        solve(l)
    else:
        chk=1
    return None




root=Tk()
root.title('Sudoku Solver')
root.geometry('450x580+400+10')
canvas=Canvas(root,height=435,width=450,bg='AntiqueWhite3')
canvas.create_rectangle(0,0,500,450,width=0,tag='screen')
canvas.tag_bind('screen','<Button-1>',unclick)
x=67
y=20
for i in range(10):
    if i%3==0:
        w=2
        if i!=0:
            y+=1
    else:
        w=1
    canvas.create_line(66,y,386,y,width=w)
    y+=35
for i in range(10):
    if i%3==0:
        w=2
        if i!=0:
            x+=1
    else:
        w=1
    canvas.create_line(x,19,x,339,width=w)
    x+=35

box_list=[]
y=20
for i in range(9):
    x=67
    if i%3==0:
        y+=1
    empty=[]
    for j in range(9):
        if j%3==0:
            x+=1
        e=box(x,y,(i,j))
        empty.append(e)
        x+=35
    box_list.append(empty)
    y+=35

x=12
for i in range(1,10):
    number(x,str(i))
    x+=35
canvas.create_rectangle(320+7,350,360+12,380,fill='white',tag='erase')
canvas.create_text(340+9,365,text='Erase',tag='erase')
canvas.create_rectangle(365+12,350,421+12,380,fill='white',tag='eraseall')
canvas.create_text(393+12,365,text='Erase All',tag='eraseall')
canvas.tag_bind('erase','<Button-1>',lambda event,arg='':call(event,arg))
canvas.tag_bind('eraseall','<Button-1>',erase_all)

canvas.create_rectangle(185,390,205,420,fill='skyblue',tag='left')
canvas.create_text(195,405,text='<',tag='left')
canvas.create_rectangle(205,390,245,420,fill='white')
canvas.create_text(225,405,text='0',tag='middle')
canvas.create_rectangle(245,390,265,420,fill='skyblue',tag='right')
canvas.create_text(255,405,text='>',tag='right')



message=scrolledtext.ScrolledText(root,height=5,width=52,padx=5)

message.insert('end','Welcome to Sudoku Solver\nEnter your sudoku')
message.see('end')
message.config(state='disabled')
scroll=Scrollbar(root)
cb1=ttk.Button(root,text='Solve',command=start)
canvas.pack()
message.pack()
cb1.pack()
Label(root,text='Created By__Subinay Panda').pack()
root.mainloop()
