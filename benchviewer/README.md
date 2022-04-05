# BenchViewer
BenchViewer is the main interface for user's to filter and download benchmarks from MQT Bench 

# Structure
- ```main.py```: File to start the server
- ```backend.py```: Containing the backend logic
- ```static/files/qasm_output.py```: Containing all available benchmark files
```
BenchViewer
│ - README.md
│ - run.py  
│ - backend.py  
│ - ...
└───static
    │ ...
    └───files
         └─── qasm_output
                └─── <all available benchmarks>
         

```

# Usage
To start the website, just run the jupyter notebook locally
```python
python main.py
```
The website is afterwards hosted at [http://127.0.0.1:5000/app/benchviewer](http://127.0.0.1:5000/app/benchviewer).