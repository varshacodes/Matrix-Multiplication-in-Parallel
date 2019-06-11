import numpy as np
from mpi4py import MPI
import csv
import random
import sys
import os
def matrix_multiply(A,B,rank,i):
        n = int(sys.argv[1])
        dimension = int(sys.argv[2])
        C =np.zeros((dimension,dimension))
        for j in range(0,dimension):
                for k in range(0,dimension):
                        row = []
                        value = 0
                        for l in range(0,n*dimension):
                                value = value + int(A[j][l])*int(B[l][k])
                        C[j][k]= value

def getB(i):
        with open('B_'+str(i)+'.csv') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                B = []
                for row in csvReader:
                        B.append(row)
        B = np.array(B)
        return B


if __name__ == '__main__':
        wt = 0
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        mpisize = comm.Get_size()
        my_host = MPI.Get_processor_name()
        n = int(sys.argv[1])
        dimension = int(sys.argv[2])
        with open('A_'+str(rank)+'.csv') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                A = []
                for row in csvReader:
                        A.append(row)
        A = np.array(A)
        os.remove('A_'+str(rank)+'.csv')
        wt1 = MPI.Wtime()
        for i in range(rank,n):
                B = getB(i)
                matrix_multiply(A,B,rank,i)

        for i in range(0,rank):
                B = getB(i)
                matrix_multiply(A,B,rank,i)
        wt2 = MPI.Wtime()
        wt = wt2 - wt1

        if rank==0:
                print ("No of Processors= "+str(n))
                print ("Matrix Dimesnion= "+str(n*dimension))
                print ("Elapsed wall time = "+str(wt))
        print("Success!")