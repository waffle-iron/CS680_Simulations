'''
Jacob McKenna
UAF CS 680 Discrete Event Simulation 
Server Class 
'''
import time # Used for the clock (seconds).
import Server
import Customers
import random as rd
import matplotlib.pyplot as plt
import FEL

from collections import deque

### Clock code from following link, 
### http://codereview.stackexchange.com/questions/26534/is-there-a-better-way-to-count-seconds-in-python
###
class Simulation():

    def __init__(self, numCust):

        self.simClock = 0
        self.FEL = FEL.FEL()
        # FEL list for now, no proper FEL is in place yet.
        # Represents customers. I'll use a class to represent this later.
        self.maxQueueLength = 0


        self.averageQueueLength = 0
        self.queue = deque()
        self.averageQueueLengthPerSecond = [] # Holds a list of average queue length over time. 

        self.servedCustomers = 0 # Both used to track when all customers have been served.
        self.totalCustomers = numCust 

        clock = 0
        for _ in range(self.totalCustomers):
            time = rd.randint(cAm, cAM)
            clock += time 
            self.arrivalTimes.append(clock)

        self.lastCustomerTime = self.arrivalTimes[-1]

    def beginServing1(self):
        self.server1.startService()

    def beginServing2(self):
        self.server2.startService()

    def serve1(self):
        self.server1.serveTheCustomer()

    def serve2(self): ### Debug Function ###
        self.server2.serveTheCustomer()

    def printServerResults(self):
        self.server1.printServerTimes()
        self.server2.printServerTimes()

    # Functions used for statistical purposes. 
    def setAndPrintServerResults(self):
        self.server1ServerTimes = self.server1.getServerTimes()
        self.server2ServerTimes = self.server2.getServerTimes()

        average1 = sum(self.server1ServerTimes)/self.simClock
        print("The average Busy Time for Server One is %f." % (average1))

        if len(self.server1ServerTimes) == 0:
            print("The average Serve Time for Server One is %.3f. No customers served." % (0))
        else:
            average1 = sum(self.server1ServerTimes)/len(self.server1ServerTimes)
            print("The average Serve Time for Server One is %.3f." % (average1))

        average2 = sum(self.server2ServerTimes)/self.simClock
        print("The average Busy Time for Server One is %f." % (average2))

        if len(self.server2ServerTimes) == 0:
            print("The average Serve Time for Server Two is %.3f. No customers served." % (0))
        else:
            average2 = sum(self.server2ServerTimes)/len(self.server2ServerTimes)
            print("The average Serve Time for Server Two is %.3f." % (average2))

    ''' 
    I chose to average the time over the entire simulation, even though the end period may be longer
    than the last customer served. Until I can refactor this into a proper Future Event List, this will be the optimal
    solution until then. 
    '''
        
    def incrementWaitTime(self):
        self.waitTime += len(self.queue)

    def finalizeWaitTime(self):
        holder = (self.waitTime / self.simClock)
        return holder

    def startSim(self, name):

        waitTimes = []

        # print(self.arrivalTimes) # Testing times, functions correctly. 

        myIter = 0 

        print(self.arrivalTimes)
        while 1:

            self.serve1()
            self.serve2()
            self.incrementWaitTime()

            if self.arrivalTimes[myIter] == self.simClock:

                self.queue.append(self.arrivalTimes[myIter])
                self.queueLengths.append(len(self.queue))

                if self.maxQueueLength < len(self.queue):
                    self.maxQueueLength = len(self.queue)

                # print("Line length %d" % len(self.queue))

                myIter += 1
                if myIter == self.totalCustomers:
                    myIter = self.totalCustomers - 1

            # The first available server will be selected to serve the next customer.
            # Server One is the default Server. 
            if (not self.server1.getBusyState() and len(self.queue) > 0):
                self.queue.popleft()
                self.beginServing1()
                self.serve1()
                self.servedCustomers += 1
                # print("\nServer One Now serving next customer at time %d.\n" % (self.simClock))

            if (not self.server2.getBusyState() and len(self.queue) > 0):
                self.queue.popleft()
                self.beginServing2()
                self.serve2()
                self.servedCustomers += 1

                # print("\nServer Two Now serving next customer at time %d.\n" % (self.simClock))

            # else:

                # print("No customer to serve or both servers are busy.")
            holder = self.finalizeWaitTime()
            waitTimes.append(holder)
            print("The average wait time right now is %f at time %d." %(self.waitTime, self.simClock))
            self.simClock += 1

            ##############################################################################
            ''' Uncomment print functions and change speed to see results in real time!'''
            ##############################################################################
            time.sleep(.0001) # 1000 iterations/simulation seconds per second. Used to quickly speed up a simulation. 
            print("The total number of customer is = %d." %(self.totalCustomers))
            if (not self.server1.getBusyState() and not self.server2.getBusyState() and self.servedCustomers == self.totalCustomers):
                break


        # print("End of Simulation %s." % (name))
        # self.setAndPrintServerResults()
        # self.finalizeWaitTime()
        # print("The maximum queue length is %d." % (self.maxQueueLength))
        # print("Server One Serve Rate = [%d, %d]." %(self.s1m, self.s1M))
        # print("Server One Serve Rate = [%d, %d]." %(self.s2m, self.s2M))
        # print("Customer Arrival Rate = [%d, %d]." %(self.cAm, self.cAM))
        # print("Average Wait Time is %03f.\n" % (self.waitTime))

        plt.plot(waitTimes)
        plt.title("Figure " + str(name) + " for Queue Lengths")
        plt.xlabel("times(s)")
        plt.ylabel("Average Wait Time")
        plt.savefig("Sim_" + str(name) + "_for_ql.png")
        plt.clf()

        # plt.plot(self.server1ServerTimes)
        # plt.title("Figure " + str(name) + " for Server One")
        # plt.xlabel("# of Customers Served")
        # plt.ylabel("Serve Time")
        # plt.savefig("Sim_" + str(name) + "_for_s1.png")
        # plt.clf()

        # plt.plot(self.server2ServerTimes)
        # plt.title("Figure " + str(name) + " for Server Two")
        # plt.xlabel("# of Customer Served")
        # plt.ylabel("Serve Time")
        # plt.savefig("Sim_" + str(name) + "_for_s2.png")
        # plt.clf()



