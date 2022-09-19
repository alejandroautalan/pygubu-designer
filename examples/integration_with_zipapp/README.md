# Simple pygubu application integration with python zipapp module

Since pygubu v0.26

Generate zip:

    python3 -m zipapp ./src -o demoapp.pyz -m demoapp.main:run
    
Run zipped application:

    python3 demoapp.pyz

![Captura de pantalla_2022-09-18_21-08-30](https://user-images.githubusercontent.com/3482471/190936090-af40ab6a-9509-4c02-8a6c-23440452bd4f.png)
