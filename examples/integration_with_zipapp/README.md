# Simple pygubu application integration with python zipapp module

Since pygubu v0.26

Generate zip:

    python3 -m zipapp ./src -o demoapp.pyz -m demoapp.main:run
    
Run zipped application:

   python3 demoapp.pyz
   
