/*
 * CarbonCalc.java
 * Calculates a persons carbon footprint
 * Input: Variables needed to determine the users carbon footprint
 * Output: The carbon footprint, along with a breakdown of how much of the footprint is caused by what
 */
import java.util.*; //for scanner

public class CarbonCalc {
	public static void main(String[] args) { //Calculate your carbon footprint
		double trans;
		double elec;
		double food;
		double totalEmissions;
		Scanner console = new Scanner(System.in);
		System.out.println("This program computes your carbon footprint.\n");
		trans = determineTransportationEmission(console);
		elec = determineElectricityEmission(console);
		food = determineFoodEmission(console);
		totalEmissions = calculateTotalEmission(trans, elec, food);
		printReport(totalEmissions, trans, elec, food);
	}//main
	
	public static double determineTransportationEmission(Scanner input) { //Transportation Emission
		double kmPerDay;
		double efficiency;
		double ltrPerYr;
		System.out.print("How many kilometres do you travel per day? (nearest tenth): ");
		kmPerDay = input.nextDouble();
		//System.out.println("You drive " + kmPerDay + " km's per day!");
		System.out.print("What is your vehicles fuel efficiency? (km/litre):");
		efficiency = input.nextDouble();
		ltrPerYr = 365 * (kmPerDay / efficiency);
		return  2.3 * ltrPerYr; //return transportation emmission to 'trans' in main
	}//determineTransportationEmission
	
	public static double determineElectricityEmission(Scanner input) { //Electrical Emission
		double kWhPerMonth;
		double numPeopleInHome;	
		System.out.print("\nWhat is your households power usage per month? (kWh):");
		kWhPerMonth = input.nextDouble();
		System.out.print("How many people are in your home? :");
		numPeopleInHome = input.nextDouble();
		return (kWhPerMonth * 12 * 0.257) / numPeopleInHome; //return electrical emission to 'elec' in main
	}//determineElectricityEmssion
	
	public static double determineFoodEmission(Scanner input) { //Food Emission
		double meat;
		double dairy;
		double fruitVeg;
		double carbs;
		System.out.print("\nPercentage of meat in your diet: ");
		meat = input.nextDouble() * 53.1;
		System.out.print("Percentage of dairy in your diet: ");
		dairy = input.nextDouble() * 13.8;
		System.out.print("Percentage of fruit and veggies in your diet: ");
		fruitVeg = input.nextDouble() * 7.6;
		System.out.print("Percentage of carbohydrates in your diet: ");
		carbs = input.nextDouble() * 3.1;		
		return meat + dairy + fruitVeg + carbs; //return food emission to 'food' in main
	}//determineFoodEmssion
	
	public static double calculateTotalEmission(double trans, double elec, double food) { //calculate the total emission
		double total = (trans + elec + food) / 1000;				
		return total; //return total to main
	}//calculateTotalEmssion
	
	public static void printReport(double total, double trans, double elec, double food) { //Display an emission report to the user
		double transPerc;	//Output doubles are rounded to 5 decimal places neat formatting
		double elecPerc;
		double foodPerc;
		System.out.print("\n\nYou produce an annual total of " + (double)Math.round(total * 100000) / 100000 + " metric tons of CO2 per year.\n"); //total emission
		transPerc = trans / (total * 10);
		elecPerc = elec / (total * 10);
		foodPerc = food / (total * 10);
		System.out.printf("\tCar: %20.5f%s\n", transPerc, "%"); //display percents of contributing factors
		System.out.printf("\tElectricity: %12.5f%s\n", elecPerc, "%");
		System.out.printf("\tFood: %19.5f%s\n", foodPerc, "%");
	}//printReport	
}//CarbonCalc