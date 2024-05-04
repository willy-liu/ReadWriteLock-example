# Multi-Threaded Server Application

This project implements a multi-threaded server that manages a shared integer array of size 10. The server allows concurrent read and exclusive write access to the array through socket communication.

## Files

- `server.py`: Implements the multi-threaded server.
- `client.py`: Contains both reader and writer client functionalities.
- `main.py`: Responsible for starting both the server and client processes.

## Server Details

The server maintains an array of 10 integers. It handles two types of client operations:
- **Read Operation (`read cond`)**: Returns values from the array that satisfy the condition specified in `cond` (e.g., `> 10`, `% 3`).
- **Write Operation (`write num[10]`)**: Updates the array with a new set of 10 integers provided by the client.

### Thread Management

- **Main Thread**: Handles incoming client requests and spawns a new thread for each request (read or write).
- **Service Threads**: Each spawned thread will:
  - Communicate with the assigned client.
  - Handle concurrency control to ensure safe operations.
  - Allow multiple concurrent readers, but ensure exclusive access for writers.
  - Implement busy loops to simulate extended operation times, increasing resource contention.

### Concurrency Control

- Writers, upon finishing, allow the next waiting writer to proceed before any readers, if any writers are waiting.
- If no writers are waiting, all readers are allowed to execute concurrently.
- Busy loops are used within the critical sections to simulate longer service times and introduce contention.

## Client Details

- Clients are implemented to test the server's concurrency control mechanisms.
- Reader and writer clients are included.
- Clients continuously make requests to test server contention and concurrency management.
- Status messages with client identifiers are printed to the screen to trace the operations.

### Testing

- **Read Client**: Makes 30 consecutive read requests and prints the results.
- **Write Client**: Makes 30 write requests in a loop, incrementing the array values each time (e.g., first loop writes values 1~10, second loop writes values 11~20, etc.).

## Usage

To run the server and client scripts simultaneously, execute the `main.py` file. This script sets up and initiates the server and clients as separate processes:

```bash
python main.py
```

### Design Tests

Test scenarios are designed to ensure that:

- Readers always receive array values written by one complete writer operation.
- The concurrency control techniques are effective under high load and contention scenarios.
  
Additional test strategies include introducing artificial delays in client operations to observe the impact on operation interleaving and outcomes.
