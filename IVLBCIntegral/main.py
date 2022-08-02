from IVLBC import IVLBC

if __name__ == "__main__":

    ROUND = int(input("Input the target round number: "))
    while not (ROUND > 0):
        print("Input a round number greater than 0.")
        ROUND = int(input("Input the target round number again: "))


    a=0
    i=0
    while not(a==1):
            i+=1
            IVLBC1 = IVLBC(ROUND, i)
            constant_bits = [i]
            print("%d / %d" % (i, 64))
            IVLBC1.set_constant_bits(constant_bits)
            IVLBC1.MakeModel()
            a=IVLBC1.solve_model()




