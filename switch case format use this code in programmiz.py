'''

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

'''
lang = input("Enter a language to learn : ")
match lang:
    case "JS":
        print("Web developer")
    case "PY":
        print("Data Scientist")
    case "PHP":
        print("Backend developer")
    case _: #like default statement in java and c vera yethavthu value va represent panna _ use pannu
        print("Nothing you will learn")