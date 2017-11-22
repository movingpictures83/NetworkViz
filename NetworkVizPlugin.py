import sys
import os
import math
from ClusterCSV2NOA.ClusterCSV2NOAPlugin import *
from CSV2GML.CSV2GMLPlugin import *
from distutils.spawn import find_executable


class NetworkVizPlugin(CSV2GMLPlugin):
   def input(self, filename):
      CSV2GMLPlugin.input(self,filename+".csv")
      # Three files will be created in addition to the output file:
      # GML file for the network, EDA file for network edges, 
      # NOA file for the clusters.
      self.gmlfile = filename+".gml"
      self.edafile = filename+".eda"
      self.csvfile = filename+".clusters.csv"
      self.noafile = filename+".clusters.noa"
      self.clusterhandle = ClusterCSV2NOAPlugin()
      self.clusterhandle.input(self.csvfile)

   def run(self):
      CSV2GMLPlugin.run(self)
      self.clusterhandle.run()

   def output(self, filename):
      filestuff = open(self.edafile, 'w')
      filestuff.write("name\tmappedWeight\tscaledWeight\n")
      for i in range(self.n):
         self.bacteria[i] = self.bacteria[i].strip()
      for i in range(self.n):
         for j in range(self.n):
               bac1 = self.bacteria[i].strip()
               bac1 = bac1[1:len(bac1)-1]
               bac2 = self.bacteria[j].strip()
               bac2 = bac2[1:len(bac2)-1]
               if (i != j):# and result[0]):
                  if (float(self.ADJ[i][j]) > 0):
                     filestuff.write(bac1+' '+'('+'pp'+')'+' '+bac2+'\t'+str(self.ADJ[i][j])+'\t'+str((float(self.ADJ[i][j]))**7)+'\n')
                  elif (float(self.ADJ[i][j]) < 0): # negatives to zero
                     filestuff.write(bac1+' '+'('+'pp'+')'+' '+bac2+'\t'+str(0)+'\t'+str((float(self.ADJ[i][j]))**7)+'\n')
      
      self.clusterhandle.output(self.noafile)
      CSV2GMLPlugin.output(self, self.gmlfile)

      filestuff2 = open(filename, 'w')
      filestuff2.write("session open file=\"pluma_viz.cys\"\n")
      filestuff2.write("network load file file=\""+self.gmlfile+"\"\n")
      filestuff2.write("table import file file=\""+self.edafile+"\" DataTypeTargetForNetworkCollection=\"Edge Table Columns\" keyColumnIndex=1 firstRowAsColumnNames=true startLoadRow=1 delimiters=\"\\t\"\n")
      filestuff2.write("table import file file=\""+self.noafile+"\" DataTypeTargetForNetworkCollection=\"Node Table Columns\" keyColumnIndex=1 firstRowAsColumnNames=true startLoadRow=1\n")
      filestuff2.write("layout allegro-fruchterman-reingold EdgeAttribute=\"mappedWeight\" defaultEdgeWeight=0 randomize=true useNormalizedEdgeWeight=false\n")
     
      cytoscape = find_executable("cytoscape.sh")
      if (cytoscape):
         os.system("cytoscape.sh -S "+filename)  
      
      
 


