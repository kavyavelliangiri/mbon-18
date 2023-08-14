# Take the healed/repaired swc file and convert from pixel coordinates to um
# Each pixel is 8 nm
# pixel x 8*10^(-3) will convert to um 

import copy

# Import swc file 
f = open('MBON-18-150-healed-repaired.swc')

# Process and load data into a list "original" 
original = []

for line in f:
    line = line.strip()
    columns = line.split()
    columns = [float(x) for x in columns]
    original.append(columns)

print('First 10 lines of file')
for i in range(10):
    print(original[i])
    #print(len(original[i]))

print(int(len(original)))

'''
Example line: 
[4.0, 0.0, 3928.0, 7024.0, 1647.0, 13.8885, 3.0]

7 entries defined as:

line[0] = compartment index
line[1] = structure type identifier (0 is undefined... all lines in this file)
line[2] = x coordinate
line[3] = y coordinate
line[4] = z coordinate
line[5] = radius
line[6] = parent compartment

So, line 2,3,4,5 all need to be scaled appropriately 
and lines 0, 1, and 6 must be integers 
'''

factor = 8*(10**(-3))
scaled = copy.deepcopy(original)
for line in scaled:
    line[0] = int(line[0])
    line[1] = int(line[1])    
    line[2] = factor*line[2]
    line[3] = factor*line[3]
    line[4] = factor*line[4]
    line[5] = factor*line[5]  
    line[6] = int(line[6])                  

print('First 10 lines of scaled file')
for i in range(10):
    print(scaled[i])

print(int(len(scaled)))    
    
    
# Output to file
out = open('MBON-18-150-Janelia-Scaled.swc','w')
for line in scaled:
    line_string = [str(line[i]) for i in range(len(line))]
    new_line = " ".join(line_string)
    new_line2 = new_line+"\n"
    out.writelines(new_line2)
out.close()

print("Finished writing file")


