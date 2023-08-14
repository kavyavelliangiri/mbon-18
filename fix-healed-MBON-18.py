### Resort the healed Janelia file to meet the NEURON constraint that parent id< child id
import statistics
import copy

# Import healed swc morphology file
f = open('healed-150-noheader-structure.swc','r')

# Process and load the data into a list "original"
original = []

for line in f:
    line = line.strip()
    columns = line.split()
    columns = [float(x) for x in columns]
    original.append(columns)

   
print('The length of original is = '+str(len(original)))
print('The entry length of original is '+str(statistics.mean([len(line) for line in original])))


# Now need to expand each line to give a column for new index and new connection partner
# new index | original index | ... | original connection | new connection 
extended = copy.deepcopy(original)
for line in extended:
    line.insert(0, line[0])
    line.insert(-1, line[-1])
    line[0] = int(line[0])
    line[1] = int(line[1])
    line[-2] = int(line[-2])
    line[-1] = int(line[-1])

print('The length of extended is = '+str(len(extended)))
print('The entry length of extended is '+str(statistics.mean([len(line) for line in extended])))

# Sort through extended with condition that parentid > childid, plus for each point confirm that the one it's being connected to was approved and added to the list

'''
Sort through once 
sifted = []
flipped_order = []
others = []

n = 1
for line in extended:
    mod_line = copy.deepcopy(line)
    # Check if it's the root
    if line[-2] == -1:
        mod_line[0] = int(len(sifted)+1)
        sifted.append(mod_line)
        n += 1
        continue
    if (line[1] > line[-2]) and (line[-2] in [sifted[i][1] for i in range(0,len(sifted))]):
        mod_line[0] = int(len(sifted)+1)    
        index = [i for i, value in enumerate(sifted) if value[1] == line[-2]]
        mod_line[-1] = sifted[index[0]][0]
        sifted.append(mod_line)
        continue
    if (line[1] < line[-2]):
        flipped_order.append(line)
        continue
    else:
        others.append(line)
'''
        

# Port sorting over to a function 
        
def sort(inputlist, sortout, reversedout, miscout): 
    for line in inputlist:
        mod_line = copy.deepcopy(line)
        # Check if it's the root
        if line[-2] == -1:
            mod_line[0] = int(len(sortout)+1)
            sortout.append(mod_line)
            continue
        if (line[1] > line[-2]) and (line[-2] in [sortout[i][1] for i in range(0,len(sortout))]):
            mod_line[0] = int(len(sortout)+1)    
            index = [i for i, value in enumerate(sortout) if value[1] == line[-2]]
            mod_line[-1] = sortout[index[0]][0]
            sortout.append(mod_line)
            continue
        if (line[1] < line[-2]):   # if it is flipped in the original, see if connection was already added to sorted list
            if line[-2] in [sortout[i][1] for i in range(0,len(sortout))]:
                mod_line[0] = int(len(sortout)+1)    
                index = [i for i, value in enumerate(sortout) if value[1] == line[-2]]
                mod_line[-1] = sortout[index[0]][0]
                sortout.append(mod_line)               
                continue
            else:  #if not in sorted list, then save for later
                reversedout.append(line)         
                continue
        else:
            miscout.append(line)
		

sifted = []
flipped_order = []
others = []		
		
sort(extended, sifted, flipped_order, others)

        
print('The length of sifted is = '+str(len(sifted)))     # 14
print('The length of flipped_order is = '+str(len(flipped_order)))   # 265
print('The length of others is = '+str(len(others)))    	 # 23210      (total = 23489)


# Deal with reversed order ones
flipped_order.reverse()

flipped_order2 = []
others2 = []
sort(flipped_order, sifted, flipped_order2, others2)

print('Second sort of flipped_order (1) ')
print('The length of sifted is = '+str(len(sifted)))      # 279    (14+265 above)
print('The length of flipped_order2 is = '+str(len(flipped_order2)))    #15
print('The length of others2 is = '+str(len(others2)))    	# 0


# So only remaining points are in others (23210)
flipped_order3 = []
others3 = []
sort(others, sifted, flipped_order3, others3)

print('Third sort of others(1)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order3 is = '+str(len(flipped_order3)))    # 0
print('The length of others3 is = '+str(len(others3)))    	#10

#check formatting of flipped_order2 and others3 to see why there are 15 points left out
#print(flipped_order2)
#print(others3)

flipped_order2.reverse() 

flipped_order4 = []
others4 = []
sort(flipped_order2, sifted, flipped_order4, others4)

