from gurobipy import *
import time

FP16 = (5,10,14,7,13,0,8,3,6,15,1,12,11,4,2,9)
key_p80=(40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,
         60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
         11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
         31,32,33,34,35,36,37,38,39,0,1,2,3,4,5,6,7,8,9,10)
class IVLBCDiff_rk:
    def __init__(self, Round):
        self.Round = Round
        self.blocksize = 16
        self.filename_model = "IVLBC " + str(self.Round) + ".lp"
        self.filename_result = "result_" + str(self.Round) + ".txt"
        fileobj = open(self.filename_model, "w")
        fileobj.close()
        fileboj = open(self.filename_result, "w")
        fileobj.close()

    def MakeModel(self):
        """
        Generate the MILP model of Present given the round number and activebits.
        """
        self.CreateObjectiveFunction()
        self.Constraint()
        self.VariableBinary()

    def CreateObjectiveFunction(self):
        """
        Create objective function of the MILP model
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Minimize\n")
        eqn = []
        for i in range(0, self.Round):
            eqn.append("x" + "_" + str(0 + i * 17))
            eqn.append("x" + "_" + str(1 + i * 17))
            eqn.append("x" + "_" + str(2 + i * 17))
            eqn.append("x" + "_" + str(3 + i * 17))
            eqn.append("x" + "_" + str(4 + +i * 17))
            eqn.append("x" + "_" + str(5 + i * 17))
            eqn.append("x" + "_" + str(6 + i * 17))
            eqn.append("x" + "_" + str(7 + i * 17))
            eqn.append("x" + "_" + str(8 + i * 17))
            eqn.append("x" + "_" + str(9 + +i * 17))
            eqn.append("x" + "_" + str(10 + i * 17))
            eqn.append("x" + "_" + str(11 + i * 17))
            eqn.append("x" + "_" + str(12 + i * 17))
            eqn.append("x" + "_" + str(13 + i * 17))
            eqn.append("x" + "_" + str(14 + +i * 17))
            eqn.append("x" + "_" + str(15 + i * 17))
            eqn.append("x" + "_" + str(16 + i * 17))

        temp = " + ".join(eqn)
        fileobj.write(temp)
        fileobj.write("\n")
        fileobj.close()

    def Constraint(self):
        assert (self.Round >= 1)
        fileobj = open(self.filename_model, "a")
        fileobj.write("Subject To\n")
        fileobj.close()
        variablein_X = IVLBCDiff_rk.CreateVariables_X(self, 0)
        variablein_H = IVLBCDiff_rk.CreateVariables_H (self, 0)
        variablein_k = IVLBCDiff_rk.CreateVariables_k(self, 0)
        variablein_K = IVLBCDiff_rk.CreateVariables_K(self, 0)
        variableout = []
        variableout_rk = []
        d = IVLBCDiff_rk.CreateVariablesdd(self, 0)

        self.Constraints(variablein_k)

        self.ConstraintsKeys_add(variablein_K[0], variablein_H[0], variablein_X[0], d[0])
        self.ConstraintsKeys_add(variablein_K[1], variablein_H[1], variablein_X[1], d[1])
        self.ConstraintsKeys_add(variablein_K[2], variablein_H[2], variablein_X[2], d[2])
        self.ConstraintsKeys_add(variablein_K[3], variablein_H[3], variablein_X[3], d[3])
        self.ConstraintsKeys_add(variablein_K[4], variablein_H[4], variablein_X[4], d[4])
        self.ConstraintsKeys_add(variablein_K[5], variablein_H[5], variablein_X[5], d[5])
        self.ConstraintsKeys_add(variablein_K[6], variablein_H[6], variablein_X[6], d[6])
        self.ConstraintsKeys_add(variablein_K[7], variablein_H[7], variablein_X[7], d[7])
        self.ConstraintsKeys_add(variablein_K[8], variablein_H[8], variablein_X[8], d[8])
        self.ConstraintsKeys_add(variablein_K[9], variablein_H[9], variablein_X[9], d[9])
        self.ConstraintsKeys_add(variablein_K[10], variablein_H[10], variablein_X[10], d[10])
        self.ConstraintsKeys_add(variablein_K[11], variablein_H[11], variablein_X[11], d[11])
        self.ConstraintsKeys_add(variablein_K[12], variablein_H[12], variablein_X[12], d[12])
        self.ConstraintsKeys_add(variablein_K[13], variablein_H[13], variablein_X[13], d[13])
        self.ConstraintsKeys_add(variablein_K[14], variablein_H[14], variablein_X[14], d[14])
        self.ConstraintsKeys_add(variablein_K[15], variablein_H[15], variablein_X[15], d[15])

        variableout = self.VariableRotation(variablein_X)

        H_16 = IVLBCDiff_rk.CreateVariable(self, "H", 16)
        H_17 = IVLBCDiff_rk.CreateVariable(self, "H", 17)
        H_18 = IVLBCDiff_rk.CreateVariable(self, "H", 18)
        H_19 = IVLBCDiff_rk.CreateVariable(self, "H", 19)
        self.ConstraintsByLF(variableout[0], variableout[1], variableout[2], variableout[3], H_16, H_17, H_18, H_19,
                             d[16])
        H_20 = IVLBCDiff_rk.CreateVariable(self, "H", 20)
        H_21 = IVLBCDiff_rk.CreateVariable(self, "H", 21)
        H_22 = IVLBCDiff_rk.CreateVariable(self, "H", 22)
        H_23 = IVLBCDiff_rk.CreateVariable(self, "H", 23)
        self.ConstraintsByLF(variableout[4], variableout[5], variableout[6], variableout[7], H_20, H_21, H_22, H_23,
                             d[17])
        H_24 = IVLBCDiff_rk.CreateVariable(self, "H", 24)
        H_25 = IVLBCDiff_rk.CreateVariable(self, "H", 25)
        H_26 = IVLBCDiff_rk.CreateVariable(self, "H", 26)
        H_27 = IVLBCDiff_rk.CreateVariable(self, "H", 27)
        self.ConstraintsByLF(variableout[8], variableout[9], variableout[10], variableout[11], H_24, H_25, H_26,
                             H_27, d[18])
        H_28 = IVLBCDiff_rk.CreateVariable(self, "H", 28)
        H_29 = IVLBCDiff_rk.CreateVariable(self, "H", 29)
        H_30 = IVLBCDiff_rk.CreateVariable(self, "H", 30)
        H_31 = IVLBCDiff_rk.CreateVariable(self, "H", 31)
        self.ConstraintsByLF(variableout[12], variableout[13], variableout[14], variableout[15], H_28, H_29, H_30,
                             H_31, d[19])

        variableout_rk = self.VariableRotation_bit(variablein_k)

        k_80 = IVLBCDiff_rk.CreateVariable(self, "k", 80)
        k_81 = IVLBCDiff_rk.CreateVariable(self, "k", 81)
        k_82 = IVLBCDiff_rk.CreateVariable(self, "k", 82)
        k_83 = IVLBCDiff_rk.CreateVariable(self, "k", 83)
        self.Constraints_SBOX(variableout_rk[40], variableout_rk[41], variableout_rk[42], variableout_rk[43], k_80,
                              k_81, k_82, k_83, variablein_X[16], d[20])

        self.ConstraintsKeys_in_Differential(variableout_rk[0], variableout_rk[1], variableout_rk[2],
                                             variableout_rk[3], variablein_K[0])
        self.ConstraintsKeys_in_Differential(variableout_rk[4], variableout_rk[5], variableout_rk[6],
                                             variableout_rk[7], variablein_K[1])
        self.ConstraintsKeys_in_Differential(variableout_rk[8], variableout_rk[9], variableout_rk[10],
                                             variableout_rk[11], variablein_K[2])
        self.ConstraintsKeys_in_Differential(variableout_rk[12], variableout_rk[13], variableout_rk[14],
                                             variableout_rk[15], variablein_K[3])
        self.ConstraintsKeys_in_Differential(variableout_rk[16], variableout_rk[17], variableout_rk[18],
                                             variableout_rk[19], variablein_K[4])
        self.ConstraintsKeys_in_Differential(variableout_rk[20], variableout_rk[21], variableout_rk[22],
                                             variableout_rk[23], variablein_K[5])
        self.ConstraintsKeys_in_Differential(variableout_rk[24], variableout_rk[25], variableout_rk[26],
                                             variableout_rk[27], variablein_K[6])
        self.ConstraintsKeys_in_Differential(variableout_rk[28], variableout_rk[29], variableout_rk[30],
                                             variableout_rk[31], variablein_K[7])
        self.ConstraintsKeys_in_Differential(variableout_rk[32], variableout_rk[33], variableout_rk[34],
                                             variableout_rk[35], variablein_K[8])
        self.ConstraintsKeys_in_Differential(variableout_rk[36], variableout_rk[37], variableout_rk[38],
                                             variableout_rk[39], variablein_K[9])
        self.ConstraintsKeys_in_Differential(k_80, k_81, k_82, k_83, variablein_K[10])
        self.ConstraintsKeys_in_Differential(variableout_rk[44], variableout_rk[45], variableout_rk[46],
                                             variableout_rk[47], variablein_K[11])
        self.ConstraintsKeys_in_Differential(variableout_rk[48], variableout_rk[49], variableout_rk[50],
                                             variableout_rk[51], variablein_K[12])
        self.ConstraintsKeys_in_Differential(variableout_rk[52], variableout_rk[53], variableout_rk[54],
                                             variableout_rk[55], variablein_K[13])
        self.ConstraintsKeys_in_Differential(variableout_rk[56], variableout_rk[57], variableout_rk[58],
                                             variableout_rk[59], variablein_K[14])
        self.ConstraintsKeys_in_Differential(variableout_rk[60], variableout_rk[61], variableout_rk[62],
                                             variableout_rk[63], variablein_K[15])

        for i in range(1, self.Round):


            variableout_rk[40]=k_80
            variableout_rk[41]=k_81
            variableout_rk[42]=k_82
            variableout_rk[43]=k_83
            variablein_X = IVLBCDiff_rk.CreateVariables_X(self, i)
            variablein_H = IVLBCDiff_rk.CreateVariables_H(self, i)
            variablein_K = IVLBCDiff_rk.CreateVariables_K(self, i)
            d = IVLBCDiff_rk.CreateVariablesdd(self, i)

            self.ConstraintsKeys_add(variablein_K[0], variablein_H[0], variablein_X[0], d[0])
            self.ConstraintsKeys_add(variablein_K[1], variablein_H[1], variablein_X[1], d[1])
            self.ConstraintsKeys_add(variablein_K[2], variablein_H[2], variablein_X[2], d[2])
            self.ConstraintsKeys_add(variablein_K[3], variablein_H[3], variablein_X[3], d[3])
            self.ConstraintsKeys_add(variablein_K[4], variablein_H[4], variablein_X[4], d[4])
            self.ConstraintsKeys_add(variablein_K[5], variablein_H[5], variablein_X[5], d[5])
            self.ConstraintsKeys_add(variablein_K[6], variablein_H[6], variablein_X[6], d[6])
            self.ConstraintsKeys_add(variablein_K[7], variablein_H[7], variablein_X[7], d[7])
            self.ConstraintsKeys_add(variablein_K[8], variablein_H[8], variablein_X[8], d[8])
            self.ConstraintsKeys_add(variablein_K[9], variablein_H[9], variablein_X[9], d[9])
            self.ConstraintsKeys_add(variablein_K[10], variablein_H[10], variablein_X[10], d[10])
            self.ConstraintsKeys_add(variablein_K[11], variablein_H[11], variablein_X[11], d[11])
            self.ConstraintsKeys_add(variablein_K[12], variablein_H[12], variablein_X[12], d[12])
            self.ConstraintsKeys_add(variablein_K[13], variablein_H[13], variablein_X[13], d[13])
            self.ConstraintsKeys_add(variablein_K[14], variablein_H[14], variablein_X[14], d[14])
            self.ConstraintsKeys_add(variablein_K[15], variablein_H[15], variablein_X[15], d[15])

            variableout = self.VariableRotation(variablein_X)

            H_16 = IVLBCDiff_rk.CreateVariable(self, "H", 16 + (i) * 16)
            H_17 = IVLBCDiff_rk.CreateVariable(self, "H", 17 + (i) * 16)
            H_18 = IVLBCDiff_rk.CreateVariable(self, "H", 18 + (i) * 16)
            H_19 = IVLBCDiff_rk.CreateVariable(self, "H", 19 + (i) * 16)
            self.ConstraintsByLF(variableout[0], variableout[1], variableout[2], variableout[3], H_16, H_17, H_18,
                                 H_19, d[16])
            H_20 = IVLBCDiff_rk.CreateVariable(self, "H", 20 + (i) * 16)
            H_21 = IVLBCDiff_rk.CreateVariable(self, "H", 21 + (i) * 16)
            H_22 = IVLBCDiff_rk.CreateVariable(self, "H", 22 + (i) * 16)
            H_23 = IVLBCDiff_rk.CreateVariable(self, "H", 23 + (i) * 16)
            self.ConstraintsByLF(variableout[4], variableout[5], variableout[6], variableout[7], H_20, H_21, H_22,
                                 H_23, d[17])
            H_24 = IVLBCDiff_rk.CreateVariable(self, "H", 24 + (i) * 16)
            H_25 = IVLBCDiff_rk.CreateVariable(self, "H", 25 + (i) * 16)
            H_26 = IVLBCDiff_rk.CreateVariable(self, "H", 26 + (i) * 16)
            H_27 = IVLBCDiff_rk.CreateVariable(self, "H", 27 + (i) * 16)
            self.ConstraintsByLF(variableout[8], variableout[9], variableout[10], variableout[11], H_24, H_25,H_26,
                                 H_27, d[18])
            H_28 = IVLBCDiff_rk.CreateVariable(self, "H", 28 + (i) * 16)
            H_29 = IVLBCDiff_rk.CreateVariable(self, "H", 29 + (i) * 16)
            H_30 = IVLBCDiff_rk.CreateVariable(self, "H", 30 + (i) * 16)
            H_31 = IVLBCDiff_rk.CreateVariable(self, "H", 31 + (i) * 16)
            self.ConstraintsByLF(variableout[12], variableout[13], variableout[14], variableout[15],H_28, H_29,
                                 H_30, H_31, d[19])

            variableout_rk = self.VariableRotation_bit(variableout_rk)

            k_80 = IVLBCDiff_rk.CreateVariable(self, "k", 80+ (i) * 4)
            k_81 = IVLBCDiff_rk.CreateVariable(self, "k", 81+ (i) * 4)
            k_82 = IVLBCDiff_rk.CreateVariable(self, "k", 82+ (i) * 4)
            k_83 = IVLBCDiff_rk.CreateVariable(self, "k", 83+ (i) * 4)
            self.Constraints_SBOX(variableout_rk[40], variableout_rk[41], variableout_rk[42], variableout_rk[43],
                                  k_80, k_81, k_82, k_83, variablein_X[16], d[20])

            self.ConstraintsKeys_in_Differential(variableout_rk[0], variableout_rk[1], variableout_rk[2],
                                                 variableout_rk[3], variablein_K[0])
            self.ConstraintsKeys_in_Differential(variableout_rk[4], variableout_rk[5], variableout_rk[6],
                                                 variableout_rk[7], variablein_K[1])
            self.ConstraintsKeys_in_Differential(variableout_rk[8], variableout_rk[9], variableout_rk[10],
                                                 variableout_rk[11], variablein_K[2])
            self.ConstraintsKeys_in_Differential(variableout_rk[12], variableout_rk[13], variableout_rk[14],
                                                 variableout_rk[15], variablein_K[3])
            self.ConstraintsKeys_in_Differential(variableout_rk[16], variableout_rk[17], variableout_rk[18],
                                                 variableout_rk[19], variablein_K[4])
            self.ConstraintsKeys_in_Differential(variableout_rk[20], variableout_rk[21], variableout_rk[22],
                                                 variableout_rk[23], variablein_K[5])
            self.ConstraintsKeys_in_Differential(variableout_rk[24], variableout_rk[25], variableout_rk[26],
                                                 variableout_rk[27], variablein_K[6])
            self.ConstraintsKeys_in_Differential(variableout_rk[28], variableout_rk[29], variableout_rk[30],
                                                 variableout_rk[31], variablein_K[7])
            self.ConstraintsKeys_in_Differential(variableout_rk[32], variableout_rk[33], variableout_rk[34],
                                                 variableout_rk[35], variablein_K[8])
            self.ConstraintsKeys_in_Differential(variableout_rk[36], variableout_rk[37], variableout_rk[38],
                                                 variableout_rk[39], variablein_K[9])
            self.ConstraintsKeys_in_Differential(k_80, k_81, k_82, k_83, variablein_K[10])
            self.ConstraintsKeys_in_Differential(variableout_rk[44], variableout_rk[45], variableout_rk[46],
                                                 variableout_rk[47], variablein_K[11])
            self.ConstraintsKeys_in_Differential(variableout_rk[48], variableout_rk[49], variableout_rk[50],
                                                 variableout_rk[51], variablein_K[12])
            self.ConstraintsKeys_in_Differential(variableout_rk[52], variableout_rk[53], variableout_rk[54],
                                                 variableout_rk[55], variablein_K[13])
            self.ConstraintsKeys_in_Differential(variableout_rk[56], variableout_rk[57], variableout_rk[58],
                                                 variableout_rk[59], variablein_K[14])
            self.ConstraintsKeys_in_Differential(variableout_rk[60], variableout_rk[61], variableout_rk[62],
                                                 variableout_rk[63], variablein_K[15])

    def CreateVariables_X(self, n):
        array = []
        for i in range(0, 17):
            array.append(("x" + "_" + str(i+n*17)))
        return array

    def CreateVariables_H(self, n):
        array = []
        for i in range(0, 16):
            array.append(("H" + "_" + str(i+n*16)))
        return array

    def CreateVariables_k(self, n):
        array = []
        for i in range(0, 80):
            array.append(("k" + "_" + str(i)))
        return array

    def CreateVariables_K(self, n):
        array = []
        for i in range(0, 16):
            array.append(("K1" + "_" + str(i+n*16)))
        return array

    def CreateVariablesdd(self, n):
        array = []
        for i in range(0, 21):
            array.append(("d" + "_" + str(i + n * 21)))
        return array

    def Constraints(self, variablex):
        fileobj = open(self.filename_model, "a")
        temp = []
        for i in range(0, 80):
            temp.append(variablex[i])
        s = " + ".join(temp)
        s += " >= 1"
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.close()

    def VariableRotation(self, x):
        eqn = []
        for i in range(0, 16):
            j = FP16[i]
            eqn.append(x[j])
        return eqn

    def VariableRotation_bit(self, x):
        eqn = []
        for i in range(0, 80):
            j = key_p80[i]
            eqn.append(x[j])
        return eqn

    def CreateVariable(self, s, n):
        array = (s + "_" + str(n))
        return array

    def ConstraintsKeys_add(self, variabley, variablev, variablex,d):
        fileobj = open(self.filename_model, "a")
        temp = []
        temp.append(variabley)
        temp.append(variablev)
        temp.append(variablex)
        s = " + ".join(temp)
        s += (" - " + d + " - " + d + " >= 0")
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.write(variabley + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablev + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablex + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.close()

    def ConstraintsKeys_in_Differential(self, variablei1, variablei2, variablei3, variablei4,variableo):
        fileobj = open(self.filename_model, "a")
        temp = []
        temp.append(variablei1)
        temp.append(variablei2)
        temp.append(variablei3)
        temp.append(variablei4)
        s = " + ".join(temp)
        s += (" - " + variableo + " >= 0")
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.write(variablei1 + " - " + variableo + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei2 + " - " + variableo + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei3 + " - " + variableo + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei4 + " - " + variableo  + " <= 0")
        fileobj.write("\n")
        fileobj.close()

    def ConstraintsByLF(self, variabley, variablev, variablex, variableu, variabley1, variablev1, variablex1,
                        variableu1, d):
        fileobj = open(self.filename_model, "a")
        temp = []
        temp.append(variabley)
        temp.append(variablev)
        temp.append(variablex)
        temp.append(variableu)
        temp.append(variabley1)
        temp.append(variablev1)
        temp.append(variablex1)
        temp.append(variableu1)
        s = " + ".join(temp)
        s += (" - " + d + " - " + d + " - " + d + " - " + d + " - " + d + " >= 0")
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.write(variabley + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablev + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablex + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variableu + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variabley1 + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablev1 + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablex1 + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variableu1 + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.close()

    def Constraints_SBOX(self, variablei1, variablei2, variablei3, variablei4, variableo1, variableo2, variableo3,
                        variableo4,X,d):
        fileobj = open(self.filename_model, "a")
        temp = []
        temp.append(variablei1)
        temp.append(variablei2)
        temp.append(variablei3)
        temp.append(variablei4)
        s = " + ".join(temp)
        s += (" - " + X+ " >= 0")
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.write(variablei1 + " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei2+ " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei3+ " - " + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablei4 + " - " + d + " <= 0")
        fileobj.write("\n")

        y= " + ".join(temp)
        y += (" - " +variableo1+ " - " +variableo2 +" - " +variableo3 +" - " +variableo4 + " >= 0")
        fileobj.write(y)
        fileobj.write("\n")

        temp1 = []
        temp1.append(variableo1)
        temp1.append(variableo2)
        temp1.append(variableo3)
        temp1.append(variableo4)
        y1 = " + ".join(temp1)
        y1 += (" - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " - " + variablei4+ " >= 0")
        fileobj.write(y1)
        fileobj.write("\n")

        fileobj.write(variablei1 + " + " +variablei3 + " + " +variablei4 + " - " +variableo3 + " > "+  "-1")#0*00**1*
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei3 + " - " + variablei4 + " + " + variableo3 + " > "+  "-1")  # 0*01**0*
        fileobj.write("\n")
        fileobj.write(" - " +variablei1 + " + " + variablei3 + " + " + variableo1 + " + " + variableo2+ " > "+  "-1")  # 1*0*00**
        fileobj.write("\n")
        fileobj.write(" - " + variablei3 + " + " + variableo1 + " + " + variableo3 + " + " + variableo4 + " > "+  "-1")  # **1*0*00
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " - " + variablei3+ " - " + variablei4 + " - " + variableo1+ " > "+  "-3")  # 00111***
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " + " + variablei4 + " - " + variablei1 + " + " + variableo3+ " > "+  "-1")  # 00*01*0*
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " - " + variablei3 + " + " + variablei4 + " + " + variableo1 + " - " + variableo3+ " > "+  "-2")  # 00100*1*
        fileobj.write("\n")
        fileobj.write( variablei1 + " - " + variablei2 + " + " + variablei3 + " + " + variablei4 + " + " + variableo1 + " + " + variableo3 + " > "+  "-1")  # 01000*0*
        fileobj.write("\n")
        fileobj.write(variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variablei4 + " - " + variableo1 + " - " + variableo3 + " > "+  "-4")  #01101*1*
        fileobj.write("\n")
        fileobj.write( variablei1 + " - " + variablei2 + " - " + variablei3 + " - " + variablei4 + " + " + variableo1 + " - " + variableo3 + " > "+  "-4")  # 01110*1*
        fileobj.write("\n")
        fileobj.write( variablei1 + " + " + variablei3 + " - " + variablei4 + " + " + variableo1 + " - " + variableo2 + " - " + variableo3+ " > "+  "-3")  # 0*01011*
        fileobj.write("\n")
        fileobj.write(" - " +variablei1 + " + " + variablei3 + " + " + variablei4 + " - " + variableo1 + " + " + variableo2 + " + " + variableo3 + " > "+  "-2")  #1*00100*
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei3 + " + " + variablei4 + " - " + variableo1 + " - " + variableo2 + " - " + variableo3 + " > "+  "-4")  # 1*00111*
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei3 + " - " + variablei4 + " - " + variableo1 + " + " + variableo2 + " - " + variableo3 + " > "+  "-4")  # 1*01101*
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei3 + " - " + variablei4 + " - " + variableo1 +  " - " + variableo2 + " + " + variableo3+ " > "+  "-4")  # 1*01110*
        fileobj.write("\n")
        fileobj.write(  variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variableo1 + " + " + variableo3 + " - " + variableo4+ " > "+  "-3")  # 011*0*01
        fileobj.write("\n")
        fileobj.write(" - " +variablei1 + " + " + variablei2 + " - " + variablei3 + " - " + variableo1 + " + " + variableo3 + " - " + variableo4 + " > "+  "-4")  #101*1*01
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " - " + variableo1 + " + " + variableo3 + " + " + variableo4 + " > "+  "-4")  # 111*1*00
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei3  + " + " + variableo1 + " - " + variableo2+ " + " + variableo3 + " - " + variableo4+ " > "+  "-3")  # 1*0*0101
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei3 + " + " + variableo1 + " + " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-4")  # 1*1*0011
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei3 + " + " + variableo1 + " - " + variableo2 + " - " + variableo3 + " + " + variableo4+ " > "+  "-4")  # 1*1*0110
        fileobj.write("\n")
        fileobj.write( variablei1 + " + " + variablei2+ " + " + variablei3 + " + " + variablei4 + " + " + variableo1 + " - " + variableo2 + " + " + variableo3 + " > "+  "-1")  # 0000010*
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " + " + variablei3 + " + " + variablei4 + " + " + variableo1 + " + " + variableo2 + " + " + variableo3+ " - " + variableo4 + " > "+  "-1")  # 00000001
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " - " + variablei3 + " - " + variablei4 + " + " + variableo1 + " + " + variableo2 + " - " + variableo3 + " + " + variableo4 + " > "+  "-3")  #00110010
        fileobj.write("\n")
        fileobj.write(variablei1 + " + " + variablei2 + " - " + variablei3 + " - " + variablei4 + " + " + variableo1 + " - " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-5")  #00110111
        fileobj.write("\n")
        fileobj.write(variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variablei4 + " + " + variableo1 + " + " + variableo2 + " - " + variableo3 + " + " + variableo4 + " > "+  "-3")  # 01100010
        fileobj.write("\n")
        fileobj.write(variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variablei4 + " + " + variableo1 + " - " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-5")  #01100111
        fileobj.write("\n")
        fileobj.write(" - " +variablei1 + " + " + variablei2 + " + " + variablei3 + " + " + variablei4 + " - " + variableo1 + " - " + variableo2 + " + " + variableo3 + " + " + variableo4 + " > "+  "-3")  # 10001100
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei2 + " + " + variablei3 + " - " + variablei4 + " - " + variableo1 + " + " + variableo2 + " + " + variableo3 + " + " + variableo4 + " > "+  "-3")  # 10011000
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei2 + " - " + variablei3 + " + " + variablei4 + " - " + variableo1 + " + " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-5")  # 10101011
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei2 + " - " + variablei3 + " + " + variablei4 + " - " + variableo1 + " - " + variableo2 + " - " + variableo3 + " + " + variableo4+ " > "+  "-5")  #10101110
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei2 + " - " + variablei3 + " - " + variablei4 + " - " + variableo1 + " + " + variableo2 + " - " + variableo3 + " + " + variableo4 + " > "+  "-5")  # 10111010
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " + " + variablei2 + " - " + variablei3 + " - " + variablei4 + " - " + variableo1 + " - " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-7")  # 10111111
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei2 + " + " + variablei3 + " + " + variablei4 +  " - " + variableo1 + " - " + variableo2 + " + " + variableo3 + " - " + variableo4+ " > "+  "-5")  # 11001101
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " - " + variablei2 + " + " + variablei3 + " - " + variablei4 + " - " + variableo1 + " + " + variableo2 + " + " + variableo3 + " - " + variableo4 + " > "+  "-5")  #11011001
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variablei4 + " - " + variableo1 + " + " + variableo2 + " - " + variableo3 + " + " + variableo4 + " > "+  "-5")  # 11101010
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " + " + variablei4 + " - " + variableo1 + " - " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-7")  #11101111
        fileobj.write("\n")
        fileobj.write(" - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " - " + variablei4 + " - " + variableo1 + " + " + variableo2 + " - " + variableo3 + " - " + variableo4 + " > "+  "-7")  #11111011
        fileobj.write("\n")
        fileobj.write( " - " + variablei1 + " - " + variablei2 + " - " + variablei3 + " - " + variablei4 + " - " + variableo1 + " - " + variableo2 + " - " + variableo3 + " + " + variableo4 + " > "+  "-7")  # 11111110
        fileobj.write("\n")
        fileobj.close()

    def VariableBinary(self):
        fileobj = open(self.filename_model, "a")
        fileobj.write("Binary\n")
        for j in range(0, 16):
            fileobj.write("H_" + str(j))
            fileobj.write("\n")
        for j in range(0, 80):
            fileobj.write("k_" + str(j))
            fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 21):
                fileobj.write("d_" + str(j + i * 21))
                fileobj.write("\n")
            for j in range(0, 17):
                fileobj.write("x_" + str(j+ i * 17))
                fileobj.write("\n")
            for j in range(0, 16):
                fileobj.write("H_" + str(16 + i * 16 + j))
                fileobj.write("\n")
            for j in range(0, 16):
                fileobj.write("K1_" + str( i * 16 + j))
                fileobj.write("\n")
            for j in range(0, 4):
                fileobj.write("k_" + str(80 + i * 4 + j))
                fileobj.write("\n")
        fileobj.write("END")
        fileobj.close()

    def SolveModel(self):
        time_start = time.time()
        m = read(self.filename_model)
        m.optimize()

        s = 0
        for v in m.getVars():
            s = s + 1
            print('%s %g' % (v.varName, v.x))
        print("s=%d" % (s))
        counter = 0
        set_zero = []
        global_flag = False
        while counter < 17 * self.Round + 1:
            m.optimize()
            # Gurobi syntax: m.Status == 2 represents the model is feasible.
            if m.Status == 2:
                print("m.Status == 2")
                obj = m.getObjective()

                if obj.getValue() > 1:
                    global_flag = True
                    print("MIN SBOX：%d" % (self.Round,obj.getValue()))
                    break
                else:
                    fileobj = open(self.filename_result, "a")
                    fileobj.write("************************************COUNTER = %d\n" % counter)
                    fileobj.close()
                    self.WriteObjective(obj)
                    print("---------------------------------")
                    print(obj)
                    print("---------------------------------")

                    for i in range(0, 17 * self.Round):
                        u = obj.getVar(i)
                        temp = u.getAttr('x')
                        if temp == 1:
                            set_zero.append(u.getAttr('VarName'))
                            u.ub = 0
                            m.update()
                            counter += 1
                            break
                        else:
                            counter += 1
            # Gurobi syntax: m.Status == 3 represents the model is infeasible.
            elif m.Status == 3:
                print("m.Status == 3")
                global_flag = True
                break
            else:
                print("Unknown error!")

        fileobj = open(self.filename_result, "a")
        if global_flag:
            fileobj.write("\nIntegral Distinguisher Found!\n\n")
            fileobj.write(("minimum active Sbox:" + str(obj.getValue())+"\n"))
            print("Integral Distinguisher Found!\n")
        else:
            fileobj.write("\nIntegral Distinguisher do NOT exist\n\n")
            print("Integral Distinguisher do NOT exist\n")

        fileobj.write("Those are the coordinates set to zero: \n")
        for u in set_zero:
            fileobj.write(u)
            fileobj.write("\n")
        fileobj.write("\n")
        time_end = time.time()
        fileobj.write(("Time used = " + str(time_end - time_start)))
        fileobj.close()
