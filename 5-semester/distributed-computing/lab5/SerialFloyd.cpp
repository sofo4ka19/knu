#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <algorithm>

using namespace std;

const double InfinitiesPercent = 50.0;
const double RandomDataMultiplier = 10;

// Оголошення всіх функцій
int Min(int A, int B);
void ProcessInitialization(int *&pMatrix, int& Size);
void ProcessInitializationTest(int *&pMatrix, int& Size);
void ProcessTermination(int *pMatrix);
void DummyDataInitialization(int *pMatrix, int Size);
void RandomDataInitialization(int *pMatrix, int Size);
void CopyMatrix(int *pMatrix, int Size, int *pMatrixCopy);
bool CompareMatrices(int *pMatrix1, int *pMatrix2, int Size);
void PrintMatrix(int *pMatrix, int RowCount, int ColCount);
void SerialFloyd(int *pMatrix, int Size);

// Функція для вибору мінімального значення
int Min(int A, int B) {
    int Result = (A < B) ? A : B;
    if ((A < 0) && (B >= 0)) Result = B;
    if ((B < 0) && (A >= 0)) Result = A;
    if ((A < 0) && (B < 0)) Result = -1;
    return Result;
}

// Ініціалізація матриці суміжності
void ProcessInitialization(int *&pMatrix, int& Size) {
    do {
        printf("Enter the number of vertices: ");
        scanf("%d", &Size);
        
        if (Size <= 0)
            printf("The number of vertices should be greater than zero\n");
    } while (Size <= 0);
    
    printf("Using graph with %d vertices\n", Size);
    
    // Виділення пам'яті для матриці
    pMatrix = new int[Size * Size];
    
    // Ініціалізація даних
    RandomDataInitialization(pMatrix, Size);
}

// Ініціалізація для тестів
void ProcessInitializationTest(int *&pMatrix, int& Size) {
    do {
        printf("Enter the number of vertices: ");
        scanf("%d", &Size);
        if(Size <= 0)
            printf("The number of vertices should be greater than zero\n");
    } while(Size <= 0);
    
    // Виділення пам'яті для матриці
    pMatrix = new int[Size * Size];
    
    // Ініціалізація даних
    RandomDataInitialization(pMatrix, Size);
}

// Завершення роботи
void ProcessTermination(int *pMatrix) {
    delete[] pMatrix;
}

// Проста ініціалізація даних
void DummyDataInitialization(int *pMatrix, int Size) {
    for (int i = 0; i < Size; i++) {
        for (int j = i; j < Size; j++) {
            if (i == j) 
                pMatrix[i * Size + j] = 0;
            else if (i == 0) 
                pMatrix[i * Size + j] = j;
            else 
                pMatrix[i * Size + j] = -1;
            pMatrix[j * Size + i] = pMatrix[i * Size + j];
        }
    }
}

// Ініціалізація випадковими даними
void RandomDataInitialization(int *pMatrix, int Size) {
    srand((unsigned)time(0));

    for (int i = 0; i < Size; i++) {
        for (int j = 0; j < Size; j++) {
            if (i != j) {
                if ((rand() % 100) < InfinitiesPercent)
                    pMatrix[i * Size + j] = -1;
                else
                    pMatrix[i * Size + j] = rand() % (int(RandomDataMultiplier)) + 1;
            } else {
                pMatrix[i * Size + j] = 0;
            }
        }
    }
}

// Скопіювати матрицю
void CopyMatrix(int *pMatrix, int Size, int *pMatrixCopy) {
    for (int i = 0; i < Size * Size; i++) {
        pMatrixCopy[i] = pMatrix[i];
    }
}

// Порівняти дві матриці
bool CompareMatrices(int *pMatrix1, int *pMatrix2, int Size) {
    for (int i = 0; i < Size * Size; i++) {
        if (pMatrix1[i] != pMatrix2[i])
            return false;
    }
    return true;
}

// Друк матриці
void PrintMatrix(int *pMatrix, int RowCount, int ColCount) {
    for (int i = 0; i < RowCount; i++) {
        for (int j = 0; j < ColCount; j++) {
            if (pMatrix[i * ColCount + j] == -1)
                printf("%4s", "INF");
            else
                printf("%4d", pMatrix[i * ColCount + j]);
        }
        printf("\n");
    }
}

// Реалізація алгоритму Флойда
void SerialFloyd(int *pMatrix, int Size) {
    int t1, t2;

    for (int k = 0; k < Size; k++) {
        for (int i = 0; i < Size; i++) {
            for (int j = 0; j < Size; j++) {
                if ((pMatrix[i * Size + k] != -1) && 
                    (pMatrix[k * Size + j] != -1)) {
                    t1 = pMatrix[i * Size + j];
                    t2 = pMatrix[i * Size + k] + pMatrix[k * Size + j];
                    pMatrix[i * Size + j] = Min(t1, t2);
                }
            }
        }
    }
}

// Головна функція
int main(int argc, char* argv[]) {
    int *pMatrix; // Матриця суміжності
    int Size; // Розмір матриці
    time_t start, finish;
    double duration = 0.0;

    printf("Serial Floyd algorithm\n");

    // Ініціалізація процесу
    ProcessInitializationTest(pMatrix, Size);

    start = clock();

    // Алгоритм Флойда
    SerialFloyd(pMatrix, Size);
    finish = clock();

    duration = (finish - start) / double(CLOCKS_PER_SEC);
    printf("Time of execution: %f\n", duration);
        
    // Завершення процесу
     ProcessTermination(pMatrix);

    return 0;
}

