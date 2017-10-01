
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;


public class ImageProcessor {

	public static void main(String[] args) throws FileNotFoundException {
		try { //Try statement to catch exceptions caused by user error
			String transformation = args[0];
			String inputFileName = null; //initilizing file names
			String outputFileName = null;
			switch (transformation) { //Switch statement to check which transformation the user wants
			//each case grabs the corresponding values from args dependant on which transformation (args[0]) is selected
			case "-ascii":
				inputFileName = args[1];
				PrintStream output = new PrintStream(new File(args[2]));
				convertAscii(inputFileName,output);
				break;
			case "-reflectV":
				inputFileName = args[1];
				outputFileName = args[2];
				reflectV(inputFileName,outputFileName);
				break;
			case "-reflectH":
				inputFileName = args[1];
				outputFileName = args[2];
				reflectH(inputFileName,outputFileName);
				break;
			case "-tile":
				int hzNum = Integer.parseInt(args[1]);
				int vtNum = Integer.parseInt(args[2]);
				if (hzNum < 1 || vtNum < 1) {
					System.err.println("The integers for horizontal tiling and vertical tiling must be 1 or greater."
							+ "\nPlease try again.");
					System.exit(-3);
				}
				inputFileName = args[3];
				outputFileName = args[4];
				tile(hzNum, vtNum, inputFileName,  outputFileName);
				break;
			case "-adjustBrightness":
				int brightAmount = Integer.parseInt(args[1]);
				inputFileName = args[2];
				outputFileName = args [3];
				adjustBrightness(brightAmount, inputFileName, outputFileName);	
				break;
			default: System.err.println("That was not a valid input.\nCheck spelling and formatting. Please try again!");
				//If transformation was not correct this will be executed.
				System.exit(-2);
				}
			}	
		catch(java.lang.NumberFormatException | IOException ex) { //once caught, use is informed that their input format is wrong.
			System.err.println("Format of input was incorrect.");
			System.exit(-2);
		}
	}	
	public static void convertAscii(String inputFileName, PrintStream output) {	//needs input file name, output file name and writeAsciiImage()
		int[][] image = readGrayscaleImage(inputFileName);
		char[][] imageout = new char[image.length][image[0].length];
		for (int row = 0; row < image.length; row++) {
			for (int column = 0; column < image[row].length; column++) {
				if (0 <= image[column][row] && 26 > image[column][row]) { //changes grayscale values of each pixel into an ascii char
					imageout[column][row] = 'M';
				} else if (26 <= image[column][row] && 51 > image[column][row]) {
					imageout[column][row] = '$';
				} else if (51 <= image[column][row] && 77 > image[column][row]) {
					imageout[column][row] = 'o';
				}  else if (77 <= image[column][row] && 103 > image[column][row]) {
					imageout[column][row] = '|';
				} else if (103 <= image[column][row] && 128 > image[column][row]) {
					imageout[column][row] = '*';
				} else if (128 <= image[column][row] && 153 > image[column][row]) {
					imageout[column][row] = ':';
				} else if (153 <= image[column][row] && 179 > image[column][row]) {
					imageout[column][row] = '=';
				} else if (179 <= image[column][row] && 205 > image[column][row]) {
					imageout[column][row] = '\'';
				} else if (205 <= image[column][row] && 231 > image[column][row]) {
					imageout[column][row] = '.';
				} else if (231 <= image[column][row] && 255 >= image[column][row]) {
					imageout[column][row] = ' ';
				}
			}
		}
		writeAsciiImage(output, imageout);
	}
	public static void writeAsciiImage(PrintStream output, char imageout[][]) { //needs a printstream object, and a char[][] with the ascii version 
		//of the image
		for (int row = 0; row < imageout.length; row++) {
			for (int column = 0; column < imageout[row].length; column++) {
				output.print(imageout[row][column]);
			}
		output.println();
		}
	}
	public static void reflectV(String inputFileName, String outputFileName) { //requires readGrayscaleImage(), writeGrayscaleImage. Parameters are the 
		//imagefilename, and the outputfilename
		int[][] image = readGrayscaleImage(inputFileName);
		int[][] imageout = new int[image.length][image[0].length];
		int x = 0;
		for (int row = 0; row < image.length; row++) {
			x = image[row].length;
			for (int column = 0; column < image[row].length; column++) {
				imageout[row][column] = image[row][x-1];
				x--;
			}
		}
		writeGrayscaleImage(outputFileName, imageout);
	}
	public static void reflectH(String inputFileName, String outputFileName) { //requires readGrayscaleImage(), writeGrayscaleImage. Parameters are the imagefilename, and the outputfilename
		int[][] image = readGrayscaleImage(inputFileName);
		int[][] imageout = new int[image.length][image[0].length];
		int x = 0;
		for (int column = 0; column < image[0].length; column++) {
			x = image.length;
			for (int row = 0; row < image.length; row++) {
				imageout[row][column] = image[x-1][column];
				x--;
			}
		}
		writeGrayscaleImage(outputFileName, imageout);
	}
	public static void tile(int hzNum, int vtNum, String inputFileName, String outputFileName) { //requires readGrayscaleImage(), writeGrayscaleImage. Parameters are the 
		//hzNum of tiles, vtNum of tiles, imagefilename, and the outputfilename
		int[][] image = readGrayscaleImage(inputFileName);
		int x = image[0].length;
		int y = image.length;
		int[][] imageout = new int[y*vtNum][x*hzNum];
		for (int i=0; i<image.length; i++) {
	        for (int j=0; j<image[0].length; j++) {
	                for (int k=0; k<vtNum; k++) {
	                        for (int l=0; l<hzNum; l++) {
	                            imageout[i +(k*y)][j + (l*x)]=image[i][j];
	                        }
	                }
	        }
	}	
		writeGrayscaleImage(outputFileName, imageout);
	}
	public static void adjustBrightness(int amount, String inputFileName, String outputFileName) { //requires readGrayscaleImage(), writeGrayscaleImage. Parameters are the 
		//amount to brighten/darken, imagefilename, and the outputfilename
		int[][] image = readGrayscaleImage(inputFileName);
		for (int y = 0; y < image.length; y++) {
			for (int x = 0; x < image[0].length; x++) {
				image[y][x] = image[y][x] + amount;
				if (image[y][x] < 0) { //checks to make sure values are within 0 and 255
					image[y][x] = 0;
				} else if (image[y][x] > 255) {
					image[y][x] = 255;
				}			
			}
		}
		writeGrayscaleImage(outputFileName, image);	
	}
		
