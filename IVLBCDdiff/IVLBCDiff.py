from gurobipy import *
import time

PN = (
    0, 1, 2, 3,28,29,30,31,40,41,42,43,52,53,54,55,
    16, 17, 18, 19,44,45,46,47,56,57,58,59,4,5,6,7,
    32, 33, 34, 35,60,61,62,63,8,9,10,11,20,21,22,23,
    48, 49, 50, 51, 12,13,14,15,24,25,26,27,36,37,38,39
)
conv = (
0, 1, -1, 0, -1, 0, 1, -1, 2,
-2, -2, -1, -1, -1, -1, 1, 2, 6,
3, -3, 1, -1, 3, -3, 1, -1, 4,
1, -1, 0, 1, -1, 0, -1, 0, 2,
-2, 1, 1, 0, 1, 2, 1, 1, 0,
3, 3, 2, -2, -2, -1, 5, 1, 0,
-1, 1, 1, 2, -2, -2, -1, 1, 4,
1, 2, 1, 1, -2, 1, 1, 0, 0,
1, 2, -2, -2, -1, -1, -1, -1, 6,
1, 2, -2, -2, -1, 1, -1, 1, 4,
-1, 0, -1, 0, 1, -1, 0, 1, 2,
1, 1, -2, 1, 1, 0, 1, 2, 0,
1, 0, 3, -2, 1, -1, 2, -2, 2,
-2, -1, 5, 1, 3, 3, 2, -2, 0,
-1, 0, 1, -1, 0, 1, -1, 0, 2,
-1, -1, 1, 2, -2, -2, -1, -1, 6,
5, 1, 3, 3, 2, -2, -2, -1, 0,
2, -2, -2, -1, 5, 1, 3, 3, 0,
-2, -2, -1, 1, -1, 1, 1, 2, 4,
-1, 1, -1, 1, 1, 2, -2, -2, 4,
-1, -1, -1, -1, 1, 2, -2, -2, 6,
)


