import salabim as sim
import math

def test1():
    print('test1')

    class X(sim.Component):
        def __init__(self,extra=1,*args,**kwargs):
            sim.Component.__init__(self,*args,**kwargs)
            self.extra=extra
            
        
        def process(self):
            while True:
                yield self.hold(1)
                pass
                
        def action2(self):
            for i in range(5):
                yield self.hold(25)

            yield self.hold(1)
                
        def actionx(self):
            pass
                
    
    class Y(sim.Component):
        
        def process(self):
            x[3].reschedule(process=x[3].action2(),at=30)
            x[4].cancel()
            yield self.hold(0.5)
            yield self.standby()
            yield self.activate(process=self.action2(0.3))

            
        def action2(self,param):
            yield self.hold(param)
            
    class Monitor(sim.Component):
        def process(self):
            while sim.now<30:
                yield self.standby()
                        
    sim.default_env.reset(True)
    q=sim.Queue()

    x=[0]
    for i in range(10):
        x.append(X(name='x.',at=i*5))
#        x[i+1].activate(at=i*5,proc=x[i+1].action())
        x[i+1].enter(q)
        
    x[6].suppress_trace=True
    i=0
    for c in q:
        print (c._name)
        i=i+1
        if i==4:
            x[1].leave(q)
            x[5].leave(q)
            x[6].leave(q)
        
    y=Y(name='y')
#    y.activate(at=20)
    sim.run(till=35)

#    env.run(4)
    
def test2():
    print('test2')

    sim.default_env.reset(True)
    x=[None]
    q=[None]
    for i in range(5):
        x.append(sim.Component(name='x.'))
        q.append(sim.Queue(name='q.'))
    y=sim.Component(name='y')
    x[1].enter(q[1])
    y.enter(q[1])
    x[1].enter(q[2])
    x[2].enter(q[2])
    x[2].enter(q[1])
    x[3].enter(q[2])
    q[1].print_statistics()

    q[2].print_statistics()
    q[1].union(q[2],'my union').print_statistics()

    q[1].difference(q[2],'my difference').print_statistics()
    q[1].intersect(q[2],'my intersect').print_statistics()
    q[1].copy('my copy').print_statistics()    
    q[1].move('my move').print_statistics()
    q[1].print_statistics()

    print (q[1])
    
    yy=q[1].component_with_name('y')
    ii=q[1].index_of(y)
    
    
def sample_and_print(dist,n):
    s=[]
    
    for i in range(n):
        s.append(dist.sample)
    print ('mean=',dist.mean,'samples', s)
    
def test3():
    print('test3')
    
    sim.default_env.reset(True)
    print('string')
    d=sim.Distribution('Exponential (1000)')
    sample_and_print(d,5)
    sim.random.seed()
    sample_and_print(d,5)
    sim.random.seed(-1)
    sample_and_print(d,5)
    
    print('triangular')
    tr=sim.Triangular(1,5,3)
    sample_and_print(tr,5)

    print('uniform')
    u=sim.Uniform(1,1.1)
    sample_and_print(u,5)
    print('constant')
    c=sim.Constant(10)
    sample_and_print(c,5)

    print('normal')
    n=sim.Normal(1,2)
    sample_and_print(n,5)
    sample_and_print(n,5)

    print('cdf')
    cdf=sim.Cdf((1,0,2,25,2,75,3,100))
    sample_and_print(cdf,5)
    sample_and_print(cdf,5)

    print('pdf')
    pdf=sim.Pdf(((1,2),100))
    sample_and_print(pdf,5)
    sample_and_print(pdf,5)

