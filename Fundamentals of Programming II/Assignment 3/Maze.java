/*
 * Maze.java
 * Maze class for CSC 115 assignment 3.
 */
public class Maze {
	
	//class variables
	private String[] mazeData;
	private int StartRow;
	private int startColumn;
	private int finishRow;
	private int finishColumn;
	MazeLocationListRefBased correctPath = new MazeLocationListRefBased();
	private boolean wasHere[][];

	//Class constructor
	public Maze(String[] textmaze, int startRow, int startCol, int finishRow, int finishCol) {
		this.mazeData = textmaze;
		this.StartRow = startRow;
		this.startColumn = startCol;
		this.finishRow = finishRow;
		this.finishColumn = finishCol;
		this.wasHere = new boolean[textmaze[1].length()][textmaze.length];	
		//System.out.println(mazeData.length); //Used for testing
		for (int j = 0; j < mazeData.length; j++) {
			for (int i = 0; i < mazeData[0].length() - 1; i++) {
				wasHere[i][j] = false;
				
			}
			System.out.println(mazeData[j]);
		}
	}	//End constructor
	
	/*Returns the correctPath of type MazeLocationListRefBased if a path is found
	 *Returns null if no path is found
	 */
	public MazeLocationList solve() {	
		if (findPath(StartRow, startColumn, finishRow, finishColumn)) {
			return correctPath; //Returns the path in order
		}		
		return null; //No valid path
	}	//end solve()	
	
	/*Recursive algorithm to find a path from current point,
	 *to finish point findPath(the start row, the start Column, the finish Row, the finish Column)
	 */
	private boolean findPath(int startRow, int startCol, int finishRow, int finishCol) {
		/*Algorithm used for finding the path in this method adapted from,
		 *Wikipedia: 
		 *http://en.wikipedia.org/wiki/Maze_solving_algorithm
		 */	
		//System.out.println(startRow + ", " + startCol); //Used for testing/debugging
		
		if (startRow == finishRow && startCol == finishCol) {
			return true; //Finished the maze
		}
		if (wasHere[startCol][startRow] == true)   {		
			//System.out.println("You were already here!"); //Used for debugging			
			return false; //If you were here already
		}
		if (mazeData[startRow].charAt(startCol) == '*' ) {		
			//System.out.println("This is a wall."); //Used for debugging	
			return false; //This is a wall
		}		
		//System.out.println("Made past!"); //Used for testing
		wasHere[startCol][startRow] = true; //Tells the program that you have now been here
		
		/*Checks down as long as not on bottom edge
		 *Sets a temp MazeLocation then adds it to the list correctPath
		 */
		if (startRow < mazeData.length -1) {
			MazeLocation temp = new MazeLocation(startCol, startRow);	
			correctPath.insertTail(temp);
			if (findPath(startRow + 1, startCol, finishRow, finishCol)) {			
				return true;
			}
			correctPath.removeTail(); //not a valid part of path
		}
		/*Checks right as long as not on right edge
		 *Sets a temp MazeLocation then adds it to the list correctPath
		 */
		if (startCol < mazeData[0].length() -1) {
			MazeLocation temp = new MazeLocation(startCol, startRow);	
			correctPath.insertTail(temp);
			if (findPath(startRow, startCol + 1, finishRow, finishCol)) {
				return true;
			}
			correctPath.removeTail(); //not a valid part of path
		}
		/*Checks left as long as not on left edge
		 *Sets a temp MazeLocation then adds it to the list correctPath
		 */
		if (startCol > 0) {
			MazeLocation temp = new MazeLocation(startCol, startRow);
			correctPath.insertTail(temp);
			if (findPath(startRow, startCol - 1, finishRow, finishCol)) {		
				return true;
			}	
			correctPath.removeTail(); //not a valid part of path
		}
		/*Checks top as long as not on top edge
		 *Sets a temp MazeLocation then adds it to the list correctPath
		 */
		if (startRow > 0) {
			MazeLocation temp = new MazeLocation(startCol, startRow);
			correctPath.insertTail(temp);
			if (findPath(startRow - 1, startCol, finishRow, finishCol)) {
				return true;
			}
			correctPath.removeTail(); //not a valid part of path
		}	
		return false;
	}//end findPath()
}	//end Maze
