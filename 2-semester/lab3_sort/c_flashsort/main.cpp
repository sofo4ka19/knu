#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <random>

void print(const std::vector<int>& arr) {
    for (int val : arr) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}
void siftDown(std::vector<int>& arr, int root, int end) {
    int child = 2 * (root + 1) - 1;
    while (child <= end) {
        if (child + 1 <= end && arr[child] < arr[child + 1]) {
            ++child;
        }
        if (arr[root] < arr[child]) {
            std::swap(arr[root], arr[child]);
            root = child;
            child = 2 * (root + 1) - 1;
        } else {
            break;
        }
    }
}

void smoothsort(std::vector<int>& arr, bool step) {
    int n = arr.size();
    for (int i = 1; (1 << i) - 1 < n; ++i) {
        int p = (1 << (i - 1)) - 1;
        int q = (1 << i) - 1;
        for (int j = p; j < n - 1; j += q) {
            siftDown(arr, j, std::min(j + q, n - 1));
        }
    }
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        siftDown(arr, 0, i - 1);
    }
}
void demo(int size){
    std::vector<int> arr;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> num(1, 1000);
    std::cout << "Input: ";
    for (int i = 0; i < size; ++i) {
        arr.push_back(num(gen));
        std::cout << arr[i]<< " ";
    }
    std::cout << std::endl;

    smoothsort(arr, true);
    std::cout << "Output: ";
    print(arr);
}
int main() {

    demo(25);
    return 0;
}