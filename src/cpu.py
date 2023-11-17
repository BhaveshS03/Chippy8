import pygame
import os
from random import randint

class cpuChip8:
    def __init__(self,size,mem,window):
        self.show = window
        self.pc=0x200
        self.V=bytearray([0]*16)
        self.i=0
        self.stack=[]
        #self.sp=0
        self.size=size
        self.mem=mem
        self.dt=0
        self.st=0
        self.keys=[]
        self.gfx=bytearray([0]*4096)
        self.keys=[False]*16
        pygame.mixer.init()
        self.beep=pygame.mixer.Sound("src/beep-02.mp3")

    def updatedelay(self):
        if self.dt>0:
            self.dt-=1

    def updatesound(self):
        if self.st>0:
            self.st-=1
        if self.st==1:
            self.beep.play()
            pass
    
    def debug_display(self):
        for y in range(32):
            for x in range(64):
                if self.gfx[x+y*64]==0:
                    print(" ",end="")
                else:
                    print("*",end="")
            print()
        os.system("cls")

    def interactions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                #''''''''''''''''   ''''''''
                #   4   5   6   7   1 2 3 c
                #   r   t   y   u   4 5 6 d
                #   f   g   h   j   7 8 9 e
                #   v   b   n   m   a 0 b f
                #''''''''''''''''   ''''''''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.keys[0]=True
                elif event.key == pygame.K_4:
                   self.keys[1]=True
                elif event.key == pygame.K_5:
                   self.keys[2]=True
                elif event.key == pygame.K_6:
                   self.keys[3]=True
                elif event.key == pygame.K_r:
                   self.keys[4]=True
                elif event.key == pygame.K_t:
                   self.keys[5]=True
                elif event.key == pygame.K_y:
                   self.keys[6]=True
                elif event.key == pygame.K_f:
                   self.keys[7]=True
                elif event.key == pygame.K_g:
                   self.keys[8]=True
                elif event.key == pygame.K_h:
                   self.keys[9]=True
                elif event.key == pygame.K_v:
                   self.keys[10]=True
                elif event.key == pygame.K_n:
                   self.keys[11]=True
                elif event.key == pygame.K_7:
                   self.keys[12]=True
                elif event.key == pygame.K_u:
                   self.keys[13]=True
                elif event.key == pygame.K_j:
                   self.keys[14]=True
                elif event.key == pygame.K_m:
                   self.keys[15]=True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    self.keys[0]=False
                elif event.key == pygame.K_4:
                   self.keys[1]=False
                elif event.key == pygame.K_5:
                   self.keys[2]=False
                elif event.key == pygame.K_6:
                   self.keys[3]=False
                elif event.key == pygame.K_r:
                   self.keys[4]=False
                elif event.key == pygame.K_t:
                   self.keys[5]=False
                elif event.key == pygame.K_y:
                   self.keys[6]=False
                elif event.key == pygame.K_f:
                   self.keys[7]=False
                elif event.key == pygame.K_g:
                   self.keys[8]=False
                elif event.key == pygame.K_h:
                   self.keys[9]=False
                elif event.key == pygame.K_v:
                   self.keys[10]=False
                elif event.key == pygame.K_n:
                   self.keys[11]=False
                elif event.key == pygame.K_7:
                   self.keys[12]=False
                elif event.key == pygame.K_u:
                   self.keys[13]=False
                elif event.key == pygame.K_j:
                   self.keys[14]=False
                elif event.key == pygame.K_m:
                   self.keys[15]=False

    def cycle(self):
        while self.pc < self.size+0x200:
            self.interactions()
            self.op = (self.mem[self.pc]<<8 | self.mem[self.pc+1])
            self.interpreter()
            self.pc+=2
            #self.debug_display()
            self.show.draw(self.gfx)
            self.updatedelay()
            self.updatesound()
            
    def interpreter(self):
        self.case=(self.op&0xf000)>>12
        self.X=(self.op&0x0f00)>>8
        self.Y=(self.op&0x00f0)>>4
        self.N=(self.op&0x000f)
        self.NN=(self.op&0x00ff)
        self.NNN=(self.op&0x0fff)
        
        if self.case==0x0:
            if self.NN == 0xe0:
                self.gfx=[0]*4096
                self.show.draw(self.gfx)
                #print("Screen Cleared")

            elif self.NN==0xee:
                self.pc=self.stack.pop()

        elif self.case==0x1:
            self.pc=self.NNN
            self.pc-=2

        elif self.case==0x2:
            self.stack.append(self.pc)
            self.pc=self.NNN
            self.pc-=2

        elif self.case==0x3:
            if self.V[self.X] == self.NN:
                self.pc+=2
        
        elif self.case==0x4:
            if self.V[self.X] != self.NN:
                self.pc+=2

        elif self.case==0x5:
            if self.V[self.X] == self.V[self.Y]:
                self.pc+=2

        elif self.case==0x6:
            self.V[self.X] = self.NN

        elif self.case==0x7:
            self.V[self.X] = (self.NN + self.V[self.X]) & 0x0ff

        elif self.case==0x8:

            if self.N==0x0:
                self.V[self.X] = self.V[self.Y]
            elif self.N==0x1:
                self.V[self.X] = (self.V[self.X] | self.V[self.Y])
            elif self.N==0x2:
                self.V[self.X] = (self.V[self.X] & self.V[self.Y])
            elif self.N==0x3:
                self.V[self.X] = (self.V[self.X] ^ self.V[self.Y])
            elif self.N==0x4:
                results = self.V[self.X] + self.V[self.Y]
                if results > 0xff:
                    self.V[self.X]=results-256
                    self.V[0xf]=1
                else:
                    self.V[self.X]=results
                    self.V[0xf]=0

            elif self.N==0x5:
                #VX-VY
                #dont forgot to borrow if result is negative
                result = self.V[self.X] - self.V[self.Y]
                if result>0:
                    self.V[self.X]=result&0xff
                    self.V[0xf]=1
                else:
                    self.V[self.X]=(result+256)&0xff
                    self.V[0xf]=0

            elif self.N==0x6:
                #self.V[0xf]=(self.V[self.X]&0b000001)
                #self.V[self.X]//=2
                self.v[0xf] = self.v[self.X ] & 0b1
                self.V[self.X] = self.V[self.X] >> 1


            elif self.N==0x7:
                #VY-VX
                #dont forgot to borrow if result is negative
                result=self.V[self.Y] - self.V[self.X]
                if result>0:
                    self.V[self.X]=result
                    self.V[0xf]=1
                else:
                    self.V[self.X]=result+256
                    self.V[0xf]=0
            elif self.N==0xe:
                #self.V[0xf]=(self.V[self.X] & 0b10000000)>>7
                #if (self.V[self.X]*2) > 0xff:
                #    self.V[self.X]=self.V[self.X]*2-256
                #else:
                 #   self.V[self.X]*=2
                self.V[0xf] = self.V & 0x80
                self.v[self.X] = self.V[self.X] << 1
 

        elif self.case==0x9:
            if self.V[self.X]!= self.V[self.Y]:
                self.pc+=2

        elif self.case==0xa:
            self.i=self.NNN

        elif self.case==0xb:
            self.pc = self.NNN+self.V[0x0]
            self.pc-=2

        elif self.case==0xc:
            self.V[self.X]= (randint(0,256) & self.NN)

        elif self.case==0xd:
            x=self.V[self.X]%64
            y=self.V[self.Y]%32
            self.V[0xf]=0

            for yline in range(self.N):
                sprite=self.mem[self.i+yline]
                for xline in range(8):
                    if sprite & (0x80>>xline)!=0:
                        idx=(x+xline)+(y+yline)*64
                        if self.gfx[idx]==1:
                            self.V[0xf]=1
                        self.gfx[idx]^=1
            #show.draw(self.gfx)
            
        
        elif self.case==0xe:
            if self.NN==0x9e:
                #Skip if key is same
                if self.keys[self.V[self.X]] == True:
                    self.pc+=2
            if self.NN==0xa1:
                #Skip if key is not same
                if self.keys[self.V[self.X]] == False:
                    self.pc+=2

        elif self.case==0xf:
            if self.NN==0x07:
                self.V[self.X] = self.dt

            elif self.NN==0x0a:
                for x in range(16):
                    if self.keys[x] == True:
                        self.V[self.X]=x
                        self.pc+=2
                else:
                    #print("waiting for key")
                    self.updatedelay()
                    self.pc-=2

            elif self.NN==0x15:
                self.dt = (self.V[self.X])
            elif self.NN==0x18:
                self.st=self.V[self.X]
            elif self.NN==0x1e:
                self.i+=self.V[self.X]
            elif self.NN==0x29:
                self.i=self.V[self.X]
            elif self.NN==0x33:
                self.mem[self.i]=int(self.V[self.X])//100
                self.mem[self.i+1]=(int(self.V[self.X])//10)%10
                self.mem[self.i+2]=int(self.V[self.X])%10
            elif self.NN==0x55:
                for i in range(self.X+1):
                    self.mem[self.i+i]=self.V[i]
            elif self.NN==0x65:
                for i in range(self.X+1):
                    self.V[i]=self.mem[self.i+i]
