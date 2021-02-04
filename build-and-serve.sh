#!/bin/sh
cd ../pygubu
python3 setup.py sdist bdist_wheel
cd ../pygubu-designer
cp ../pygubu/dist/* ./dist

python3 setup.py sdist bdist_wheel
cd dist
python3 -m http.server 8080
cd ..
