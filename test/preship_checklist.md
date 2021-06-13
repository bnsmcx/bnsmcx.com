# Pre-ship Checklist

1. Are all the if/else statements in their simplest form?
	* Assign a boolean variable based directly on an expression rather than using if/else branches
2. Can any repetitive tasks be pulled out into a separate function?
	* Use parameters to handle slight differences in very similar repetitive tasks.
3. (Python) Are all parameters and return types annotated in function declaration?
4. Did you get a 10/10 pylint score?  If not, can you justify the deductions?
5. Are you doing any needless string parsing?  Check to see if there is a built in method/function that returns exactly what you need, or, adapt what you "need" to the standard return value.
6. Are line breaks for long expressions logical?  If you must break, break in a meaningful way that improves readability. This is a good place to use nesting.
7. Are you using an internal method from some external library?  Or an internal built in python method?  Don't.  If there isn't a better solution, write one.
8. Are your return expressions simple?  Don't have the return statement be a complex expression.  Pull the expression into a variable and return the variable.
9. Do any functions attempt to do multiple things?  Refactor.  Every function should do a single thing well.  This is true at every level of design, just with increasing granularity.
10.  Addition by subtraction.  What can you remove entirely.  Always consider a fix or refactor that results in less code.  Our codebase should be as small and durable as possible.
