import lab1_25010610_25010127 as lab

print(lab.infer("~X v Y", "X v Z"))
print(lab.infer("a > b", "a > r"))
print(lab.infer("P > Q", "P"))
print(lab.infer("P", "P > Q"))
print(lab.infer("P > Q","P"))
print(lab.infer("P > Q", "~Q"))
print(lab.infer("P > Q", "Q > R"))
print(lab.infer("P v Q", "~P"))