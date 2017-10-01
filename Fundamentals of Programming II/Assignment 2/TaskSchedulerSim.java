import java.util.*;
import java.io.*;

/**
 * Provided for CSC 115, Assignment Two (2015 Spring)
 *
 * Accepts the name of a file containing a sequence of events for
 * some simulated operating system:
 *
 * - TA: task arrival (priority & number)
 * - SC: task scheduling
 * - TD: task deletion (removal)
 * - ST: status
 *
 * Each line from the input is analyzed, and appropriate
 * operations performed on a TaskList instance. The results
 * of SC and ST operations are saved as output in the
 * file whose name is specified on the command line.
 *
 * @author Mike Zastre (UVic Department of Computer Science)
 * @version 1
 */
public class TaskSchedulerSim {
    public static void main(String args[]) {
        String infileName = null;
        String outfileName = null;

        // Process the command-line options and arguments.
        try {
            for (int i = 0; i < args.length; i++) {
                if (args[i].equals("-i")) {
                    infileName = args[i+1];
                } else if (args[i].equals("-o")) {
                    outfileName = args[i+1];
                }
            }

            if (infileName == null) {
                System.out.println("Usage: please provide an input filename");
            }

            if (outfileName == null) {
                System.out.println("Usage: please provide an output filename");
            }

            if (infileName == null || outfileName == null) {
                System.exit(1);
            }

            // If we reach this point in the code, we have all the 
            // information needed to proceed with processing.

            Scanner infileScanner;
            PrintStream outfileStream;

            // **************************************************
            // THE NEXT STATMENT IS THE ONLY LINE TO BE MODIFIED
            // AND ONLY THE RIGHT-HAND SIDE AT THAT (TO THE RIGHT
            // OF THE = SIGN). SORRY FOR SHOUTING (AGAIN).
            //
            // Cipher c = new NullCipher(key);

            infileScanner = new Scanner(new File(infileName));
            outfileStream = new PrintStream(new File(outfileName));

            // TaskList tl = new TaskListArrayBased(200);
            TaskList tl = new TaskListRefBased(200);
            while (infileScanner.hasNext()) {
                int taskPriority;
                int taskNumber;

                String op = infileScanner.next();
                if (op.equals("ST")) {
                    outfileStream.println("[" + tl.getLength() + "]");
                } else if (op.equals("TA")) {
                    taskPriority = infileScanner.nextInt();
                    taskNumber = infileScanner.nextInt();
                    tl.insert(new Task(taskPriority, taskNumber));
                } else if (op.equals("TD")) {
                    taskPriority = infileScanner.nextInt();
                    taskNumber = infileScanner.nextInt();
                    tl.remove(new Task(taskPriority, taskNumber));
                } else if (op.equals("SC")) {
                    Task nextT = tl.removeHead();
                    if (nextT != null) {
                        outfileStream.println(nextT.number);
                    } else {
                        outfileStream.println("NULL");
                    }
                }
            }

            outfileStream.close();
        } 
        catch (IOException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
        catch (ArrayIndexOutOfBoundsException e) {
            System.err.println("Probably not enough arguments provided.\n");
            System.exit(1);
        }
    }

}
