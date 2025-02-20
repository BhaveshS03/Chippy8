from pygame import display,time,draw

class display_func:
    def __init__(self) -> None:
        self.width=64
        self.height=32
        self.scale=10
        self.surface=0
        self.initialize()

    def initialize(self):
        display.init()
        self.surface=display.set_mode((self.width*self.scale,self.height*self.scale))
        display.flip()

    def draw(self,gfx):
        if gfx==[0]*4096:
            self.surface.fill((75, 54, 33))
        else:
            for data in range(4096):
                x=data%64
                y=data//64            
                if gfx[data]==1:
                    draw.rect(self.surface,(255,255,255),(x*self.scale,y*self.scale,self.scale,self.scale))
                elif gfx[data]==0:
                    draw.rect(self.surface,(75, 54, 33),(x*self.scale,y*self.scale,self.scale,self.scale))
        time.Clock().tick(6000)
        display.flip()