import numpy as np
from mpi4py import MPI
import csv
import sys
import os
def matrix_multiply(A,B,rank,i):
        n = int(sys.argv[1])
        dimension = int(sys.argv[2])
        rows = int(dimension/n)
        columns = int(dimension/n)
        C =np.zeros((dimension,dimension))
        wt1 = MPI.Wtime()
        for j in range(0,rows):
                for k in range(0,columns):
                        row = []
                        value = 0
                        for l in range(0,dimension):
                                value = value + int(A[j][l])*int(B[l][k])
                        C[j][k]= value
        wt2 = MPI.Wtime()
        with open('C-'+str(rank)+','+str(i)+'.csv', mode='w') as C_file:
                C_writer = csv.writer(C_file, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
                for i in range(0,dimension):
                        C_writer.writerow(C[i])
        wt = wt2 - wt1
        return wt

def getB(i):
        with open('B-'+str(i)+'.csv') as csvDataFile:
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
        with open('A-'+str(rank)+'.csv') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                A = []
                for row in csvReader:
                        A.append(row)
        A = np.array(A)
        os.remove('A-'+str(rank)+'.csv')
        for i in range(rank,n):
                B = getB(i)
                wt = wt + matrix_multiply(A,B,rank,i)

        for i in range(0,rank):
                B = getB(i)
                wt = wt + matrix_multiply(A,B,rank,i)

        if rank==0:
                print ("Elapsed wall time = "+str(wt))