def test4():
    print('test4')
    class X(sim.Component):
        def process(self):
            yield self.hold(10)
            yield self.request(res,4)
            yield self.hold(20)
            res.requesters.print_statistics()
            res.claimers.print_statistics()
            for i in range(1):
                self.release(res,4)
    
    class Y(sim.Component):
        def process(self):
            yield self.hold(11)
            yield self.request(res,1,priority=1-self.i)
            if self.request_failed:
                pass
            else:
                yield self.hold(1)
                self.release(res)

    class Z(sim.Component):
        def process(self):
            yield self.hold(20)
            y[4].reschedule()
            res.capacity=2
            
    sim.default_env.reset(True)
    res=sim.Resource(name='res.',capacity=4)
    res.x=0
    x=X(name='x')
    y=[0]
    for i in range(6):
        c=Y(name='y.')
        c.i=i
        y.append(c)

    z=Z(name='z')
    sim.run(till=1000)
    
def test5():
    print('test5')
    
    class X1(sim.Component):
        
        def process(self):
            while True:
                while True:
                    yield self.request(r1,2,5,r2,greedy=True,fail_at=self.now+6)
                    if not self.request_failed():
                        break
                yield self.hold(1)
                self.release(r1,r2)
                yield self.passivate()
    class X2(sim.Component):
        
        def process(self):
            while True:
                yield self.request((r1,3),(r2,1,1))
                yield self.hold(1)
                self.release(r1)
                yield self.passivate()
    class X3(sim.Component):
        
        def process(self):
            while True:
                yield self.request(r1,r2)
                yield self.hold(1)
                self.release(r1,r2)
                yield self.passivate()
            
    class Y(sim.Component):
        
#        def __init__(self,*args,**kwargs):
#            sim.Component.__init__(self,*args,**kwargs)
            
        def process(self):
            yield self.hold(3)
            x1.cancel()
            yield self.hold(10)
            r2.capacity=1
            pass

            
                        
    sim.default_env.reset(True)
    q=sim.Queue(name='q')
    r1=sim.Resource(name='r1',capacity=3)
    r2=sim.Resource(name='r2',capacity=0)    
    r3=sim.Resource(name='r3',capacity=1)  
      
    x1=X1()
    x2=X2()
    x3=X3()

        
    y=Y(name='y')
    sim.run(till=21)    
    
def test6():
    print('test6')
    class X(sim.Component):
        def process(self):
            yield self.passivate()
            yield self.hold(1)
            
    sim.trace(True)
    x=X()
    print (x.status)
    q=sim.Queue(name='Queue.')
    q.name='Rij.'
    print (q.name)
    q.clear()
    sim.run(till=10)
    x.reactivate()
    sim.run()
    
def test7():
    print('test7')

    class X1(sim.Component):
        def process(self):
            yield self.request(r1,5,r2,2,greedy=True,fail_at=5)
            yield self.passivate()
    

    class X2(sim.Component):
        def process(self):
            yield self.request(r1,8,r2)
            yield self.passivate()
    
    class X3(sim.Component):
        def process(self):
            yield self.request(r1,7)
            yield self.passivate()
    

    sim.trace(True)
    x=sim.default_env
    print(sim.default_env)
    sim.default_env.reset(True)
    print(x==sim.default_env)
    print(sim.default_env)
    
    x1=X1()
    x2=X2()
    x3=X3()
    
    X4=sim.Component()
    
    r1=sim.Resource(capacity=10,anonymous=True)    
    r2=sim.Resource()    
    r3=sim.Resource()    
    
    q={}
    for i in range(1,5):
        q[i]=sim.Queue()
        
    x1.enter(q[1])    
    x1.enter(q[2])    
    x1.enter(q[3])   
    
    x2.enter(q[1])    
    x3.enter(q[1])    
    
    
        
    sim.run(10)
    r2.capacity=2
    sim.run(20)

    print(sim.default_env)

    print(x1)
    print(x2)
    print(x3)

    print (q[1])
    print (q[2])
    print (q[3])
    print (q[4])
    
    print(r1)
    print(r2)
    print(r3)
    
    d=sim.Exponential(10)
    print(d)
    print(sim.Uniform(1,2))
    print(sim.Triangular(40,150,55))
    print(sim.Distribution('Constant(5)'))


        
