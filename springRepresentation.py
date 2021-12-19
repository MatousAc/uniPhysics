GlowScript 2.9 VPython
## constants and data
g = 9.8
L0 = 0.26
ks = 1.8
dt = .02
angle = 30
angle_r = angle * pi / 180
air_density = 1.2

## objects (origin is at ceiling)
ceiling = box(pos=vector(0,0,0), length=0.2, height=0.01, width=0.2) 
ball = sphere(pos=vector(0.2,-0.3,0), radius=0.025,
              color=color.orange, make_trail = True)
spring = helix(pos=ceiling.pos, color=color.cyan, thickness=.003, coils=40, radius=0.010)
# make the spring axis be a vector from the ceiling.pos to the ball


## initial values
ball.velocity = vector(.2,.5,.5)
ball.mass = 0.03
Fgrav = ball.mass * g * vector( 0, -1, 0 )

## improve the display
scene.autoscale = False          ## turn off automatic camera zoom
scene.center = vector(0,-L0,0)   ## move camera down 
scene.waitfor('click')           ## wait for a mouse click

## set up a graph
graph1=graph(title='y vs. t')
ygraph = gcurve(gdisplay=graph1,color=ball.color)
graph2=graph(title='v vs. t')
vgraph = gcurve(gdisplay=graph2,color=color.blue)

# Figure axis


# Pre-Calculate Fnet, delta_s and ball.velocity
#Fspring = Fgrav / sin(angle_r)
s = ( mag(Fgrav) / ( ks * sin(angle_r) ))
ball.pos = ( L0 + s ) * vector( cos(angle_r), -sin(angle_r), 0 )
spring.axis = ball.pos - ceiling.pos
Fspring = ks * s
ball.velocity = sqrt( Fspring * cos(angle_r) ** 2 * ( L0 + s ) / ball.mass ) * vector( 0 , 0, -1 )

print( 'Smallest air density that makes a difference: ' + air_density )

## calculation loop
t = 0
while t <100:
    # pause long enough to make this real-time
    sleep(dt)
    
    #Update net force on ball: gravity + spring
    L = ball.pos - ceiling.pos
    Lhat = norm(L)
    s = L - L0 * Lhat
    Fspring = -ks * s
    Vhat = norm(ball.velocity)
    Fair = ( .25 * air_density * pi * ball.radius ** 2 * mag(ball.velocity) ** 2 ) * -Vhat
    Fnet = Fgrav + Fspring + Fair
    
    #Update velocity
    ball.velocity = ball.velocity + Fnet / ball.mass * dt
    
    #Update position (and re-draw spring)
    ball.pos = ball.pos + ball.velocity * dt
    spring.axis = ball.pos - ceiling.pos
    
    t = t + dt

    # update the graphs to show the y-component of position and velocity
    ygraph.plot(pos=(t, ball.pos.y))
    vgraph.plot(pos=(t, ball.velocity.y))
    
    