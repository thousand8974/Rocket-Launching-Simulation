from vpython import *
#Web VPython 3.2


rocket_parts = []
height = 0.5
rocket_parts.append( cylinder( pos=vector(0,0,0), color=color.red, size=vector(height,0.1,0.1), axis=vector(0,1,0) , make_trail = True ))

rocket_parts.append( cone( pos=rocket_parts[0].pos+rocket_parts[0].size.x*rocket_parts[0].axis*2, color=color.red,
                           size=vector(rocket_parts[0].size.y,rocket_parts[0].size.y,rocket_parts[0].size.y),
                           axis=vector(0,1,0)) )
rocket_parts.append(triangle( v0=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(1,0,0),color=color.red),
                v1=vertex(pos=rocket_parts[0].pos+1.5*rocket_parts[0].size.y*vector(1,0,0),color=color.red),
                v2=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(1,2,0),color=color.red) ))
rocket_parts.append(triangle( v0=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(-1,0,0),color=color.red),
                v1=vertex(pos=rocket_parts[0].pos+1.5*rocket_parts[0].size.y*vector(-1,0,0),color=color.red),
                v2=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(-1,2,0),color=color.red) ))
rocket_parts.append(triangle( v0=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(0,0,1),color=color.red),
                v1=vertex(pos=rocket_parts[0].pos+1.5*rocket_parts[0].size.y*vector(0,0,1),color=color.red),
                v2=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(0,2,1),color=color.red) ))
rocket_parts.append(triangle( v0=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(0,0,-1),color=color.red),
                v1=vertex(pos=rocket_parts[0].pos+1.5*rocket_parts[0].size.y*vector(0,0,-1),color=color.red),
                v2=vertex(pos=rocket_parts[0].pos+0.5*rocket_parts[0].size.y*vector(0,2,-1),color=color.red) ))
             
rocket = compound(rocket_parts,pos=vector(0,0,0))
rocket.velocity = vector(0,0,0)
rocket.mass=100.0
rocket.fuel_mass=50.0
rocket.angle=0

initial_mass = rocket.mass + rocket.fuel_mass
initial_fuel_mass = rocket.fuel_mass

propellant = []

graph(fast=True)
r_pos = gcurve(color=color.red)

mdot = 1.0 # Rate of mass loss per time.
dt = 0.001
t = 0
scene.camera.follow(rocket)

ground = box( pos=vector(0,-height/2-0.05,0), color=vector(0.8,0.8,0.8), size=vector(2,0.01,2) )

def force_fun(mass,posn):
    earth = []
    earth.pos=vector(0,-height*100,0)
    earth.mass=1000
    grav = -1*earth.mass/earth.pos.y**2
#    force = mass*vector(0,grav,0)
    
    G = 1 # Change to 6.67e-11 to use real-world values.
    # Calculate distance vector between rocket and earth.
    r_vec = posn-earth.pos
    # Calculate magnitude of distance vector.
    r_mag = mag(r_vec)
    # Calcualte unit vector of distance vector.
    r_hat = r_vec/r_mag
    # Calculate force magnitude.
    force_mag = G*mass*earth.mass/r_mag**2
    # Calculate force vector.
    force = -force_mag*r_hat

    return force

n = 1 # Count of the number of frames since the last propellant was displayed.
np = 10 # Number of frames between displaying propellant.

angle_amplitude = pi/5
angle_period = 10
angle = rocket.angle

attach_trail(rocket,radius=0.01)

while (rocket.fuel_mass > 0):
    rate(10000)
    new_angle = angle_amplitude*sin(2*pi*t/angle_period)
    rocket.rotate(angle=new_angle-rocket.angle,axis=vector(0,0,1))
    rocket.angle = new_angle
    exhaust_velocity = -100*vector(sin(rocket.angle),cos(rocket.angle),0)
    dm = mdot*dt # Amount of mass lost in time dt.
    if (rocket.pos.y > 0):
        force = force_fun(rocket.mass+rocket.fuel_mass,rocket.pos)
    else:
        force = vector(0,0,0)
    n = n + 1
    if (n==np):
        propellant.append( sphere( color=color.green, pos=rocket.pos-height*vector(-sin(rocket.angle),cos(rocket.angle),0), velocity=rocket.velocity+exhaust_velocity, radius=rocket.size.y*0.025, mass=dm ) )
        n = 1
    rocket.velocity = rocket.velocity + dm/(rocket.mass+rocket.fuel_mass)*(-exhaust_velocity) + force/(rocket.mass+rocket.fuel_mass)*dt
    rocket.pos = rocket.pos + rocket.velocity*dt
    rocket.fuel_mass = rocket.fuel_mass - dm
    #rocket.opacity = rocket.fuel_mass/initial_fuel_mass
    for p in propellant:
        p.force = force_fun(p.mass,p.pos)
        p.velocity = p.velocity + p.force/p.mass*dt
        p.pos = p.pos + p.velocity*dt
        if (p.pos.y < ground.pos.y):
            p.pos.y = ground.pos.y
            p.velocity = vector(0,0,0)
            p.visible = False
    t = t + dt
    r_pos.plot(pos=(t,rocket.pos.y))

print((1-rocket.velocity.y/(mag(exhaust_velocity)*log(initial_mass/rocket.mass)))*100,"% decrease in speed due to external forces")

