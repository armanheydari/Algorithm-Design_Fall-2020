string = input("enter your statement: ")
res = {}
for c in string:
    res[c]=0
for c in string:
    res[c]+=1
print(res)