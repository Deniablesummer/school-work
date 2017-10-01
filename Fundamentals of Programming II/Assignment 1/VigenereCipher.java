
public class VigenereCipher implements Cipher {
	private char[] currentKey;
			
	    public VigenereCipher(String key)  {
	    	currentKey = key.toCharArray();	    	
	    }
	    
	    //Encrypts a string. 
	    //@param plainText String of text you would like to encrypt
	    //@return String cipherText String of text that has been encrypted using the key
	    public String encrypt(String plainText) {
	    	String cipherText = "";
	    	int keyLength = currentKey.length;
	    	int currentKeySlot = 0;
	    	int currentCharKeyInt;
	    	int[] encodedText = new int[plainText.length()];
	    	//Loops for each char on the message
	    	for (int i = 0; i < plainText.length(); i++) {
	    		currentCharKeyInt = currentKey[currentKeySlot];
	    		encodedText[i] = ((plainText.charAt(i) - 97) + (currentCharKeyInt - 97)) % 26 + 97;
	    		
	    		//Change the currentCharKey back to 0 if at end of key, and plus one if not.\
	    		currentKeySlot++;
	    		if(currentKeySlot == keyLength) {
	    			currentKeySlot = 0;
	    		}
	    	}
	    	cipherText = intArrayToString(encodedText);
	    	return cipherText;
	    }//encrypt

	    //Decrypts the text with the designated key
	    //@param cipherText The text to be decrypted
	    //@return The text that has been decrypted
	    public String decrypt(String cipherText) {
	    	int keyLength = currentKey.length;
	    	int currentKeySlot = 0;
	    	int currentCharKeyInt;
	    	int[] encodedText = new int[cipherText.length()];
	    	
	    	encodedText = stringToIntArray(cipherText);
	    	
	    	for (int i = 0; i < cipherText.length(); i++) {
	    		currentCharKeyInt = currentKey[currentKeySlot];
	    		encodedText[i] = ((26 + (cipherText.charAt(i) - 97) - (currentCharKeyInt - 97)) % 26)+ 97;
	    		
	    		//Change the currentCharKey back to 0 if at end of key, and plus one if not.
	    		if(currentKeySlot == keyLength - 1) {
	    			currentKeySlot = 0;
	    		} else {
	    			currentKeySlot++;
	    		}
	    	}
	    	cipherText = intArrayToString(encodedText);
	        return cipherText;
	    }//decrypt

	    /**
	     * Establishes the key to be used by the Cipher. 
	     * @param key A plain text key.
	     */
	    public void setKey(String key) {
	    	currentKey = key.toCharArray();
	    	
	    }//setKey
	    
	    //Converts an array of integers into a string of text
	    //Each integer represents a character in the string
	    private String intArrayToString(int[] encodedText) {
	    	char[] text = new char[encodedText.length];
	    	String text2 = "";
	    	for (int i = 0; i < encodedText.length; i++) {
	    		text[i] += encodedText[i];
	    		text2 += text[i];
	    	}    	
	    	return text2;
	    }//intArrayToString
	    
	    //Converts a String into an integer array
	    //Each integer represents a character in the string (between 0 and 26
	    private int[] stringToIntArray(String text) {
	    	int[] encodedText = new int[text.length()];
	    	for (int i = 0; i < text.length(); i++) {
	    		encodedText[i] = text.charAt(i) - 97;
	    	}   	
	    	return encodedText;
	    }//stringToIntArray
	    
	    //public static void main(String[] Args){
    	//Test for dumbArray
    	/*int[] array = {0,20,11,1,3,9,10,94};
    	dumbArray(array, "wwwweoooo"); */
	    //}
    
	    /* void dumbArray(int[] array, String text) {
    	System.out.print(text);
    	for (int i = 0; i < array.length; i++) {
    		System.out.print(", " + array[i] );
    	}
    	System.out.println();
    }//dumbArray */
}