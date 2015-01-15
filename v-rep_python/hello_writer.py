import vrep
import numpy
import time
import sys

import matplotlib.pyplot as plt

hello = numpy.genfromtxt('hello.csv',delimiter=',',skip_header=3,usecols = (1, 2, 3),dtype=numpy.float)
object_name = 'feltPen_invisible'
# object_name = 'Sphere'

plt.figure()
plt.plot(-hello[300:,0],-hello[300:,1])
plt.show()



hello = numpy.array(hello[300:523+300,[0,1]])

hello[:,0] = -(hello[:,0]-hello[0,0])/2.0
hello[:,1] = -(hello[:,1]-hello[0,1])/2.0


print 'Program started'
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print 'Connected to remote API server'
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait)
    if res==vrep.simx_return_ok:
        print 'Number of objects in the scene: ',len(objs)
        res,v0=vrep.simxGetObjectHandle(clientID,object_name,vrep.simx_opmode_oneshot_wait)
        print "Ok, I'm in!"
        # Reads the pen position X,Y,Z
        res,pos=vrep.simxGetObjectPosition(clientID,v0,vrep.sim_handle_parent,vrep.simx_opmode_oneshot_wait)
        print "Initial Position", pos
        # sys.exit()
        i = 0
        for hi in hello:
            time.sleep(0.05)
            cmd_pos = numpy.array(pos)+numpy.concatenate([hi,[0]]) # Sums X and Y
            print "Cmd Position: ", i, hi, cmd_pos
            i+=1
            # Sets the new position
            res = vrep.simxSetObjectPosition(clientID,v0,vrep.sim_handle_parent,cmd_pos,vrep.simx_opmode_oneshot_wait)
            if res!=0:
                vrep.simxFinish(clientID)
                print 'Remote API function call returned with error code: ',res
                break
        cmd_pos = numpy.array(pos)+numpy.concatenate([hello[-1],[0.05]]) # lift the pen
        res = vrep.simxSetObjectPosition(clientID,v0,vrep.sim_handle_parent,cmd_pos,vrep.simx_opmode_oneshot_wait)
        time.sleep(0.05)
        final_pos = numpy.concatenate([[-0.6019,0.2206],[cmd_pos[2]]])
        dif_pos = final_pos - cmd_pos
        dif_pos = dif_pos/10.0
        for i in range(10):
            cmd_pos = cmd_pos+dif_pos#numpy.concatenate([[-0.6019,0.2206],[cmd_pos[2]]]) # lift the pen
            res = vrep.simxSetObjectPosition(clientID,v0,vrep.sim_handle_parent,cmd_pos,vrep.simx_opmode_oneshot_wait)
            time.sleep(0.05)

    else:
        print 'Remote API function call returned with error code: ',res
    vrep.simxFinish(clientID)
else:
    print 'Failed connecting to remote API server'
print 'Program ended'