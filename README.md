# actr-ato-train
Purpose of the progrom is that a simly actr model is used to control train by tracing ATO curve,  the train model is used is the subway. 
At present, the model can only recognize "+", "-" and "0" simply. By judging these three symbols, the corresponding operations in the declarative memory are extracted, then the manual module of actr pushes the button namely "up" to acceleration, "keep" to hold and "down" to deceleration. 

The future idea is to understand the cognitive mechanism of how human drivers accelerate or decelerates running trains through speed, distance and other ATO information. 
 
actr-ato-train include .lisp * 2,sp_new.lisp is formal，sp_new_2 is a modified version, maybe not run, if you have better suggesttion,you can send me by 18120255@bjtu.edu.cn. I would be grateful！

Note that speedtrace.py, SYL_improved.py, and SYL_spt2.py are three separate versions.
speedtrace.py and SYL_SPT2 all need actr7.x and python3.7, load sp_new_2 or sp_new. however, sp_new_2 may not run.
