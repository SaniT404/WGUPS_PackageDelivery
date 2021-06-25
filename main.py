"""
Collin Walker #000703668
"""

""" Req. A
Algorithm Overview:
The delivery algorithm shall run as follows:
    1Aa.    Sort truck specific packages
    1Ab.    Sort grouped packages
    1Ac.    Add packages to specified truck
    1Ba.    Sort deadline packages by average distance to deadline package nodes.
    1Bb.    Distribute sorted deadline packages into trucks evenly.
    1Ca.    Sort remaining packages by average distance to package nodes.
    1Cb.    Distribute remaining packages to truck capacity - lowest average distance in lower truckids
    1Da.    Generate Delayed Package flags and add to trucks
    2Aa.    Deliver packages according to truck’s load sequence
    2Ab.    Return to hub for delayed package when flag’s pickup time passes. Deliver package.
    2Ac.    Return to hub when truck is empty
    2Ba.    Pickup truck capacity’s worth of packages and continue step 2Aa - 2Ac
"""

"""
Operation time:
Operation time for the package delivery algorithm depends on one primary factor:
the amount of nodes in the graph.  The entire algorithm’s complexity hinges on
the complexity of finding the average distance for each node to all other nodes.
This code was implemented in O(N^2) complexity.  If a way could be found to
reduce this code, the entire algorithm would collapse to a Worst Case complexity
of O(NLogN) in line with the built in python sort() function (detailed under
“Built In Methods”).

Market Adaptability, Scalability, and Maintainability:
    This algorithm is scalable in many ways and not so scalable in other ways.
The biggest breakdown of the solution comes in a large amount of emergency
packages.  Having too many emergency packages will deteriorate the algorithm’s
ability to run it’s efficient route by constantly interjecting deviations in
order to accommodate.  If the number of emergency packages remains low however,
then the program will run fairly efficiently as the number of trucks, packages,
and delivery nodes increase.
    Large amounts of package changes (addresses or otherwise), in conjunction
with a large amount of deadline packages, will degrade performance considerably.
The algorithm plans an efficient route to deliver all packages according to
their deadlines.  Package alterations will interject deviations that degrades
the efficiency of the route.
    Given an average case of emergency packages, package alterations, deadline
packages, and sufficient trucks, this algorithm will scale well according to its
ability to calculate the average distance to all nodes for all nodes - N^2
    One adaptable feature of this algorithm is its ability to deal with both
directed and undirected graphs.  In fact, this algorithm will become more
efficient than other algorithms when given a more directed edge graph.
    One adaptability failure may be a decrease in efficiency when given a highly
clustered graph with a large amount of clusters, due to its method of organizing
packages according to its average distance to all other nodes.
"""




from DataStructures.graph import Graph
from DataStructures.packageinterface import PackageInterface
from package import Package
from truck import Truck
from hub import Hub
import csv

"""
initializeGraph() :: graph - Reads list of nodes from csv, formats node data,
and adds node to graph.  Returns graph when complete.
Algorithm Complexity - Best Case: O(N^2) Average Case: O(N^2) Worst Case: O(N^2)
----------------------------------------------------------------------------
Open CSV File
Get rows from csv.reader
''' BC: O(N) AC: O(N) WC: O(N) '''
For row in rows:
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    If first row: Add vertex to graph for each location
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    else: Add undirected edge to graph
return graph
"""
def initializeGraph():
    nodes = []
    slcgraph = Graph()

    with open('distancetable.csv') as distancetable:
        rows = csv.reader(distancetable, delimiter=',', quotechar='"')
        rownumber = 0
        """ BC: O(N) AC: O(N) WC: O(N) """
        for row in rows:
            # if first row: read the nodes and add to graph
            if(rownumber == 0):
                """ BC: O(N) AC: O(N) WC: O(N) """
                for location in row:
                    lparts = location.split('\n')
                    slcgraph.add_vertex(lparts[1])
                    nodes.append((lparts[1], lparts[0]))
            # else: read weights and add undirected edges to graph
            else:
                currentnode = ''
                """ BC: O(N) AC: O(N) WC: O(N) """
                for i in range(len(row)):
                    # get currentnode
                    if(i == 0):
                        lparts = row[i].split('\n')
                        currentnode = lparts[1].strip()
                    # add undirected weight between colnode(currentnode) and rownode(nodes[i-2][0])
                    if(i > 1 and row[i] != ''):
                        #print(nodes[i-2][0], currentnode)
                        rownode = nodes[i-2][0].strip()
                        slcgraph.add_undirected_edge(currentnode, rownode, row[i])

            rownumber += 1

    return slcgraph