print('Fourth sort of flipped_order (2)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order4 is = '+str(len(flipped_order4)))    # 0
print('The length of others4 is = '+str(len(others4))) #0

flipped_order5 = []
others5 = []
sort(others3, sifted, flipped_order5, others5)   

print('Fourth sort of others (3)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order5 is = '+str(len(flipped_order5)))    # 0
print('The length of others5 is = '+str(len(others5))) #0

flipped_order6 = []
others6 = []
sort(flipped_order4, sifted, flipped_order6, others6)   

print('Fourth sort of flipped_order (4)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order6 is = '+str(len(flipped_order6)))    # 0
print('The length of others6 is = '+str(len(others6))) #0


flipped_order7 = []
others7 = []
sort(others5, sifted, flipped_order7, others7)   

print('Fourth sort of others (5)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order7 is = '+str(len(flipped_order7)))    # 0
print('The length of others7 is = '+str(len(others7))) #0

flipped_order8 = []
others8 = []
sort(flipped_order6, sifted, flipped_order8, others8)   

print('Fourth sort of flipped_order (6)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order6 is = '+str(len(flipped_order8)))    # 0
print('The length of others6 is = '+str(len(others8))) #0

flipped_order9 = []
others9 = []
sort(flipped_order8, sifted, flipped_order9, others9)   

print('Fourth sort of flipped_order (8)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order9 is = '+str(len(flipped_order9)))    # 0
print('The length of others9 is = '+str(len(others9))) #0

flipped_order10 = []
others10 = []
sort(flipped_order9, sifted, flipped_order10, others10)   

print('Fourth sort of flipped_order (9)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order10 is = '+str(len(flipped_order10)))    # 0
print('The length of others10 is = '+str(len(others10))) #0

flipped_order11 = []
others11 = []
sort(flipped_order10, sifted, flipped_order11, others11)   

print('Fourth sort of flipped_order (10)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order11 is = '+str(len(flipped_order11)))    # 0
print('The length of others11 is = '+str(len(others11))) #0

flipped_order12 = []
others12 = []
sort(flipped_order11, sifted, flipped_order12, others12)   

print('Fourth sort of flipped_order (11)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order12 is = '+str(len(flipped_order12)))    # 0
print('The length of others12 is = '+str(len(others12))) #0

flipped_order13 = []
others13 = []
sort(others7, sifted, flipped_order13, others13)   

print('Fourth sort of others (7)')
print('The length of sifted is = '+str(len(sifted)))      # 23489  (279 + 23210 in others)
print('The length of flipped_order13 is = '+str(len(flipped_order13)))    # 0
print('The length of others13 is = '+str(len(others13))) #0

# So all points are now sifted!!!!! 

print('Check that the new indices are increasing 1 +=1 to 23489')


intended_indices = [*range(1,23490)]
actual_indices = [i[0] for i in sifted]
if intended_indices == actual_indices:
    print("The indices are all good!")
else:
    print("There is a problem!")


# Check that the new partners are all good. For each point: point(old connection)
# Find the line that has line(old index) = point(old connection)
# Confirm that line(new index) = point(new connection)
good = 0
problems = []
problem_index = []
for point in sifted:
    if point[-1] == -1:
        good += 1
        continue
    if point[-1] > 0:
        partner_index = [i for i, value in enumerate(sifted) if point[-2] == value[1]]
        if point[-1] == sifted[partner_index[0]][0]:
            good += 1
            continue
        else: 
            print('The new index and connection dont match at')
            print(good)
            problems.append(point)
            good += 1
            continue
    else:
        print('A point doesnt have a new index that is numeric')
        problem_index.append(point)
        good += 1
        continue
            
print('If no error messages from connection comparison, look at good number should be 23489')
print(good)            # = 19950!!!!!!!


# Trim off the old indices and connection partners....no longer needed
final = copy.deepcopy(sifted)
for line in final:
    del line[1]
    del line[-2]
    
    
print('The length of final is = '+str(len(original)))   # Should be 19950
print('The entry length of final is '+str(statistics.mean([len(line) for line in final])))  #SHould be 7




# Output to file
out = open('MBON-18-150-healed-repaired.swc','w')


# Output to file
out = open("MBON-18-150-healed-repaired.swc", "w")
for line in final:
    line_string = [str(line[i]) for i in range(len(line))]
    new_line = " ".join(line_string)
    new_line2 = new_line+"\n"
    out.writelines(new_line2)
out.close()

print("Finished writing file")


