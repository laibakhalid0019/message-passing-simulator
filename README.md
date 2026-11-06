# PDC Message-Passing Simulator

An interactive simulator developed for the **Parallel and Distributed Computing (PDC)** assignment. This project demonstrates message-passing communication protocols, deadlock detection, parallel performance metrics, and serial fraction analysis.

## Features

### 1. Message-Passing Simulation
- Blocking non-buffered communication.
- Blocking buffered communication.
- Send and receive operations.
- Deadlock detection.
- Identification of stuck processes.
- Execution order of completed operations.

### 2. Deadlock Analysis
- Simulation of all four communication fragments (A, B, C, D).
- Comparison of buffered and non-buffered protocols.
- Identification of deadlock conditions.
- Automatic deadlock correction by reversing operations of odd-numbered processes.

### 3. Idling Overhead and Finite Buffers
- Sender idle-time calculation.
- Receiver idle-time calculation.
- Message transfer completion time.
- Comparison of buffered and non-buffered communication.

### 4. Parallel Performance Metrics
- Parallel execution time.
- Speedup.
- Efficiency.
- Parallel cost.
- Total overhead.
- Isoefficiency analysis.
- Granularity analysis.

### 5. Serial Fraction Analysis
- Experimental serial fraction calculation.
- Amdahl's Law.
- Maximum theoretical speedup.
- Predicted speedup for different processing elements.

## Technologies Used

- Python
- HTML, CSS and JavaScript (for the interactive interface)
- Mathematical performance models

## Assignment Topics Covered

- Chapter 5: Analytical Modeling
- Chapter 6: Message-Passing Paradigm

## How to Run

For the Python simulator:

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/pdc-message-passing-simulator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pdc-message-passing-simulator
   ```

3. Run the simulator:

   ```bash
   python pdc_simulator.py
   ```

No external Python packages are required.

## Project Structure

```text
pdc-message-passing-simulator/
│
├── pdc_simulator.py
├── README.md
└── .gitignore
```

## Purpose

The purpose of this project is to provide a practical understanding of parallel computing concepts through simulation and interactive calculations. It helps students understand communication synchronization, deadlocks, performance overhead, scalability, and parallel efficiency.

---

**Course:** Parallel and Distributed Computing (PDC)  
**Assignment:** Assignment 3  
**Language:** Python  
**Project Type:** Educational Simulator
