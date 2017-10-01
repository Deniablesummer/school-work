import java.util.*;
import java.io.*;
import java.awt.*;
public class Slugs {	
	public static void main(String[] args) throws FileNotFoundException {		
		try { // Try/catch to catch if FileNotFoundException is thrown.
			Scanner input = new Scanner(new File("slug_details.txt")); //Read file, for the output filename, boxSize, and movement distance
			String filename = input.next();
			int boxSize = input.nextInt();
			int distance = input.nextInt();
			PrintStream output = new PrintStream(new File(filename)); //Creates the file needed for outputting the coords.
		output.println(boxSize + " " + boxSize); //Prints side lengths to the file
		
		Point[] slug; //Init object array
		slug = new Point[4];		
		for(int i = 0; i < slug.length; i++) {
		    slug[i] = new Point();
		}
		slug = initSlugs(boxSize);
		moveSlugs(slug, distance, output, boxSize);
		System.out.println("Simulation Complete.");
		}
		catch (java.io.FileNotFoundException ex) {
			System.out.println("Error: File \"slugs_details.txt\" not found."); 
			System.exit(-1); //Exit with code -1
		}
	}//main	
	public static void writeToFile(PrintStream output, int[] coords) { //Writes each set of coords to a line in file
			for (int i=0; i < 4; i++) {
				output.print(coords[i] + " ");
			}
			output.println();
	}//writeToFile
	public static void moveSlugs(Point[] slug, int d, PrintStream output, int boxSize) { //Simulates movement of slugs, goes to writeToFile each time a slug moves
		double distance = boxSize; //Init need variables
		double ratio;
		int[] points = {0,0,0,0}; //array to print to txt file {oldx,oldy,newx,newy}	
		while (distance > d) {
			for (int i = 0; i < 4; i++) {
				distance = Math.sqrt((int) Math.pow((slug[(i+1)%4].x - slug[i].x), 2) 
						+ (int) Math.pow((slug[(i+1)%4].y - slug[i].y), 2));
				if (distance < d){
					break; //if movement distance is less than distance between two points, break from while loop
				}
				points[0] = slug[i].x; //Represents starting points
				points[1] = slug[i].y; //""	
				ratio = d / distance;
				slug[i].y += (slug[(i+1)%4].y - slug[i].y) * ratio; //y-coord movement
				slug[i].x += (slug[(i+1)%4].x - slug[i].x) * ratio; //x-coord movement
				points[2] = slug[i].x; //Represents ending points
				points[3] = slug[i].y; //""
				writeToFile(output, points); 
			}
		}
	}//moveSlugs	
	public static Point[] initSlugs(int boxSize) { //initializes slugs to each corner of the box. Input: box side length. Returns: Point object array
		Point[] slug; //Init object array
		slug = new Point[4];		
		for(int i = 0; i < slug.length; i++) {
		    slug[i] = new Point();
		}	
		slug[0].x = 0; //Init starting points for the 4 slugs
		slug[0].y = 0;
		slug[1].x = 0;
		slug[1].y = boxSize;
		slug[2].x = boxSize;
		slug[2].y = boxSize;
		slug[3].x = boxSize;
		slug[3].y = 0;	
		return slug;
	}//initSlugs
}