def initializePackageInterface():
    packages = PackageInterface()
    with open('packages.csv') as packagestable:
        rows = csv.reader(packagestable, delimiter=',', quotechar='"')
        rownumber = 0
        for row in rows:
            newpackage = Package(row[0], row[1], row[2], row[4], row[5], row[6], row[7])
            packages.addPackage(newpackage)

    return packages

def initializeTitle():
    print("")
    print("WGUPS - Admin Console")
    print("    Coded by Collin Walker")
    print("")
    return
def initializeMenu():

    print("")
    print("Select an option:")
    print("1) Run work day")
    print("2) Look up packages at time")
    print("3) Exit")
    print("")

    selection = input()
    return selection
""" Req. G """
def initializeLookupByTimeMenu():
    def convertTimeToSeconds(timestring):
        seconds = 0
        ampm = timestring.split()[-1]
        time = timestring.split()[0].split(':')
        hour = int(time[0])
        minute = int(time[1])
        if(ampm == 'pm' and hour != 12):
            hour += 12
        hour -= 8
        seconds += (hour * 60 * 60)
        seconds += (minute * 60)
        return seconds

    time = input("Time (HH:mm [am/pm]): ")
    print("")

    timeseconds = convertTimeToSeconds(time)
    return timeseconds
def initializeExit():
    print("Exiting...")
    print("")
    return


def main():
    # Initialize core components of algorithm
    # Initialize Map (Graph)
    """ BC: O(N^2) AC: O(N^2) WC: O(N^2) """
    route_map = initializeGraph()


    # Print the program title and menu
    initializeTitle()
    selection = initializeMenu()
    # Begin menu loop
    while(selection != 3):
        if(selection == '1'):
            # Initialize Packages and Package Interface
            package_interface = initializePackageInterface()

            # Initialize Hub
            """ BC: O(N) AC: O(N) WC: O(N) """
            hub = Hub(2, '4001 South 700 East', route_map, package_interface) # 2 trucks, address, map
            # Receive packages - sort and load onto trucks
            """ BC: O(N^2) AC: O(N^2) WC: O(N^2) """
            hub.receivePackages(package_interface.getAllPackages())
            hub.work() # BC: O(N^2) AC: O(N^2) WC: O(N^2)
        elif(selection == '2'):
            packagetime = initializeLookupByTimeMenu()
            # Initialize Packages and Package Interface
            package_interface = initializePackageInterface()

            # Initialize Hub
            """ BC: O(N) AC: O(N) WC: O(N) """
            hub = Hub(2, '4001 South 700 East', route_map, package_interface) # 2 trucks, address, map
            # Receive packages - sort and load onto trucks
            """ BC: O(N^2) AC: O(N^2) WC: O(N^2) """
            hub.receivePackages(package_interface.getAllPackages())
            hub.work(time=packagetime)  # BC: O(N^2) AC: O(N^2) WC: O(N^2)
        elif(selection == '3'):
            initializeExit()
            break
        else:
            print("Invalid selection.  Type \"1\", \"2\", or \"3\".")

        # Print menu
        selection = initializeMenu()

def maintwo():
    # Initialize core components of algorithm
    # Initialize Map (Graph)
    """ BC: O(N^2) AC: O(N^2) WC: O(N^2) """
    route_map = initializeGraph()

    # Initialize Packages and Package Interface
    package_interface = initializePackageInterface()

    # Initialize Hub
    """ BC: O(N) AC: O(N) WC: O(N) """
    hub = Hub(2, '4001 South 700 East', route_map, package_interface) # 2 trucks, address, map
    # Receive packages - sort and load onto trucks
    """ BC: O(N^2) AC: O(N^2) WC: O(N^2) """
    hub.receivePackages(package_interface.getAllPackages())

main()
