
Solution with Suggester Node
- Start with buggy code
- Insert duplicate entry
- Study the db-graph-with-failure-awareness.py which involves the suggester node

Solution by stopping the planning step to stop retrials
Next, again start with the buggy code to trace 
- See in Langsmith
- Modify code to stop the retry logic in case of error in the plan
- Add structured tracability using @tracable()
  