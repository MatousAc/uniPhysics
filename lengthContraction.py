GlowScript 3.0 VPython

# Declare Necessary Variables
dt = 0.01   # delta t
time = 0
k = 0.2     # Spring Constant
c = 1       # Light Speed, for Now

# Setting the Scene
scenery = []
scene.autoscale = False

# Dimensions
scene.width     = 1720
scene.height    = 830
scene.background= vector( 0, 0, 0 )
#scene.background= vector( .02, .02, .23 )

# Image Background
background  = sphere( 
    texture = "https://i.imgur.com/hlZrVDB.jpg" ,
    radius  = 40,
    shininess = 0 ,
    axis    = vec( 1, 1, 1 )
    )

# Assign Textures
texture_list    = [ 
    "https://i.imgur.com/8yCj0Aog.jpg", 
    "https://i.imgur.com/yrCS96j.png", 
    "https://i.imgur.com/bU9USjt.jpg", 
    "https://i.imgur.com/dc9kxhq.jpeg",
    "https://i.imgur.com/VCK9QsT.jpg",
    "https://i.imgur.com/qdWJkbc.jpeg",
    "https://i.imgur.com/DC3vdIP.jpg",
    "https://i.imgur.com/56VP72hg.jpg",
    "https://i.imgur.com/bInJVt0.jpg",
    "https://i.imgur.com/AAczZKf.jpg",
    "https://i.imgur.com/bpNpk9v.jpg",
    "https://i.imgur.com/4rg9A1I.jpg"
    ]


def pickSurface( surf ) :
    index       = surf % ( texture_list.length )
    return texture_list[ index ]


# Declare Gamma Function
def gamma( velocity ):
    return ( 1 / ( sqrt( 1 - (( velocity ** 2 ) / ( c ** 2 )) ) ))

def gamma_alt( velocity ):
    return ( 1 / ( sqrt( 1 + (( velocity ** 2 ) / ( c ** 2 )) ) ))

# Create Class for Space Boxes
class prop():
    def __init__(self, posn, siz, surf):
        global scenery
        self.pos = posn
        self.siz = siz # Rest Size
        self.body = box( pos = posn, size = siz, texture = pickSurface(surf) )
        scenery.append(self)

# Create Boxes
for x in range(-3, 7):
    for y in range(-3, 7):
        for z in range(-3, 7):
            prop(posn = vec(2 * x, 2 * y, 2 * z), siz = vec(0.3, 0.3, 0.3), surf = (x * y + z) )

# Create Star
mouseposition = scene.waitfor('click').pos ## wait for mouse click, save the mouse position
star = sphere( 
    radius      = 0.5, 
    color       = mouseposition,
    pos         = mouseposition,
    make_trail  = True,
    trail_color = mouseposition,
    retain      = 70
    )

star.momentum = vec(3, -3.4, 4.5,)
star.mass = 1.0

# Follow the Star
# scene.camera.follow(star)

while (True):
    rate(1000)
    force = -k * star.pos
    
    # Relativistic Motion
    star.momentum = star.momentum + ( force * dt )
    star.gamma = gamma_alt(mag(star.momentum)/star.mass)
    star.pos = star.pos + ( star.gamma * star.momentum / star.mass * dt )

    time += dt
    star.velocity = star.momentum /  star.mass * star.gamma 
    gamma_box = vec(gamma(star.velocity.x), gamma(star.velocity.y), gamma(star.velocity.z))
    
    for cube in scenery:
        cube.body.size.x = cube.siz.x/gamma_box.x
        cube.body.size.y = cube.siz.y/gamma_box.y
        cube.body.size.z = cube.siz.z/gamma_box.z
        cube.body.pos.x = cube.pos.x/gamma_box.x
        cube.body.pos.y = cube.pos.y/gamma_box.y
        cube.body.pos.z = cube.pos.z/gamma_box.z
    
    # Aesthetics
    star.trail_color = star.pos
    star.color = star.velocity

    
    
    