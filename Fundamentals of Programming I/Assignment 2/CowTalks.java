/*
 * CowTalks.java
 * Has a cow speak a statement in a "text bubble"
 * Input: Message for the cow to speak
 * Output: Message chosen by a the user, and a cow
 */
import java.util.*;

public class CowTalks {

	public static void main(String[] args) { //Gets the message, then executes printMessage and printCow
		int messageLength = 0;
			
		Scanner console = new Scanner(System.in);
		System.out.print("What would you like the cow to say? : ");
		String message = console.nextLine();
		messageLength = message.length();

		printMessage(messageLength, message);
		printCow();		
	}
	
	public static void printMessage(int messageLength, String message) { //Prints the message inside a box
		for (int i = 0; i < (messageLength + 4); i++) {
			System.out.print("*");
		}
		System.out.println("\n| " + message + " |"); 
		for (int i = 0; i < (messageLength + 4); i++) {
			System.out.print("*");
		}
	}
	
	public static void printCow() { //Prints the cow
		System.out.println("\n         \\   ^--^");
		System.out.println("          \\  (oo)\\_______");
		System.out.println("             (__)\\       )\\/\\");
		System.out.println("                  ||----w |");
		System.out.println("                  ||     ||");
	}
}
