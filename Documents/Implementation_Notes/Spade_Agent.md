# AAS Agent 

We tried a FSM but its an ```anti-pattern``` to the concept of BDI.
The FSM is more rigied and dose not allow the plans to flow dynmicaly .

So creating an FSM acutly pushes the implementaion to commet to the FSM which takes away the dynamics of the BDI approach .

## Lists and Spade 

Storing values in belifes as string of a list such ```"[data1,data2,...]"``` dose not work ! 
due to the mehtod inside the ```bdi.py``` :

```(python)
@staticmethod
        def _remove_source(belief, source):
            if ")[source" in belief and not source:
                belief = belief.split("[")[0].replace('"', "")
            return belief
```

Example : 

```(shell)
free_time_slots(["08:00-08:30","08:30-09:00",...])[source=python]
splitting at '[' returns 'free_time_slots(' so inner part is empty -> ('',).
```