	// THIS METHOD MAY BE CALLED, BUT MUST NOT BE MODIFIED!
    // This method reads an image file.
    // expects one parameter: a filename of an image file to be read
    // returns a 2D array of ints representing grayscale values in the input image
    public static int[][] readGrayscaleImage(String filename) {
        int [][] result = null; //create the array
        try {
            File imageFile = new File(filename);
    //create the file
            BufferedImage image = ImageIO.read(imageFile);
            int height = image.getHeight();
            int width  = image.getWidth();
            result = new int[height][width];
        //read each pixel value
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    int rgb = image.getRGB(x, y);
                    result[y][x] = rgb & 0xff;
                }
            }
        }
        catch (IOException ioe) {
            System.err.println("Problems reading file named " + filename);
            System.exit(-1);
        }
        return result;
        //once we're done filling it, return the new array
    }
    // THIS METHOD MAY BE CALLED, BUT MUST NOT BE MODIFIED!
    // This method creates an output image based on an array of ints and writes it to a file.
    // expects two parameters: a filename for the image file that will be created
    // and a 2D array of ints that will be converted into the image
    public static void writeGrayscaleImage(String filename, int[][] array) {
        int width = array[0].length;
        int height = array.length;
        try {
            BufferedImage image = new BufferedImage(width, height,
            		BufferedImage.TYPE_INT_RGB);
    //create the image          
            //set all its pixel values based on values in the input array
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    int rgb = array[y][x];
                    rgb |= rgb << 8;
                    rgb |= rgb << 16;
                    image.setRGB(x, y, rgb);
                }
            }
            //write the image to a file
            File imageFile = new File(filename);
            ImageIO.write(image, "jpg", imageFile);
        }
        catch (IOException ioe) {
            System.err.println("Problems writing file named " + filename);
            System.exit(-1);
        }
    }
}