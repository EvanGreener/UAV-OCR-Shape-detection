# UAV-OCR-Shape-detection

Image recognition program for UAV Concordia. Goal is to classify characters and shapes.

## Prequisites:

- Python is installed
- VS code is installed
- Python extension from microsoft installed in VS code
- pip (python package manager) is installed

## Installation instructions on local machine (Mac OS)

1. Make sure your working directory is the project

```zsh
cd UAV-OCR-Shape-detection/
```

2. Install virtual environment

```zsh
pip install virtualenv
```

3. Create virtual environment

```zsh
python3 -m venv .venv
```

4. Activate virtual environment

```zsh
source .venv/bin/activate
```

5. Set your python interpreter to the one in the .venv

   1. Click the python interpreter at the bottom right
      ![](step5.0.png)
   2. Select the interpreter that's in the venv folder
      ![](step5.1.png)

6. Install the dependencies

```zsh
pip install --upgrade pip
```
```zsh
pip install -r requirements.txt
```

7. Install tesseract (pytesseract is just a wrapper, still needs the actual c++ code)
   1. Download the pkg installer based on the os you have https://www.macports.org/install.php
   2. Install tesseract with MacPorts
   ```zsh
   sudo port install tesseract
   ```
8. Press the play button at the top left of the python script you want to run and you should be good to go!

