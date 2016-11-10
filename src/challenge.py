import sys
import numpy
from datetime import datetime
from decimal import Decimal

def main(infile,outfile):
    ifile = open(infile,'r')
    ofile = open(outfile,'w')
    x = ifile.tell()
    firstline = ifile.readline()
    s = 'created_time": "'
    firsta = firstline.find(s)
    firstb = firstline.find('"',firsta+len(s))
    firstt = firstline[firsta+len(s):firstb]
    firsttime = datetime.strptime(firstt,"%Y-%m-%dT%H:%M:%SZ")
                                    
    testtime = firsttime
    myarray = []
    acc_array = []
    graph_array = []
    ifile.seek(x)
    for line in ifile:
        #re-null variables for each line
        t = ''
        target = ''
        actor = ''
        #get time, target, and actor for each line from file
        s = 'created_time": "'
        a = line.find(s)
        b = line.find('"',a+len(s))
        t = line[a+len(s):b]
        ts = datetime.strptime(t,"%Y-%m-%dT%H:%M:%SZ")        
        difference = ts-testtime
        ss = '"target": "'
        aa = line.find(ss)
        bb = line.find('"',aa+len(ss))
        target = line[aa+len(ss):bb]
        sss = '"actor": "'
        aaa = line.find(sss)
        bbb = line.find('"',aaa+len(sss))
        actor = line[aaa+len(sss):bbb]
        #check if any of the fields are empty
        if (target != '' and actor != '' and t != ''):
            myarray.append([ts,target,actor])
            if (actor in acc_array):
                j = acc_array.index(actor)
                graph_array[j]+=1
            else:
                acc_array.append(actor)
                graph_array.append(1)
            if (target in acc_array):
                j = acc_array.index(target)
                graph_array[j]+=1
            else:
                acc_array.append(target)
                graph_array.append(1)
            myarray = sorted(myarray,key=lambda l:l[0])
            #If the difference in time from the current time is greater than 60 then remove that entry from the list
            if (difference.total_seconds() > 60 ):
                for i in myarray:
                    if ((ts - i[0]).total_seconds() > 60):
                        graph_array[acc_array.index(i[1])] -=1
                        graph_array[acc_array.index(i[2])] -=1
                        myarray.remove(i)
                    else:
                        testtime = i[0]
                        break
            #write to the output file the median without including the zeros
            x = Decimal(numpy.median(numpy.asarray(graph_array)[numpy.nonzero(numpy.asarray(graph_array))]))
            out = str.format("{0:.2f} \n",x)
            ofile.write(out)
        
main(sys.argv[1],sys.argv[2])
