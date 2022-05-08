# BenchViewer
BenchViewer is the main interface for user's to filter and download benchmarks from MQT Bench 

# Structure
- ```main.py```: File to start the server
- ```backend.py```: Containing the backend logic
- ```static/files/qasm_output.py```: Containing all available benchmark files
```
BenchViewer
│ - README.md
│ - backend.py  
│ - main.py  
│ - ...
└───static
    │ ...
    └───files
         └─── qasm_output
                └─── <all available benchmarks>
                └─── MQTBench_all.zip
         

```

# Usage
Before starting, all benchmarks must be zipped into a `MQTBench_all.zip` archive. 
To start the website afterwards, just run the jupyter notebook locally:
```python
python main.py
```
The website is afterwards hosted at [http://127.0.0.1:5000/mqtbench](http://127.0.0.1:5000/mqtbench).