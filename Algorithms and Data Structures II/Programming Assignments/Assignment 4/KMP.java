

/* 

Rahnuma Islam Nishat - 08/02/2014
*/

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;


public class  KMP 
{
	/***************************************************************************************
	*    Title: KMP.java
	*    Author: Robert Sedgewick and Kevin Wayne
	*    Date: 2 Apr 2017
	*    Code version: <code version>
	*    Availability: http://algs4.cs.princeton.edu/53substring/KMP.java.html
	*    Has Been Modified: True
	*
	***************************************************************************************/
   private static String pattern;
   private final int R;       // the radix
   private static int[][] dfa;       // the KMP automoton

   
   public KMP(String pattern) {
	   this.R = 256;
       this.pattern = pattern;

       // build DFA from pattern
       int m = pattern.length();
       dfa = new int[R][m]; 
       dfa[pattern.charAt(0)][0] = 1; 
       for (int x = 0, j = 1; j < m; j++) {
           for (int c = 0; c < R; c++) 
               dfa[c][j] = dfa[c][x];     // Copy mismatch cases. 
           dfa[pattern.charAt(j)][j] = j+1;   // Set match case. 
           x = dfa[pattern.charAt(j)][x];     // Update restart state.
       }
   }
   public static int search(String txt) {  
	// simulate operation of DFA on text
       int m = pattern.length();
       int n = txt.length();
       int i, j;
       for (i = 0, j = 0; i < n && j < m; i++) {
           j = dfa[txt.charAt(i)][j];
       }
       if (j == m) return i - m;    // found
       return n;                    // not found
   }

        
  	public static void main(String[] args) throws FileNotFoundException{
		Scanner s;
		if (args.length > 0){
			try{
				s = new Scanner(new File(args[0]));
			} catch(java.io.FileNotFoundException e){
				System.out.println("Unable to open "+args[0]+ ".");
				return;
			}
			System.out.println("Opened file "+args[0] + ".");
			String text = "";
			while(s.hasNext()){
				text+=s.next()+" ";
			}
			
			for(int i=1; i<args.length ;i++){
				KMP k = new KMP(args[i]);
				int index = search(text);
				if(index >= text.length())System.out.println(args[i]+ " was not found.");
				else System.out.println("The string \""+args[i]+ "\" was found at index "+index + ".");
			}
			
			//System.out.println(text);
			
		}else{
			System.out.println("usage: java SubstringSearch <filename> <pattern_1> <pattern_2> ... <pattern_n>.");
		}
		
		
	}
}




