(* Assignment 1 Simple Test *)

(* These are basic test cases.  *)

(* loads the bindings from the file with your solutions *)

(* All the tests should evaluate to true. For example, the REPL should say: val test1 = true : bool *)

use "hw1.sml";

(* Some bindings to avoid repetition *)

val feb28_2012 = (2012, 2, 28);
val feb12_2011 = (2011, 2, 12);
val dec1_2013 = (2013,  12,  1);
val march31_2011 = (2011,  3,  31);
val april28_2011 = ( 2011,  4,  28);
val june1_2013 = (2013,  6,  1);

val test1 = is_older(( 1,  2,  3),( 2,  3,  4)) = true;
val test1a = is_older(feb28_2012,dec1_2013) = true;
val test1b = is_older(dec1_2013, feb28_2012) = false;
val test1c = is_older(dec1_2013, dec1_2013) = false;

val test2 = number_in_month([feb28_2012,dec1_2013],2) = 1;
val test2a = number_in_month([feb28_2012,dec1_2013],3) = 0;
val test2b = number_in_month([feb28_2012,dec1_2013,march31_2011,april28_2011],3) = 1;
val test2b = number_in_month([feb28_2012,dec1_2013,feb12_2011,march31_2011,april28_2011],2) = 2;

val test3a = number_in_months([feb28_2012,dec1_2013,march31_2011,april28_2011],[2,3,4]) = 3;

val test4  = dates_in_month([feb28_2012,dec1_2013],2) = [feb28_2012];
val test4a = dates_in_month([feb28_2012,dec1_2013],12) = [dec1_2013];
val test4b = dates_in_month([feb28_2012,dec1_2013],3) = [];
val test4c = dates_in_month([feb28_2012,feb12_2011,dec1_2013],2) = [feb28_2012,feb12_2011];

val test5a = dates_in_months([feb28_2012,dec1_2013,march31_2011,april28_2011],[2,3,4]) = [feb28_2012,march31_2011,april28_2011];
                                                                                             
val test5d = dates_in_months([feb28_2012,dec1_2013,march31_2011,april28_2011],[5,7]) = [];

val test6 = get_nth(["hi", "there", "how", "are", "you"], 2) = "there";
val test6a = get_nth(["hi", "there", "how", "are", "you"], 7) = "never" handle InvalidParameter => true;
val test6b = get_nth(["hi", "there", "how", "are", "you"], 0) = "never" handle InvalidParameter => true;
val test6c = get_nth([], 0) = "never" handle InvalidParameter => true;

val test7 = date_to_string(june1_2013) = "June 1, 2013";
val test7a = date_to_string(april28_2011) = "April 28, 2011";

val test8 = number_before_reaching_sum(10, [1,2,3,4,5]) = 3
val test8a = number_before_reaching_sum(10, [11,1,2,3,4,5]) = 0
val test8b = number_before_reaching_sum(12, [11,1,2,3,4,5]) = 1
val test8c = number_before_reaching_sum(1, [1,2,3,4,5]) = 0;
val test8d = number_before_reaching_sum(6, [1,2,3,4,5]) = 2;

val test9  = what_month(70) = 3;
val test9a = what_month(31) = 1;
val test9b = what_month(32) = 2;
val test9c = what_month(360) = 12;
val test91 = what_month(70) = 3;
val test92 = what_month(30) = 1;
val test93 = what_month(1) = 1;
val test94 = what_month(32) = 2;
val test95 = what_month(365) = 12;
val test96 = what_month(364) = 12;

val test10 = month_range(31, 34) = [1,2,2,2];
val test10a = month_range(360, 365) = [12,12,12,12,12,12];
val test10b = month_range(31,31 + 28 +1) = [1,
                                           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
                                           3];
val test10c = month_range(35, 34) = [];
val test10d = month_range(35, 35) = [2];
val test10e = month_range(31+29, 31+29) = [3];

val test11 = oldest([feb28_2012,march31_2011,april28_2011]) = SOME march31_2011;
val test11a = oldest([april28_2011]) = SOME april28_2011;
val test11b = oldest([]) = NONE;

val test12 = reasonable_date( 2014,  12,  31);
val test12a = not (reasonable_date ( 2015,  2,  29));

val test12b = reasonable_date( 2012,  2,  29);
val test12c = not (reasonable_date( 2014,  0,  31));
val test12d = not (reasonable_date( 2014,  13,  31));
val test12e = not (reasonable_date( 2013,  2,  29));

val test610 = reasonable_date (2014, 10, 14) = true;
