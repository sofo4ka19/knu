#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <mpi.h>

using namespace std;

// Declarations of global variables
int ProcRank; // Rank of current process
int ProcNum;  // Number of processes
const double InfinitiesPercent = 50.0;
const double RandomDataMultiplier = 10;

// Function declarations (from both files)
int Min(int A, int B);
void ProcessInitialization(int *&pMatrix, int *&pProcRows, int &Size, int &RowNum);
void ProcessInitializationTest(int *&pMatrix, int *&pProcRows, int &Size, int &RowNum);
void ProcessTermination(int *pMatrix, int *pProcRows);
void DummyDataInitialization(int *pMatrix, int Size);
void DataDistribution(int *pMatrix, int *pProcRows, int Size, int RowNum);
void ResultCollection(int *pMatrix, int *pProcRows, int Size, int RowNum);
void ParallelFloyd(int *pProcRows, int Size, int RowNum);
void RowDistribution(int *pProcRows, int Size, int RowNum, int k, int *pRow);
void ParallelPrintMatrix(int *pProcRows, int Size, int RowNum);
void TestDistribution(int *pMatrix, int *pProcRows, int Size, int RowNum);
void TestResult(int *pMatrix, int *pSerialMatrix, int Size);

bool CompareMatrices(int *pMatrix1, int *pMatrix2, int Size);
void SerialFloyd(int *pMatrix, int Size);
void PrintMatrix(int *pMatrix, int RowCount, int ColCount);
void CopyMatrix(int *pMatrix, int Size, int *pMatrixCopy); // Added function declaration

// Function to calculate minimum of two values
int Min(int A, int B) {
    int Result = (A < B) ? A : B;
    if ((A < 0) && (B >= 0)) Result = B;
    if ((B < 0) && (A >= 0)) Result = A;
    if ((A < 0) && (B < 0)) Result = -1;

    return Result;
}

// Main function
int main(int argc, char *argv[]) {
    int *pMatrix;
    int Size;
    int *pProcRows;
    int RowNum;
    double start, finish;
    double duration = 0.0;
    int *pSerialMatrix = nullptr;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &ProcNum);
    MPI_Comm_rank(MPI_COMM_WORLD, &ProcRank);

    for (int i = 0; i < 7; i++) {
        if (i == 0)
            Size = 10;
        else
            Size = 500 + (i - 1) * 100;

        ProcessInitializationTest(pMatrix, pProcRows, Size, RowNum);

        if (ProcRank == 0) {
            pSerialMatrix = new int[Size * Size];
            DummyDataInitialization(pMatrix, Size);  // Replace CopyMatrix with DummyDataInitialization
        }

        start = MPI_Wtime();

        DataDistribution(pMatrix, pProcRows, Size, RowNum);

        ParallelFloyd(pProcRows, Size, RowNum);

        ResultCollection(pMatrix, pProcRows, Size, RowNum);

        finish = MPI_Wtime();

        duration = finish - start;
        if (ProcRank == 0) {
            printf("Time of execution: %f\n", duration);
            delete[] pSerialMatrix;
        }

        ProcessTermination(pMatrix, pProcRows);
    }

    MPI_Finalize();

    return 0;
}

// Functions from ParallelFloydTest.cpp

// Copy matrix from pMatrix to pMatrixCopy
void CopyMatrix(int *pMatrix, int Size, int *pMatrixCopy) {
    copy(pMatrix, pMatrix + Size * Size, pMatrixCopy);
}

// Compare two matrices
bool CompareMatrices(int *pMatrix1, int *pMatrix2, int Size) {
    return equal(pMatrix1, pMatrix1 + Size * Size, pMatrix2);
}

// Serial Floyd algorithm
void SerialFloyd(int *pMatrix, int Size) {
    int t1, t2;

    for(int k = 0; k < Size; k++)
        for(int i = 0; i < Size; i++)
            for(int j = 0; j < Size; j++)
                if((pMatrix[i * Size + k] != -1) &&
                (pMatrix[k * Size + j] != -1)) {
                    t1 = pMatrix[i * Size + j];
                    t2 = pMatrix[i * Size + k] + pMatrix[k * Size + j];
                    pMatrix[i * Size + j] = Min(t1, t2);
                }
}

// Print matrix in a formatted way
void PrintMatrix(int *pMatrix, int RowCount, int ColCount) {
    for(int i = 0; i < RowCount; i++) {
        for(int j = 0; j < ColCount; j++) {
            printf("%7d", pMatrix[i * ColCount + j]);
            fflush(stdout);
        }
        printf("\n");
        fflush(stdout);
    }
}

