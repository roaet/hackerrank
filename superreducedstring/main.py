import sys

def reduce_string(istring):
    stack = []
    for l in istring:
        stack.append(l)
        if len(stack) <= 1:
            continue
        if stack[-1] == stack[-2]:
            stack.pop()
            stack.pop()
    return "".join(stack)
       

start_string = raw_input().strip()
old_string = start_string
next_string = reduce_string(old_string)
while next_string != old_string:
    old_string = next_string
    next_string = reduce_string(next_string)
if len(next_string) == 0:
    next_string = "Empty String"
print next_string
