class Package:
    def __init__(self, id, address, city, zipcode, deadline, weight, notes):
        self.packageID = id
        self.deliveryAddress = address
        self.deliveryCity = city
        self.deliveryZipCode = zipcode
        self.deliveryDeadline = deadline
        self.deliveryWeight = weight
        self.deliveryStatus = ""
        self.packageNotes = notes
        self.earliestDeliveryTime = None
        self.assignedTruck = None

    def parseNotes(self):
        # Set Earliest Load Time from Delay
        if ('Delayed' in self.getPackageNotes()):
            # Initialize deadline
            secondsdelayed = 0
            # Extract arrival time
            delaynotes = self.packageNotes.split()
            ampm = delaynotes[-1]
            time = delaynotes[-2]
            # Convert arrival time to seconds
            time = time.split(':')
            hour = int(time[0])
            minute = int(time[1])
            if(ampm == 'pm'):
                hour += 12
            hour -= 8
            secondsdelayed += (hour * 60 * 60)
            secondsdelayed += (minute * 60)
            # Set Earliest Load Time to secondsdelayed
            self.setEarliestDeliveryTime(secondsdelayed)
        # Set Earliest Load Time from Wrong Address
        if('Wrong address' in self.getPackageNotes()):
            # delay package until 10:20
            secondsdelayed = 0
            hour = 2
            minute = 20
            secondsdelayed += (hour * 60 * 60)
            secondsdelayed += (minute * 60)
            self.setEarliestDeliveryTime(secondsdelayed)
            # Set package address to 410 S State St., Salt Lake City, UT 84111
            self.setDeliveryAddress('410 S State St')
            self.setDeliveryCity('Salt Lake City')
            #self.setDeliveryState('UT')
            self.setDeliveryZipCode('84111')
        if('on truck' in self.getPackageNotes()):
            # Extract assigned truck
            trucknotes = self.packageNotes.split()
            # Assign truck
            self.setAssignedTruck(int(trucknotes[-1]))


    # Getters
    def getPackageID(self):
        return self.packageID

    def getDeliveryAddress(self):
        return self.deliveryAddress

    def getDeliveryDeadline(self):
        return self.deliveryDeadline

    def getDeliveryDeadlineSeconds(self):
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
        seconds = 0
        if(self.getDeliveryDeadline() != 'EOD'):
            seconds = convertTimeToSeconds(self.deliveryDeadline)
        return seconds

    def getDeliveryCity(self):
        return self.deliveryCity

    def getDeliveryZipCode(self):
        return self.deliveryZipCode

    def getDeliveryWeight(self):
        return self.deliveryWeight

    def getDeliveryStatus(self):
        return self.deliveryStatus

    def getPackageNotes(self):
        return self.packageNotes

    def getEarliestDeliveryTime(self):
        return self.earliestDeliveryTime

    def getAssignedTruck(self):
        return self.assignedTruck

    # Setters
    def setDeliveryAddress(self, address):
        self.deliveryAddress = address
        return

    def setDeliveryDeadline(self, deadline):
        self.deliveryDeadline = deadline
        return

    def setDeliveryCity(self, city):
        self.deliveryCity = city
        return

    def setDeliveryZipCode(self, zipcode):
        self.deliveryZipCode = zipcode
        return

    def setDeliveryWeight(self, weight):
        self.deliveryWeight = weight
        return

    def setDeliveryStatus(self, status):
        self.deliveryStatus = status
        return

    def setPackageNotes(self, notes):
        self.packageNotes = notes
        return

    def setEarliestDeliveryTime(self, earliestdeliverytime):
        self.earliestDeliveryTime = earliestdeliverytime
        return

    def setAssignedTruck(self, assignedtruck):
        self.assignedTruck = assignedtruck
        return

    def __lt__(self, other):
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
        self_deadline = convertTimeToSeconds(self.getDeliveryDeadline())
        other_deadline = convertTimeToSeconds(other.getDeliveryDeadline())
        return self_deadline < other_deadline

    def __le__(self, other):
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
        self_deadline = convertTimeToSeconds(self.getDeliveryDeadline())
        other_deadline = convertTimeToSeconds(other.getDeliveryDeadline())
        return self_deadline <= other_deadline

    def __gt__(self, other):
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
        self_deadline = convertTimeToSeconds(self.getDeliveryDeadline())
        other_deadline = convertTimeToSeconds(other.getDeliveryDeadline())
        return self_deadline > other_deadline

    def __ge__(self, other):
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
        self_deadline = convertTimeToSeconds(self.getDeliveryDeadline())
        other_deadline = convertTimeToSeconds(other.getDeliveryDeadline())
        return self_deadline >= other_deadline

    def __str__(self):
        printstring = ''
        printstring += 'ID:' + self.packageID + '\t'
        printstring += 'ADDRESS:' + self.deliveryAddress + '\t'
        printstring += 'CITY:' + self.deliveryCity + '\t'
        printstring += 'ZIP:' + self.deliveryZipCode + '\t'
        printstring += 'DEADLINE:' + self.deliveryDeadline + '\t'
        printstring += 'WEIGHT:' + self.deliveryWeight + '\t'
        printstring += 'STATUS:' + self.deliveryStatus + '\t'
        printstring += 'NOTES:' + self.packageNotes + '\t'
        return printstring
