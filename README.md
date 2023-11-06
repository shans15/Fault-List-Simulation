# Fault-List-Simulation

## Overview
This project involves developing a program for fault listing and simulation in digital circuits. The program is designed to handle bench files representing digital circuits, allowing users to analyze and simulate various fault scenarios.

## Features

### A. Fault Listing
- **Circuit Bench File Input**: Users can input a circuit bench file (default is `c.bench`).
- **Fault List Generation**: The program generates a complete list of possible faults for the given circuit, displaying it on the screen and writing to a file `f.txt`.

### B. Fault Simulation
- **Circuit Analysis**: Displays the number of bits expected for circuit input and output.
- **Good Circuit Simulation**: Simulates and prints the output for all-0 and all-1 input test vectors for the fault-free circuit.
- **Fault Impact Simulation**: Users can specify a fault and simulate its effect under all-0 and all-1 input test vectors. The program will show the final values of each node and conclude the detectability of the fault.