def test8():
    print('test8')

    class AnimatePolar(sim.Animate):
        def __init__(self,r,*args,**kwargs):
            self.r=r
            super().__init__(*args,**kwargs)
            
        def x(self,t):
            tangle=sim.interpolate(t,self.t0,self.t1,0,2*math.pi)
            sint=math.sin(tangle)
            cost=math.cos(tangle)
            x,y=(100+self.r*cost-0*sint,100+self.r*sint+0*cost)
            return x
                        
        def y(self,t):
            tangle=sim.interpolate(t,self.t0,self.t1,0,2*math.pi)
            sint=math.sin(tangle)
            cost=math.cos(tangle)
            x,y=(100+self.r*cost-0*sint,100+self.r*sint+0*cost)
            return y
            
        def angle(self,t):
            return sim.interpolate(t,self.t0,self.t1,0,360)
            
        def fillcolor(self,t):
            f=sim.interpolate(t,self.t0,self.t1,0,1)
            if f<0.5:
                return sim.colorinterpolate(f,0,0.5,sim.colorspec_to_tuple('red'),sim.colorspec_to_tuple('blue'))
            else:
                return sim.colorinterpolate(f,0.5,1,sim.colorspec_to_tuple('blue'),sim.colorspec_to_tuple('green'))
        
        def text(self,t):
            angle=sim.interpolate(t,self.t0,self.t1,0,360)
            return '{:3.0f}'.format(angle)

            
    class X(sim.Component):
        def slideraction(self):
            print ('value='+str(self.myslider.v))
            
        def process(self):
            
            AnimatePolar(r=100,text='A',t1=10)            
            
            x=0
            for fontsize in range(8,30):
                sim.Animate(x0=x,y0=height-100,text='aA1',font=('Calibri,calibri'),fontsize0=fontsize)
                x+=fontsize*2
            x=0
            for fontsize in range(8,30):
                sim.Animate(x0=x,y0=height-200,text='aA1',font='CabinSketch-Bold',fontsize0=fontsize)
                x+=fontsize*2
            
                                    
            self.rx=sim.Animate(x0=600,y0=300,linewidth0=1,
                            rectangle0=(-200,-200,200,200),t1=10,fillcolor0='green#7f',angle1=0)
            self.rx=sim.Animate(x0=500,y0=500,linewidth0=1,line0=(-500,0,500,0),t1=10,fillcolor0='black')
            self.rx=sim.Animate(x0=500,y0=500,linewidth0=1,line0=(0,-500,0,500),t1=10,fillcolor0='black')

            self.rx=sim.Animate(x0=500,y0=500,linewidth0=10,polygon0=(0,0,100,0,100,100,50,50,0,100),offsetx1=100,offsety1=100,t1=10,fillcolor0='red#7f',angle1=360)
            self.rx=sim.Animate(x0=600,y0=300,linewidth0=1,rectangle0=(-200,-200,200,200),t1=10,fillcolor0='blue#7f',angle1=360)

#            self.t1=sim.Animate(x0=500,y0=500,fillcolor0='black',
#                text='Test text',x1=500,y1=500,t1=25,font='CabinSketch-#Bold',fontsize0=20,anchor='ne',angle1=0,fontsize1=50)


            self.i1=sim.Animate(x0=250,y0=250,offsetx0=100,offsety0=100,angle0=0,angle1=360,circle0=(20,),fillcolor0=('red',0),linewidth0=2,linecolor0='blue',circle1=(20,),t1=15)

