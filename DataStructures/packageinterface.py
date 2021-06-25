""" Req. D1
The PackageInterface class is a hash table intended to store packages.
It stores packages by packageID with a hashing function that determines where
in the hash table the package should be stored.  The hash function is a simple
modulus of the packageID by the size of the hash table (packageID % N)
"""

class PackageInterface:
    """ BC: O(N) AC: O(N) WC: O(N) """
    def __init__(self, size=40):
        # Initialize Hash Table
        self.packages = []
        self.size = size
        # Populate Hash Table with cells
        """ BC: O(N) AC: O(N) WC: O(N) """
        for i in range(size):
            self.packages.append([])

    # Hash add function
    """ Req. E """
    def addPackage(self, package):
        # Get packageID
        id = int(package.getPackageID())
        # Hash function
        index = id % self.size
        # Add package to hash table
        self.packages[index].append(package)

    """
    updatePackage(updatedpackage) :: isSuccess - Attempts to update package by using
    locating with packageID.  Returns true or false if success or failure.
    Algorithm Complexity: Best Case: O(1) Average Case: O(1) Worst Case: O(N)
        ** If many packages were added after PackageInterface was instantiated,
        ** packageInterface update can devolve to O(N)
    ----------------------------------------------------------------------------
    Get index
    ''' BC: O(1) AC: O(1) WC: O(N) '''
    for package in packages_at_index:
        if uppdatedpackage.packageID == package.packageID: replace package; return true
    return false
    """
    def updatePackage(self, package):
        # Ensure packageID is int; Hash function
        index = int(package.getPackageID()) % self.size
        # Loop through hash cell; Update package if packageID exists and return True
        """ BC: O(1) AC: O(1) WC: O(N) """
        for i in range(len(self.packages[index])):
            pid = int(self.packages[index][i].getPackageID())
            if(pid == package.getPackageID()):
                self.packages[index][i] = package
                return True
        # Return False indicating packageID does not exist
        return False

    # Hash lookup by key function
    """ Req. F """
    """
    lookupPackage(packageID) :: package - Looks up package by key function
    Algorithm Complexity: Best Case: O(1) Average Case: O(1) Worst Case: O(N)
        ** If many packages were added after PackageInterface was instantiated,
        ** packageInterface lookup can devolve to O(N)
    ----------------------------------------------------------------------------
    Get index
    ''' BC: O(1) AC: O(1) WC: O(N) '''
    for package in packages_at_index:
        if package found: return package
    return None
    """
    def lookupPackage(self, packageID):
        # Ensure packageID is int; Hash function
        index = int(int(packageID) % self.size)
        # Loop through hash cell; return package if packageID is matched
        """ BC: O(1) AC: O(1) WC: O(N) """
        for i in range(len(self.packages[index])):
            pid = int(self.packages[index][i].getPackageID())
            if(pid == packageID):
                return self.packages[index][i]
        # Return None if no package was found
        return None

    """
    lookupPackagesByNode(node) :: packagelist - Returns list of packages that
    have a delivery address of given node.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N^2)
        ** If many packages were added after PackageInterface was instantiated,
        ** packageInterface lookup can devolve to O(N^2)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    For hashcell in hashtable:
        ''' BC: O(1) AC: O(1) WC: O(N) '''
        For package in hashcell:
            If package.deliveryaddress == node: Add package to packagelist
    return packagelist
    """
    def lookupPackagesByNode(self, node):
        # Initialize packages to return
        returnlist = []
        # Loop Hash table
        """ BC: O(N) AC: O(N) WC: O(N) """
        for i in range(len(self.packages)):
            # Loop Hash cell
            """ BC: O(1) AC: O(1) WC: O(N) """
            for j in range(len(self.packages[i])):
                # If package delivery address is == node, append to return list
                if(self.packages[i][j].getDeliveryAddress() == node):
                    returnlist.append(self.packages[i][j])
        # Return packages if returnlist len > 0
        if(len(returnlist) > 0):
            return returnlist
        # Return None if no packages were found
        return None

    """
    getAllPackages() :: allpackages - Returns all packaages in a list.
    Algorithm Complexity: Best Case: O(N) Average Case: O(N) Worst Case: O(N^2)
        ** If many packages were added after PackageInterface was instantiated,
        ** packageInterface lookup can devolve to O(N^2)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    For hashcell in hashtable:
        ''' BC: O(1) AC: O(1) WC: O(N) '''
        For package in hashcell:
            Do add package to allpackages
    return allpackages
    """
    def getAllPackages(self):
        allpackages = []
        """ BC: O(N) AC: O(N) WC: O(N) """
        for list in self.packages:
            """ BC: O(1) AC: O(1) WC: O(N) """
            for package in list:
                allpackages.append(package)

        return allpackages

    def __str__(self):
        printstring = ''
        for list in self.packages:
            for package in list:
                printstring += str(package) + '\n'

        return printstring
