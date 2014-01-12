# Aerofoil .dat to .geo file converter
""" firstly, we ask the user to provide us the name of the dat file"""
tries = 0

while tries <= 3:
        datfile = input ('Please enter the name of aerofoil file (without the .dat)\n')
        aero = open(datfile + '.dat', 'r')
        for line in aero:
                print(line,'')
        correct = input ('Is this the correct file? Y/N \n')
        if correct == 'Y' or correct.upper() == 'Y':
                print ('Creating new mesh....')
                break
        elif tries == 2:
                print ('Too many incorrect inputs \n')
                break
        else:
                print ('Please reinput your aerofoil \n')
                tries += 1

""" next, we create the new geo file"""
mesh = open(datfile + '.geo', 'r+')
aero = open(datfile + '.dat', 'r')
""" this section creates the points for the mesh and set up the spline"""
linecnt = 0
spline = []
for line in aero:
        linecnt +=1
        new = line.split(' ')
        if len(new) == 5 and linecnt >3:
                mesh.write('Point(%s) = {%s, %s, 0, 0.15}; \n' % (str(linecnt-3),str(new[-3]),str(new[-1]).replace('\n','')))
                spline.append(linecnt-3)
        elif len(new) == 4 and linecnt >3:
                mesh.write('Point(%s) = {%s, %s, 0, 0.15}; \n' % (str(linecnt-3),str(new[-2]),str(new[-1]).replace('\n','')))
                spline.append(linecnt-3)

"""this section determines whether an extra line is required to close off the aerofoil"""
extraline = False
with open(datfile + '.dat','r')as aero:
        lines = aero.readlines()
        if lines[3] == lines[int(linecnt/2)+2]:
                extraline = True
"""time to close the original .dat file"""
aero.close()

""" this section created the spline"""
spline = spline[int((linecnt/2)-3)::-1]
splines ='Spline(1) ={'+(str(spline))+'}'
splines = splines.replace('[','')
splines = splines.replace(']','')
mesh.write(splines)
   
mesh.close()

