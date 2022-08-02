
class Sbox_properties:
    def __init__(self):
        pass

    def involutive_sbox(self, sbox):
        '''
          Determine whether the S-box satisfies involutive
          '''
        for i in range(0, 16):
            a = sbox[i]
            if i != sbox[a]:
                break

        if i < 15:
            return 0
        else:
            return 100


    def fixed_point(self, sbox):
        '''
        Counting the number of fixed points in the S-box.
         '''
        fix_point = 0
        for i in range(0, 16):
            if i == sbox[i]:
                fix_point = fix_point + 1

        return fix_point


    def hextobin(self, word):
        '''
          Decimal to binary.
           '''
        word = bin(word)[2:]
        for i in range(0, 8 - len(word)):
            word = '0' + word
        return word


    def Balancedness(self, array):
        '''
       Determine whether the S-box satisfies balancedness.
       If yes, true is returned;
       If no, False is returned.
        '''
        if len(set(array)) == len(array):
            return True
        else:
            return False

