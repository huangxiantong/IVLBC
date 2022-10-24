from IVLBC import IVLBC

if __name__ == "__main__":

    ROUND = int(input("Input the target round number: "))
    while not (ROUND > 0):
        print("Input a round number greater than 0.")
        ROUND = int(input("Input the target round number again: "))

    ACTIVEBITS = int(input("Input the number of acitvebits: "))
    while not (ACTIVEBITS < 64 and ACTIVEBITS > 0):
        print("Input a number of activebits with range (0, 64):")
        ACTIVEBITS = int(input("Input the number of acitvebits again: "))

    IVLBC1 = IVLBC(ROUND, ACTIVEBITS)
    constant_bits = [ACTIVEBITS]
    print("%d / %d" % (ACTIVEBITS, 64))
    IVLBC1.set_constant_bits(constant_bits)
    IVLBC1.MakeModel()
    a=IVLBC1.solve_model()




