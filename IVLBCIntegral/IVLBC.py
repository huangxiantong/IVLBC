
from gurobipy import *

import time


class IVLBC:
    def __init__(self, Round, activebits):
        self.Round = Round
        self.activebits = activebits
        self.blocksize = 64
        self.filename_model = "IVLBC_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
        self.filename_result = "result_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
        fileobj = open(self.filename_model, "w")
        fileobj.close()
        fileboj = open(self.filename_result, "w")
        fileobj.close()

    # Linear inequalities for the Sbox of IVLBC
    S_T = [[1, 1, 1, 1, -1, -1, -1, -1, 0],\
    [-2, -4, -2, -3, -1, 1, 3, 2, 6],\
    [-2, -1, -1, -3, 1, 2, -1, 1, 4],\
    [0, 0, 0, 3, -1, -1, -1, -2, 2],\
    [-1, -2, 0, -1, 2, 2, 1, 3, 0],\
    [0, 2, 0, 0, -1, -1, -1, 0, 1],\
    [-1, 1, -1, 0, 2, -2, -1, -2, 4],\
    [0, -1, -1, -1, -1, 0, 1, 1, 2],\
    [0, 0, 1, 0, -1, 0, 0, -1, 1],\
    [1, 0, 1, 0, 0, -1, -1, -2, 2],\
    [0, 0, -1, -1, 1, 2, 1, 1, 0],\
    [1, 0, 0, 1, 0, -1, -1, -1, 1]]

    NUMBER = 9
    # Permute_Nibbles
    PN = [0,7,10,13,4,11,14,1,8,15,2,5,12,3,6,9]

    def MakeModel(self):
        """
        Generate the MILP model of IVLBC given the round number and activebits.
        """
        self.CreateObjectiveFunction()
        self.Constrain()
        self.Init()
        self.VariableBinary()

    def CreateObjectiveFunction(self):
        """
        Create objective function of the MILP model.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Minimize\n")
        eqn = []
        for i in range(0, 16):
            for j in range(0, 4):
                eqn.append("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i))
        temp = " + ".join(eqn)
        fileobj.write(temp)
        fileobj.write("\n")
        fileobj.close()

    def Constrain(self):
        """
        Generate the constraints used in the MILP model.
        """
        assert (self.Round >= 1)
        fileobj = open(self.filename_model, "a")
        fileobj.write("Subject To\n")
        fileobj.close()
        variablein = IVLBC.CreateVariables(0, "x")
        variableout = IVLBC.CreateVariables(1, "x")
        t_vars = IVLBC.CreateVariables(0, "t")

        if self.Round == 1:
            self.ConstraintsBySbox(variablein, t_vars)
            t_vars = IVLBC.LinearLaryer(t_vars)
            self.constraints_by_mixing_layer(t_vars, variableout, 0)

        else:
            self.ConstraintsBySbox(variablein, t_vars)
            t_vars = IVLBC.LinearLaryer(t_vars)
            self.constraints_by_mixing_layer(t_vars, variableout, 0)
            for i in range(1, self.Round):
                variablein = variableout
                variableout = IVLBC.CreateVariables(i + 1, "x")
                t_vars = IVLBC.CreateVariables(i, "t")
                self.ConstraintsBySbox(variablein, t_vars)
                t_vars = IVLBC.LinearLaryer(t_vars)
                self.constraints_by_mixing_layer(t_vars, variableout, i)

    def CreateVariables(n, s):
        """
        Generate the variables used in the model.
        """
        array = [["" for i in range(0, 4)] for j in range(0, 16)]
        for i in range(0, 16):
            for j in range(0, 4):
                array[i][j] = s + "_" + str(n) + "_" + str(j) + "_" + str(i)
        return array

    def ConstraintsBySbox(self, variable1, variable2):
        fileobj = open(self.filename_model, "a")
        for k in range(0, 16):
            for coeff in IVLBC.S_T:
                temp = []
                for u in range(0, 4):
                    temp.append(str(coeff[u]) + " " + variable1[k][u])
                for v in range(0, 4):
                    temp.append(str(coeff[v + 4]) + " " + variable2[k][v])
                temp1 = " + ".join(temp)
                temp1 = temp1.replace("+ -", "- ")
                s = str(-coeff[IVLBC.NUMBER - 1])
                s = s.replace("--", "")
                temp1 += " >= " + s
                fileobj.write(temp1)
                fileobj.write("\n")
        fileobj.close()

    def constraints_by_mixing_layer(self, variables_in, variables_out, round_number):
        """
        Mix_Columns of IVLBC
        """
        a_vars = IVLBC.CreateVariables(round_number, "a")
        b_vars = IVLBC.CreateVariables(round_number, "b")
        c_vars = [[0 for i in range(4)] for j in range(24)]
        for i in range(24):
            for j in range(0, 4):
                c_vars[i][j] = "c" + "_" + str(round_number) + "_" + str(j) + "_" + str(i)

        # Constraints by 4-bit copies:
        for i in range(0, 4):
            self.constraints_by_4bit_copy(variables_in[0 + 4 * i], a_vars[0 + 4 * i], b_vars[0 + 4 * i])
            self.constraints_by_4bit_copy(variables_in[1 + 4 * i], a_vars[1 + 4 * i], b_vars[1 + 4 * i])
            self.constraints_by_4bit_copy(variables_in[2 + 4 * i], a_vars[2 + 4 * i], b_vars[2 + 4 * i])
            self.constraints_by_4bit_copy(variables_in[3 + 4 * i], a_vars[3 + 4 * i], b_vars[3 + 4 * i])
            self.constraints_by_4bit_copy(c_vars[0 + 6 * i], c_vars[1 + 6 * i], c_vars[2 + 6 * i])
            self.constraints_by_4bit_copy(c_vars[3 + 6 * i], c_vars[4 + 6 * i], c_vars[5 + 6 * i])

        # Constraints by 4-it xors:
        for i in range(0, 4):
            self.constraints_by_4bit_xor(a_vars[0 + 4 * i], c_vars[4 + 6 * i], variables_out[3 + 4 * i])
            self.constraints_by_4bit_xor(b_vars[0 + 4 * i], b_vars[3 + 4 * i], c_vars[0 + 6 * i])
            self.constraints_by_4bit_xor(c_vars[1 + 6 * i], a_vars[1 + 4 * i], variables_out[2 + 4 * i])
            self.constraints_by_4bit_xor(b_vars[1 + 4 * i], b_vars[2 + 4 * i], c_vars[3 + 6 * i])
            self.constraints_by_4bit_xor(c_vars[2 + 6 * i], a_vars[2 + 4 * i], variables_out[1 + 4 * i])
            self.constraints_by_4bit_xor(c_vars[5 + 6 * i], a_vars[3 + 4 * i], variables_out[0 + 4 * i])

    def constraints_by_4bit_copy(self, variablex, variableu, variabley):
        fileobj = open(self.filename_model, "a")
        for j in range(0, 4):
            temp = []
            temp.append(variablex[j])
            temp.append(variableu[j])
            temp.append(variabley[j])
            s = " - ".join(temp)
            s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()

    def constraints_by_4bit_xor(self, variabley, variablev, variablex):
        fileobj = open(self.filename_model, "a")
        for j in range(0, 4):
            temp = []
            temp.append(variablex[j])
            temp.append(variablev[j])
            temp.append(variabley[j])
            s = " - ".join(temp)
            s += " = 0"
            fileobj.write(s)
            fileobj.write("\n")
        fileobj.close()

    @classmethod
    def LinearLaryer(cls, variable):
        """
        Permute_Nibbles of IVLBC.
        """
        array = [["" for i in range(0, 4)] for j in range(0, 16)]
        for i in range(0, 16):
            array[cls.PN[i]] = variable[i]
        return array

    def Init(self):
        """
        Generate constraints introudced by the initial division property.
        """
        variableout = IVLBC.CreateVariables(0, "x")
        fileobj = open(self.filename_model, "a")
        eqn = []
        for i in range(0, self.activebits):
            temp = variableout[15 - (i // 4)][i % 4] + " = 1"
            fileobj.write(temp)
            fileobj.write("\n")
        for i in range(self.activebits, 64):
            temp = variableout[15 - (i // 4)][i % 4] + " = 0"
            fileobj.write(temp)
            fileobj.write("\n")
        fileobj.close()

    def VariableBinary(self):
        """
        Specify the variable type.
        """
        fileobj = open(self.filename_model, "a")
        fileobj.write("Binary\n")
        for i in range(0, (self.Round + 1)):
            for j in range(0, 16):
                for k in range(0, 4):
                    fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
                    fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 16):
                for k in range(0, 4):
                    fileobj.write("t_" + str(i) + "_" + str(k) + "_" + str(j))
                    fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 16):
                for k in range(0, 4):
                    fileobj.write("a_" + str(i) + "_" + str(k) + "_" + str(j))
                    fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 16):
                for k in range(0, 4):
                    fileobj.write("b_" + str(i) + "_" + str(k) + "_" + str(j))
                    fileobj.write("\n")
        for i in range(0, self.Round):
            for j in range(0, 24):
                for k in range(0, 4):
                    fileobj.write("c_" + str(i) + "_" + str(k) + "_" + str(j))
                    fileobj.write("\n")
        fileobj.write("END")
        fileobj.close()


    def set_constant_bits(self, constant_bits):
        self.constant_bits = constant_bits

    def solve_model(self):
        """
        Solve the MILP model to search the integral distinguisher of IVLBC.
        """
        time_start = time.time()
        balanced_bits = ["?" for i in range(64)]
        balanced_flag = False
        m = read(self.filename_model)

        m.setParam("OutputFlag", 0)
        obj = m.getObjective()
        for i in range(0, self.blocksize):
            mask = [0 for j in range(64)]
            mask[i] = 1
            temporary_constraints = m.addConstrs(
                (obj.getVar(j) == mask[j] for j in range(64)), name='temp_constraints')
            m.optimize()
            if m.Status == 3:
                balanced_flag = True
                balanced_bits[i] = "b"
            m.remove(temporary_constraints)
            m.update()
        fileobj = open(self.filename_result, "a")
        bb = 0
        if balanced_flag:
            bb = 1
            fileobj.write("Indices of constant bits : %s\n" %
                          ",".join(map(str, self.constant_bits)))
            fileobj.write("Integral distinguisher found :)\n")
            print("\nIndices of constant bits : %s" %
                  ",".join(map(str, self.constant_bits)))
            print("Integral distinguisher found :)")
        else:
            fileobj.write("Indices of constant bits : %s\n" %
                          ",".join(map(str, self.constant_bits)))
            fileobj.write("Integral distinguisher doesn't exist :(\n")
            bb = 0
            print("\nIndices of constant bits : %s" %
                  ",".join(map(str, self.constant_bits)))
            print("Integral distinguisher doesn't exist :(")
        output_state = ["".join(balanced_bits[4 * i: 4 * i + 4])
                        for i in range(16)]
        fileobj.write("output state : %s" % " ".join(output_state))
        print(" ".join(output_state))
        time_end = time.time()
        elapsed_time = time_end - time_start
        fileobj.write("\nTime used = %.2f\n\n" % elapsed_time)
        print("Time used = %.2f\n" % elapsed_time)
        fileobj.close()
        return bb

    def WriteObjective(self, obj):
            """
     Write the objective value into filename_result.
    """
            fileobj = open(self.filename_result, "a")
            fileobj.write("The objective value = %d\n" %obj.getValue())
            eqn1 = []
            eqn2 = []
            for i in range(0, self.blocksize):
                    u = obj.getVar(i)
                    if u.getAttr("x") != 0:
                            eqn1.append(u.getAttr('VarName'))
                            eqn2.append(u.getAttr('x'))
            length = len(eqn1)
            for i in range(0,length):
                    s = eqn1[i] + "=" + str(eqn2[i])
                    fileobj.write(s)
                    fileobj.write("\n")
            fileobj.close()




