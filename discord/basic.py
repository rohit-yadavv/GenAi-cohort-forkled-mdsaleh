username = "nikhil"
username = "mohammed"
print(username)
# username[0] = "nohammed"
l1 = [1, 2, 3, 4]
print(l1)
l1[0] = 9
print(l1)

# python datatypes
"""
1. stirng
2. numbers
3. boolean
4. list - []
5. tuple - ()
6. dictinory or dict - {}
7. set - {}
8. none
"""

d1 = {"name": "sandeep", "age": 23}
t1 = (1, 2, ("nikhil", 20))
l2 = [1, 3, 4, 5]
# print(True + 4)

sets = {1, 2, 3, 4, 5}
sets | {1, 2, 3}
sets & {2, 4}
sets - {1, 2, 5}

a = None

# condtionals
"""
1. if
2. if - else
3. if - elif - else
4. match
"""

# if age >= 18:
#     print("eligible for vote")
# else:
#     print("not eligible for voting")
age = 13
# if age < 13:
#     print("child")
# elif age >= 13 and age < 20:
#     print("teenager")
# elif age >= 20 and age < 40:
#     print("adult")
# else:
#     print("senior or old age")


# match age:
#     case age if age < 13:
#         print("child")
#     case age if age >= 13 and age < 20:
#         print("teenager")
#     case age if age >= 20 and age < 40:
#         print("adult")
#     case _:
#         print("senior or old age")


# loops
"""
1. while loop
2. for loop
"""
num = 1
sums = 0
# while num <= 10:
#     sums = sums + 2
#     num = num + 1
#     print(sums)

for i in range(1, 11, 2):
    sums = i + 1
    # print(sums)

# n = 20
# r = range(1, n+1)
# print(type(r))
# print(r)

# numbers = [1, 2, 3, 4, 5]
# for i in numbers:
#     print(i)

# print("length:", len(numbers))

day = 1
# match day:
#   case 1 | 2 | 3 | 4 | 5:
#     print("Today is a weekday")
#   case 6 | 7:
#     print("I love weekends!")


# if day == 1 & day == 2 & day == 3:
#     print("Today is a weekday")
# else:
#     print("nothing")


# def a():
#     if day == 1:
#         return True
    
# print(a())

# functions
"""
1. normal function
2. parameter function
3. *args function
4. **kwargs function  name="saleh", age=23
5. lamda function
"""

# normal function
# def add():
#     a = 2 + 2
#     return a

# print(add())

# def addTwoNum(a, b):
#     z = a + b
#     return z

# print(addTwoNum(5, 9))

# # *ags function
# def printValues(*args):
#     for i in args:
#         print(i)
#     print(args)
#     # print(*args)

# printValues(1, 2, 3, 4)

# # **kwargs
# def printValueTwo(**kwargs):
#     for key, value in kwargs.items():
#         print(f"{key}: {value}")

# printValueTwo(fName="mohammed", lname="saleh", age=23)

square = lambda x, y: (x ** 2) + y
print(square(3, 2))

# list compreheshion
square_num = [x ** 2 for x in range(11)]
print(square_num)