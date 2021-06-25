class Truck:
    def __init__(self, map, currentlocation, id):
        self.truckID = id
        self.packages = [] # Last in - First out
        self.home = currentlocation
        self.currentLocation = currentlocation
        self.map = map
        self.clock = 0 # Seconds
        self.mileage = 0 # Miles traveled
        self.capacity = 16
        self.dX = 18 # Miles Per Hour
        self.emergencyBeacons = [] # (packageid, time-in-seconds) - when to return to hub for which emergency package
        self.dayCompleted = False

    def loadPackage(self, package):
        self.packages.append(package)

    """
    loadEmergencyPackage(package) :: - loads emergency package in first priority
    and removes emergency beacon.
    Algorithm Complexity: Best Case: O(1) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    Do add package to packages
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    For emergencybeacon in emergencybeacons:
        if emergencybeacon.ID == package.ID: remove emergencybeacon
    """
    def loadEmergencyPackage(self, package):
        # Load emergency package
        self.packages.append(package)
        # Remove emergency beacon by packageID
        """ BC: O(1) AC: O(N) WC: O(N) """
        for i in range(len(self.emergencyBeacons)):
            if(self.emergencyBeacons[i][0] == package.getPackageID()):
                self.emergencyBeacons.pop(i)
                break

    """
    loadPackages(packages) :: - Loads list of packages into truck, or as many as
    capacity allows.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    if capacity allows: load all packages (for loop)
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    else: load as many as possible (for loop)
    """
    def loadPackages(self, packages):
        # If number of prepared packages > capacity: warn operator; load to capacity
        # Else load all packages
        if(len(packages) > self.capacity):
            print()
            print("WARNING - Attempting to load more packages than capacity can handle.")
            print("          Some packages will not be loaded.")
            print()
            # Load to capacity
            """ BC: O(N) AC: O(N) WC: O(N) """
            for i in range(self.capacity):
                self.packages.append(packages[i])
        else:
            """ BC: O(N) AC: O(N) WC: O(N) """
            for i in range(len(packages)):
                self.packages.append(packages[i])

    def unloadPackages(self):
        # Save packages for return
        package_dump = self.packages
        # Empty truck
        self.packages = []
        # Return packages
        return package_dump

    """
    updatePackage(pack) :: bool - Attempts to update package in truck's
    package list.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    For package in packages:
        if package.ID() == pack.ID(): package = pack; return True
    return False
    """
    def updatePackage(self, package):
        # Find package
        """ BC: O(N) AC: O(N) WC: O(N) """
        for i in range(len(self.packages)):
            if(self.packages[i].getPackageID() == package.getPackageID()):
                # Update package
                self.packages[i] = package
                # Return True indicating package was found and updated
                return True
        # Return False indicating package was not found
        return False

    # Travel to next destination
    """
    travel() :: - causes truck to travel to next delivery location.  If
    emergency beacon is lit, return to hub for emergency package.
    Algorithm Complexity - Best Case: O(1) Average Case: O(1) Worst Case: O(1)
    ----------------------------------------------------------------------------
    Do get next location
    Do get distance to next location
    Do increment clock according to distance and speed
    Do set current location to next location
    """
    def travel(self):
        # Retrieve next destination
        next_location = self.packages[-1].getDeliveryAddress()
        # Retrieve distance to next destination
        distance = self.map.getDistance(self.currentLocation, next_location)
        # Increment clock according to truck speed and distance
        time = (((distance / self.dX) * 60) * 60) # ((Hours) Minutes) Seconds)
        self.clock += time
        self.mileage += distance
        # Set self.currentLocation to next_location
        self.currentLocation = next_location


    def deliver(self):
        # If there are no packages, deliver nothing
        if(len(self.packages) <= 0):
            return None
        # Get timestamp for delivery status
        timestamp = self.getTimestamp()
        # Update package status to "Delivered"
        self.packages[-1].setDeliveryStatus("T" + str(self.truckID) + " DELIVERED - " + timestamp)
        # Remove package from truck and return that package
        return self.packages.pop()

    def returnToHub(self):
        # Retrieve distance to next home
        distance = self.map.getDistance(self.currentLocation, self.home)
        # Increment clock according to truck speed and distance
        time = (((distance / self.dX) * 60) * 60) # ((Hours) Minutes) Seconds)
        self.clock += time
        self.mileage += distance
        # Set self.currentLocation to next_location
        self.currentLocation = self.home

    def getTruckID(self):
        return self.truckID

    def getAllPackages(self):
        return self.packages

    """
    getDeadlinePackages(until=None) :: - Retrieves truck's deadline packages.
    Optionally retrieves deadline packages until a certain time.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    for package in packages:
        if deadlinepackages: append to deadline_packages list.
        if deadlinepackages before until: append to deadline_packages list.
    return deadline_packages
    """
    def getDeadlinePackages(self, until=None):
        # Initialize return list
        deadline_packages = []
        # Find all packages with deadlines and append to deadline_packages
        """ BC: O(N) AC: O(N) WC: O(N) """
        for i in range(len(self.packages)):
            if(self.packages[i].getDeliveryDeadline() != 'EOD' and until == None):
                deadline_packages.append(self.packages[i])
            elif(self.packages[i].getDeliveryDeadline() != 'EOD' and until != None):
                if(self.packages[i].getDeliveryDeadline() < until):
                    deadline_packages.append(self.packages[i])
        # Return deadline_packages
        return deadline_packages

    def getClock(self):
        return self.clock

    def getTimestamp(self):
        # Initialize timestamp parts
        hour = 8 # start of day
        minute = 0 # start of day
        second = 0 # start of day
        # Calculate elapsed timestamp parts
        h_elapse = self.clock / (60 * 60) # hours elapsed
        h_elapse_rem = self.clock % (60 * 60) # remaining seconds
        m_elapse = h_elapse_rem / (60) # minutes elapsed
        m_elapse_rem = h_elapse_rem % (60) # remaining seconds
        s_elapse = m_elapse_rem # seconds elapsed
        # Add elapse to initialized timestamp parts
        hour = (hour + h_elapse)
        minute += (minute + m_elapse)
        second += (second + s_elapse)
        # Create timestamp string
        timestamp = str(int(hour)) + ":" + str(int(minute)) + ":" + str(int(second))
        # Return timestamp
        return timestamp

    def getMileage(self):
        return self.mileage

    def getSpeed(self):
        return self.dX

    def getCapacity(self):
        return self.capacity

    def getCurrentLocation(self):
        return self.currentLocation

    def getNextLocation(self):
        return self.packages[-1].getDeliveryAddress()

    def getDayCompleted(self):
        return self.dayCompleted

    def setDayCompleted(self, completed):
        if(completed == True or completed == False):
            self.dayCompleted = completed
        else:
            print("TypeError - Cannot set truck day completed flag to non-boolean")
        return

    def isEmpty(self):
        if(not self.packages):
            return True
        else:
            return False

    def isHome(self):
        if(self.currentLocation == self.home):
            return True
        else:
            return False

    def addEmergencyBeacon(self, packageid, time):
        self.emergencyBeacons.append((packageid, time))

    def __str__(self):
        printstring = ""
        # Print truck information
        printstring += "T" + str(self.truckID) + " "
        printstring += "@ " + self.currentLocation + " "
        printstring += "@ " + self.getTimestamp()
        printstring += "@ " + str(self.getMileage()) + " - "
        # print emergency beacons if exists
        if(self.emergencyBeacons):
            # Identify emergency beacons with pre and post exclamation marks
            printstring += "!!!"
            # print beacons as [packageid]@[beacontime]
            for i in range(len(self.emergencyBeacons)):
                printstring += self.emergencyBeacons[i][0] + "@"
                printstring += str(self.emergencyBeacons[i][1]) + ","
            printstring += "!!! "
        # print cargo contents
        printstring += str([x.getPackageID() for x in self.getAllPackages()])
        return printstring
