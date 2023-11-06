#Sarthak Hans

def parse_circuit_file(filename):
  #Parse the circuit file and return inputs, outputs, gates, and gate order.
  inputs = {}
  outputs = {}
  gates = {}
  gate_order = []

  with open(filename, 'r') as file:
      for line in file:
          line = line.strip()
          if line.startswith('#') or not line:
              continue

          if line.startswith('INPUT('):
              input_name = line.split('(')[1][:-1]
              inputs[input_name] = 0

          elif line.startswith('OUTPUT('):
              output_name = line.split('(')[1][:-1]
              outputs[output_name] = None

          elif '=' in line:
              left, right = line.split('=', 1)
              gate_name = left.strip()
              gate_info = right.strip()
              gate_order.append(gate_name)

              output_wire, remaining = gate_info.split('(', 1)
              remaining = remaining.rstrip(')')
              input_wires = [w.strip() for w in remaining.split(',')]

              gates[gate_name] = {
                  'type': output_wire,
                  'inputs': input_wires,
                  'output': None
              }

  return inputs, outputs, gates, gate_order

def generate_full_fault_list(inputs, gates):
  #Generate a list of all possible faults for the circuit.
  fault_list = []

  for node in inputs:
      fault_list.append(f"{node}-0")
      fault_list.append(f"{node}-1")

  for gate in gates:
      fault_list.append(f"{gate}-0")
      fault_list.append(f"{gate}-1")

  return fault_list

def simulate(inputs, outputs, gates, gate_order, input_vector):
  # Reset outputs and gates' outputs to initial states
  for key in outputs:
      outputs[key] = None
  for key in gates:
      gates[key]['output'] = None

  for i, node in enumerate(inputs.keys()):
      inputs[node] = int(input_vector[i])

  for gate in gate_order:
      gate_info = gates[gate]
      input_values = [inputs[inp] if inp in inputs else gates[inp]['output'] for inp in gate_info['inputs']]

      if gate_info['type'] == 'NAND':
          gates[gate]['output'] = int(not all(input_values))
      elif gate_info['type'] == 'AND':
          gates[gate]['output'] = int(all(input_values))
      elif gate_info['type'] == 'OR':
          gates[gate]['output'] = int(any(input_values))
      elif gate_info['type'] == 'NOT':
          gates[gate]['output'] = int(not input_values[0])
      elif gate_info['type'] == 'NOR':
          gates[gate]['output'] = int(not any(input_values))
      elif gate_info['type'] == 'XOR':
          gates[gate]['output'] = int(input_values.count(1) % 2 == 1)
      elif gate_info['type'] == 'BUFF':
        gates[gate]['output'] = input_values[0]

  for output in outputs:
      outputs[output] = inputs[output] if output in inputs else gates[output]['output']

  return ''.join(str(outputs[out]) for out in outputs)

def simulate_with_fault(inputs, outputs, gates, gate_order, input_vector, fault):
  #Simulate the circuit with a given fault and input vector.
  fault_node, fault_value = fault.split('-')
  fault_value = int(fault_value)

  for i, node in enumerate(inputs.keys()):
      inputs[node] = int(input_vector[i])

  if fault_node in inputs:
      inputs[fault_node] = fault_value

  for gate in gate_order:
      gate_info = gates[gate]
      input_values = [inputs[inp] if inp in inputs else gates[inp]['output'] for inp in gate_info['inputs']]

      for idx, inp in enumerate(gate_info['inputs']):
          if inp == fault_node:
              input_values[idx] = fault_value

      if gate_info['type'] == 'NAND':
          gates[gate]['output'] = int(not all(input_values))
      elif gate_info['type'] == 'AND':
          gates[gate]['output'] = int(all(input_values))
      elif gate_info['type'] == 'OR':
          gates[gate]['output'] = int(any(input_values))
      elif gate_info['type'] == 'NOT':
          gates[gate]['output'] = int(not input_values[0])
      elif gate_info['type'] == 'NOR':
          gates[gate]['output'] = int(not any(input_values))
      elif gate_info['type'] == 'XOR':
          gates[gate]['output'] = int(input_values.count(1) % 2 == 1)
      elif gate_info['type'] == 'BUFF':
        gates[gate]['output'] = input_values[0]

  for output in outputs:
      outputs[output] = inputs[output] if output in inputs else gates[output]['output']

  return ''.join(str(outputs[out]) for out in outputs)

