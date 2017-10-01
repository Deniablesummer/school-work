/**
 * TaskList.java
 * Created for CSC 115 Assignment Two.
 */

/**
 * An interface implemented by all TaskList classes. Operations
 * are meant to support a task simulator (i.e., task arrivals,
 * scheduling/dispatching, deletion).
 */
public interface TaskList {
    /** 
     * Examines the task list; if there are no tasks
     * returnst true, otherwise false.
     * @return whether or not the list contains tasks
     */
    public boolean isEmpty();

    /** 
     * Either retrieves or computes the number of tasks
     * currently stored in the task list.
     * @return number greater than or equal to 0 corresponding
     * to number of items inthe
     */
    public int  getLength();

    /**
     * If the list has at least one task, then the task at
     * the head is removed from the list, and this task
     * is returned. If there are no items in the list,
     * then the value returned is null.
     * @return a Task object corresponding the the task at the
     * head of the list; possibly null.
     */
    public Task removeHead();

    /**
     * If there are no items in the list, the value of
     * of null is returned.
     *
     * If the list has at least one task, then the list
     * is searched for a task with the same priority and
     * number as t. When found, this task is removed from
     * the list, and t is returned; otherwise the value
     * of null is returned.
     * @param t Task to be removed from the list.
     * @return a Task object corresponding the the task at the
     * head of the list; possibly null.
     */
    public Task remove(Task t);

    /** 
     * Accepts a task to be inserted into the list. Assume
     * PREV is the task in the list after insertion, and
     * SUCC is the task in the list after insertion. The
     * following two conditions must hold.
     * (1) t.priority > SUCC.priority
     * (2) if PREV.priority == t.priority, then
     *     PREV must have been inserted at an earlier
     *     time than t.
     * (3) if PREV.priority > t.priority, then t is
     *     the only task in the list having t.priority.
     * Also: No two tasks in the list may have the same
     * task number.
     * @param t task to be placed into the task list
     */
    public void insert(Task t);

    /**
     * Takes an integer value indicate that the ith task
     * in the list is to be returned. When i is 0, the first
     * task is returned, when i is 1, the second task is
     * returned, etc. If there is no such task i, then null
     * is returned. The list is not modified by this operation.
     * @param i indicates the number of task from the start of
     * of the list which will be the task returned
     * @return contents of the ith task in the list; possibly null
     */ 
    public Task retrieve(int i);
}
