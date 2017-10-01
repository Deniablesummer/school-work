//TODO: Before Submitting - Uncomment next line
//package SelectMedian;

/**
 *
 * @author Rahnuma Islam Nishat
 * January 20, 2017
 * CSC 226 - Spring 2017
 */

import java.util.ArrayList;
import java.util.List;

public class SelectMedian {
	
	//Selects kth smallest element of integer list A in linear time
    public static int LinearSelect(int[] A, int k){
        //LinearSort
    	//Psuedo code below taken from lecture slides
    	//---------------------------------------------------------------
    	/* if A.length() = 1 then return S
    	 * Let L,E,G be empty sequences
    	 * 
    	 * p = pickCleverPivot(A)
    	 * partition(L,E,G,S,p)
    	 * 
    	 * if k <= L.length() then return LinearSelect(L,K)
    	 * else if k <= L.length() + E.length() then return p
    	 * else return LinearSelect(G, k - L.length() - E.length())
    	 */
    	//---------------------------------------------------------------
    	//LinearSort
    	//Psuedo code above taken from lecture slides
    	
    	
    	//Select kth element
    	if (A.length == 1) 
    		return A[0];
    	
    	List<Integer> L = new ArrayList<>();
    	List<Integer> E = new ArrayList<>();
    	List<Integer> G = new ArrayList<>();
    	int p;
    	
    	p = pickCleverPivot(A);

        //Partitions elements into L, E, and G based on pivot p
    	for (int i = 0; i < A.length; i++) {
    		if (A[i] < p) 
    			L.add(A[i]);
    		 else if (A[i] > p) 
    			G.add(A[i]);
    		 else 
    			E.add(A[i]);
    	}
    	
    	if (k <= L.size()) 
    			return LinearSelect(convertIntegers(L),k);
    	else if (k <= L.size() + E.size())
    			return p;
    	else return LinearSelect(convertIntegers(G), k - L.size() - E.size());
    }
    
    //Picks pivot based on median of medians
    private static int pickCleverPivot(int[] A) {
    	//TODO: Pick a clever pivot
    	//int numberOfGroups = A.length / 7;
    	//for (int i = 0; i < A.length; i++) {
    		
    	//}
    	
    	//Not a clever pivot
    	return A[A.length/2];
    }
    
    //Code below taken from
    //http://stackoverflow.com/questions/718554/how-to-convert-an-arraylist-containing-integers-to-primitive-int-array
    //----------------------------------------------------------------------------------------------------------------
    public static int[] convertIntegers(List<Integer> integers)
    {
        int[] ret = new int[integers.size()];
        for (int i=0; i < ret.length; i++)
        {
            ret[i] = integers.get(i).intValue();
        }
        return ret;
    }
    //----------------------------------------------------------------------------------------------------------------
    //Code above taken from
    //http://stackoverflow.com/questions/718554/how-to-convert-an-arraylist-containing-integers-to-primitive-int-array


    
    public static void main(String[] args) {
        int[] A = {50, 54, 49, 49, 48, 49, 56, 52, 51, 52, 50, 59};
        		// 48, 49, 49, 49, 50, 50, 51, 52, 52, 54, 56, 59,
        System.out.println("The median weight is " + LinearSelect(A, A.length/2));
    }
    
}
