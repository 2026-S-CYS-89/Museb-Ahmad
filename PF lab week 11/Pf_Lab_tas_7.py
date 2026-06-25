n=int(input("enter the number of students"))
i=1
while i<=n:
        name=input("student")
        roll_no =int(input("enter roll no"))
        a=int(input("enter obtained marks"))
        b=int(input("enter total marks number"))
        c=a/b*100
        print(name)
        print(roll_no)
        print(c)
        if c>90:
         print("A")
        elif c > 85:
            print("A-")
        elif c>80:
         print("B+")
        elif c>75:
          print("B")
        elif c>70:
            print("B-")
        elif c>65:
            print("C+")
        elif c>60:
            print("C")
        elif c>55:
            print("C-")
        elif c>50:
            print("D")
        else:
            print("you are fail")
        i=i+1
