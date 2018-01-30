/* 
 * Author: James Ryan
 * Assignment 1
 * SSI.c 
 * Simple Shell Interpreter
*/

/* RESOURCES USED
 *Tokenize a string
 * https://stackoverflow.com/questions/15472299/split-string-into-tokens-and-save-them-in-an-array
 *Change terminal font color
 * https://stackoverflow.com/questions/3585846/color-text-in-terminal-applications-in-unix
 *Using execvp()
 * https://stackoverflow.com/questions/27541910/how-to-use-execvp
 *Using fork and execvp()
 * http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/exec.html
*/

/* Imports */
#include <unistd.h> 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <stdbool.h> //needed for bools

#define FONTRED  "\x1B[31m" //Red text color
#define FONTNRM  "\x1B[0m"  //Normal text color
//Debug printout: printf(FONTRED "[DEBUG]" FONTNRM " \n");

/* Function Declarations */
void process_command(char* command);
void execute(char* command[], bool bgFlag);
void parse(char *line, char **argv);
void change_directory(char *directory);

/* Background process list structure */
struct Bg_Process_List {
	pid_t processID;
	char command[1024];
	struct Bg_Process_List* next;
};

/* Global Variables */
char cwd[1013];
char prompt[1024]; //9 additional characters needed for prompt
struct Bg_Process_List Bgroot;

//main
int main(int argc, const char* argv[]) {
	//Initialization of SSI
	//char prompt[1024]; //User prompt before userinput
	if (getcwd(cwd, sizeof(cwd)) == NULL) {
		perror("getcwd() error");
		exit(-1);
	}
	/* seperate cwd var from prompt shown to user */
	strcpy(prompt, "SSI: ");
	strcat(cwd, "/");
	strcat(prompt, cwd);
	strcat(prompt, " > ");
	//End of Initialization
	
	//Start of SSI
	for (;;) {
		/* Using readline from sample code provided */
		char* userInput = readline(prompt); //get user input, removes \n
		//printf(FONTRED "[DEBUG]" FONTNRM " User Input: %s\n", userInput);
		
		/* Check User input */
		if (!strcmp(userInput, "exit")){ //user indicates to exit
			//printf(FONTRED "[DEBUG]" FONTNRM " User entered 'exit'\n");
			exit(0);
			printf(FONTRED "[ERROR]" FONTNRM " Failed to exit. Please try again.\n");
		} else if (!strcmp(userInput, "")) {
			/* Skip processing if input empty */
			//printf(FONTRED "[DEBUG]" FONTNRM " User entered empty input\n");
		} else {//else process input command
			process_command(userInput);
		}
		free(userInput);
	}
	return(0);
}

void process_command(char* command){
	/* Tokenize Command into array */
	//printf(FONTRED "[DEBUG]" FONTNRM " Tokenizing command %s\n", command);
	char *tokenizedArray[64];
	parse(command, tokenizedArray);
	/* Check if command to be executed in the background */
	if (!strcmp(tokenizedArray[0], "bg")){
		//printf(FONTRED "[DEBUG]" FONTNRM " Background execution detected\n");
		char** bgCommand = tokenizedArray + 1;
		execute(bgCommand, true);
	} else {
		execute(tokenizedArray, false);
	}
	return;
}

/* HELPER FUNCTION USED TO PARSE INPUT STRING INTO A CHAR ARRAY
 * UNMODIFIED
 * http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/exec.html
 */
void  parse(char *line, char **argv)
{
     while (*line != '\0') {       /* if not the end of line ....... */ 
          while (*line == ' ' || *line == '\t' || *line == '\n')
               *line++ = '\0';     /* replace white spaces with 0    */
          *argv++ = line;          /* save the argument position     */
          while (*line != '\0' && *line != ' ' && 
                 *line != '\t' && *line != '\n') 
               line++;             /* skip the argument until ...    */
     }
     *argv = '\0';                 /* mark the end of argument list  */
}

/* Executes command entered by user */
void execute(char **command, bool bgFlag) {
	pid_t pid;
	pid_t pidCheck;
	int status;
	if (!strcmp(command[0], "cd")){
		/* Change directory */
		//printf(FONTRED "[DEBUG]" FONTNRM " change directory.\n");
		change_directory(command[1]);
	} else if (!strcmp(command[0], "bglist")) {
		/* List background processes */
		printf(FONTRED "[ERROR]" FONTNRM " Functionality not implemented.\n");
		/*struct Bg_Process_List currentNode = Bgroot;
		while (currentNode.next != NULL) {
			currentNode = *currentNode.next;
			printf("%d\n", currentNode.processID);
		} */
	} else {
		if ((pid = fork()) < 0) {
			/* Error occured */
		} else if (pid == 0) {
			/* Child process */	
			if (execvp(*command, command) < 0) {
				/* execvp failed */
				printf(FONTRED "[ERROR]" FONTNRM "Command Execution Failed.\n");
			}
		} else {
			/* Parent process */
			if (!bgFlag) {
				/* Not a background process */
				waitpid(pid, NULL, 0);
			} else {
				/* Background process */
				//TODO: Add process info to a list
				/*struct Bg_Process_List current = Bgroot;
				while (current.next != NULL) {
					current = *current.next;
				}
				current.processID = pid;
				//strcpy(current.command, commandString);
				//printf(FONTRED "[DEBUG]" FONTNRM "current.command = %s\n", current.command);
				*/
			}
			do {
				if ((pidCheck = waitpid(0, NULL, WNOHANG)) == -1) {
					//printf(FONTRED "[ERROR]" FONTNRM " waitpid() error.\n");
				} else if (pidCheck > 0) {
					/* Process has finished */
					//TODO: Remove process info from list
					printf("%d: Process has terminated.\n", pidCheck);
				}
			} while (pidCheck > 0);
		}
	}	
	return;
}

/* Changes directory to specified directory */
void change_directory(char *directory) {
	if (!strcmp(directory, "~")) {
		/* Go to home directory */
		if (chdir(getenv("HOME")) == -1) {
			/* chdir error */
			printf(FONTRED "[ERROR]" FONTNRM " chdir() Error\n");
			return;
		} else {
			if (getcwd(cwd, sizeof(cwd)) == NULL) {
				perror("getcwd() error");
				exit(-1);
			}
		}
	} else {
		/* Go to directory */
		if (chdir(directory) == -1) {
			/* chdir error */
			printf(FONTRED "[ERROR]" FONTNRM " chdir() Error\n");
		} else {
			if (getcwd(cwd, sizeof(cwd)) == NULL) {
				perror("getcwd() error");
				exit(-1);
			}
		}
	} 
	//Change user prompt
	strcpy(prompt, "SSI: ");
	strcat(cwd, "/");
	strcat(prompt, cwd);
	strcat(prompt, " > ");
}