#            self.ry=sim.Animate(x0=500,y0=300,linewidth0=1,polygon0=(-100,-100,100,-100,0,100),t1=10,fillcolor0='blue',angle1=90)

            self.i1=sim.Animate(x0=500,y0=500,angle0=0,layer=1,image='salabim.png',width0=300,x1=500,y1=500,angle1=360,t1=20,anchor='center')
    
            yield self.hold(3)
            self.i1.update(image='Upward Systems.jpg',angle1=self.i1.angle1,t1=self.i1.t1,width0=self.i1.width0)
            return
            self.myslider=sim.AnimateSlider(x=600,y=height,width=100,height=20,vmin=5,vmax=10,v=23,resolution=1,label='Test slider',action=self.slideraction) 
            
            return
            
            
            self.p1=sim.AnimatePolygon(
            x0=200,y0=200,polygon0=(-100,-100,100,-100,100,100,-100,100),
            t1=25,x1=100,y1=100,fillcolor1='red',linecolor0='blue',linewidth0=3)
            self.p2=sim.Animate(linewidth0=2,linecolor0='black',linecolor1='white',
                x0=100,y0=600,fillcolor0='green',polygon0=(-50,-50,50,-50,0,0),angle1=720,t1=8)
            self.r1=sim.Animate(layer=1,x0=500,y0=500,rectangle0=(0,0,100,100),fillcolor0='yellow',linecolor0='red',linewidth0=2,angle1=180,t1=10)
            self.t1=sim.Animate(x0=200,y0=200,fillcolor0='black',
                text='Test text',x1=100,y1=100,anchor='center',t1=25,font='courier',fontsize1=50)
            self.r2=sim.Animate(rectangle0=(-5,-5,5,5))
            
            i=0
            for s in ['ne','n','nw','e','center','w','se','s','sw']:
                sim.Animate(x0=200,y0=200,text=s,t0=i,t1=i+1,anchor=s,keep=False,fillcolor0='red')
                i=i+1

            self.p2=sim.Animate(x0=500,y0=500,line0=(0,0,100,100),angle1=360,t1=10,linecolor0='red',linewidth0=5)
            self.r2=sim.Animate(x0=300,y0=700,rectangle0=(-300,-300,300,300),fillcolor0='',linecolor0='black', linewidth0=2)
            self.c1=sim.Animate(x0=300,y0=700,circle0=(0,),fillcolor0='blue',circle1=(60,),t1=20)
            self.i1=sim.Animate(x0=500,y0=500,angle0=0,layer=1,image='BOA.png',width0=300,x1=500,y1=500,angle1=360,t1=20,anchor='center')
#            self.i1=sim.AnimateText(text='ABCDEF',x0=500,y0=200,angle0=0,layer=1,angle1=360,t1=20,anchor='center')
            yield self.hold(10)
#            self.t1.update(color0='white',x1=100,y1=100,t1=25)
            self.r1.update()
            self.c1.update(t1=20,radius1=0)
            
    import os

    sim.trace(True)
    x=X()
#    s='abcdefghijk' 
    
#    size=getfontsize_to_fit(s,10000)
#    print ('--fontsize_to_fit',size)
#    print('--width-1=', getwidth(s,'',size-1))
#    print('--width  =', getwidth(s,'',size))
#    print('--width+1=', getwidth(s,'',size+1))
#    assert False

    height=768
    sim.animation_speed(1)
    sim.run(15,animate=True,modelname='Salabim test') 
    sim.run(till=30,animate=True)
    print('THE END')


def test9():
    print('test9')
    class X(sim.Component):
        def process(self):
            yield self.passivate('One')
            yield self.passivate('Two')
            yield self.passivate()
            yield self.hold(1)
        
    class Y(sim.Component):
        def process(self):
            while True:
                print('sim.now=',sim.now())
                yield self.hold(1)
                print(x.passive_reason)
                if self.is_passive:
                    x.reactivate()
                
                
    sim.trace(True)
    x=X()
    y=Y()
    sim.run(till=6)
    
    
def test10():
    print('test10')
    for s in ('blue','','black#23','#123456','#12345678',(1,2,3),(4,5,6,7),('blue',8),('blue#67',1),('#123456',23)):
        t=sim.colorspec_to_tuple(s)
        print(s,'==>',t)
        
