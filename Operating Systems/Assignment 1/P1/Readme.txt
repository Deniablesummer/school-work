==============
#SSI
James Ryan
V00830984
==============


MAKE FILE
==============
Make
	Using make, will compile all the necessary files, producing an executable called SSI
Make clean
	Using make clean, will remove all executable files created from the make command, leaving the source code.


FUNCTIONALITY
=============

Change Directories
	Use command cd <directory> to change directories
		The directory specified in <directory> can be relative or absolute.
	Use "cd .." to move to the parent directory.
		"cd ../../" will move to the parent's parent directory. This will work recursively until the highest folder has been reached.
	Use "cd ~" to move to the HOME directory specified in the user's PATH.

Run Programs
	Use <program> <args> to execute programs.
	<program> must be specified by it's file path if it's not specified in the user's PATH.
		Example: For SSI to run SSI, specify ./SSI
			 For SSI to run ls, specify ls
	<args> specifies the arguments to be used by the program.
		There can be any number of arguments, as long as the program supports it.

Background Processes
	SSI can run programs in the background. To do this, preface the command with "bg" before the rest of the command
		Example: "bg sleep 5"
	bglist - FUNCTIONALITY NOT SUPPORTED IN THIS VERSION OF SSI
		To list all the current background processes enter the command "bglist"
	When a background process has terminated, a prompt will be given in the following format.
		"<ProcessID>: Process has terminated."

Exit
	To exit SSI, enter "exit"


OTHER NOTES		
=============
The following is a list of all outside code snippets/examples used to help create this program.
	*Tokenize a string
	* https://stackoverflow.com/questions/15472299/split-string-into-tokens-and-save-them-in-an-array
 	*Change terminal font color
 	* https://stackoverflow.com/questions/3585846/color-text-in-terminal-applications-in-unix
	*Using execvp()
	* https://stackoverflow.com/questions/27541910/how-to-use-execvp
	*Using fork and execvp()
	* http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/exec.html

	parse() was not written by me, and has not been modified from it's orginal source located below:
		http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/exec.html

END OF README
	
