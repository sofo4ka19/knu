#include <string>
#include <iostream>
#include <thread>
#include <cstddef>
#include "windows.h"
#include "psapi.h"

size_t get_current_virtual_memory() {
    PROCESS_MEMORY_COUNTERS_EX pmc;
    GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));
    SIZE_T virtualMemUsedByMe = pmc.PrivateUsage;
    return virtualMemUsedByMe;
}

size_t get_current_physical_memory() {
    PROCESS_MEMORY_COUNTERS_EX pmc;
    GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));
    SIZE_T physMemUsedByMe = pmc.WorkingSetSize;
    return physMemUsedByMe;
}

inline long long memory_difference(size_t start, size_t end) {
    if (end >= start) {
        return end - start;
    }
    else {
        return (-1)*(start - end);
    }

}

struct BenchmarkMax {
    size_t start_virtual_memory;
    size_t start_physical_memory;
    std::string name;
    size_t max_virtual_memory;
    size_t max_physical_memory;
    bool is_running;
    std::thread measurement_thread;

    BenchmarkMax(std::string name) :
            start_virtual_memory(get_current_virtual_memory()),
            start_physical_memory(get_current_physical_memory()),
            name(name),
            max_virtual_memory(0),
            max_physical_memory(0),
            is_running(true),
            measurement_thread(&BenchmarkMax::run, this)
    { }


    void measure() {
        size_t current_virtual_memory = get_current_virtual_memory();
        if (current_virtual_memory > max_virtual_memory) {
            max_virtual_memory = current_virtual_memory;
        }

        size_t current_physical_memory = get_current_physical_memory();
        if (current_physical_memory > max_physical_memory) {
            max_physical_memory = current_physical_memory;
        }
    }

    void run() {
        do {
            measure();
        } while (is_running); // need to run measure at least once
    }

    ~BenchmarkMax() {
        is_running = false;
        measurement_thread.join();

        std::cout << "BenchmarkMax " << name << ": virtual " << memory_difference(start_virtual_memory, max_virtual_memory) <<
                  " bytes, physical " << memory_difference(start_physical_memory, max_physical_memory) << " bytes" << std::endl;
    }

};