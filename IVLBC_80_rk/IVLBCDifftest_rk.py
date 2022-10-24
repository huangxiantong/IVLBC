from IVLBCDiff_rk import IVLBCDiff_rk

if __name__ == "__main__":
	ROUND = int(input("Input the target round number: "))
	while not (ROUND > 0):
		print("Input a round number greater than 0.")
		ROUND = int(input("Input the target round number again: "))
	IVLBC =IVLBCDiff_rk(ROUND)

	IVLBC.MakeModel()

	IVLBC.SolveModel()
