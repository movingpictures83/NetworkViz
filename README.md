# NetworkViz
# Language: Python
# Dependencies: ClusterCSV2NOA  CSV2GML 
# Input: prefix (network and cluster CSV files, and CYS file)
# Output: BAT or COM (input file for Cytoscape)

PluMA plugin to visualize a network with Cytoscape, starting from CSV file format.
This saves the need to use multiple stages to convert to GML, NOA and other
compatible files for Cytoscape.  NetworkViz does this by directly invoking
other PluMA plugins to perform these conversions.

The plugin accepts a file prefix, and will subsequently assume the following input files:
prefix.csv (network)
prefix.clusters.csv (clusters)
prefix.cys (Cytoscape style file)

The network CSV file should contain rows and columns that represent nodes, with entry 
(i, j) representing the weight of the edge from node i to node j.

The cluster CSV file should be in the following format:

"","x"
"1","Family.Lachnospiraceae.0001"
"2","Family.Ruminococcaceae.0003"
"3","Family.Lachnospiraceae.0029"
"4","Family.Lachnospiraceae.0043"
"5","Family.Ruminococcaceae.0019"
"6","Family.Lachnospiraceae.0095"
"","x"
"1","Family.Porphyromonadaceae.0005"
"2","Family.Porphyromonadaceae.0006"
"3","Family.Lachnospiraceae.0045"
"4","Order.Clostridiales.0007"
"","x"
"1","Kingdom.Bacteria.0001"
"2","Family.Porphyromonadaceae.0013"
"3","Phylum.Firmicutes.0004"

Each "","x" signifies a new cluster.

The style file takes the standard Cytoscape format and can be prepared in advance by the user.
The attached example includes a style file that visualizes nodes based on cluster.

In addition generating an output script for Cytoscape, this plugin
will produce several intermediate files along the way:

prefix.gml (Equivalent GML file to the CSV network, compatible with Cytoscape and produced by the CSV2GML plugin)
prefix.noa (Equivalent NOA file to the CSV clusters, compatible with Cytoscape and produced by the ClusterCSV2NOA plugin).  Cluster then becomes an attribute
of each node in the network.
prefix.eda (EDA or EDge Attribute File for Cytoscape).  Every edge is given a mappedWeight and a scaledWeight attribute.
The mappedWeight is the edge weight for all positive edges, and zero for all negative edges.
The scaledWeight is the edge weight to the power 7.  
Both of these can be useful when running built-in visualization algorithms, such as Fruchterman-Reingold.  With mappedWeighty setting all edges
to positive values, negative edges get treated as zero and will be far away from each other in the network.  By using the scaledWeight
the difference between edge weights effectively becomes larger, more clearly separating node pairs connected by highly weighted edges from those that
have more medium-range weights.

The plugin also invokes Cytoscape automatically, if it is in the system PATH.
