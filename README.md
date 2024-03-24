# OnlineShoppingPlatform-using-gRPC

This project implements an online shopping platform leveraging gRPC for communication between distributed systems deployed on Google Cloud servers. The platform provides a seamless shopping experience for users while showcasing the power of distributed systems and the efficiency of gRPC as a communication protocol.


## Tech Stack

<a href="https://www.python.org/" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/python-colored.svg" width="45" height="45" alt="Python" /></a>
<a href="https://cloud.google.com/" target="_blank" rel="noreferrer"><img src="https://static-00.iconduck.com/assets.00/google-cloud-icon-1024x823-wiwlyizc.png" height="42" alt="Google Cloud" /></a>&nbsp;
<a href="https://protobuf.dev/" target="_blank" rel="noreferrer"><img src="https://www.techunits.com/wp-content/uploads/2021/07/pb.png" height="45" alt="protobuf" /></a>
<a href="https://grpc.io/" target="_blank" rel="noreferrer"><img src="https://github.com/aryanGupta-09/OnlineShoppingPlatform-using-gRPC/assets/96881807/4f1a5d76-cc79-448b-91b1-2bad3a464333" height="45" alt="gRPC" /></a>

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