def main():
  # A. Fault listing
  # 1. Ask for filename
  filename = input("Enter the circuit filename (default: c.bench): ") or "c.bench"
  inputs, outputs, gates, gate_order = parse_circuit_file(filename)

  # 2. Generate and display fault list
  fault_list = generate_full_fault_list(inputs, gates)
  print("\nFull Fault List:")
  for fault in fault_list:
      print(fault)
  with open('f.txt', 'w') as file:
      for fault in fault_list:
          file.write(fault + '\n')
  print(f"\nTotal number of faults: {len(fault_list)}")
  print(f"Faults saved to 'f.txt'")

  # B. Fault sim
  # 1. Circuit Analysis
  print(f"\nCircuit Analysis:")
  print(f"Expected input bits: {len(inputs)}")
  print(f"Expected output bits: {len(outputs)}")

  # 2. Good circuit simulation
  all_0 = '0' * len(inputs)
  all_1 = '1' * len(inputs)
  print(f"\nAll-0 Test Vector Output: {simulate(inputs, outputs, gates, gate_order, all_0)}")
  print(f"All-1 Test Vector Output: {simulate(inputs, outputs, gates, gate_order, all_1)}")

  # 3. Simulate with a specific fault
  while True:
      fault = input("\nEnter a fault (e.g., 'gate-0' for gate stuck-at-0) or 'q' to quit: ")
      if fault == 'q':
          break
      if fault not in fault_list:
          print("Invalid fault. Please enter a valid fault.")
          continue

      fault_all_0_output = simulate_with_fault(inputs, outputs, gates, gate_order, all_0, fault)
      fault_all_1_output = simulate_with_fault(inputs, outputs, gates, gate_order, all_1, fault)
      print(f"\nAll-0 Test Vector Output with fault {fault}: {fault_all_0_output}")
      print(f"All-1 Test Vector Output with fault {fault}: {fault_all_1_output}")

      if fault_all_0_output != simulate(inputs, outputs, gates, gate_order, all_0):
          print(f"The fault {fault} can be detected by the all-0 input test vector.")
      else:
          print(f"The fault {fault} cannot be detected by the all-0 input test vector.")

      if fault_all_1_output != simulate(inputs, outputs, gates, gate_order, all_1):
          print(f"The fault {fault} can be detected by the all-1 input test vector.")
      else:
          print(f"The fault {fault} cannot be detected by the all-1 input test vector.")

  # 4. Custom test vector simulation
  while True:
      custom_test_vector = input("\nEnter a custom test vector or 'q' to quit: ")
      if custom_test_vector == 'q':
          break
      if len(custom_test_vector) != len(inputs):
          print(f"Invalid input length. Expected {len(inputs)} bits.")
          continue

      fault = input("Enter a fault for simulation: ")
      if fault not in fault_list:
          print("Invalid fault. Please enter a valid fault.")
          continue

      fault_output = simulate_with_fault(inputs, outputs, gates, gate_order, custom_test_vector, fault)
      normal_output = simulate(inputs, outputs, gates, gate_order, custom_test_vector)
      print(f"\nOutput with fault {fault}: {fault_output}")
      if fault_output != normal_output:
          print(f"The fault {fault} can be detected by the test vector {custom_test_vector}.")
      else:
          print(f"The fault {fault} cannot be detected by the test vector {custom_test_vector}.")

  # 5. Custom test vector against full fault list
  while True:
      custom_test_vector = input("\nEnter a custom test vector or 'q' to quit for full fault list: ")
      if custom_test_vector == 'q':
          break
      if len(custom_test_vector) != len(inputs):
          print(f"Invalid input length. Expected {len(inputs)} bits.")
          continue

      detected_faults = 0
      for fault in fault_list:
          fault_output = simulate_with_fault(inputs, outputs, gates, gate_order, custom_test_vector, fault)
          normal_output = simulate(inputs, outputs, gates, gate_order, custom_test_vector)
          if fault_output != normal_output:
              print(f"The fault {fault} can be detected by the test vector {custom_test_vector}.")
              detected_faults += 1

      print(f"\nTotal faults detected by {custom_test_vector}: {detected_faults}/{len(fault_list)}")
      print(f"Coverage: {(detected_faults/len(fault_list))*100:.2f}%")

if __name__ == "__main__":
  main()
