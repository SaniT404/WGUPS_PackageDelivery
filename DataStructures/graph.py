class Graph:
    def __init__(self):
        self.nodes = []
        self.adjacency_matrix = []

    """
    add_vertex(new_vertex) :: - Adds new vertex to graph.
    Algorithm Complexity - Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    for node in nodes:
        Do set new column row to 0
    Do add new column to adjacency matrix
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    for column in adjacency_matrix:
        Do add 0 to column
    Do add new_vertex to node list
    """
    def add_vertex(self, new_vertex):
        # update adjacency matrix with zeroes to reflect new node
            # add new column for new node to adjacency matrix
        newcol = []
        for i in range(len(self.nodes)):
            newcol.append('0')
        self.adjacency_matrix.append(newcol)
            # add zeroes to all existing columns for new node
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].append('0')
        # add new vertex to node list
        self.nodes.append(new_vertex.strip())

    def add_directed_edge(self, from_vertex, to_vertex, weight):
        row = self.nodes.index(from_vertex)
        col = self.nodes.index(to_vertex)

        self.adjacency_matrix[row][col] = weight

    def add_undirected_edge(self, vertex_a, vertex_b, weight):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def getDistance(self, from_vertex, to_vertex):
        row = self.nodes.index(from_vertex)
        col = self.nodes.index(to_vertex)

        return float(self.adjacency_matrix[row][col])

    """
    calculateRouteTimeSeconds(nodelist, speed) :: secondselapsed - Calculates
    the time it will take to visit each node in nodelist traveling at specified
    speed.
    Algorithm Complexity - Best Case: O(N) Average Case: O(N) Worst Case: O(N)
    ----------------------------------------------------------------------------
    ''' BC: O(N) AC: O(N) WC: O(N) '''
    for node in nodelist:
        Get distance between each node
        Determine time to travel distance, add to total
    return total_elapsed_seconds
    """
    def calculateRouteTimeSeconds(self, nodelist, speed):
        # Initialize variables
        current_location = ""
        next_location = ""
        elapsed = 0
        # Loop package list, get distance between each node, and record travel time
        for i in range(len(nodelist)):
            if(i == 0):
                current_location = nodelist[i]
            else:
                current_location = nodelist[i-1]
                next_location = nodelist[i]
                distance = self.getDistance(current_location, next_location)
                time = (((distance / speed) * 60) * 60) # ((Hours) Minutes) Seconds)
                elapsed += time
        return elapsed



    def __str__(self):
        printstring = ""
        # Print graph nodes
        for i in range(len(self.nodes)):
            printstring += self.nodes[i] + '\n'
        # Print adjacency matrix
        # loop col
        for i in range(len(self.adjacency_matrix)):
            # loop row
            for j in range(len(self.adjacency_matrix[i])):
                printstring += self.adjacency_matrix[i][j] + ' '
            printstring += '\n'

        return printstring
