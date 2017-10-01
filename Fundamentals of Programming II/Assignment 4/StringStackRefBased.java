/*
 * March 2015
 * StringStackRefBased.java
 * Refernce Based Stack implimentation used for EvalInfix.java
 */
public class StringStackRefBased implements StringStack{
	private StringNode head;
	private int stackLength;	
	
	public StringStackRefBased() {
		head = null;	
		stackLength = 0;
	}

	public boolean isEmpty() {
		if (stackLength != 0)
			return false;
		return true;
	}

	public String pop() throws StringStackException {
		if (stackLength == 0) 
			throw new StringStackException("Tried to pop an empty stack.");
		String temp = head.item;
		head = head.next;
		stackLength--;
		return temp;
		
	}

	public void popAll() {
		head = null;
		stackLength = 0;
	}

	public void push(String item) throws StringStackException {
		StringNode temp = new StringNode(item);
		temp.next = head;
		head = temp;
		stackLength++;
		
	}

	public String peek() throws StringStackException {
		if (stackLength == 0) 
			throw new StringStackException("Im sorry, you tried to peek into an empty stack!");
		return head.item;
	}

	/*public static void main(String[] args) {
		// Test 1: Pop stack of length 0
		// Should throw StringStackException
		StringStackRefBased aStringStack = new StringStackRefBased();
		System.out.println("Test 1:");
		try {			
			aStringStack.pop();
		} catch (StringStackException e) {
			System.out.println(e);
		}	
		// Test 2: Push an item onto stack
		// Check if stack is empty and print the item in the stack
		System.out.println("Test 2:");
		try {
			aStringStack.push("I was successfully pushed!");
			System.out.println("Is stack empty: " + aStringStack.isEmpty());
			System.out.println(aStringStack.head.item);
		} catch (StringStackException e) {			
		}
		// Test 3: Push 2 items onto a stack, popAll, then push an item onto stack
		// Peek into the stack and should have only 3rd item left.
		// Checks if stack is empty after popAll() and after push("push3")
		System.out.println("Test 3:");
		try{
			aStringStack.push("Push1");
			aStringStack.push("Push2");
			aStringStack.popAll();
			System.out.println("Is stack empty: " + aStringStack.isEmpty());
			aStringStack.push("Push3");
			System.out.println("Is stack empty: " + aStringStack.isEmpty());
			System.out.println(aStringStack.peek());
		} catch(StringStackException e) {			
		}			
	}*/

}