def test11():
    class Do1(sim.Component):
        def process(self):
            while True:
                if q1.length==0:
                    yield self.passivate()
                print('------')
                for cc in q1:
                    print(now(),cc.name)
                    yield self.hold(1)
            
    class Do2(sim.Component):
        def process(self):
            c[0].enter(q1)
            c[1].enter(q1)
            c[2].enter(q1)
            if d1.is_passive:
                d1.reactivate()
            yield self.hold(till=1.5)

            c[3].enter(q1)
            c[4].enter_at_head(q1)
            if d1.is_passive:
                d1.reactivate()
                
            yield self.hold(till=20.5)
            for cc in q1:
                cc.leave(q1)
            if d1.is_passive:
                d1.reactivate()
                
    class X(sim.Component):
        pass
        
    d2=Do2()
    d1=Do1()
    
    q1=sim.Queue('q1')
    q2=sim.Queue('q2')
    c={}
    for i in range(10):
        c[i]=sim.Component(name='c'+str(i))
        c[i].enter(q2)
    c[0].enter(q1)
    c[0].set_priority(q1,10)
    print(q1)

    c[3].set_priority(q2,10)

    c[1].set_priority(q2,-1)
    c[5].set_priority(q2,10)    
    for c in q2:
        print(c.name)
    for c in reversed(q2):
        print(c.name,c in q1)

    assert False
    print ('--')
    print(q2[-1])
    print('---')
    run(till=100)
    print (q1._iter_touched)     
    
    
    

def test12():
    def give_now():
        return 'Now={0:5.2f}'.format(Animation.t)
        
    class X(Component):
        def process(self):
            Animate(text=give_now,x0=100,y0=100,x1=500,y1=500,t1=10)
            while True:
                print(default_env)
                yield self.hold(1)
           
    trace(True)
    animation_speed(1)
    a=Environment(name='piet.')
    b=Environment(name='piet.')
    c=Environment(name='piet.')
    print(a)
    print(b)
    print(c)    
    
    X(auto_start=False)
    X(auto_start=False)
    X(auto_start=False)
    X()       
    animation_speed(0.1)
    run(4,animate=True,video='x.mp4')
    run(2)
    run(4,animate=True)
    finish()

def test13():
    q=sim.Queue()
    for i in range(10):
        c=sim.Component(name='c.')
        q.add(c)
        
    print(q)
    for c in q:
        print (c.name)
        
    for i in range(20):
        print(i,q[i].name)
        
def test14():
    class X(Component):
        def process(self):
            yield self.request(*r)
            print(self.claimed_resources)
            
    X()
    r=[Resource() for i in range(10)]
    run(till=10)
    
def test15():
    d=Pdf(('r',1,'c',1))
    d=Pdf((1,2,3,4) ,1) 
    print(d.mean)
    s=''
    for i in range(100):
        x=d.sample
        s=s+str(x)
    print(s)    
        
        
def test16():
    a=sim.Animate(text='Test',x0=100,y0=100,fontsize0=30,fillcolor0='red')
    a=sim.Animate(line0=(0,0,500,500),linecolor0='white',linewidth0=6)
    sim.run(animate=True)
    
    
def test17():
    def actiona():
        bb.remove()
        sl.remove()        
    def actionb():
        ba.remove()        

    
    for x in range(10):
        for y in range(10):
            a=sim.Animate(rectangle0=(0,0,95,65),x0=5+x*100,y0=5+y*70,fillcolor0='blue',linewidth0=0)
    ba=sim.AnimateButton(x=100,y=700,text='A',action=actiona)
    bb=sim.AnimateButton(x=200,y=700,text='B',action=actionb)
    sl=sim.AnimateSlider(x=300,y=700,width=300)
    
            
    sim.default_env.animation_parameters(animate=True)
    sim.run(10)
    sim.animation_parameters(animate=False)
    sim.run(100)
    sim.animation_parameters(animate=True,background_color='yellow')
    sim.run(10)
    
if __name__ == '__main__':
    test17()
