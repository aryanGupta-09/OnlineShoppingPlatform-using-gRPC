# OnlineShoppingPlatform-using-gRPC

This project implements an online shopping platform leveraging gRPC for communication between distributed systems deployed on Google Cloud servers. The platform provides a seamless shopping experience for users while showcasing the power of distributed systems and the efficiency of gRPC as a communication protocol.


## Tech Stack

<a href="https://www.python.org/" target="_blank" rel="noreferrer"><img src="https://github.com/aryanGupta-09/GitHub-Profile-Icons/blob/main/Languages/Python.svg" width="45" height="45" alt="Python" /></a>
<a href="https://cloud.google.com/" target="_blank" rel="noreferrer"><img src="https://github.com/aryanGupta-09/GitHub-Profile-Icons/blob/main/Distributed%20Systems%20and%20Cloud/GoogleCloud.png" height="42" alt="Google Cloud" /></a>&nbsp;
<a href="https://protobuf.dev/" target="_blank" rel="noreferrer"><img src="https://github.com/aryanGupta-09/GitHub-Profile-Icons/blob/main/Distributed%20Systems%20and%20Cloud/Protobuf.png" width="64" height="38" alt="Protobuf" /></a>&nbsp;
<a href="https://grpc.io/" target="_blank" rel="noreferrer"><img src="https://github.com/aryanGupta-09/GitHub-Profile-Icons/blob/main/Distributed%20Systems%20and%20Cloud/gRPC.png" width="75" height="38" alt="gRPC" /></a>

## Installation

1. Clone the repo
```bash
  git clone https://github.com/aryanGupta-09/OnlineShoppingPlatform-using-gRPC.git
```

2. Go to the project directory
```bash
  cd OnlineShoppingPlatform-using-gRPC
```

3. Generate the Python code for gRPC
```bash
  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. market.proto
```

4. Run the Python files
