from gurobipy import *
import time

FP16 = (5,10,14,7,13,0,8,3,6,15,1,12,11,4,2,9)

class IVLBCLin:
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
        self.VariableBinary()

    def CreateObjectiveFunction(self):
        """
        Create objective function of the MILP model
        """

        fileobj = open(self.filename_model, "a")
        fileobj.write("Minimize\n")
        eqn = []
        for i in range(0, self.Round):
            eqn.append("x" + "_" + str(0 + i * 16))
            eqn.append("x" + "_" + str(1 + i * 16))
            eqn.append("x" + "_" + str(2 + i * 16))
            eqn.append("x" + "_" + str(3 + i * 16))
            eqn.append("x" + "_" + str(4 + +i * 16))
            eqn.append("x" + "_" + str(5 + i * 16))
            eqn.append("x" + "_" + str(6 + i * 16))
            eqn.append("x" + "_" + str(7 + i * 16))
            eqn.append("x" + "_" + str(8 + i * 16))
            eqn.append("x" + "_" + str(9 + +i * 16))
            eqn.append("x" + "_" + str(10 + i * 16))
            eqn.append("x" + "_" + str(11 + i * 16))
            eqn.append("x" + "_" + str(12 + i * 16))
            eqn.append("x" + "_" + str(13 + i * 16))
            eqn.append("x" + "_" + str(14 + +i * 16))
            eqn.append("x" + "_" + str(15 + i * 16))

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
        variablein = IVLBCLin.CreateVariables(self, 0)
        variableout = []
        d = IVLBCLin.CreateVariablesdd(self, 0)
        if self.Round == 2:

            self.Constraints(variablein)
            variableout = self.VariableRotation(variablein)
            x_16 = IVLBCLin.CreateVariable(self, "x", 16)
            x_17 = IVLBCLin.CreateVariable(self, "x", 17)
            x_18 = IVLBCLin.CreateVariable(self, "x", 18)
            x_19 = IVLBCLin.CreateVariable(self, "x", 19)
            self.ConstraintsByLF(variableout[0], variableout[1], variableout[2], variableout[3], x_16, x_17, x_18, x_19,
                                 d[0])
            x_20 = IVLBCLin.CreateVariable(self, "x", 20)
            x_21 = IVLBCLin.CreateVariable(self, "x", 21)
            x_22 = IVLBCLin.CreateVariable(self, "x", 22)
            x_23 = IVLBCLin.CreateVariable(self, "x", 23)
            self.ConstraintsByLF(variableout[4], variableout[5], variableout[6], variableout[7], x_20, x_21, x_22, x_23,
                                 d[1])
            x_24 = IVLBCLin.CreateVariable(self, "x", 24)
            x_25 = IVLBCLin.CreateVariable(self, "x", 25)
            x_26 = IVLBCLin.CreateVariable(self, "x", 26)
            x_27 = IVLBCLin.CreateVariable(self, "x", 27)
            self.ConstraintsByLF(variableout[8], variableout[9], variableout[10], variableout[11], x_24, x_25, x_26,
                                 x_27, d[2])
            x_28 = IVLBCLin.CreateVariable(self, "x", 28)
            x_29 = IVLBCLin.CreateVariable(self, "x", 29)
            x_30 = IVLBCLin.CreateVariable(self, "x", 30)
            x_31 = IVLBCLin.CreateVariable(self, "x", 31)
            self.ConstraintsByLF(variableout[12], variableout[13], variableout[14], variableout[15], x_28, x_29, x_30,
                                 x_31, d[3])

        else:
            self.Constraints(variablein)
            variableout = self.VariableRotation(variablein)
            x_16 = IVLBCLin.CreateVariable(self, "x", 16)
            x_17 = IVLBCLin.CreateVariable(self, "x", 17)
            x_18 = IVLBCLin.CreateVariable(self, "x", 18)
            x_19 = IVLBCLin.CreateVariable(self, "x", 19)
            self.ConstraintsByLF(variableout[0], variableout[1], variableout[2], variableout[3], x_16, x_17, x_18, x_19,
                                 d[0])
            x_20 = IVLBCLin.CreateVariable(self, "x", 20)
            x_21 = IVLBCLin.CreateVariable(self, "x", 21)
            x_22 = IVLBCLin.CreateVariable(self, "x", 22)
            x_23 = IVLBCLin.CreateVariable(self, "x", 23)
            self.ConstraintsByLF(variableout[4], variableout[5], variableout[6], variableout[7], x_20, x_21, x_22, x_23,
                                 d[1])
            x_24 = IVLBCLin.CreateVariable(self, "x", 24)
            x_25 = IVLBCLin.CreateVariable(self, "x", 25)
            x_26 = IVLBCLin.CreateVariable(self, "x", 26)
            x_27 = IVLBCLin.CreateVariable(self, "x", 27)
            self.ConstraintsByLF(variableout[8], variableout[9], variableout[10], variableout[11], x_24, x_25, x_26,
                                 x_27, d[2])
            x_28 = IVLBCLin.CreateVariable(self, "x", 28)
            x_29 = IVLBCLin.CreateVariable(self, "x", 29)
            x_30 = IVLBCLin.CreateVariable(self, "x", 30)
            x_31 = IVLBCLin.CreateVariable(self, "x", 31)
            self.ConstraintsByLF(variableout[12], variableout[13], variableout[14], variableout[15], x_28, x_29, x_30,
                                 x_31, d[3])

            for i in range(1, self.Round - 1):
                variableout[0] = x_16
                variableout[1] = x_17
                variableout[2] = x_18
                variableout[3] = x_19
                variableout[4] = x_20
                variableout[5] = x_21
                variableout[6] = x_22
                variableout[7] = x_23
                variableout[8] = x_24
                variableout[9] = x_25
                variableout[10] = x_26
                variableout[11] = x_27
                variableout[12] = x_28
                variableout[13] = x_29
                variableout[14] = x_30
                variableout[15] = x_31
                d = IVLBCLin.CreateVariablesdd(self, i)
                variableout = self.VariableRotation(variableout)
                x_16 = IVLBCLin.CreateVariable(self, "x", 16 + (i) * 16)
                x_17 = IVLBCLin.CreateVariable(self, "x", 17 + (i) * 16)
                x_18 = IVLBCLin.CreateVariable(self, "x", 18 + (i) * 16)
                x_19 = IVLBCLin.CreateVariable(self, "x", 19 + (i) * 16)
                self.ConstraintsByLF(variableout[0], variableout[1], variableout[2], variableout[3], x_16, x_17, x_18,
                                     x_19, d[0])
                x_20 = IVLBCLin.CreateVariable(self, "x", 20 + (i) * 16)
                x_21 = IVLBCLin.CreateVariable(self, "x", 21 + (i) * 16)
                x_22 = IVLBCLin.CreateVariable(self, "x", 22 + (i) * 16)
                x_23 = IVLBCLin.CreateVariable(self, "x", 23 + (i) * 16)
                self.ConstraintsByLF(variableout[4], variableout[5], variableout[6], variableout[7], x_20, x_21, x_22,
                                     x_23, d[1])
                x_24 = IVLBCLin.CreateVariable(self, "x", 24 + (i) * 16)
                x_25 = IVLBCLin.CreateVariable(self, "x", 25 + (i) * 16)
                x_26 = IVLBCLin.CreateVariable(self, "x", 26 + (i) * 16)
                x_27 = IVLBCLin.CreateVariable(self, "x", 27 + (i) * 16)
                self.ConstraintsByLF(variableout[8], variableout[9], variableout[10], variableout[11], x_24, x_25, x_26,
                                     x_27, d[2])
                x_28 = IVLBCLin.CreateVariable(self, "x", 28 + (i) * 16)
                x_29 = IVLBCLin.CreateVariable(self, "x", 29 + (i) * 16)
                x_30 = IVLBCLin.CreateVariable(self, "x", 30 + (i) * 16)
                x_31 = IVLBCLin.CreateVariable(self, "x", 31 + (i) * 16)
                self.ConstraintsByLF(variableout[12], variableout[13], variableout[14], variableout[15], x_28, x_29,
                                     x_30, x_31, d[3])

    def CreateVariables(self, n):
        """
        Generate the variables used in the model
        """
        array = []
        for i in range(0, 16):
            array.append(("x" + "_" + str(i)))
        return array

    def CreateVariablesdd(self, n):
        """
        Generate the variables used in the model
        """

        array = []
        for i in range(0, 4):
            array.append(("d" + "_" + str(i + n * 4)))
        return array

    def Constraints(self, variablex):


        fileobj = open(self.filename_model, "a")
        temp = []
        for i in range(0, 16):
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

    def CreateVariable(self, s, n):
        """
        Generate the variables used in the model.
        """
        array = (s + "_" + str(n))
        return array

    def ConstraintsByLF(self, variabley, variablev, variablex, variableu, variabley1, variablev1, variablex1,
                        variableu1, d):

        print("Input a round number greater than 10.")
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
        fileobj.write(variabley + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablev + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablex + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variableu + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variabley1 + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablev1 + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variablex1 + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.write(variableu1 + " -" + d + " <= 0")
        fileobj.write("\n")
        fileobj.close()

    def VariableBinary(self):

        fileobj = open(self.filename_model, "a")
        fileobj.write("Binary\n")
        for j in range(0, 16):
            fileobj.write("x_" + str(j))
            fileobj.write("\n")
        for i in range(0, self.Round - 1):
            for j in range(0, 4):
                fileobj.write("d_" + str(j + i * 4))
                fileobj.write("\n")
            for j in range(0, 16):
                fileobj.write("x_" + str(16 + i * 16 + j))
                fileobj.write("\n")
        fileobj.write("END")
        fileobj.close()

    def SolveModel(self):
        """
        Solve the MILP model to search the integral distinguisher of Present.
        """

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
        while counter < 16 * self.Round + 1:
            m.optimize()

            if m.Status == 2:
                print("m.Status == 2")
                obj = m.getObjective()
                sum = 0
                result = 0
                for v in m.getVars():
                    print('%s %g' % (v.varName, v.x))
                    sum = sum + 1
                    print("sum=%d" % (sum))
                    if sum < 16 * self.Round + 1:
                        result = result + v.x
                        # print('%s %g' % (v.varName, v.x))
                    else:
                        break
                print("min_activesbox：%d" % (self.Round, result))
                if obj.getValue() > 1:
                    global_flag = True
                    print("obj.getValue()=%d" % (obj.getValue()))
                    break
                else:
                    fileobj = open(self.filename_result, "a")
                    fileobj.write("************************************COUNTER = %d\n" % counter)
                    fileobj.close()
                    self.WriteObjective(obj)
                    print("---------------------------------")
                    print(obj)
                    print("---------------------------------")

                    for i in range(0, 16 * self.Round):
                        u = obj.getVar(i)
                        temp = u.getAttr('x')
                        if temp == 1:
                            set_zero.append(u.getAttr('VarName'))
                            u.ub = 0
                            m.update()
                            counter += 1
                            #  print("counter1=%d "%(counter))
                            break
                        else:
                            counter += 1
                        #   print("counter2=%d "%(counter))
            # Gurobi syntax: m.Status == 3 represents the model is infeasible.
            elif m.Status == 3:
                print("m.Status == 3")
                global_flag = True
                break
            else:
                print("Unknown error!")

        fileobj = open(self.filename_result, "a")
        if global_flag:
            fileobj.write("\n Active SBox Found!\n\n")
            print("Active SBox Found!\n")
        else:
            fileobj.write("\nActive SBox do NOT exist\n\n")
            print("Active SBox do NOT exist\n")

        fileobj.write("Those are the coordinates set to zero: \n")
        for u in set_zero:
            fileobj.write(u)
            fileobj.write("\n")
        fileobj.write("\n")
        time_end = time.time()
        fileobj.write(("Time used = " + str(time_end - time_start)))
        fileobj.close()
