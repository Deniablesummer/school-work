/*
 * TaskListRefBased
 * 
 */
import java.util.*;
public class TaskListRefBased implements TaskList {
	private int length;
	private int arrivalTime;
	private TaskListNode curr = new TaskListNode(0,0);
	private TaskListNode head = new TaskListNode(0,0);
	private TaskListNode temp = new TaskListNode(0,0);
	private TaskListNode prev = new TaskListNode(0,0);
	private Task tempTask = new Task(0,0);
	
	public TaskListRefBased(int i) {
		this.length = 0;
	}

	/** 
     * Examines the task list; if there are no tasks
     * returnst true, otherwise false.
     * @return whether or not the list contains tasks
     */
	public boolean isEmpty() {
		if (this.length == 0) {
			return true;
		} else {
			return false;
		}
	}

	/** 
     * Either retrieves or computes the number of tasks
     * currently stored in the task list.
     * @return number greater than or equal to 0 corresponding
     * to number of items inthe
     */
	public int getLength() {
		return this.length;
	}

	/**
     * If the list has at least one task, then the task at
     * the head is removed from the list, and this task
     * is returned. If there are no items in the list,
     * then the value returned is null.
     * @return a Task object corresponding the the task at the
     * head of the list; possibly null.
     */
	public Task removeHead() {
		if (length == 0 ) {
			return null;
		}
		this.length--;
		tempTask.priority = head.priority;
		tempTask.number = head.number;
		head = head.next;			 
		return tempTask;
	}

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
	public Task remove(Task t) {
		if (length == 0) {
			return null;
		}
		curr = head;
		//if task to be removed is head
		if (curr.priority == t.priority) {
			tempTask = removeHead();
			return tempTask;
		}
		//find the task to be removed and remove it
		prev = curr;
		curr = curr.next;
		for (int i = 0; i < length; i++) {
			if (curr.priority == t.priority) {
				tempTask.priority = curr.priority;
				tempTask.number = curr.number;
				prev.next = curr.next;
				curr.next = null;
				this.length--;
				return tempTask;
			}
			prev = curr;
			curr = curr.next;
		}
		//if none of above cases found, return null
		return null;		
	}

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
	public void insert(Task t) {
		//If list length is 0 before insert
		if (this.length == 0) {
			head.priority = t.priority;
			head.number = t.number;
			head.next = null;
		} else {
			//If head is lower priority then new task
			if (head.priority < t.priority) {
				temp.priority = t.priority;
				temp.number = t.number;
				temp.next = head;
				head = temp;
			} else {
				//if head is the only item
				if (head.next == null) {
					temp.priority = t.priority;
					temp.number = t.number;
					head.next = temp;
					length++;
					return;
				}
				//find where to put the task
				curr = head.next;
				prev = head;
				for (int i = 0; i < length; i++) {		
					if (curr.priority < t.priority) {
						temp.priority = t.priority;
						temp.number = t.number;
						temp.next = curr;
						prev.next = temp;
						length++;
						return;
					}
				prev = curr;
				curr = curr.next;
				}
			}
		}
	}
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
	public Task retrieve(int i) {
		if (length <= i) {
		return null;
		}
		if (i == 0) {
			tempTask.priority = head.priority;
			tempTask.number = head.number;
			return tempTask;
		}
		int ind = 0;
		curr = head;
		do {
			curr = curr.next;
			ind++;
		} while (ind < i);
		tempTask.priority = curr.priority;
		tempTask.number = curr.number;
		return tempTask;
	}

	
	
	
}
