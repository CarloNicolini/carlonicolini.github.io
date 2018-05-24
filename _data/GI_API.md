**GRAPHINSIGHT 1.3 API**

-   void setBatchMode(bool batchMode);

-   void initEmpty();

-   void openFile(const QString &filename);

-   void evalFile(const QString &filename);

// List of Methods callable from Graph class

// Put the program in batch mode, it means that after every operation,
the OpenGL status is not updated, this makes frequent operations such as
node or edges insertion and removal much faster

void setBatchMode(bool batchMode);

// Initialize a new empty graph, set the all the visual attributes to
their default status

void initEmpty();

// Open a graph file in .net or .dimacs format, it's equivalent to “Open
File...”

void openFile(const QString &filename);

// Evaluate a Python script in .py format, exceptions are thrown if
something goes wrong

void evalFile(const QString &filename);

// Add a textual attribute as new column to the current dataset

void addAttribute(const QString &attributeName);

// Remove the selected attribute by name, if it is not present as column
in the dataset, exception is thrown

void removeAttribute(const QString &attributeName);

// Initialize a new layout for the current graph. The first parameters
can be one of the 16 layout methods available as variables
(LayoutMethodXXX). If the selected layout method index is out of range
an exception is thrown. This method is also synchronized with the GUI
selection of layout method, so changing via GUI or via this method is
the same, except that this method can force the randomization of nodes
coordinates

void initLayout(int layoutMethod,int dimensions, bool randomize=false,
bool shakeZ=false);

// Do nsteps of the current layout method. While computing the “Graph
Drawing” group box is disabled. You can stop the current layout only via
console

void steps(int nsteps);

// Stop the current layout computation, reenable the Graph Drawing group
box

void stop();

// Graph Methods

// Insert a node in the current graph with a integer ID. If the node
already exists an exception is thrown

void insertNode(int nodeId);

// Insert a node in the current graph with a list of string properties.
They must be as much as the number of dataset attributes otherwise an
exception is thrown to the user. If the node already exists an exception
is thrown

void insertNode(int nodeId, const QStringList &nodeProperties);

// Overloaded method to insert a node with given property if the number
of dataset attributes is 1. If the node already exists an exception is
thrown

void insertNode(int nodeId, const QString &nodeProperty);

/

// Remove the node with the selected ID. If the node is not found an
exception is thrown. This is an expensive operation.

void removeNode(int nodeId);

// Insert an undirected edge in the graph. If the edge already exists
and exception is thrown. If the source or target nodes don't exist an
exception is thrown.

void insertEdge(int source, int target, double weight=1.0);

// Modify the weight of the undirected edge from “source” to “target”
node. If the edge does not exist an exception is thrown

void setEdgeWeight(int source, int target, double weight);

// Modify an existing node property, if the node does not exist and
exception is thrown

void setNodeAttribute(int nodeId, const QStringList &nodeAttributes);

// Remove an edge. If the edge does not exist between “source” and
“target” an exception is thrown. If “source” or “target” don't exist an
exception is thrown.

void removeEdge(int source, int target);

// Return the number of nodes of current graph

int getNodesCount() const;

// Return the number of edges of graph

int getEdgesCount() const ;

// Return the number of weakly connected components of the graph

int getComponentsCount() const;

// Return a Python list of lists containing the node wrappers to the
nodes in the connected components PyObject \*getConnectedComponents();

// Return a selected node. If the node doesn't exist an exception is
thrown

LNode \*getNode(int nodeid);

// Return the graph-theoretic distance between two nodes. If one of
these nodes does not exist an exception is thrown

double getNodesDistance(int fromNode, int toNode);

// Return the weight of the edge from node fromNodeId to toNodeId

double getEdgeWeight(int fromNodeId, int toNodeId);

// Return a Python list of node wrappers along the shortest path between
“fromNode” and “toNode”

QList&lt;LNode \*&gt; getShortestDistancePath(int fromNode, int toNode);

// Synchronize python and C++ structures

void sync();

// return the python dictionary of nodes, nodes are indexed by their ID,
so if you want to get the node with id = 100, do G.nodes()\[100\] or
otherwise G.getNode(100)

PyObject\* nodes();

// Methods callable from Node class

// Get the node degree. If the weight of the edges incident to node is
!= 1 then getDegree() is different from getNumNeighbors()

double getDegree() const;

// Get the node weight

double getWeight() const;

// Get the connected component index of the node in the current graph

int getComponent() const;

// Get the node ID

int getId() const;

// Get the node index (not useful)

int getIndex() const;

// Get the node number of neighbors node

unsigned int getNumNeighbors() const;

// Get a Python dictionary of node neighbors, indexeable by their ID

PyObject \*neighbors();

// Get the node X coordinate

double getX() const;

// Get the node Y coordinate

double getY() const;

// Get the node Z coordinate

double getZ() const;

// Get the list of id of current node neighbors as Python list of
integers

QList&lt;int&gt; getNeighborsId() const;

// Move the current node by displacement dx,dy,dz

void move(const double &dx, const double &dy, const double &dz);

// Set this node coordinates x,y,z

void setPos(const double &x, const double &y, const double &z);

// Set this node color in RGB values. r,g,b must be values in \[0,255\],
otherwise an exception is thrown

void setColorRGB(int r,int g,int b);
