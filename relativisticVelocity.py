GlowScript 3.0 VPython

# Setup Graph Objects
gdisplay(xtitle = "time", ytitle = "position")
star_pos_graph = gcurve(color = color.blue, label = "star position")
black_hole_pos_graph = pos_graph = gcurve(color = color.green, label = "black hole position")

gdisplay(xtitle = "time", ytitle = "speed")
star_vel_graph = gcurve(color = color.blue, label = "star velocity")
black_hole_vel_graph = gcurve(color = color.green, label = "black hole velocity")

def gamma( velocity ) :
    return ( 1 / ( sqrt( 1 + (( velocity ** 2 ) / ( c ** 2 )) ) ))

c = 1 # 3e8
dt = 0.01
time = 0

# Make Star
star = sphere( 
    radius = 0.5, 
    color = color.blue,
    pos = vec(0, 0, 0)
    )

# Make Non-Relativistic Black-Hole
black_hole = sphere( 
    radius = 0.5, 
    color = color.green,
    pos = vec(0, 0, 0)
    )

star.momentum = vec(0, 0, 0,)
star.mass = 1.0
black_hole.momentum = vec(0, 0, 0,)
black_hole.mass = 1.0

while (True):
    rate(100)
    force = vec(1, 0, 0)
    
    # Non-Relativistic Motion
    black_hole.momentum = black_hole.momentum + ( force * dt )
    black_hole.gamma = 1.0
    black_hole.pos = black_hole.pos + ( black_hole.gamma * black_hole.momentum / black_hole.mass * dt )

    # Relativistic Motion
    star.momentum = star.momentum + ( force * dt )
    star.gamma = gamma(mag(star.momentum)/star.mass) # 1.0 / sqrt(1.0+(mag(star.momentum)**2/(star.mass**2*c**2))) #gamma(mag(star.momentum)/star.mass)
    star.pos = star.pos + ( star.gamma * star.momentum / star.mass * dt )
    

    time += dt
    
    # Update Graphs
    star_pos_graph.plot(pos = (time, star.pos.x))
    black_hole_pos_graph.plot(pos = (time, black_hole.pos.x))
    
    star_velocity = star.momentum /  star.mass * star.gamma
    star_vel_graph.plot(pos = (time, star_velocity.x))
    
    black_hole_velocity = black_hole.momentum /  black_hole.mass * black_hole.gamma
    black_hole_vel_graph.plot(pos = (time, black_hole_velocity.x))
    
    
    