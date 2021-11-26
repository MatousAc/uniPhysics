GlowScript 2.9 VPython

# Import Dependencies
from visual import *

# First Lets Define Useful Variables and Initialize Lists
scale_field     = 1.9e-5 # This Number Appropriately Scales Arrows To the Scene
particle_number = 2
oofpez = K      = 8.99e9 # This Is Another, More Fun, Name for "K"
e0              = ( 1 / ( 4 * pi * K ) ) # I Use Epsilon In My Calculations
L               = 0.8
Q               = 50e-9
Nq              = 36
theta1          = 0
dtheta1         = ( 2 * pi / Nq )
dQ              = Q/Nq
rad_ring        = 0.1
arrow_dist      = 1.5
arr_am          = 17
x               = - arrow_dist / 2
dx              = arrow_dist / ( arr_am - 1 )
y               = - arrow_dist / 2
dy              = arrow_dist / ( arr_am - 1 )
obs_list        = [] 
particles       = []
texture_list    = [ 
    "https://i.imgur.com/8yCj0Aog.jpg", 
    "https://i.imgur.com/yrCS96j.png", 
    "https://i.imgur.com/bU9USjt.jpg", 
    "https://i.imgur.com/dc9kxhq.jpeg",
    "https://i.imgur.com/XHC1paa.jpg",
    "https://i.imgur.com/qdWJkbc.jpeg",
    "https://i.imgur.com/DC3vdIP.jpg",
    "https://i.imgur.com/SeDAly7.jpg",
    "https://i.imgur.com/CI3GsGX.jpg",
    "https://i.imgur.com/AAczZKf.jpg",
    "https://i.imgur.com/MBCZh43.jpg",
    "https://ae01.alicdn.com/kf/HTB12mliajzuK1RjSspeq6ziHVXaO/5064-Colorful-Lion-DIY-Paint-By-Numbers.jpg",
    "https://i.imgur.com/F3OQY8T.jpg",
    ]
surf            = 0
charge_increment= 0

elapsed_time    = 0
time            = 1000
dt              = 1e-11



# This Function Calculates the Electric Field At Any Given Location

def chargeRing( theta1, surf ) :
    thetac      = theta1 * .02    
    
    a   = sphere( # Create the Sphere
        pos     = vector( 0, rad_ring * cos(theta1) , rad_ring * sin(theta1) ) ,
        radius  = ( 0.008 ) ,
        #color   = vec( col1, col2, col3 ) ,
        texture     = pickSurface( surf ) ,
        emissive= True ,
        q       = dQ
        )
    sources.append( a ) # Add Sphere To the List

def pickSurface( surf ) :
    index       = surf % ( texture_list.length )
    return texture_list[ index ]
    
    

def electricField( object_pos ) :
    field       = vec( 0, 0, 0 )
    for scharge in sources : 
        r               = object_pos - scharge.pos
        field          += oofpez * ( scharge.q / mag( r ) ) * norm( r )
    for particle in particles :
        if ( object_pos != particle.pos ) :
            r           = object_pos - particle.pos
            field      += oofpez * ( particle.q / mag( r ) ) * norm( r )
    return field

def build_arrow( iterable, Enet, obs_spot ) :
        electric_field  = arrow(
        pos         = obs_spot ,
        # The "1 - col" Gives Me the Opposite Colour Of the Rod
        color       = colour( iterable ) ,
        emissive    = True ,
        axis        = ( Enet * scale_field ) ,
        shaftwidth  = 0.003 # * mag(Enet) * scale_field * 10 , # to scale shaftwidth
        )
        return electric_field

def electron_position( particle, field ) :
    force               = field * particle.q
    acceleration        = force / particle.mass
    particle.velocity  += ( acceleration * dt )
    particle.pos       += ( particle.velocity * dt )
    particle.color      = particle.pos * 4 + vec( .3, .4, .5 )
    particle.trail_color= particle.color - vec( -.2, .2, .3 )

def colour( iterable ) : # This Makes Things Different Colours
    col1        = (( iterable * 600 * Nq / arr_am )  + 165  )      / 255 # Red
    col2        = (( iterable * 650 * Nq / arr_am )  + 170 )      / 255 # Green
    col3        = ((-iterable * 460 * Nq / arr_am )  + 180 )      / 255 # Blue
    # print( "Colour Vector for " + iterable + ": " + ( vec( col1, col2, col3 ) )  )
    return vec( col1, col2, col3 )

def vortex( half_time ) :
    for scharge in sources :
        half_time  += 1
        theta       = scharge.pos.diff_angle(vec( 0, 1, 0 ))
        if half_time > ( Nq / 2 ) :
            theta = -theta
        scharge.rotate( 
        angle       = ( pi / 1000 ) , 
        axis        = scharge.pos.cross(vec( -1, 0, 0 )) ,
        origin      = vec( 0, ( rad_ring * cos(theta)), ( rad_ring * sin(theta)) ) - vec( .017, .007, .007 )
        #origin = vec( .3 , -.2 , .4 ) - scharge.pos 
        )

# Here's My Variables for Creating Spheres and Charged Arrows
sources         = [] # This Is Where the Spheres Will Be Stored

# Set the Dimensions Of the Scene Display ( I Like Them A Little Bigger )
scene.width     = 1700
scene.height    = 770
scene.background= vector( 0, 0, 0 )
#scene.background= vector( .02, .02, .23 )

# Set An Image Background
background  = sphere( 
    texture = "https://i.imgur.com/hlZrVDB.jpg" ,
    radius  = 1.5,
    shininess = 0 ,
    axis    = vec( 0, 1, 1 )
    )

'''
# Make A Rod and A List of Source Charges
ring( 
    pos         = vector( 0, 0, 0 ) ,
    axis        = vector( 1, 0, 0 ) ,
    color       = color.green ,
    thickness   = ( 0.008 ) , 
    radius      = ( rad_ring ) ,
    opacity     = ( 0.05 ) # So Spheres Inside Are Visible
    )
'''

while theta1 < ( 2 * pi - dtheta1 / 2 ) :
    chargeRing( theta1, surf )
    surf       += 1
    theta1     += dtheta1

# Drawing Arrows
while x < arrow_dist / 2 + dx / 2  :
    
    # This Picks the Location Of the Next Field Arrow
        obs_spot    = vec( x, 0, 0 )
        Enet        = vector( 0, 0, 0 )       
        # This Loop Calculates the Net Electric Field At Every Observation Pos.
        Enet        = electricField( obs_spot )
        electric_field = build_arrow( x, Enet, obs_spot )
        obs_list.append( electric_field )
        x              += dx

# Initializing Our Particles
for i in range ( particle_number ) :
    charge_increment += 1
    mouseposition = scene.waitfor('click').pos ## wait for mouse click, save the mouse position 
    particle        = sphere(
            pos     = mouseposition ,
            radius  = ( 0.01 ),
            velocity= vec( 0, 0, 0 ) ,
            mass    = 9.11e-31 ,
            q       = ( -1.6e-18 * ( charge_increment ** 2 ) ) ,
            make_trail  = True ,
            trail_type  = 'points' ,
            interval    = 8 ,
            trail_color = mouseposition ,
            retain      = 23
        )
    particles.append( particle )

while ( elapsed_time < time ) :
    rate(1000)
    for particle in particles :
        field = electricField( particle.pos )
        electron_position( particle, field )
    
    background.rotate( angle = ( pi / 100000 ), axis = vec( 0, 1, 1 ), origin = vec( 0, 0, 0 ) )
    vortex( elapsed_time )
    elapsed_time += dt
