<!-- Auto-generated guide for AI coding agents working on this repo. -->
# Copilot instructions — Gauss‑Seidel lab

Purpose: Short, actionable guidance for an AI code assistant working on this small C++ codebase (serial + MPI parallel Gauss–Seidel solvers).

**Big Picture**
- **Project role:** Two implementations of the same numerical solver: `SerialGauss-Seidel.cpp` (single-process) and `ParallelGauss-Seidel.cpp` (MPI-based distributed stripe decomposition).
- **How they relate:** The parallel version distributes rows of the global grid to ranks, exchanges bordering rows using `MPI_Sendrecv`, performs local Gauss–Seidel updates, reduces local maxima with `MPI_Allreduce`, then gathers results with `MPI_Gatherv`/`MPI_Scatterv`.

**Build & Run**
- **Serial build:** `g++ -O2 SerialGauss-Seidel.cpp -o serial_gs`
- **Serial run:** `./serial_gs` (runs a built-in test loop of 12 sizes)
- **Parallel build (MPI):** `mpicxx -O2 ParallelGauss-Seidel.cpp -o parallel_gs`
- **Parallel run example:** `mpirun -np 4 ./parallel_gs` or `mpiexec -n 4 ./parallel_gs`
- **Notes:** The parallel program uses MPI for both control and timing (`MPI_Wtime`). Use small `-np` and small grid sizes when iterating during development.

**Project-specific patterns & conventions**
- **Globals for MPI:** `ProcNum` and `ProcRank` are file‑level globals used across functions — respect these when refactoring (avoid hiding them accidentally).
- **Stripe distribution logic:** Row counts are computed repeatedly with the same formula (see `DataDistribution`, `ResultCollection`, and `ProcessTestInitialization`). When changing distribution, update every location consistently.
- **MPI primitives used:** `MPI_Scatterv`/`MPI_Gatherv` for variable-length stripe exchange, `MPI_Sendrecv` for neighbor boundary exchange, `MPI_Bcast` for broadcasting `Size` and `Eps`, `MPI_Allreduce` for global max.
- **Memory management:** Manual `new[]` / `delete[]` ownership — preserve lifetime semantics (root process allocates full matrix; workers only their stripe). If converting to smart pointers, ensure correct ownership per rank.

**Notable gotchas (discoverable from the code)**
- `CopyData` in `ParallelGauss-Seidel.cpp` currently does `std::copy(pMatrix, pMatrix + Size, pSerialMatrix);` — that copies only `Size` elements; intended size appears to be `Size*Size`. Fixing this is required if adding a serial-vs-parallel correctness test.
- Test harness: both programs run a loop of 12 tests with sizes [10,100, (i-1)*1000]. The parallel binary uses `ProcessTestInitialization` in tests (no interactive prompts). If you call `ProcessInitialization` instead, the root process will prompt for input.
- Printing & I/O: root (`ProcRank==0`) handles most user-facing prints. Don't move prints into worker ranks unless explicitly testing per-rank output.

**Examples to reference when editing**
- Boundary exchange: see `ExchangeData` (uses `MPI_Sendrecv` with tags `4` and `5`).
- Distribution: see `DataDistribution` (uses `MPI_Scatterv` and computes `pSendNum/pSendInd`).
- Gathering: see `ResultCollection` (uses `MPI_Gatherv`).

**When changing code — checklist for AI edits**
- Keep MPI initialization/finalize pairing (`MPI_Init` / `MPI_Finalize`) intact.
- Update all occurrences of row‑count logic when changing distribution algorithm.
- If you replace raw arrays with containers, keep cross-rank memory layout identical (row-major indexing `p[i*Size + j]`).
- Add unit/regression tests by running the binaries with small sizes (10, 100). Validate parity between serial & parallel results after fixing `CopyData`.

**Where to look next**
- `ParallelGauss-Seidel.cpp` — primary MPI logic and data movement.
- `SerialGauss-Seidel.cpp` — canonical solver loop and timing.

If anything above is unclear or you want more detail (example unit test harness, CI job, or to convert to CMake), tell me which area to expand and I will iterate.
