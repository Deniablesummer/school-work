/* ShortestPath.java
   CSC 226 - Spring 2017
      
   This template includes some testing code to help verify the implementation.
   To interactively provide test inputs, run the program with
	java ShortestPath
	
   To conveniently test the algorithm with a large input, create a text file
   containing one or more test graphs (in the format described below) and run
   the program with
	java ShortestPath file.txt
   where file.txt is replaced by the name of the text file.
   
   The input consists of a series of graphs in the following format:
   
    <number of vertices>
	<adjacency matrix row 1>
	...
	<adjacency matrix row n>
	
   Entry A[i][j] of the adjacency matrix gives the weight of the edge from 
   vertex i to vertex j (if A[i][j] is 0, then the edge does not exist).
   Note that since the graph is undirected, it is assumed that A[i][j]
   is always equal to A[j][i].
	
   An input file can contain an unlimited number of graphs; each will be 
   processed separately.


   B. Bird - 08/02/2014
*/

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.PriorityQueue;
import java.util.Stack;
import java.util.ArrayList;


//Do not change the name of the ShortestPath class
public class ShortestPath{

	static int pathArray[];
	public static int numVerts;
	public static int dist[];
	/* ShortestPath(G)
		Given an adjacency matrix for graph G, calculates and stores the shortest paths to all the
                vertces from the source vertex.
		
		If G[i][j] == 0, there is no edge between vertex i and vertex j
		If G[i][j] > 0, there is an edge between vertices i and j, and the
		value of G[i][j] gives the weight of the edge.
		No entries of G will be negative.
	*/
	static void ShortestPath(int[][] G, int source){
		numVerts = G.length;
		pathArray = new int[numVerts];
		/***************************************************************************************
		*    Title: Dijkstra's Algorithm
		*    Author: Aakash Hasija
		*    Date: 13 Mar 2017
		*    Code version: Unknown
		*    Availability: http://www.geeksforgeeks.org/greedy-algorithms-set-6-dijkstras-shortest-path-algorithm/
		*    Has Been Modified: True
		*
		***************************************************************************************/
		dist = new int[numVerts]; 
		Boolean sptSet[] = new Boolean[numVerts];

		// Initialize all distances as INFINITE and stpSet[] as false
		for (int i = 0; i < numVerts; i++) {
			dist[i] = Integer.MAX_VALUE;
			sptSet[i] = false;
		}

		// Distance of source vertex from itself is always 0
		dist[source] = 0;
		for (int count = 0; count < numVerts - 1; count++) {
			int u = minDistance(dist, sptSet, numVerts);
			sptSet[u] = true;
			for (int v = 0; v < numVerts; v++)
				if (!sptSet[v] && G[u][v]!=0 && dist[u] != Integer.MAX_VALUE && dist[u] + G[u][v] < dist[v]) {
					dist[v] = dist[u] + G[u][v];
					pathArray[v] = u;
				}
		}
	
	}
	// A utility function to find the vertex with minimum distance value,
    // from the set of vertices not yet included in shortest path tree 
    static int minDistance(int dist[], Boolean sptSet[], int numVerts){
        int min = Integer.MAX_VALUE, min_index=-1;
        for (int v = 0; v < numVerts; v++) {
            if (sptSet[v] == false && dist[v] <= min) {
                min = dist[v];
                min_index = v;
            }
        }
        return min_index;
    }
	
    //Author: James Ryan 
    static void PrintPaths(int source){
    	int next;
    	String temp;
    	for (int i = 0; i < dist.length; i++) {
    		next = i;
    		System.out.print("The path from " + source + " to " + i + " is: ");
    		temp = "" + next;
    		while (next != source) {
    			temp =  pathArray[next] + " --> " + temp;
    			next = pathArray[next];
    		}
    		System.out.print(temp);
    		System.out.println(" and the total distance is : " + dist[i]);
    	}
    }
        
		
	/* main()
	   Contains code to test the ShortestPath function. You may modify the
	   testing code if needed, but nothing in this function will be considered
	   during marking, and the testing process used for marking will not
	   execute any of the code below.
	*/
	public static void main(String[] args) throws FileNotFoundException{
		Scanner s;
		if (args.length > 0){
			try{
				s = new Scanner(new File(args[0]));
			} catch(java.io.FileNotFoundException e){
				System.out.printf("Unable to open %s\n",args[0]);
				return;
			}
			System.out.printf("Reading input values from %s.\n",args[0]);
		}else{
			s = new Scanner(System.in);
			System.out.printf("Reading input values from stdin.\n");
		}
		
		int graphNum = 0;
		double totalTimeSeconds = 0;
		
		//Read graphs until EOF is encountered (or an error occurs)
		while(true){
			graphNum++;
			if(graphNum != 1 && !s.hasNextInt())
				break;
			System.out.printf("Reading graph %d\n",graphNum);
			int n = s.nextInt();
			int[][] G = new int[n][n];
			int valuesRead = 0;
			for (int i = 0; i < n && s.hasNextInt(); i++){
				for (int j = 0; j < n && s.hasNextInt(); j++){
					G[i][j] = s.nextInt();
					valuesRead++;
				}
			}
			if (valuesRead < n*n){
				System.out.printf("Adjacency matrix for graph %d contains too few values.\n",graphNum);
				break;
			}
			long startTime = System.currentTimeMillis();
			
			ShortestPath(G, 0);
                        PrintPaths(0);
			long endTime = System.currentTimeMillis();
			totalTimeSeconds += (endTime-startTime)/1000.0;
			
			//System.out.printf("Graph %d: Minimum weight of a 0-1 path is %d\n",graphNum,totalWeight);
		}
		graphNum--;
		System.out.printf("Processed %d graph%s.\nAverage Time (seconds): %.2f\n",graphNum,(graphNum != 1)?"s":"",(graphNum>0)?totalTimeSeconds/graphNum:0);
	}
}




