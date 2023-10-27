from vpython import *
#Web VPython 3.2


scene = canvas(height=200)
graph(height=100)

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

stage1_mass = 130e3
stage1_fuel_mass = 2.290e6-stage1_mass
stage1_burn_time = 168
stage1_mdot = stage1_fuel_mass/stage1_burn_time
stage1_thrust = 35.1e6
stage1_ve = stage1_thrust/stage1_mdot

stage2_mass = 40.1e3
stage2_fuel_mass = 496.2e3-stage2_mass
stage2_burn_time = 360
stage2_mdot = stage2_fuel_mass/stage2_burn_time
stage2_thrust = 5.141e6
stage2_ve = stage2_thrust/stage2_mdot

stage3_mass = 13.5e3
stage3_fuel_mass = 123e3-stage3_mass
stage3_burn_time = 165+335
stage3_mdot = stage3_fuel_mass/stage3_burn_time
stage3_thrust = 1e6
stage3_ve = stage3_thrust/stage3_mdot

rocket.mass=stage1_mass+stage2_mass+stage2_fuel_mass+stage3_mass+stage3_fuel_mass
rocket.fuel_mass=stage1_fuel_mass
rocket.angle=0

initial_mass = rocket.mass + rocket.fuel_mass
initial_fuel_mass = rocket.fuel_mass

propellant = []

graph(fast=True)
r_pos = gcurve(color=color.red)

mdot = stage1_mdot # Rate of mass loss per time.
dt = 0.01
rate_val = 1000000
t = 0
scene.camera.follow(rocket)

ground = box( pos=vector(0,-height/2-0.05,0), color=vector(0.8,0.8,0.8), size=vector(2,0.01,2) )

def force_fun(mass,posn):
    earth = []
    earth.pos=vector(0,-6.371e6,0)
    earth.mass=5.972e24
#    grav = -1*earth.mass/earth.pos.y**2
#    force = mass*vector(0,grav,0)
    
    G = 6.67e-11
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

angle_amplitude = 0
angle_period = 10
angle = rocket.angle

attach_trail(rocket,radius=0.01,retain=500)

while (rocket.fuel_mass > 0):
    rate(rate_val)
    new_angle = angle_amplitude*sin(2*pi*t/angle_period)
    rocket.rotate(angle=new_angle-rocket.angle,axis=vector(0,0,1))
    rocket.angle = new_angle
    exhaust_velocity = -stage1_ve*vector(sin(rocket.angle),cos(rocket.angle),0)
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


# STAGE TWO!

print('Stage two separation at t =',t)

rocket2 = rocket.clone(pos=rocket.pos)
rocket2.angle = rocket.angle
rocket2.velocity = rocket.velocity
rocket2.size = (2/3)*rocket2.size
rocket2.mass = stage2_mass+stage3_mass+stage3_fuel_mass
rocket2.fuel_mass = stage2_fuel_mass
mdot = stage2_mdot # Rate of mass loss per time.
scene.camera.follow(rocket2)

n = 1 # Count of the number of frames since the last propellant was displayed.
np = 10 # Number of frames between displaying propellant.

angle_amplitude = 0
angle_period = 10
angle = rocket2.angle

attach_trail(rocket2,radius=0.01,retain=500)
r2_pos = gcurve(color=color.green)

