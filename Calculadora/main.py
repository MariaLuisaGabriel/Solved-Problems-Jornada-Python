while 1:
    print("Escreva dois números e a operação, caso queira sair, aperte Enter")
    a = input()
    if a == "\r\n": #para linux: "\n"
        break
    
    a = int(a)
    b = int(input())
    op = input()
    
    eq = f"{a} {op} {b}"
    print("Resultado: "+str(eval(eq)))
