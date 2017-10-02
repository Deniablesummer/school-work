 /*Assignment 4
 *For 23 numbers, finds thes fibonacci number (n) for number (i)
 *Then blinks LED#(i mod 6) n number of times
 */


//Including libraries
#include <stdio.h>
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>

/*Returns a Fibonnaci Number
 *Params: int n : the 'n'th number you want to compute
 *Return: int : the fibonnaci number
 *Maximum n'th fibonnaci number is 22 because of an int overflow
 */
int Fibon(int n) {
	if (n < 2)
		return n;
	else
		return (Fibon(n - 1) + Fibon(n - 2));

}

//blinks 'i'th LED on the LED board
//n number of times
void blinkLED(int i, int n) {
	//sets PORTL and PORTB to output
	DDRL = 0xFF;
  	DDRB = 0xFF;
	switch (i) {
		case 0: //Flash LED0 n times
			for (int counter = 0; counter < n; counter++) {
				PORTL = 10000000;
				_delay_ms(100);
				PORTL = 0x00;
				_delay_ms(100);
			}
			break;
		case 1: //Flash LED1 n times
			for (int counter = 0; counter < n; counter++) {
				PORTL = 10100000;
				_delay_ms(100);
				PORTL = 0x00;
				_delay_ms(100);
			}
			break;
		case 2: //Flash LED2 n times
			for (int counter = 0; counter < n; counter++) {
				PORTL = 10101000;
				_delay_ms(100);
				PORTL = 0x00;
				_delay_ms(100);
			}
			break;
		case 3: //Flash LED3 n times
			for (int counter = 0; counter < n; counter++) {
				PORTL = 10101010;
				_delay_ms(100);
				PORTL = 0x00;
				_delay_ms(100);
			}
			break;
		case 4: //Flash LED4 n times
			for (int counter = 0; counter < n; counter++) {
				PORTB = 10101000;
				_delay_ms(100);
				PORTB = 0x00;
				_delay_ms(100);
			}
			break;
		case 5: //Flash LED5 n times
			for (int counter = 0; counter < n; counter++) {
				PORTB = 10101010;
				_delay_ms(100);
				PORTB = 0x00;
				_delay_ms(100);
			}
			break;
	}
	//.1sec pause then clears all LEDS
	_delay_ms(100);
	PORTL = 0x00;
	PORTB = 0x00;
}

//main
int main(void){
	for (int x = 0; x <= 22; x++){
		blinkLED((x % 6), Fibon(x));
	}
	return 0;
} //endmain