while (rocket2.fuel_mass > 0):
    rate(rate_val)
    new_angle = angle_amplitude*sin(2*pi*t/angle_period)
    rocket2.rotate(angle=new_angle-rocket2.angle,axis=vector(0,0,1))
    rocket2.angle = new_angle
    exhaust_velocity = -stage2_ve*vector(sin(rocket2.angle),cos(rocket2.angle),0)
    dm = mdot*dt # Amount of mass lost in time dt.
    if (rocket2.pos.y > 0):
        force = force_fun(rocket2.mass+rocket2.fuel_mass,rocket2.pos)
    else:
        force = vector(0,0,0)
    n = n + 1
    if (n==np):
        propellant.append( sphere( color=color.green, pos=rocket2.pos-height*vector(-sin(rocket2.angle),cos(rocket2.angle),0), velocity=rocket2.velocity+exhaust_velocity, radius=rocket2.size.y*0.025, mass=dm ) )
        n = 1
    rocket2.velocity = rocket2.velocity + dm/(rocket2.mass+rocket2.fuel_mass)*(-exhaust_velocity) + force/(rocket2.mass+rocket2.fuel_mass)*dt
    rocket2.pos = rocket2.pos + rocket2.velocity*dt
    rocket2.fuel_mass = rocket2.fuel_mass - dm
    #rocket2.opacity = rocket2.fuel_mass/initial_fuel_mass
    force = force_fun(rocket.mass,rocket.pos)
    rocket.velocity = rocket.velocity + force/rocket.mass*dt
    if (rocket.pos.y > 0):
        rocket.pos = rocket.pos + rocket.velocity*dt
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
    r2_pos.plot(pos=(t,rocket2.pos.y))

# STAGE THREE!

print('Stage three separation at t =',t)

rocket3 = rocket2.clone(pos=rocket2.pos)
rocket3.angle = rocket2.angle
rocket3.velocity = rocket2.velocity
rocket3.size = (2/3)*rocket3.size
rocket3.mass = stage3_mass
rocket3.fuel_mass = stage3_fuel_mass
mdot = stage3_mdot # Rate of mass loss per time.
scene.camera.follow(rocket3)

n = 1 # Count of the number of frames since the last propellant was displayed.
np = 10 # Number of frames between displaying propellant.

angle_amplitude = 0
angle_period = 10
angle = rocket2.angle

attach_trail(rocket3,radius=0.01,retain=500)
r3_pos = gcurve(color=color.blue)

while (rocket3.fuel_mass > 0):
    rate(rate_val)
    new_angle = angle_amplitude*sin(2*pi*t/angle_period)
    rocket3.rotate(angle=new_angle-rocket3.angle,axis=vector(0,0,1))
    rocket3.angle = new_angle
    exhaust_velocity = -stage3_ve*vector(sin(rocket3.angle),cos(rocket3.angle),0)
    dm = mdot*dt # Amount of mass lost in time dt.
    if (rocket3.pos.y > 0):
        force = force_fun(rocket3.mass+rocket3.fuel_mass,rocket3.pos)
    else:
        force = vector(0,0,0)
    n = n + 1
    if (n==np):
        propellant.append( sphere( color=color.green, pos=rocket3.pos-height*vector(-sin(rocket3.angle),cos(rocket3.angle),0), velocity=rocket3.velocity+exhaust_velocity, radius=rocket3.size.y*0.025, mass=dm ) )
        n = 1
    rocket3.velocity = rocket3.velocity + dm/(rocket3.mass+rocket3.fuel_mass)*(-exhaust_velocity) + force/(rocket3.mass+rocket3.fuel_mass)*dt
    rocket3.pos = rocket3.pos + rocket3.velocity*dt
    rocket3.fuel_mass = rocket3.fuel_mass - dm
    #rocket2.opacity = rocket2.fuel_mass/initial_fuel_mass
    force = force_fun(rocket.mass,rocket.pos)
    rocket.velocity = rocket.velocity + force/rocket.mass*dt
    if (rocket.pos.y > 0):
        rocket.pos = rocket.pos + rocket.velocity*dt
    force = force_fun(rocket2.mass,rocket.pos)
    rocket2.velocity = rocket2.velocity + force/rocket2.mass*dt
    if (rocket2.pos.y > 0):
        rocket2.pos = rocket2.pos + rocket2.velocity*dt
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
    r2_pos.plot(pos=(t,rocket2.pos.y))
    r3_pos.plot(pos=(t,rocket3.pos.y))
    
print("launch finished!")