// Process initialization for test purposes
void ProcessInitializationTest(int *&pMatrix, int *&pProcRows, int &Size, int &RowNum) {
    if (ProcRank == 0) {
        if (Size < ProcNum)
            printf("The number of vertices should be greater than the number of processes\n");
        printf("Using the graph with %d vertices\n", Size);
    }

    MPI_Bcast(&Size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int RestRows = Size;
    for (int i = 0; i < ProcRank; i++)
        RestRows -= RestRows / (ProcNum - i);
    RowNum = RestRows / (ProcNum - ProcRank);

    pProcRows = new int[Size * RowNum];

    if (ProcRank == 0) {
        pMatrix = new int[Size * Size];
        DummyDataInitialization(pMatrix, Size);
    }
}

// Dummy data initialization
void DummyDataInitialization(int *pMatrix, int Size) {
    for (int i = 0; i < Size; i++) {
        for (int j = i; j < Size; j++) {
            if (i == j) pMatrix[i * Size + j] = 0;
            else if (i == 0) pMatrix[i * Size + j] = j;
            else pMatrix[i * Size + j] = -1;
            pMatrix[j * Size + i] = pMatrix[i * Size + j];
        }
    }
}

// Data distribution across processes
void DataDistribution(int *pMatrix, int *pProcRows, int Size, int RowNum) {
    int *pSendNum = new int[ProcNum];
    int *pSendInd = new int[ProcNum];

    int RestRows = Size;
    RowNum = Size / ProcNum;
    pSendNum[0] = RowNum * Size;
    pSendInd[0] = 0;

    for (int i = 1; i < ProcNum; i++) {
        RestRows -= RowNum;
        RowNum = RestRows / (ProcNum - i);
        pSendNum[i] = RowNum * Size;
        pSendInd[i] = pSendInd[i - 1] + pSendNum[i - 1];
    }

    MPI_Scatterv(pMatrix, pSendNum, pSendInd, MPI_INT, pProcRows, pSendNum[ProcRank], MPI_INT, 0, MPI_COMM_WORLD);

    delete[] pSendNum;
    delete[] pSendInd;
}

// Result collection after parallel execution
void ResultCollection(int *pMatrix, int *pProcRows, int Size, int RowNum) {
    int *pReceiveNum = new int[ProcNum];
    int *pReceiveInd = new int[ProcNum];

    int RestRows = Size;
    RowNum = Size / ProcNum;
    pReceiveInd[0] = 0;
    pReceiveNum[0] = RowNum * Size;

    for (int i = 1; i < ProcNum; i++) {
        RestRows -= RowNum;
        RowNum = RestRows / (ProcNum - i);
        pReceiveNum[i] = RowNum * Size;
        pReceiveInd[i] = pReceiveInd[i - 1] + pReceiveNum[i - 1];
    }

    MPI_Gatherv(pProcRows, pReceiveNum[ProcRank], MPI_INT, pMatrix, pReceiveNum, pReceiveInd, MPI_INT, 0, MPI_COMM_WORLD);

    delete[] pReceiveNum;
    delete[] pReceiveInd;
}

// Parallel Floyd algorithm
void ParallelFloyd(int *pProcRows, int Size, int RowNum) {
    int *pRow = new int[Size];
    int t1, t2;

    for (int k = 0; k < Size; k++) {
        RowDistribution(pProcRows, Size, RowNum, k, pRow);

        for (int i = 0; i < RowNum; i++) {
            for (int j = 0; j < Size; j++) {
                if ((pProcRows[i * Size + k] != -1) && (pRow[j] != -1)) {
                    t1 = pProcRows[i * Size + j];
                    t2 = pProcRows[i * Size + k] + pRow[j];
                    pProcRows[i * Size + j] = Min(t1, t2);
                }
            }
        }
    }

    delete[] pRow;
}

// Row distribution for parallel algorithm
void RowDistribution(int *pProcRows, int Size, int RowNum, int k, int *pRow) {
    int ProcRowRank, ProcRowNum, RestRows = Size, Ind = 0, Num = Size / ProcNum;

    for (ProcRowRank = 1; ProcRowRank <= ProcNum; ProcRowRank++) {
        if (k < Ind + Num) break;
        RestRows -= Num;
        Ind += Num;
        Num = RestRows / (ProcNum - ProcRowRank);
    }

    ProcRowRank--;
    ProcRowNum = k - Ind;

    if (ProcRowRank == ProcRank)
        copy(&pProcRows[ProcRowNum * Size], &pProcRows[(ProcRowNum + 1) * Size], pRow);

    MPI_Bcast(pRow, Size, MPI_INT, ProcRowRank, MPI_COMM_WORLD);
}


