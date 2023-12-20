


class element:
    def __init__(self,name=None,left=None,top=None,right=None,bottom=None,width=None,height=None,parent=None):

        self.base_left=left
        self.base_top=top
        self.base_width=width
        self.base_height=height
        self.base_bottom=bottom
        self.base_right=right
        self.parent=parent
        self.name=name

        self.left=None
        self.top=None
        self.width=None
        self.height=None
        self.bottom=None
        self.right=None
        
        self.calculate()


    def get_width(self):
        if self.base_width:
            return self.base_width
       # if self.base_left and self.base_right:
            
    def get_right(self):
        if self.base_right:
            if self.base_right>-1:
                return self.base_right
            elif self.parent:
                return self.parent.right+self.base.right
        
        return None

    def calculate(self):
        """Recalculates the box's bounding positions based on original settings"""
        l=self.base_left
        t=self.base_top
        w=self.base_width
        h=self.base_height
        b=self.base_bottom
        r=self.base_right
        p=self.parent

        # IF the variables exist
        if l != None:
            if l>-1:
                self.left=l
            elif p != None:
                self.left=p.right+l
        elif p!=None:
            self.left=p.left

        if r != None:
            if r>-1:
                self.right=r
            elif p != None:
                self.right=p.right+r
        elif p!=None:
            self.right=p.right

        if t != None:
            if t>-1:
                self.top=t
            elif p:
                self.top=p.top+t
        elif p!=None:
                self.top=p.top

        if b != None:
            if b>-1:
                self.bottom=b
            elif p != None:
                self.bottom=p.bottom+b
        elif p!=None:
                self.bottom=p.bottom
                
        # the +_ 1 is for INCLUSIVE numbers. we start at 0. and even if top and bottom are
        # the same line which is 0 height, its actualy 1
        # if the variables are not explicitly set, we need a width and height to calcuate with

        if w != None:
            self.width=w
            if l == None and r != None:
                self.left=self.right-w+1

            if r == None and l != None:
                self.right=self.left+w-1
        else:
            if self.left != None and self.right!=None:
                self.width=self.right-self.left+1


        if h != None:
            self.height=h

            if t == None and b != None:
                self.top=self.bottom-h-1

            if b == None and t != None:
                self.bottom=self.top+h-1
        else:
            if self.top != None and self.bottom!=None:
                self.height=self.bottom-self.top+1

        info=self.info()
        #raise ValueError(f"Left cannot be none {info}")
        if self.left==None:
            raise ValueError(f"Left cannot be none {info}")
        if self.right==None:
            raise ValueError(f"Right cannot be none {info}")
        if self.top==None:
            raise ValueError(f"Top cannot be none {info}")
        if self.bottom==None:
            raise ValueError(f"Bottom cannot be none {info}")
        if  self.width==None:
            raise ValueError(f"Width cannot be none {info}")
        if self.height==None:
            raise ValueError(f"Height cannot be none {info}")



    def info(self):
        info=f"\
                Name: {self.name} \n \
                base_left: {self.base_left}\n \
                base_top: {self.base_top}\n \
                base_width: {self.base_width}\n \
                base_height: {self.base_height}\n \
                base_bottom: {self.base_bottom}\n \
                base_right: {self.base_right}\n \
                parent: {self.parent}\n \
                left:  {self.left}  - top:    {self.top} \n \
                right: {self.right} - bottom: {self.bottom}\n \
                width: {self.width} - height: {self.height} \n \
                "        
        return info

    def set(self,width,height):
        self.base_width=width
        self.height=height
        self.calculate()
    
