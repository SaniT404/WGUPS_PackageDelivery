from DataStructures.graph import Graph
from DataStructures.packageinterface import PackageInterface
from package import Package
from truck import Truck

def printListOfPackages(nameofpackages, packages):
    printpackages = []
    for i in range(len(packages)):
        printpackages.append(packages[i].getPackageID())

    print(nameofpackages + ": ", printpackages)
    return
def printListOfTruckPackages(truck_packages):
    prtruckpackages = []
    for i in range(len(truck_packages)):
        prtruckpackages.append([])
        for j in range(len(truck_packages[i])):
            prtruckpackages[i].append(truck_packages[i][j].getPackageID())
    print("TRUCK PACKAGES: ", prtruckpackages)

class Hub:
    def __init__(self, number_of_trucks, address, map, packageinterface):
        self.trucks = []
        self.receiving = [] # [(truckid, clock)]
        self.packageInterface = packageinterface
        self.address = address
        self.map = map
        self.routes = []
        self.isDayStarted = False
        self.workDayCompleted = False
        # Initialize trucks
        for i in range(number_of_trucks):
            self.trucks.append(Truck(map, address, i+1))

    """
    work(time=-1) :: - Executes work day, delivering packages according to
    special notes and delivery deadlines.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N^2)
    ----------------------------------------------------------------------------
    # Reverse routes for easy removal/traversal
    ''' O(N) AC: O(N) WC: O(N) '''
    Do reverse routes

    ''' O(N) AC: O(N) WC: O(N) '''
    Do distribute packages

    # work day is complete if all packages are delivered.
    # number of trips back to hub is a multiplier and does not affect
    # delivering number of package's complexity.
    While work day not complete:
        # x number of trucks is multiplier, not packages,
        # therefore have no impact on complexity.
    	For truck in trucks:
            ''' BC: O(N) AC: O(N) WC: O(N) '''
    		While truck not empty:
    			If time != -1 and truck clock has reached or will reach time in 1 turn: break
    			Do truck travel
                Do truck deliver
                ''' BC: O(1) AC: O(1) WC: O(N) '''
    			Do update package
    		If truck clock has reached time: work day complete; break
    		Elif packages still exist: return to hub.
    		If work day completed: mark truck completed
    		If all trucks have completed work day: workday is completed
        ''' BC: O(N) AC: O(N) WC: O(N) '''
    	If work day not completed: distributePackages()
    return
    """

    def work(self, time=-1):
        # Set work day completed flag to false
        self.workDayCompleted = False
        # Set time flag to false
        reachedtime = False

        print("STARTING DAY")

        # Reverse routes for easy removal/traversal
        self.routes.reverse()
        for tripi in range(len(self.routes)):
            for trucki in range(len(self.routes[tripi])):
                self.routes[tripi][trucki][0].reverse()
        # Distribute first trip's packages
        self.distributePackages()

        # Mark start of day
        self.isDayStarted = True
        """ Number of trips is multiplier, """
        """ therefore has no effect on complexity. """
        while(not self.workDayCompleted):
            """ Number of trucks is multiplier, therefore no effect on complexity."""
            for i in range(len(self.trucks)):
                # Set work day completed flag to True - do all required work, then compare truck completion at end to see if this is still true.  If not, continue working
                self.workDayCompleted = True
                """ BC: O(N) AC: O(N) WC: O(N) """
                while(not self.trucks[i].isEmpty()):
                    # If time constraint is specified: check truck time and exit
                    #   truck's work day when you reach time constraint
                    if(time != -1):
                        # Get current truck time
                        trucktime = self.trucks[i].getClock()
                        # Get current truck's next travel time
                        trucknexttraveltime = self.map.calculateRouteTimeSeconds([self.trucks[i].getCurrentLocation(), self.trucks[i].getNextLocation()], self.trucks[i].getSpeed())
                        # If next travel will exceed time constraint or current truck clock is equal to time constraint
                        if((trucktime < time and (trucknexttraveltime + trucktime) > time) or (trucktime == time)):
                            # Indicate that truck has reached time constraint
                            reachedtime = True
                            # Break loop; move to next truck.
                            break

                    # Travel to next package address
                    self.trucks[i].travel()

                    # Deliver the package
                    delivered_package = self.trucks[i].deliver()
                    # Update package interface with delivered package
                    """ BC: O(1) AC: O(1) WC: O(N) """
                    self.packageInterface.updatePackage(delivered_package)
                # If time constraint was specified and reached
                if(reachedtime):
                    # Reset reachedtime indicator
                    reachedtime = False
                    if(i == len(self.trucks) - 1):
                        self.workDayCompleted = True
                        break
                # If packages exist at hub, return
                elif(self.routes):
                    # Return to hub
                    self.trucks[i].returnToHub()

                # Check if truck day is finished (if truck is empty and no packages left at hub)
                if( not self.trucks[i].getAllPackages() and (not self.routes)):
                    # Indicate truck work day is completed
                    self.trucks[i].setDayCompleted(True)
                # If even one truck work day is not completed, self.workDayCompleted will evaluate to False; work continues
                self.workDayCompleted = self.workDayCompleted and self.trucks[i].getDayCompleted()
            # If workday not completed, sort onhold_packages and remaining_packages into trucks
            if(not self.workDayCompleted):
                self.distributePackages()


        print()
        print()
        print()
        print("PACKAGES:")
        print(self.packageInterface)
        for i in range(len(self.trucks)):
            print("T" + str(self.trucks[i].getTruckID()) + " Clock: ", self.trucks[i].getTimestamp(), " - ", self.trucks[i].getClock(), " Mileage: ", self.trucks[i].getMileage(), " Mi.")

        return

    """
    distributePackages(packages) :: - Distributes sorted/received packages into trucks available for receiving.
    Algorithm Complexity - Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    Get next truck routes from end of self.routes
    For each truck:
        ''' BC: O(N) AC: O(N) WC: O(N) '''
        Load packages onto truck
    return

    """

    def distributePackages(self):
        routes = self.routes.pop(-1)
        for trucki in range(len(routes)):
            """ BC: O(N) AC: O(N) WC: O(N) """
            self.trucks[trucki].loadPackages(routes[trucki][0])


    """
    receivePackages(packages) ::  - Take packages, call package sorting, and
    prepare them in hub.
    Algorithm Complexity: Best Case: O(N^2) Average Case: O(N^2) Worst Case: O(N^2)
    ----------------------------------------------------------------------------
    ''' BC: O(N^2) AC: O(N^2) WC: O(N^2) '''
    routes = sortPackages()

    For trip in routes:
        for truck in trip:
            Remove placeholder package
            ''' BC: O(N) AC: O(N) WC: O(N) '''
            for package in truck:
                If not first trip: Set package status to 'Awaiting pickup'
                If first trip: Set package status to 'Out for Delivery'
                If package.earliestLoadTime: Set package status to 'Delayed'
    Return

    """

    def receivePackages(self, packages):
        # Sort receiving packages
        """  """
        self.routes = self.sortPackages(packages)

        for tripi in range(len(self.routes)): # trips
            for trucki in range(len(self.routes[tripi])): # trucks
                # Remove the placeholder package at the beginning of each truck route
                del self.routes[tripi][trucki][0][0]
                packagestr = ""
                for packi in range(len(self.routes[tripi][trucki][0])): # packages
                    package = self.routes[tripi][trucki][0][packi]
                    packagestr += str(package.getPackageID()) + ", "
                    if(tripi > 0):
                        # Set package status to "Awaiting pickup from hub"
                        package.setDeliveryStatus("Awaiting pickup from hub")
                        """ BC: O(1) AC: O(1) WC: O(N) """
                        self.packageInterface.updatePackage(package)
                    if(tripi == 0):
                        # Set package status to "Awaiting pickup from hub"
                        package.setDeliveryStatus("Out for Delivery")
                        """ BC: O(1) AC: O(1) WC: O(N) """
                        self.packageInterface.updatePackage(package)
                    if(package.getEarliestDeliveryTime()):
                        # Set package status to "Delayed"
                        package.setDeliveryStatus("Delayed")
                        """ BC: O(1) AC: O(1) WC: O(N) """
                        self.packageInterface.updatePackage(package)

        return

    """
    sortPackages(packages) :: returns sortedPackages - This method parses
    package notes, and sorts them into truck routes and trips.
    Algorithm Complexity - Best Case: O(N^2) Average Case: O(N^2) Worst Case: O(N^2)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    For package in packages
    	package.parseNotes()
    	Do sort into list queues
    # while merge not complete is multiplier, therefore does not affect complexity.
    While merge not completed:
        ''' BC: O(1) AC: (logN) WC: O(N) '''
        ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
        '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
        ''' the two loops are fundamentally tied to eachother because as one increases, the other decreases. '''
    	For groupedpackage in grouped_packages:
    		For packagenumber in groupedpackage:
    			If packagenumber in other groupedpackage:  Merge groupedpackage
    # Replace grouped packageIDs with actual package
    ''' BC: O(1) AC: (logN) WC: O(N) '''
    ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
    '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
    ''' the two loops are fundamentally tied to eachother because as one increases, the other decreases. '''
    For groupedpackage in grouped_packages:
        For packagenumber in groupedpackage:
            ''' O(1) AC: O(1) WC: O(N) '''
            packagenumber = lookupPackage(packagenumber)

    ''' BC: O(N) AC: O(N) WC: O(N) '''
    ''' First two while loops ensure each package is addressed. '''
    While packages exist not in routes:
        Generate object to hold trip
        while trip's route not completed:
            if truck capacity allows:
                ''' BC: O(N) AC: O(N) WC: O(N) '''
                for package in deadline, remaining, and truck packages:
                    If package location same as last package added's location: add package; move on to next truck
                ''' BC: O(N) AC: O(N) WC: O(N) '''
                If deadline_packages exist: determine most eligible candidate to add
                Else if grouped_packages exist:
                    ''' BC: O(1) AC: (logN) WC: O(N) '''
                    If group's assigned truck is current truck: Add all group packages
                ''' BC: O(N) AC: O(N) WC: O(N) '''
                Else if remaining_packages or truck_packages exist:
                    Determine best candidate package between remaining_packages and truck_packages
            Increment truck
        Increment trip

    return routes
    """
    def sortPackages(self, packages):
        # Initialize sorting containers
        # Create truck package list
        truck_packages = []
        for i in range(len(self.trucks)):
            truck_packages.append([])
        # Create lists of packages that must be grouped together
        grouped_packages = []
        # Create temporary list for all deadline packages
        deadline_packages = []
        # Create temporary list for all remaining packages until sorted
        remaining_packages = []

        # Pre-Sorting procedures
        # Parse each package's notes and add to sorting container
        """ BC: O(N) AC: O(N) WC: O(N) """
        for package in packages:
            package.parseNotes()
            # Prepare "deliver with" packages
            if ('delivered with' in package.getPackageNotes()):
                # Get grouped package numbers
                packagenumbers = package.getPackageNotes().split(', ')
                packagenumbers[0] = packagenumbers[0].split()[-1]
                packagenumbers.append(str(package.getPackageID()))
                # Add to grouped_packages
                grouped_packages.append(packagenumbers)
            # Sort assigned truck packages
            elif(package.getAssignedTruck() != None):
                truck_packages[package.getAssignedTruck() - 1].append(package)
            # Sort remaining packages with deadline into deadline_packages
            elif(package.getDeliveryDeadline() != 'EOD'):
                deadline_packages.append(package)
            # Sort remaining packages
            else:
                remaining_packages.append(package)
        # Combine grouped_packages into largest possible group
        mergecompleted = False
        """ while merge not complete is multiplier of N, because dependent on the inside 2 loops (P1, P2) """
        while(not mergecompleted):
            # Assume merge completed flag true; alter if merge occurs
            mergecompleted = True
            ''' BC: O(1) AC: (logN) WC: O(N) '''
            ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
            '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
            ''' the two loops (P1, P2) are fundamentally tied to eachother because as one increases, the other decreases. '''
            for i in range(len(grouped_packages)): # P1
                # If first iteration, do nothing
                if(i != 0):
                    # Initialize merge list flag
                    mergelists = False
                    # Loop items in last list and check if in current list
                    for item in grouped_packages[i-1]: # P2
                        if(item in grouped_packages[i]):
                            # Set merge list flag if lastpackagelist item is in current package list
                            mergelists = True
                            # Set merge completed flag to false if merge occurs
                            mergecompleted = False
                    if(mergelists):
                        # Merge lists, excluding duplicates
                        grouped_packages[i] = list(set(grouped_packages[i]) | set(grouped_packages[i-1]))
                        # Delete the old list
                        grouped_packages.pop(i-1)
                        break
        # Replace group_packages' package IDs with actual packages
        # Create list to keep track of which group belongs to which truck
        gp_assignedtruck = []
        ''' BC: O(1) AC: (logN) WC: O(N) '''
        ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
        '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
        ''' the two loops (P1, P2) are fundamentally tied to eachother because as one increases, the other decreases. '''
        for i in range(len(grouped_packages)):
            # Populate group assigned truck list with filler data
            gp_assignedtruck.append(-1)
            for j in range(len(grouped_packages[i])):
                # Replace grouped_packages id number with the package itself
                grouped_packages[i][j] = self.packageInterface.lookupPackage(int(grouped_packages[i][j]))

        # Main Greedy Algorithm
        # Initialize index keeping track of trucks' route number
        trip = 0
        # Initialize structure to contain routes.
        routes = [] # list of list of lists - [trip1[[truck1route, mileage], [truck2route, mileage]], trip2[[route1, mileage], [route2, mileage]], ... tripn[[route1, mileage], [route2, mileage]]]
        # Do loop as long as packages still exist in sorting containers
        while(deadline_packages or grouped_packages or remaining_packages or truck_packages):
            # Create n truck number routes and queue subsequent routes.
            # Prepare list to hold truck routes
            if(trip+1 > len(routes)):
                truckroutes = []
                """ Number of trucks is multiplier, therefore no effect on complexity."""
                for i in range(len(self.trucks)):
                    # Place holder package is position 1 - hub.  Will be removed after route generation
                    placeholderpackage = Package(-1, self.address, '', '', '', 0, '')
                    # Add first package and initialize route mileage
                    truckroutes.append([[placeholderpackage], 0]) # (route, mileage)
                # Add list of truck routes for trip to routes
                routes.append(truckroutes)
            # Initialize flag to determine when trip routes are built
            triproutescomplete = False
            # Initialize flag to determine when truck routes for trip are built
            truckroutecomplete = False
            # Initialize index to track current truck
            trucki = 0
            # Do loop until the current trip is generated
            while(not triproutescomplete):
                # Initialize flag to skip truck if needed
                skiptruck = False
                # If truck has space for more packages: find most eligible package
                if(len(routes[trip][trucki][0]) < self.trucks[trucki].getCapacity() + 1):
                    # 1st most eligible package are those with same delivery location.
                    # Initialization
                    foundduplocation = False
                    selectedpackage = None
                    selectedmileage = None
                    # Loop through trucks in current trip
                    """ Number of trucks is multiplier, therefore no effect on complexity."""
                    for truckindex in range(len(routes[trip])):
                        # First order of route generation is to check if package exists with same location as last visited location.
                        """ BC: O(N) AC: O(N) WC: O(N) """
                        # Loop through deadline_packages looking for package with same location as last location
                        for i, package in enumerate(deadline_packages):
                            if(package.getDeliveryAddress() == routes[trip][truckindex][0][-1].getDeliveryAddress()):
                                if(truckindex == trucki):
                                    # If package's earliest load time > mileage time, ignore package.
                                    mileage = routes[trip][trucki][1]
                                    hours = mileage / self.trucks[trucki].getSpeed()
                                    minutes = hours * 60
                                    seconds = minutes * 60
                                    earliestdeliverytime = package.getEarliestDeliveryTime()
                                    if(earliestdeliverytime):
                                        if(seconds < package.getEarliestDeliveryTime()):
                                            continue
                                    # Otherwise set selected package/mileage to be added to route
                                    selectedpackage = package
                                    selectedmileage = 0
                                    foundduplocation = True
                                    # Remove the determined package from source list
                                    del deadline_packages[i]
                                    break
                                else:
                                    continue
                        # If desired package has been found, break loop to go add to truck's route
                        if(foundduplocation):
                            break
                        """ BC: O(N) AC: O(N) WC: O(N) """
                        # Loop through remaining_packages looking for package with same location as last location
                        for i, package in enumerate(remaining_packages):
                            if(package.getDeliveryAddress() == routes[trip][truckindex][0][-1].getDeliveryAddress()):
                                if(truckindex == trucki):
                                    # If package's earliest load time > mileage time, ignore package.
                                    mileage = routes[trip][trucki][1]
                                    hours = mileage / self.trucks[trucki].getSpeed()
                                    minutes = hours * 60
                                    seconds = minutes * 60
                                    earliestdeliverytime = package.getEarliestDeliveryTime()
                                    if(earliestdeliverytime):
                                        if(seconds < package.getEarliestDeliveryTime()):
                                            continue
                                    # Otherwise set selected package/mileage to be added to route
                                    selectedpackage = package
                                    selectedmileage = 0
                                    foundduplocation = True
                                    # Remove the determined package from source list
                                    del remaining_packages[i]
                                    break
                                else:
                                    continue
                        # If desired package has been found, break loop to go add to truck's route
                        if(foundduplocation):
                            break
                        if(truck_packages):
                            """ BC: O(N) AC: O(N) WC: O(N) """
                            for i, package in enumerate(truck_packages[truckindex]):
                                if(package.getDeliveryAddress() == routes[trip][truckindex][0][-1].getDeliveryAddress()):
                                    if(truckindex == trucki):
                                        # If package's earliest load time > mileage time, ignore package.
                                        mileage = routes[trip][trucki][1]
                                        hours = mileage / self.trucks[trucki].getSpeed()
                                        minutes = hours * 60
                                        seconds = minutes * 60
                                        earliestdeliverytime = package.getEarliestDeliveryTime()
                                        if(earliestdeliverytime):
                                            if(seconds < package.getEarliestDeliveryTime()):
                                                continue
                                        # Otherwise set selected package/mileage to be added to route
                                        selectedpackage = package
                                        selectedmileage = 0
                                        foundduplocation = True
                                        # Remove the determined package from source list
                                        del truck_packages[truckindex][i]
                                        break
                                    else:
                                        continue
                        # If desired package has been found, break loop to go add to truck's route
                        if(foundduplocation):
                            break
                    # If package with same location as last package is found, add it to the truck's route
                    if(foundduplocation):
                        # Add package to current truck route
                        routes[trip][trucki][0].append(selectedpackage)
                        # Increment truck route's mileage
                        routes[trip][trucki][1] += selectedmileage
                    # Second order of route generation is to prioritze deadline packages
                    # Prioritize deadline packages by adding to route first.
                    elif(deadline_packages):
                        # Get last package added's vertex to retrieve distance
                        fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                        # Determine soonest deadline with closest distance
                        selectedindex = 0 # initialize selection to first index
                        selectedpackage = deadline_packages[0] # initialize selection to first package
                        selectedmileage = self.map.getDistance(fromv, selectedpackage.getDeliveryAddress())
                        # Loop through each deadline package to find the most eligible package.
                        # Eligibility is determined in the following order:
                        #   deadline > distance
                        """ BC: O(N) AC: O(N) WC: O(N) """
                        for i, package in enumerate(deadline_packages):
                            # Skip 0th index (selection already set)
                            if(i == 0 and len(deadline_packages) != 1):
                                # Check if selected package is in grouped_packages
                                ''' BC: O(1) AC: (logN) WC: O(N) '''
                                ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
                                '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
                                ''' the two loops (P1, P2) are fundamentally tied to eachother because as one increases, the other decreases. '''
                                for j in range(len(grouped_packages)): # P1
                                    if(package in grouped_packages[j]): # P2
                                        # If current truck isn't assigned truck: move on
                                        if(gp_assignedtruck[j] != trucki):
                                            if(len(deadline_packages) != 1):
                                                # Get last package added's vertex to retrieve distance
                                                fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                                # Increment selected package to next package
                                                selectedindex = i+1 # initialize selection to next index
                                                selectedpackage = deadline_packages[i+1] # initialize selection to next package
                                                selectedmileage = self.map.getDistance(fromv, selectedpackage.getDeliveryAddress())
                                            else: # If the length of deadline_packages is 1 and package needs to be on other truck, skip current truck
                                                skiptruck = True
                                # If package's earliest load time > mileage time, increment selected package initialization.
                                mileage = routes[trip][trucki][1]
                                hours = mileage / self.trucks[trucki].getSpeed()
                                minutes = hours * 60
                                seconds = minutes * 60
                                earliestdeliverytime = package.getEarliestDeliveryTime()
                                if(earliestdeliverytime):
                                    if(seconds < package.getEarliestDeliveryTime()):
                                        if(len(deadline_packages) != 1):
                                            # Get last package added's vertex to retrieve distance
                                            fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                            # Increment selected package to next package
                                            selectedindex = i+1 # initialize selection to next index
                                            selectedpackage = deadline_packages[i+1] # initialize selection to next package
                                            selectedmileage = self.map.getDistance(fromv, selectedpackage.getDeliveryAddress())
                                continue
                            # Perform Eligibility checks
                            # Determine if current deadline package is in grouped_packages and whether eligible to add on current truck
                            grouppackageineleigible = False
                            ''' BC: O(1) AC: (logN) WC: O(N) '''
                            ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
                            '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
                            ''' the two loops (P1, P2) are fundamentally tied to eachother because as one increases, the other decreases. '''
                            # See if package is in grouped_packages
                            for j in range(len(grouped_packages)): # P1
                                if(package in grouped_packages[j]): # P2
                                    # If group doesn't have assigned truck, assign it
                                    if(gp_assignedtruck[j] == -1):
                                        gp_assignedtruck[j] = trucki
                                    elif(gp_assignedtruck[j] != trucki): # if current truck isn't assigned truck: move on
                                        grouppackageineleigible = True
                            # If ineligible then move on to next package candidate
                            if(grouppackageineleigible):
                                continue
                            # Determine if duplicate location exists in other truck.  If so, skip package candidate
                            duplicatebelongselsewhere = False
                            """ Number of trucks is multiplier, therefore no effect on complexity."""
                            for truckindex in range(len(routes[trip])):
                                if(package.getDeliveryAddress() == routes[trip][truckindex][0][-1].getDeliveryAddress() and truckindex != trucki):
                                    duplicatebelongselsewhere = True
                            # If duplicate location exists in other truck then move on to the next package candidate
                            if(duplicatebelongselsewhere):
                                continue
                            # If package's earliest load time > mileage time, skip.
                            mileage = routes[trip][trucki][1]
                            hours = mileage / self.trucks[trucki].getSpeed()
                            minutes = hours * 60
                            seconds = minutes * 60
                            earliestdeliverytime = package.getEarliestDeliveryTime()
                            if(earliestdeliverytime):
                                if(seconds < earliestdeliverytime):
                                    continue
                            # Update selection if deadline is sooner or if same but distance is closer
                            if(package < selectedpackage):
                                # Get last package added's vertex to retrieve distance
                                fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                selectedindex = i
                                selectedpackage = package
                                selectedmileage = self.map.getDistance(fromv, package.getDeliveryAddress())
                            elif(package <= selectedpackage):
                                # Get last package added's vertex to retrieve distance
                                fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                packagetov = package.getDeliveryAddress()
                                selectedtov = selectedpackage.getDeliveryAddress()
                                packaged = self.map.getDistance(fromv, packagetov)
                                selectedpackaged = self.map.getDistance(fromv, selectedtov)
                                # If current package is closer than the selected package - reassign selected package
                                if(packaged < selectedpackaged):
                                    # Reassign selected package
                                    selectedindex = i
                                    selectedpackage = package
                                    selectedmileage = packaged
                        # Add package to truck route if not told to skip truck
                        if(not skiptruck):
                            # Remove package from list to indicate addition to route
                            del deadline_packages[selectedindex]
                            # Add package to current truck route
                            routes[trip][trucki][0].append(selectedpackage)
                            # Increment truck route's mileage
                            routes[trip][trucki][1] += selectedmileage
                        else:
                            skiptruck = False
                    # If deadline packages have all been sorted.
                    elif(grouped_packages or remaining_packages or truck_packages):
                        # Initialize flag to indicate whether grouped_packages have been inserted
                        inserted = False
                        # Create list of remaining_packages' IDs for easy reference
                        remaining_packages_ids = [x.getPackageID() for x in remaining_packages]
                        ''' BC: O(1) AC: (logN) WC: O(N) '''
                        ''' if packages(N)=50: at most, group packages can be 25 with 2 elements each. (25 * 2 = 50 = N)     '''
                        '''                     or group packages can be 2 with 25 elements each. (2 * 25 = 50 = N)          '''
                        ''' the two loops (P1, P2) are fundamentally tied to eachother because as one increases, the other decreases. '''
                        # Loop through grouped_packages if current truck is the assigned truck
                        for i in range(len(grouped_packages)): # P1
                            if(gp_assignedtruck[i] == trucki):
                                # Set flag to indicate whether grouped_packages should be inserted
                                doinsert = False
                                # Prepare list to contain indexes of packages needed to delete from grouped_packages
                                deadlinedeletion = []
                                for j in range(len(grouped_packages[i])): # P2
                                    # If package is already in the route, mark for deletion from grouped_packages
                                    if(grouped_packages[i][j] in routes[trip][trucki][0]):
                                        # Mark for deletion
                                        deadlinedeletion.append(j)
                                        # Indicate grouped_packages should be inserted
                                        doinsert = True
                                    # Since inserting packages, we need to remove them from other sorting containers (to prevent duplicates)
                                    pid = grouped_packages[i][j].getPackageID()
                                    if(str(pid) in remaining_packages_ids):
                                        index = remaining_packages_ids.index(pid)
                                        # Remove from remaining_packages
                                        del remaining_packages[index]
                                        del remaining_packages_ids[index]
                                # Remove deadline packages from grouped_packages
                                for j in range(len(deadlinedeletion)):
                                    del grouped_packages[i][deadlinedeletion[j] - j]
                                # Insert grouped_packages according to nearest neighbor
                                if(doinsert):
                                    # Do until all are inserted
                                    while(grouped_packages[i]): # P2
                                        # Get last package added's vertex to retrieve distance
                                        fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                        # Initialize selection to first index
                                        selectedindex = 0
                                        # Initialize selection to first package
                                        selectedpackage = grouped_packages[i][0]
                                        selectedmileage = self.map.getDistance(fromv, selectedpackage.getDeliveryAddress())
                                        # Loop through grouped_packages and determine most eligible candidate to insert
                                        for k, package in enumerate(grouped_packages[i]):
                                            # If package's earliest load time > mileage time, skip.
                                            mileage = routes[trip][trucki][1]
                                            hours = mileage / self.trucks[trucki].getSpeed()
                                            minutes = hours * 60
                                            seconds = minutes * 60
                                            earliestdeliverytime = package.getEarliestDeliveryTime()
                                            if(earliestdeliverytime):
                                                if(seconds < package.getEarliestDeliveryTime()):
                                                    continue
                                            # Get last package added's vertex to retrieve distance
                                            fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                            # determine package distances
                                            packagetov = package.getDeliveryAddress()
                                            selectedtov = selectedpackage.getDeliveryAddress()
                                            packaged = self.map.getDistance(fromv, packagetov)
                                            selectedpackaged = self.map.getDistance(fromv, selectedtov)
                                            # If current package is closer than the selected package - reassign selected package
                                            if(packaged < selectedpackaged):
                                                selectedindex = k
                                                selectedpackage = package
                                                selectedmileage = packaged
                                        # Remove the package from grouped_packages since about to be inserted
                                        del grouped_packages[i][selectedindex]
                                        # Add package to current truck route
                                        routes[trip][trucki][0].append(selectedpackage)
                                        # Increment truck route's mileage
                                        routes[trip][trucki][1] += selectedmileage
                                        # Indicate that package has been inserted
                                        inserted = True
                            # Check if group of packages is emptied
                            if(not grouped_packages[i]):
                                del grouped_packages[i]
                        # If no grouped_packages to add, add from remaining_packages
                        if(not inserted):
                            # Get last package added's vertex to retrieve distance
                            fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                            # initialize selection to first index
                            selectedindex = 0
                            selectedpackage = None
                            selectedfrom = ""
                            selectedmileage = 0
                            # Selection comes from remaining_packages or truck_packages
                            if(remaining_packages):
                                # initialize selection to first package
                                selectedpackage = remaining_packages[0]
                                selectedfrom = "remaining"
                            elif(truck_packages[trucki]):
                                # initialize selection to first package
                                selectedpackage = truck_packages[trucki][0]
                                selectedfrom = "truck"
                            # Get the distance of selected package
                            if(selectedpackage):
                                selectedmileage = self.map.getDistance(fromv, selectedpackage.getDeliveryAddress())
                            """ BC: O(N) AC: O(N) WC: O(N) """
                            # Loop through remaining_packages for candidate
                            for k, package in enumerate(remaining_packages):
                                # If package's earliest load time > mileage time, skip.
                                mileage = routes[trip][trucki][1]
                                hours = mileage / self.trucks[trucki].getSpeed()
                                minutes = hours * 60
                                seconds = minutes * 60
                                earliestdeliverytime = package.getEarliestDeliveryTime()
                                if(earliestdeliverytime):
                                    if(seconds < package.getEarliestDeliveryTime()):
                                        continue
                                # Get last package added's vertex to retrieve distance
                                fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                # initialize selection to first index
                                packagetov = package.getDeliveryAddress()
                                selectedtov = selectedpackage.getDeliveryAddress()
                                packaged = self.map.getDistance(fromv, packagetov)
                                selectedpackaged = self.map.getDistance(fromv, selectedtov)
                                # If current package is closer than the selected package - reassign selected package
                                if(packaged < selectedpackaged):
                                    selectedindex = k
                                    selectedpackage = package
                                    selectedmileage = packaged
                                    # Indicate where package came from in order to delete when done
                                    selectedfrom = "remaining"
                            # If truck_packages exist, loop through them as well to determine route candidate
                            if(truck_packages and truck_packages[trucki]):
                                """ BC: O(N) AC: O(N) WC: O(N) """
                                for k, package in enumerate(truck_packages[trucki]):
                                    # If package's earliest load time > mileage time, skip.
                                    mileage = routes[trip][trucki][1]
                                    hours = mileage / self.trucks[trucki].getSpeed()
                                    minutes = hours * 60
                                    seconds = minutes * 60
                                    earliestdeliverytime = package.getEarliestDeliveryTime()
                                    if(earliestdeliverytime):
                                        if(seconds < package.getEarliestDeliveryTime()):
                                            continue
                                    # Get last package added's vertex to retrieve distance
                                    fromv = routes[trip][trucki][0][-1].getDeliveryAddress()
                                    # initialize selection to first index
                                    packagetov = package.getDeliveryAddress()
                                    selectedtov = selectedpackage.getDeliveryAddress()
                                    packaged = self.map.getDistance(fromv, packagetov)
                                    selectedpackaged = self.map.getDistance(fromv, selectedtov)
                                    # If current package is closer than the selected package - reassign selected package
                                    if(packaged < selectedpackaged):
                                        selectedindex = k
                                        selectedpackage = package
                                        selectedmileage = packaged
                                        # Indicate where package came from in order to delete when done
                                        selectedfrom = "truck"
                            # Delete selected package from source - remaining_packages or truck_packages
                            if(selectedfrom == "remaining"):
                                del remaining_packages[selectedindex]
                            elif(selectedfrom == "truck"):
                                if(truck_packages[trucki]):
                                    del truck_packages[trucki][selectedindex]
                            # Determine if truck_packages still exist
                            truckpackagesempty = True
                            """ Number of trucks is multiplier, therefore no effect on complexity."""
                            for truckpackagegroup in truck_packages:
                                truckpackagesempty = truckpackagesempty and not truckpackagegroup
                            # If not then set to empty list
                            if(truckpackagesempty):
                                truck_packages = []
                            # Add best candidate package to truck's route/mileage
                            if(selectedpackage is not None):
                                # Add package to current truck route
                                routes[trip][trucki][0].append(selectedpackage)
                                # Increment truck route's mileage
                                routes[trip][trucki][1] += selectedmileage
                    else:
                        triproutescomplete = True
                else:
                    # Mark triproutescomplete if all truck routes are complete
                    triproutescomplete = True
                    # Ensure all trip routes are complete
                    """ Number of trips is multiplier, """
                    """ therefore has no effect on complexity. """
                    for i in range(len(routes[trip])):
                        testing = len(routes[trip][i][0]) == self.trucks[i].getCapacity()+1
                        triproutescomplete = triproutescomplete and testing

                # Increment selected truck
                if(trucki < len(self.trucks)-1):
                    trucki += 1
                else:
                    trucki = 0
            # Increment trip after truck trip routes have been determined
            trip += 1

        return routes
