(*  Assignment #1 *)
(*	
	CSC 330
	James Ryan
	V00830984
	Created: 1/8/2017
	Revised: 1/12/2017
	Version: 0.11
*)

type DATE = (int * int * int)
exception InvalidParameter

(*
	ml - a list of months
	d1 - date 1
	d2 - date 2
	dl - a list of dates
	sl - a list of strings
	month - a month represented as a number
	DATE - a data type representing a date (year, month, day)
	il - a list of integers
*)
val number_of_days_in_each_month = [31,28,31,30,31,30,31,31,30,31,30,31]


(* Part 1 *)
fun is_older(d1: DATE, d2: DATE): bool =
	if #1 d1 < #1 d2
	then true
	else if #1 d1 > #1 d2
		then false
	else if #2 d1 < #2 d2
		then true
	else if #2 d1 > #2 d2
		then false
	else if #3 d1 < #3 d2
		then true
	else false
					
(* Part 2 *)
fun number_in_month(dl: DATE list, month: int): int =
	if null dl (*if list empty, return 0*)
		then 0
	else if #2(hd(dl)) = month 
		then 1 + number_in_month(tl(dl), month)
	else number_in_month(tl(dl), month)
	
(* Part 3 *)	
fun number_in_months(dl: DATE list, ml: int list): int =
	if null ml
		then 0
	else number_in_month(dl, hd(ml)) + number_in_months(dl, tl(ml))
	
(* Part 4 *)
fun dates_in_month(dl: DATE list, month: int): DATE list =
	if null dl (*if list empty, return empty list*)
		then []
	else if #2(hd(dl)) = month 
		then hd(dl)::dates_in_month(tl(dl), month)
	else dates_in_month(tl(dl), month)
	
(* Part 5 *)
fun dates_in_months(dl: DATE list, ml: int list): DATE list =
	if null ml
		then []
	else dates_in_month(dl, hd(ml)) @ dates_in_months(dl, tl(ml))
	
(* Part 6 *)
fun get_nth(sl: string list, n: int) =
	if null sl
		then raise InvalidParameter
	else if n < 1
		then raise InvalidParameter
	else if n = 1
		then hd(sl)
	else get_nth(tl(sl), (n - 1))
	
(* Part 7 *)
fun date_to_string(d: DATE) =
	let
		val months = ["January ", "February ", "March ", "April ", "May ", "June ", "July ", "August ", "September ", "October ", "November ", "December "]
	in
		get_nth(months, (#2 d)) ^  Int.toString(#3 d) ^ ", " ^ Int.toString(#1 d)
	end
	
(* Part 8 *)
fun number_before_reaching_sum(sum: int, il: int list): int =
	if null il
		then raise InvalidParameter
	else if sum - hd(il) <= 0
		then 0
	else number_before_reaching_sum((sum - hd(il)), (tl(il))) + 1
	
(* Part 9 *)
fun what_month(day: int): int =
		number_before_reaching_sum(day , number_of_days_in_each_month) + 1

(* Part 10 *)
fun month_range(day1: int, day2: int): int list =
	if day1 > day2
		then []
	else what_month(day1)::month_range(day1 + 1, day2)
	
(* Part 11 *)
fun oldest(dl: DATE list): DATE option =
	let
		val x = oldest(tl(dl))
	in
		if null dl
			then NONE
		else if isSome x
				then if is_older(hd(dl), (valOf x))
					then SOME (hd(dl))
				else x
			else SOME (hd(dl))
	end

