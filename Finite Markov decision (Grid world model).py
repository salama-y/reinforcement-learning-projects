import tkinter as tk
import sympy
class GridWorldass:
    def __init__(self, master):
        self.master = master
        
        self.gridworld = [['.', '.', '.', 'G'],
                          ['.', 'X', '.', 'E'],
                          ['S', '.', '.', '.']]
        self.actions={(0,0):('R','D'),
                 (0,1):('R','L'),
                 (0,2):('R','L','D'),
                 #(0,3):('L','D'), terminal reward
                 (1,0):('U','D'),
                 (1,2):('U','R','D'),
                 #(1,3):('U','L','D'), #terminal penalty
                 (2,0):('U','R'),
                 (2,1):('L','R'),
                 (2,2):('U','L','R'),
                 (2,3):('U','L')
        }
        self.rewards={(0,3):1,(1,3):-1}
        self.cell_size = 100
        self.canvas = tk.Canvas(self.master,
                                width=len(self.gridworld[0])*self.cell_size,
                                height=len(self.gridworld)*self.cell_size)
        self.canvas.pack()
        self.draw_gridworld()

    def draw_gridworld(self):
        for i in range(len(self.gridworld)):
            for j in range(len(self.gridworld[0])):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                x2=x0+self.cell_size/2
                y2=y0+self.cell_size/2
                pos=str(i)+","+str(j)
                
                
                if self.gridworld[i][j] == 'S':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
                elif self.gridworld[i][j] == 'X':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
                elif self.gridworld[i][j] == 'G':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='green')
                elif self.gridworld[i][j] == 'E':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='red')
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
                self.canvas.create_text(x2,y2,text=pos,fill="black",font=('Helvetica 11'))
     
    def state_value_function(self,Discount_factor):
        v00,v01,v02,v10,v12,v20,v21,v22,v23=sympy.symbols('v00 v01 v02 v10 v12 v20 v21 v22 v23')
        v13=0
        v03=0 #terminal state
        eq1=0.5*(0+Discount_factor*v00)+0.25*(0+Discount_factor*v01)+0.25*(0+Discount_factor*v10)-v00
        eq2=0.5*(0+Discount_factor*v01)+0.25*(0+Discount_factor*v02)+0.25*(0+Discount_factor*v00)-v01
        eq3=0.25*(0+Discount_factor*v02)+0.25*(1+Discount_factor*v03)+0.25*(0+Discount_factor*v01)+0.25*(0+Discount_factor*v12)-v02
        
        eq4=0.5*(0+Discount_factor*v10)+0.25*(0+Discount_factor*v00)+0.25*(0+Discount_factor*v20)-v10
        eq5=0.25*(0+Discount_factor*v12)+0.25*(0+Discount_factor*v02)+0.25*(-1+Discount_factor*v13)+0.25*(0+Discount_factor*v22)-v12
        
        eq6=0.5*(0+Discount_factor*v20)+0.25*(0+Discount_factor*v10)+0.25*(0+Discount_factor*v21)-v20
        eq7=0.5*(0+Discount_factor*v21)+0.25*(0+Discount_factor*v22)+0.25*(0+Discount_factor*v20)-v21
        eq8=0.25*(0+Discount_factor*v22)+0.25*(0+Discount_factor*v21)+0.25*(0+Discount_factor*v12)+0.25*(0+Discount_factor*v23)-v22
        eq9=0.5*(0+Discount_factor*v23)+0.25*(-1+Discount_factor*v13)+0.25*(0+Discount_factor*v22)-v23
        sol= sympy.solve((eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9),(v00,v01,v02,v03,v10,v12,v13,v20,v21,v22,v23))
        print(sol)
        value_state_sol=[[sol[v00],sol[v01],sol[v02],v03],
                        [sol[v10],0,sol[v12],v13],
                        [sol[v20],sol[v21],sol[v22],sol[v23]]]
        return value_state_sol
    def step(self,i,j,action):
        if(action== 'U'):
            return (i-1,j)
        elif(action=='D'):
            return (i+1,j)
        elif(action=='L'):
            return (i,j-1)
        elif(action=='R'):
            return (i,j+1)
        
    def action_value_function(self,discount_factor,sol):
        action_value_matrix={}
        for i in range(len(sol)):
            for j in range(len(sol[i])):
                if((i,j) in self.actions):
                    URDL=list((0,0,0,0)) # tuple of action value for each state Up,Right,Down,Left
                    if('U' in self.actions[(i,j)]):
                        
                        (x,y)=self.step(i,j,'U')
                        if((x,y) in self.rewards):
                            #action_value_matrix.update({(i,j):self.rewards[(x,y)]+discount_factor*sol[i][j]})
                            URDL[0]=(self.rewards[(x,y)]+discount_factor*sol[x][y])
                        else:
                            URDL[0]=0+discount_factor*sol[x][y]
                    else:
                         URDL[0]= (0+discount_factor*sol[i][j])
                    if('R' in self.actions[(i,j)]):
                        (x,y)=self.step(i,j,'R')
                        if((x,y) in self.rewards):
                            #action_value_matrix.update({(i,j):self.rewards[(x,y)]+discount_factor*sol[i][j]})
                            URDL[1]=(self.rewards[(x,y)]+discount_factor*sol[x][y])
                        else:
                            URDL[1]=0+discount_factor*sol[x][y]
                    else:
                         URDL[1] =(0+discount_factor*sol[i][j])   
                    if('D' in self.actions[(i,j)]):
                        
                        (x,y)=self.step(i,j,'D')
                        if((x,y) in self.rewards):
                            #action_value_matrix.update({(i,j):self.rewards[(x,y)]+discount_factor*sol[i][j]})
                            URDL[2] = (self.rewards[(x,y)]+discount_factor*sol[x][y])
                        else:
                            URDL[2]= (0+discount_factor*sol[x][y])
                    else:
                         URDL[2] =(0+discount_factor*sol[i][j])
                    if('L' in self.actions[(i,j)]):
                        
                        (x,y)=self.step(i,j,'L')
                        if((x,y) in self.rewards):
                            #action_value_matrix.update({(i,j):self.rewards[(x,y)]+discount_factor*sol[i][j]})
                            URDL[3] = (self.rewards[(x,y)]+discount_factor*sol[x][y])
                        else:
                            URDL[3]= (0+discount_factor*sol[x][y])
                    else:
                         URDL[3] =(0+discount_factor*sol[i][j])
                    URDL=tuple(URDL)
                    action_value_matrix.update({(i,j):URDL})
                else:
                    URDL=tuple(URDL)
                    action_value_matrix.update({(i,j):("NULL")}) #no actions to be made( terminal state or wall)
        return action_value_matrix         
                


                    



    

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Small Gridworld")
    # Create the gridworld GUI
    gridworld_gui = GridWorldass(root)
    sol=gridworld_gui.state_value_function(0.9)
    action_value=gridworld_gui.action_value_function(0.9,sol)
    print(action_value) 
    # Start the main event loop
    root.mainloop()