class IVLBCDiff:
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
        Generate the MILP model of IVLBC given the round number.
        """
        self.CreateObjectiveFunction()  # Create the objective function of MILP model.
        self.Constraint()  # Generate the constraints used in the MILP model.
        self.VariableBinary()  #Specify the variable type.

    def CreateObjectiveFunction(self):
        """
        Create the objective function of the MILP model.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Minimize\n")
        eqn = []
        for i in range(0, self.Round):
            for j in range(0,16):
                eqn.append("A" + "_" + str(j+ i * 16))

        temp = " + ".join(eqn)
        fileobj.write(temp)
        fileobj.write("\n")
        fileobj.close()

    def Constraint(self):
        """
        Generate the constraints used in the MILP model.
        """
        assert (self.Round >= 1)
        fileobj = open(self.filename_model, "a")
        fileobj.write("Subject To\n")
        fileobj.close()
        variablein = IVLBCDiff.CreateVariables(self, 0)
        self.Constraints(variablein) #Generate the constraint that there must be 1 active S-box.
        fileobj = open(self.filename_model, "a")
        eqn = []
        for i in range(0, self.Round):
            for j in range(0, 16):
                eqn.append("A" + "_" + str(j + i * 16))
        temp = " + ".join(eqn)
        temp += " >= 1"
        fileobj.write(temp)
        fileobj.write("\n")
        fileobj.close()
        for i in range(0, self.Round):
            variablein = IVLBCDiff.CreateVariables(self, i)
            # The constraints of Sub_Cells.
            variablein_y = IVLBCDiff.CreateVariablesY(self, i)
            variablein_A = IVLBCDiff.CreateVariablesA(self, i)
            self.Constraintssss(variablein_A, variablein)
            self.Constraints_Sbox(variablein, variablein_y)

            # The constraints of Permute_Nibbles.
            variablein_z = IVLBCDiff.CreateVariablesZ(self, i)
            self.VariableRotation(variablein_z, variablein_y)
            # The constraints of Mix_Columns.
            variableout_x = IVLBCDiff.CreateVariables(self, i + 1)
            d = IVLBCDiff.CreateVariablesdd(self, i)
            self.Constraint_mc(variableout_x, variablein_z, d)

    def CreateVariables(self, round):
        """
        Generate the variables used in the model.
        """
        array = []
        for i in range(0, 64):
            array.append(("x" + "_" + str(round * 64 + i)))
        return array

    def CreateVariablesY(self, round):
        """
        Generate the variables used in the model.
        """
        array = []
        for i in range(0, 64):
            array.append(("y" + "_" + str(round * 64 + i)))
        return array

    def CreateVariablesA(self, round):
        """
        Generate the variables used in the model.
        """
        array = []
        for i in range(0, 16):
            array.append(("A" + "_" + str(round * 16 + i)))
        return array

    def CreateVariablesZ(self, n):
        """
        Generate the variables used in the model.
        """
        array = []
        for i in range(0, 64):
            array.append(("z" + "_" + str(i + n * 64)))
        return array

    def CreateVariablesdd(self, n):
        """
        Generate the variables used in the model.
        """
        array = []
        for i in range(0, 32):
            array.append(("d" + "_" + str(i + n * 32)))
        return array

    def Constraints(self, variablex):
        """
        Generate the constraint that there must be 1 active S-box.
        """
        fileobj = open(self.filename_model, "a")
        temp = []
        for i in range(0, 64):
            temp.append(variablex[i])
        s = " + ".join(temp)
        s += " >= 1"
        fileobj.write(s)
        fileobj.write("\n")
        fileobj.close()


    def VariableRotation(self, variablein_z, variablein_y):
        """
        Bit Rotation.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 64):
            j = PN[i]
            fileobj.write(variablein_y[j] + " - " + variablein_z[i] + " = 0")
            fileobj.write("\n")
        fileobj.close()

    def Constraint_mc(self, variableout_x, variablein_z, d):
        """
        Generate the constraints of Mix_Columns.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 4):
            self.Constraints_XOR(d[i * 8], variablein_z[i * 16 + 4], variablein_z[i * 16 + 8])
            self.Constraints_XOR(d[i * 8 + 1], variablein_z[i * 16 + 5], variablein_z[i * 16 + 9])
            self.Constraints_XOR(d[i * 8 + 2], variablein_z[i * 16 + 6], variablein_z[i * 16 + 10])
            self.Constraints_XOR(d[i * 8 + 3], variablein_z[i * 16 + 7], variablein_z[i * 16 + 11])
            self.Constraints_XOR(d[i * 8 + 4], variablein_z[i * 16], variablein_z[i * 16 + 12])
            self.Constraints_XOR(d[i * 8 + 5], variablein_z[i * 16 + 1], variablein_z[i * 16 + 13])
            self.Constraints_XOR(d[i * 8 + 6], variablein_z[i * 16 + 2], variablein_z[i * 16 + 14])
            self.Constraints_XOR(d[i * 8 + 7], variablein_z[i * 16 + 3], variablein_z[i * 16 + 15])
            self.Constraints_XOR(variableout_x[i * 16], d[i * 8], variablein_z[i * 16 + 12])
            self.Constraints_XOR(variableout_x[i * 16 + 1], d[i * 8 + 1], variablein_z[i * 16 + 13])
            self.Constraints_XOR(variableout_x[i * 16 + 2], d[i * 8 + 2], variablein_z[i * 16 + 14])
            self.Constraints_XOR(variableout_x[i * 16 + 3], d[i * 8 + 3], variablein_z[i * 16 + 15])
            self.Constraints_XOR(variableout_x[i * 16 + 4], d[i * 8 + 4], variablein_z[i * 16 + 8])
            self.Constraints_XOR(variableout_x[i * 16 + 5], d[i * 8 + 5], variablein_z[i * 16 + 9])
            self.Constraints_XOR(variableout_x[i * 16 + 6], d[i * 8 + 6], variablein_z[i * 16 + 10])
            self.Constraints_XOR(variableout_x[i * 16 + 7], d[i * 8 + 7], variablein_z[i * 16 + 11])
            self.Constraints_XOR(variableout_x[i * 16 + 8], d[i * 8 + 4], variablein_z[i * 16 + 4])
            self.Constraints_XOR(variableout_x[i * 16 + 9], d[i * 8 + 5], variablein_z[i * 16 + 5])
            self.Constraints_XOR(variableout_x[i * 16 + 10], d[i * 8 + 6], variablein_z[i * 16 + 6])
            self.Constraints_XOR(variableout_x[i * 16 + 11], d[i * 8 + 7], variablein_z[i * 16 + 7])
            self.Constraints_XOR(variableout_x[i * 16 + 12], d[i * 8], variablein_z[i * 16])
            self.Constraints_XOR(variableout_x[i * 16 + 13], d[i * 8 + 1], variablein_z[i * 16 + 1])
            self.Constraints_XOR(variableout_x[i * 16 + 14], d[i * 8 + 2], variablein_z[i * 16 + 2])
            self.Constraints_XOR(variableout_x[i * 16 + 15], d[i * 8 + 3], variablein_z[i * 16 + 3])

        fileobj.close()

    def Constraintssss(self, variablein_A, variablein):
        """
        Generate the constraints by Sub_Cells.
        """
        fileobj = open(self.filename_model, "a")
        for i in range(0, 16):
            fileobj.write(variablein_A[i] + " - " + variablein[i*4] + " >= 0")
            fileobj.write("\n")
            fileobj.write(variablein_A[i] + " - " + variablein[i*4+ 1] + " >= 0")
            fileobj.write("\n")
            fileobj.write(variablein_A[i] + " - " + variablein[i*4+ 2] + " >= 0")
            fileobj.write("\n")
            fileobj.write(variablein_A[i] + " - " + variablein[i*4+ 3] + " >= 0")
            fileobj.write("\n")
            fileobj.write(variablein[i*4] + " + " + variablein[i*4+ 1] + " + " + variablein[
                i * 4 + 2] + " + " + variablein[i*4+ 3] + " - " + variablein_A[i] + " >= 0")
            fileobj.write("\n")
        fileobj.close()

    def Constraints_Sbox(self,variablein, variablein_y):
        """
        Generate the constraints by Sub_Cells.
        """
        fileobj = open(self.filename_model, "a")
        buf = ''
        for i in range(0, 16):
            fileobj.write(" 4 " + variablein[i * 4] + " + 4 " + variablein[i * 4 + 1] + " + 4 " + variablein[
                i * 4 + 2] + " + 4 " + variablein[i * 4 + 3] + " - " + variablein_y[i * 4] + " - " + variablein_y[
                              i * 4 + 1] + " - " + variablein_y[i * 4 + 2] + " - " + variablein_y[i * 4 + 3] + " >= 0")
            fileobj.write("\n")
            fileobj.write(" 4 " + variablein_y[i * 4] + " + 4 " + variablein_y[i * 4 + 1] + " + 4 " + variablein_y[
                i * 4 + 2] + " + 4 " + variablein_y[i * 4 + 3] + " - " + variablein[i * 4] + " - " + variablein[
                              i * 4 + 1] + " - " + variablein[i * 4 + 2] + " - " + variablein[i * 4 + 3] + " >= 0")
            fileobj.write("\n")
            for k in range(0, 21):
                for l in range(0, 9):
                    if conv[9 * k + l] > 0:
                        if l <= 3:
                            buf = buf + " + " + str(conv[9 * k + l]) + " " + variablein[i * 4+l]
                        if 4 <= l and l <= 7:
                            buf = buf + " + " + str(conv[9 * k + l]) + " " + variablein_y[i * 4 + l-4]
                        if l == 8:
                            buf = buf + " >= -" + str(conv[9 * k + l]) + "\n"
                    if conv[9 * k + l] < 0:
                        if l <= 3:
                            buf = buf + " - " + str(-conv[9 * k + l])  + " " + variablein[i * 4+l]
                        if 4 <= l and l <= 7:
                            buf = buf + " - " + str(-conv[9 * k + l]) + " " +  variablein_y[i * 4 + l-4]
                        if l == 8:
                            buf = buf + " >= " + str(-conv[9 * k + l]) + "\n"
                    if conv[9 * k + l] == 0:
                        if l == 8:
                            buf = buf + " >= " + str(conv[9 * k + l]) + "\n"
        fileobj.write(buf)
        fileobj.close()


    def Constraints_XOR(self, variabley, variablev, variablex):
        """
        Generate the constraints by XOR operation.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write(variabley + " + " + variablev + " - " + variablex + " >= 0")
        fileobj.write("\n")
        fileobj.write(variabley + " - " + variablev + " + " + variablex + " >= 0")
        fileobj.write("\n")
        fileobj.write(" - " + variabley + " + " + variablev + " + " + variablex + " >= 0")
        fileobj.write("\n")
        fileobj.write(variabley + " + " + variablev + " + " + variablex + " <= 2")
        fileobj.write("\n")
        fileobj.close()

    def VariableBinary(self):
        """
        Specify the variable type.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Binary\n")
        for j in range(0, 64):
            fileobj.write("x_" + str(j))
            fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 64):
                fileobj.write("x_" + str(64 + i * 64 + j))
                fileobj.write("\n")
            for j in range(0, 16):
                fileobj.write("A_" + str(i * 16 + j))
                fileobj.write("\n")
            for j in range(0, 64):
                fileobj.write("y_" + str(i * 64 + j))
                fileobj.write("\n")
            for j in range(0, 64):
                fileobj.write("z_" + str(i * 64 + j))
                fileobj.write("\n")
            for j in range(0, 32):
                fileobj.write("d_" + str(i * 32 + j))
                fileobj.write("\n")
        fileobj.write("END")
        fileobj.close()

    def SolveModel(self):
        """
        Solve the MILP model to search the differential path of IVLBC.
        """
        time_start = time.time()
        m = read(self.filename_model)
        m.optimize()
        s = 0
        for v in m.getVars():
            s = s + 1
            fileobj = open(self.filename_result, "a")
            fileobj.write('%s %g' % (v.varName, v.x))
            fileobj.write("\n")
        counter = 0
        set_zero = []
        global_flag = False
        while counter < 16 * self.Round:
            m.optimize()
            if m.Status == 2:
                print("m.Status == 2")
                obj = m.getObjective()
                if obj.getValue() >=1:
                    global_flag = True
                    fileobj = open(self.filename_result, "a")
                    fileobj.write("%d-th round minimum active Sbox:%d\n" % (self.Round,obj.getValue()))
                    fileobj.close()
                    print("obj.getValue()=%d" % (obj.getValue()))
                    break
                else:
                    fileobj = open(self.filename_result, "a")
                    fileobj.write("************************************COUNTER = %d\n" % counter)
                    fileobj.close()
                    for i in range(0, 16 * self.Round):
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
            elif m.Status == 3:
                print("m.Status == 3")
                global_flag = True
                break
            else:
                print("Unknown error!")

        fileobj = open(self.filename_result, "a")
        if obj.getValue() >=1:
            fileobj.write("\nMinimum Active SBox Found!\n")
            print("Minimum Active SBox Found!\n")
        else:
            fileobj.write("\nMinimum Active SBox do NOT exist\nn")
            print("Minimum Active SBox do NOT exist\n")
        time_end = time.time()
        fileobj.write(("Time used = " + str(time_end - time_start)))
        fileobj.close()


