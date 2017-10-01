/*
 * Hello World
 * Calculates new position
 * Outputs outputs a float representing the new position
 * 	calculated
 */
public class PositionCalculator {

	public static void main(String[] args) {
		double initialPos = 5.0;
		double initialVel = 2.0;
		double acceleration = 1.5;
		double time = 10.0;
		double newPos;
		
		newPos = initialPos + (initialVel * time) + (acceleration * (time * time))/2;
		System.out.println("The new position is: " + newPos);
		//Output should be 110.0
	}

}
