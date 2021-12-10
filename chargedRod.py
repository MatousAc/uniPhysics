GlowScript 2.9 VPython

# Import Dependencies
from visual import *

# First Lets Define Useful Variables and Initialize Lists
colour_ct       = 0 # I Am Using This Loop Variable To 
                    # Control the Color Of the Shpheres And Arrows
scale_field     = 2e-3 # This Number Appropriately Scales Arrows To the Scene
oofpez = K      = 8.99e9 # This Is Another, More Fun, Name for "K"
e0              = ( 1 / ( 4 * pi * K ) ) # I Use Epsilon In My Calculations
L               = .8 # Length Of My Charged Rod
Q               = 2e-9 # Total Charge
Nq              = 200 # Number Of Spheres
dx              = L/Nq
dQ              = Q/Nq

# Here's My Variables for Creating Spheres and Charged Arrows
sources         = [] # This Is Where the Spheres Will Be Stored
x               = -L/2 + ( dx / 2 ) # The Position Of the First Sphere
                                    # Half Length To the Left, And A Half
                                    # Diameter To the Right
Enet            = vector( 0, 0, 0 ) # A Vector for Total Field At A Point

# Here I Define My Variables for the Electric Field Arrows
theta           = 0
dtheta          = pi / 90
ex              = - L / 2 # "ex" Because "x" Is Already Being Used
dex             = L / 70 # Number Of Arrow Rings
R               = 0.06 # This Is How Far the Arrows Are From the Rod
obs_list        = [ ( vector( -0.02, 0,01, 0 )) ] # Placement Of Observation Arrows
# obs_colour      = [] # Currently Being Used To Colour the Arrows

# Set the Dimensions Of the Scene Display ( I Like Them A Little Bigger )
scene.width     = 1700
scene.height    = 780
scene.background= vector( .02, .02, .23 ) #vector( ( 117 / 255 ), ( 190 / 255 ), ( 216 / 255 ) )

# for j in range( 0, 4 ): # A For Loop Can Be Used Here For Adding More Rods
# i               = j / 10
# x               = -L/2 + ( dx / 2 )
colour_ct       = 0
## Make A Rod and A List of Source Charges
cylinder( 
    pos         = vector( -L / 2, 0, 0 ) ,
    axis        = vector( L, 0, 0 ) ,
    color       = color.blue ,
    radius      = ( 0.013 ) , # Why Is It Always This Radius?
    opacity     = ( 0.2 ) # So Spheres Inside Are Visible
    )

while x < ( L / 2 ) :
    # I Just Wanted To Make Every Sphere A Different Colour
    colour_ct  += 1
    col1        = ((-x * 600 )  + 255 )      / 255 # Red
    col2        = (( x * 300 )  + 220 )      / 255 # Green
    col3        = (( x * 360 )  + 180 )      / 255 # Blue
    if colour_ct> ( x / Nq ) : # Not Sure When This Executes, But I Know It Works
        col2    = (( x * 300 )  + 120 )      / 255 # Green, For Second Half Of Rod
    
    a   = sphere( # Create the Sphere
        pos     = vector( x, 0, 0 ) ,
        radius  = ( 0.01 ) ,
        color   = vector( (1 - col1) , (1 - col2 ) , ( 1- col3 ) ),
        q       = dQ
        )
        
    sources.append( a ) # Add Sphere To the List
    # obs_colour.append( a.color )
    x           = x + dx

colour_ct       = 0 # Just Re-Setting My Count Variable Here

# ex              = - L / 2 # ex Has To Be Set Back To the Initial Value If More Than One Rod
while ex < 1.2 * L / 2 : # change to 1.8 to see the field extended farther!
    theta = 0
    while ( theta < ( 2 * pi )) :
        R           = theta / 20 # If I Want To Spiral, I Uncomment This Allow
                            # While Loop To Go To -  7 * pi -
        # This Picks the Location Of the Next Field Arrow
        obs_spot    = vector( ex, ( R * cos(theta) ), ( R * sin(theta) ) ) 
        Enet        = vector( 0, 0, 0 )

            
        # This Makes Every Arrow A Different Colour
        colour_ct  += 1
        col1        = ((-ex * 600 )  + 255 )      / 255 # Red
        col2        = (( ex * 300 )  + 220 )      / 255 # Green
        col3        = (( ex * 360 )  + 180 )      / 255 # Blue
        if colour_ct> ( ex / ( L / dex ) ) : #
            col2    = (( ex * 300 )  + 120 )      / 255 # Green, For Second Half Of Rod
        
        # This Loop Calculates the Net Electric Field At Every Observation Pos.
        for scharge in sources : 
            r       = obs_spot - scharge.pos
            Enet   += oofpez * ( dQ / mag( r ) ) * norm( r )
    
        electric_field  = arrow(
            pos         = obs_spot ,
            # The "1 - col" Gives Me the Opposite Colour Of the Rod
            color       = vector( ( col1 ) , ( col2 ), ( col3 ) ) ,
            emissive    = True ,
            axis        = ( Enet * scale_field ) ,
            shaftwidth  = 0.001, # * mag(Enet) * scale_field * 10 , # to scale shaftwidth
            headwidth   = 0.003 ,
            headlength  = 0.004 ,
            )
        
        obs_list.append( electric_field )
        
        theta          += dtheta
    ex                 += dex

