/*
 * Feb 2015
 * EvalInfix.java
 * CSC 115 assignment 3.
 * Evaluates in Infix expression into a postfix expression then solves
 */

public class EvalInfix {
    /**
     * First ensure the arithmetic operations plus parentheses
     * are surrounded by spaces. Then go ahead and split up the
     * whole expression using spaces (i.e, the operands will be
     * nicely separated from everything else by at least a single
     * space). This will not work for negative numbers.
     */
    public static String[] tokenize(String s) {
        // Note the missing minus character...
        String symbols[] = {"\\(", "\\)", "\\+", "\\-", "\\*", "\\/"};

        // First eliminate any quotation marks
        s = s.replaceAll("'", " ");
        s = s.replaceAll("\"", " ");

        // Now all operators or parentheses, surround the character
        // with a single space on either side.
        for (int i = 0; i < symbols.length; i++) {
            String regex = symbols[i];
            String replace = " " + regex + " ";
            s = s.replaceAll(regex, replace);
        }   
        // Special case: If there is a unary minus, then then
        // what appears to the right of the symbol is whitespace
        // and a digit; what appears to the left whitespace
        // and a non-digit symbol.
        s = s.replaceAll("(^|([\\+\\-\\*\\/]))\\s+\\-\\s+(\\d+)", "$1 -$3");

        // Eliminate extra whitespaces at start and end of the
        // transformed string. 
        s = s.trim();

        // Finally, take advantage of the whitespace to create an
        // array of strings where each item in the array is one
        // of the elements in the original string passed in to this
        // method.
        return s.split("\\s+");
    } 
    //Checks if the expressions brackets are balanced
    //Returns true if they are, false if not
   public static boolean isBalanced(String expr) {
    	StringStackRefBased braceStack = new StringStackRefBased();
    	try {
    		for (int i = 0; i < expr.length(); i++) {
    			if (expr.charAt(i) == '(') {
    				braceStack.push("");
    			}
    			if (expr.charAt(i) == ')') {
    				braceStack.pop();
    			}
    		}
    	} catch (StringStackException e) {
    		return false; //Pop an empty stack means is not balanced
    	}
    	if (braceStack.isEmpty()) {
    		return true; //If the stack is empty expression is balanced
    	}
    	return false;
    }
   //Checks if item is an int
   public static boolean isInt(String item) {
    	try{
    		  int num = Integer.parseInt(item);
    		  return true;
    		} catch (NumberFormatException e) {
    		  return false;
    		}
    }
   //checks if the item is a double
   public static boolean isDouble(String str) {
        try {
            Double.parseDouble(str);
            if (isInt(str)) {
            	return false;
            }
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
   //Checks if items 2 precedence is high than item 1
   //returns true if true, false if false
   public static boolean checkPrecedence(String item1, String item2) {
	   //System.out.println("Checking " + item2 + " " + item1); //used for testing/verify that was comparing correct items 
	   if (item2.charAt(0) == '*') {
		   //System.out.println("Precedence returning true1");//Used for testing
		   return true;
	   }
	   if (item2.charAt(0) == '/') {
		   //System.out.println("Precedence returning true");//Used for testing
		   return true;
	   }
	   
	   return false;	   
   }
   //Converts String expr into postfix form
   //returns it as a StringList - RefBased
   public static StringList toPostfix(String expr){
	   StringStackRefBased theStack = new StringStackRefBased();
	   StringListRefBased theList = new StringListRefBased();
	   String[] express = tokenize(expr);
	   int operandCount = 0;
	   int operatorCount = 0;
	   try {
       for (int i = 0; i < express.length; i++) {
    	   //System.out.println(express[i]); //Used for testing
    	   if (isInt(express[i])) {
    		   operandCount++;
    		   theList.insertTail(express[i]);
    		   //System.out.println("I have added something to the list " + express[i]);//Used for testing    		   
    	   } else if (express[i].charAt(0) == '(') {
    		   //System.out.println("adding ( to stack"); //Used for testing
    			   theStack.push(express[i]);    		   
    	   } else if (express[i].charAt(0) == '+' ||
        				express[i].charAt(0) == '-' ||
        				express[i].charAt(0) == '*' ||
        				express[i].charAt(0) == '/') {
    		   operatorCount++;
    		   //System.out.println("I have entered the loop"); Used for testing
    		   while ( !theStack.isEmpty() &&
        				theStack.peek().charAt(0) != '(' &&
        				checkPrecedence(express[i], theStack.peek())) {
        			//temp = theStack.pop();
    			   //System.out.println("I am inserting " + express[i] +" into the list");//Used for testing
    			   theList.insertTail(theStack.pop());
    		   } 
    		   //System.out.println("I am adding " + express[i] + " to the stack"); //Used for testing
    		   theStack.push(express[i]);
        	} else if (express[i].charAt(0) == ')') {
        		while (theStack.peek().charAt(0) != '(') {
        			//temp = theStack.pop();
        			theList.insertTail(theStack.pop());
        		}
        		theStack.pop();
        	}
    	   }

       while (!theStack.isEmpty()) {
		   //temp = theStack.pop();
		   //System.out.println("I am adding something from the stack to the list"); //Used for testing
		   theList.insertTail(theStack.pop());
	   }
	   } catch (StringStackException e) {      			
	   }
	   //Checks if invalid syntax
	   //Compares the amount of operators to operands
	   if (operandCount != (operatorCount) -1 ) {
		   return null;
	   }
        return theList;
    }
   //Evaluates a postFix equation
   //Returns the answer as a string
   //Will error out if it attempts to divide by zero
   public static String evaluatePostfix(StringList expr) {
    	StringStackRefBased theStack = new StringStackRefBased();
    	int temp1 = 0;
    	int temp2 = 0;
    	String temp = "";
    	//If its an operand pop onto stack.
    	//If its an operator pop 2 items off stack then 
    	//operate those two items by the operator
    	try {
    		for (int i = 0; i < expr.getLength(); i++) {
    			//System.out.println(expr.retrieve(i)); //Used for testing
    			switch (expr.retrieve(i)) {
    			case "*":temp1 = Integer.parseInt(theStack.pop());
    					 temp2 = Integer.parseInt(theStack.pop());
    					 temp1 = temp1 * temp2;
    					 theStack.push(Integer.toString(temp1));
    					 break;				
    			case "/":temp1 = Integer.parseInt(theStack.pop());
				 		 temp2 = Integer.parseInt(theStack.pop());
				 		 temp1 = temp2 / temp1;
				 		 theStack.push(Integer.toString(temp1));
				 		 break;
    			case "-":temp1 = Integer.parseInt(theStack.pop());
				 		 temp2 = Integer.parseInt(theStack.pop());
				 		 temp1 = temp2 - temp1;
				 		 theStack.push(Integer.toString(temp1));
				 		 break;
    			case "+":temp1 = Integer.parseInt(theStack.pop());
				 		 temp2 = Integer.parseInt(theStack.pop());				 		 
				 		 temp1 = temp1 + temp2;
				 		 theStack.push(Integer.toString(temp1));
				 		 break;
    			default: theStack.push(expr.retrieve(i));   				
    			}		
    		}
    		temp = theStack.pop();
    	} catch (NumberFormatException e) {
    		
    	} catch (ArithmeticException e) {
    		System.out.println("Can not evaluate, tried to divide by 0.");
    	} catch (StringStackException e) {    		
    	}
    	return temp;
    }
   //Evaluates an expression
   //Will convert to postFix format then evaluate it.
   //returns <unbalanced ()> if "()" are unbalanced.
   //returns <noninteger> if an operand is not of integer format
   public static String evaluateExpression(String expr) {
       String result = "";
       String[] express = tokenize(expr);
       //Check if brackets are balanced
       if (isBalanced(expr) == false) {
        	return "<unbalanced ()>";
       }
       //Check that there are doubles in operands
       for (int i = 0; i < express.length; i++) {
    	   if (isDouble(express[i]))
    		   return "<noninteger>";
       }
       StringList exprList = toPostfix(expr);
       if (exprList == null) {
    	   return "<sytnax error>";
       }
       //System.out.println(exprList); //Used for testing - Shows expression in postfix format
       result = evaluatePostfix(exprList);
       return result;
    }
    public static void main(String args[]) {
        if (args.length < 1) {
            System.err.println("usage: java EvalInfix '<expression>'");
            System.exit(1);
        }
        System.out.println(evaluateExpression(args[0]));
    }
}