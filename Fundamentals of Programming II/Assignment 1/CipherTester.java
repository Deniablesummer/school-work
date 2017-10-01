//Used to test VigenereCipher.java class
//

public class CipherTester {
	
	public static void main(String[] Args) {
		String key = "bo";
		VigenereCipher test = new VigenereCipher(key);
		String encryptedText = test.encrypt("hello");
		System.out.println(encryptedText);
		
		System.out.println(test.decrypt(encryptedText));
		
		
	}
}
