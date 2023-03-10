from math import sqrt, pi , log, sin


def LineCalc(A_coord,B_coord,C_coord,radius,Rac, bundled=False,f= 50, kg = 0.779,dBundle = 0,nBundle=1):
    
    ''' 
    A,B,C coords in format [[x,y]]
    radius: in meters, radius of the conductor
    Rac: Resistance of the conductor in Ohm/km
    f: frequency of the grid
    kg: Coefficient of the conductor
    dBubnle: Distance between conductors
    nBundle: Number of conductors in the bundle
    
    '''  

    if bundled:
        pass

    
    # GMD

    GMDab = 1
    GMDbc = 1
    GMDac = 1

    for A in A_coord:
        for B in B_coord:
            GMDab *= dist(A,B)
    GMDab = (GMDab)**(1/(len(A_coord)*len(B_coord)))

    for A in A_coord:
        for C in C_coord:
            GMDac *= dist(A,C)
    GMDac = (GMDac)**(1/(len(A_coord)*len(C_coord)))

    for C in C_coord:
        for B in B_coord:
            GMDbc *= dist(C,B)
    GMDbc = (GMDbc)**(1/(len(C_coord)*len(B_coord)))


    GMD = (GMDab*GMDbc*GMDac)**(1/3)

    
    print('GMD: ',GMD)
    print('GMDab: ',GMDab)
    print('GMDac: ',GMDac)
    print('GMDbc: ',GMDbc)
    


    # GMR

    if bundled:
        rBundle = dBundle/(2*sin(pi/nBundle))
        GMRbundle = (kg*nBundle*radius*(rBundle)**(nBundle-1))**(1/nBundle)
        rCond = GMRbundle 
        GMR = GMRbundle

        distA = 1
        for A in A_coord:
            for i in range(A_coord.index(A)+1,len(A_coord)):
                distA = dist(A,A_coord[i])
        GMRa = (rCond*distA)**(1/len(A_coord))

        distB = 1
        for B in B_coord:
            for i in range(B_coord.index(B)+1,len(B_coord)):
                distB = dist(B,B_coord[i])
        GMRb = (rCond*distB)**(1/len(B_coord))

        distC = 1
        for C in C_coord:
            for i in range(C_coord.index(C)+1,len(C_coord)):
                distC = dist(C,C_coord[1])
        GMRc = (rCond*distC)**(1/len(C_coord))

        GMR = (GMRa*GMRb*GMRc)**(1/3)


    else:
        rCond = radius

        distA = 1
        for A in A_coord:
            for i in range(A_coord.index(A)+1,len(A_coord)):
                distA = dist(A,A_coord[i])
        GMRa = (kg*rCond*distA)**(1/len(A_coord))

        distB = 1
        for B in B_coord:
            for i in range(B_coord.index(B)+1,len(B_coord)):
                distB = dist(B,B_coord[i])
        GMRb = (kg*rCond*distB)**(1/len(B_coord))

        distC = 1
        for C in C_coord:
            for i in range(C_coord.index(C)+1,len(C_coord)):
                distC = dist(C,C_coord[1])
        GMRc = (kg*rCond*distC)**(1/len(C_coord))

        GMR = (GMRa*GMRb*GMRc)**(1/3)




    # Req
    if bundled:
        rBundle = dBundle/(2*sin(pi/nBundle))
        Reqbundle = (nBundle*radius*(rBundle)**(nBundle-1))**(1/nBundle)
        rCond = Reqbundle
        Req = Reqbundle

    else:
        rCond = radius

    
    distA = 1
    for A in A_coord:
        for i in range(A_coord.index(A)+1,len(A_coord)):
            distA = dist(A,A_coord[1])
    Reqa = (rCond*distA)**(1/len(A_coord))

    distB = 1
    for B in B_coord:
        for i in range(B_coord.index(B)+1,len(B_coord)):
            distB = dist(B,B_coord[1])
    Reqb = (rCond*distB)**(1/len(B_coord))

    distC = 1
    for C in C_coord:
        for i in range(C_coord.index(C)+1,len(C_coord)):
            distC = dist(C,C_coord[1])
    Reqc = (rCond*distC)**(1/len(C_coord))

    Req = (Reqa*Reqb*Reqc)**(1/3)





    # Inductance
    L = 0.2*log((GMD)/GMR) #mH/km  / Should give around 1 mH/km
    Xl = 2*pi*f*L*1000 # Ohm/km

    # Capacitance      
    C = 1000/(18*log(GMD/Req)) # nF/km / around 0-20nF/km in overhead lines
    R = Rac/(len(A_coord)*nBundle)

    print('R= ',R,' L: ', L,'  C: ',C)
    pass


def dist(P1,P2):

    distance = ((P1[0]-P2[0])**2  + (P1[1]-P2[1])**2)**(1/2)
    return distance



# Distances
a = 9   #m
b = 7   #m
c = a   #m
d = 6.5 #m
e = d   #m

# Ejemplo Smart Grids

'''

line = LineCalc(

        A_coord= [[-a/2,d],[c/2,-e]],
        B_coord=[[-b/2,0],[b/2,0]],
        C_coord=[[-c/2,-e],[a/2,d]],

        Rac= 0.062,
        kg=0.809,
        radius=0.03040/2,
        bundled= False,
        )

'''



### Ejercicio Clase Bundled line


line = LineCalc(

        A_coord= [[0,6+7/2]],
        B_coord=[[-4,-7/2]],
        C_coord=[[8,7/2]],

        Rac= 0.062,
        kg=0.809,
        radius=0.03042/2,
        bundled= True,
        nBundle=2,
        dBundle= 0.4
        )


# Ejercicio diapos Double line

'''

line = LineCalc(

        A_coord= [[-3,6],[3,-6]],
        B_coord=[[-3.5,0],[3.5,0]],
        C_coord=[[-3,-6],[3,6]],

        Rac= 0.144,
        kg=0.826,
        radius=0.021/2,
        bundled= False,
        nBundle=1
        )

'''