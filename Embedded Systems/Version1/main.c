/*
 * RGB to YCC and Back Again Color Space Converter and Image Compressor
 *
 * Author: James Ryan
 * Version: 1 - Pure Software Proof of Concept Implementation
 *
 * Reference Resources Used:
 * ================================================================================================================== *
 * (1) https://sistenix.com/rgb2ycbcr.html - RGB to YCbCr conversion
 * (2) http://www.picturetopeople.org/p2p/image_utilities.p2p/color_converter?color_space=RGB&color_channel1=111&color_
 * channel2=222&color_channel3=255&ResultType=view - Online Color Converter used for verification
 * (3) https://en.wikipedia.org/wiki/Image_file_formats - Image file formats
 * (4) https://stackoverflow.com/questions/51224682/read-file-byte-by-byte-using-c - Reading file in C
 * (5) http://netpbm.sourceforge.net/doc/ppm.html - PPM Format Specification
 */


#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

uint8_t *convertRGBtoYCC(uint8_t red, uint8_t green, uint8_t blue);
uint8_t *convertYCCtoRGB(int y, int cb, int cr);
uint8_t avg(uint8_t p1, uint8_t p2, uint8_t p3, uint8_t p4);


typedef struct {
    uint8_t byte1, byte2, byte3;
}pixel;


int main() {
    // Initialize App
    uint8_t *x;
    FILE *fp;
    FILE *outputfile;
    int i, j;
    char buff[16];

    fp = fopen("vic.ppm", "rb");
    if (fp == NULL) {
        fprintf(stderr, "cannot open input file\n");
        return 1;
    }
    outputfile = fopen("output.ppm", "wb");
    if (fp == NULL) {
        fprintf(stderr, "cannot open input file\n");
        return 1;
    }

    /*
     * Start Reading Image
     */
    uint8_t byte1, byte2, byte3;
    //read image header

    //read magic number - P6
    fgets(buff,sizeof(buff), fp);
    if (buff[0] != 'P' || buff[1] != '6') {
        fprintf(stderr, "Invalid image format (must be 'P6')\n");
        fclose(fp);
        fclose(outputfile);
        exit(1);
    }
    fprintf(outputfile, "P6\n");

    //printf("P6\n");
    //TODO skip comments

    int horz, vert;
    //get image size
    fscanf(fp, "%i %i\n", &horz, &vert);
    //printf("%i %i\n", horz, vert);
    // get width, then height
    fprintf(outputfile, "%i %i\n", horz, vert);
    // max val
    int maxval;
    fscanf(fp, "%d\n", &maxval);


    fprintf(outputfile, "%d\n", maxval);
    //printf("%d\n", maxval);
    pixel aPixel;
    pixel twoRows[2][horz];
    uint8_t *y[horz];
    int cb_avg[horz/2];
    int cr_avg[horz/2];

    /*
     * For each set of two rows of pixels.
     * *read and convert to YCC
     * *average Cb and Cr for each set of 2x2 pixels
     * *convert back to RGB
     * *write to output image
     */
    for (i = 0; i < vert; i+=2) { // for each 2 rows of pixels
	//Get two rows of pixels
        for (j=0; j < horz; j++) { //row1
            aPixel.byte1 = getc(fp);
            aPixel.byte2 = getc(fp);
            aPixel.byte3 = getc(fp);
            x = convertRGBtoYCC(aPixel.byte1, aPixel.byte2, aPixel.byte3);
            aPixel.byte1 = x[0];
            aPixel.byte2 = x[1];
            aPixel.byte3 = x[2];
            twoRows[0][j] = aPixel;
        }

        for (j=0; j < horz; j++) { //row2
            aPixel.byte1 = getc(fp);
            aPixel.byte2 = getc(fp);
            aPixel.byte3 = getc(fp);
            x = convertRGBtoYCC(aPixel.byte1, aPixel.byte2, aPixel.byte3);
            aPixel.byte1 = x[0];
            aPixel.byte2 = x[1];
            aPixel.byte3 = x[2];
            twoRows[1][j] = aPixel;
        }
	// Average Cb and Cr values for 2 by 2 pixels
	for (j=0; j<horz; j+=2) {
	    cb_avg[j/2] = avg(twoRows[0][j].byte2, twoRows[0][j+1].byte2, twoRows[1][j].byte2, twoRows[1][j+1].byte2);
            cr_avg[j/2] = avg(twoRows[0][j].byte3, twoRows[0][j+1].byte3, twoRows[1][j].byte3, twoRows[1][j+1].byte3);
	}
	// End of RGB to YCC - now convert back to RGB and write to file
        for (j=0; j < horz; j+=2) { //row1
            x = convertYCCtoRGB(twoRows[0][j].byte1, cb_avg[j/2], cr_avg[j/2]);
            fwrite(&x[0], 1, 1, outputfile);
            fwrite(&x[1], 1, 1, outputfile);
            fwrite(&x[2], 1, 1, outputfile);
	    x = convertYCCtoRGB(twoRows[0][j+1].byte1, cb_avg[j/2], cr_avg[j/2]);
            fwrite(&x[0], 1, 1, outputfile);
            fwrite(&x[1], 1, 1, outputfile);
            fwrite(&x[2], 1, 1, outputfile);
	}

	
	for (j=0; j < horz; j+=2) { //row2
            x = convertYCCtoRGB(twoRows[1][j].byte1, cb_avg[j/2], cr_avg[j/2]);
            fwrite(&x[0], 1, 1, outputfile);
            fwrite(&x[1], 1, 1, outputfile);
            fwrite(&x[2], 1, 1, outputfile);
	    x = convertYCCtoRGB(twoRows[1][j+1].byte1, cb_avg[j/2], cr_avg[j/2]);
            fwrite(&x[0], 1, 1, outputfile);
            fwrite(&x[1], 1, 1, outputfile);
            fwrite(&x[2], 1, 1, outputfile);
	}      
    }

    free(x);

    fclose(fp);
    fclose(outputfile);
    return 0;
}

/*
 * Function: convertRGBtoYCC
 * converts provided RGB color to YCbCr
 *
 * red  : uint8_t representing the red value
 * green: uint8_t representing the green value
 * blue : uint8_t representing the blue value
 *
 * returns: an uint8_t array containing the YCC values
 */
uint8_t *convertRGBtoYCC(uint8_t red, uint8_t green, uint8_t blue) {
    uint8_t *YCC = malloc(sizeof(uint8_t)*3);
    YCC[0] = (0.257 * red) + (0.504 * green) + (0.098 * blue) + 16;
    YCC[1] = (-0.148 * red) - (0.291 * green) + (0.439 * blue) + 128;
    YCC[2] = (0.439 * red) - (0.369 * green) - (0.071 * blue) + 128;
    return YCC;
}
/*
 * Function: convertYCCtoRGB
 * converts provided YCC color to RGB
 *
 * y  : uint8_t representing the luma value
 * cb: uint8_t representing the Cb value
 * cr : uint8_t representing the Cr value
 *
 * returns: an uint8_t array containing the RGB values
 */
uint8_t *convertYCCtoRGB(uint8_t y, uint8_t cb, uint8_t cr){
    uint8_t *RGB = malloc(sizeof(uint8_t)*3);
    RGB[0] = y + 1.402 * (cr -128);
    RGB[1] = y - 0.344138 * (cb - 128) - 0.714136 * (cr - 128);
    RGB[2] = y + 1.772 * (cb -128);
    return RGB;
}

uint8_t avg(uint8_t p1, uint8_t p2, uint8_t p3, uint8_t p4) {
	return (p1 + p2 + p2 + p4) / 4;
}
