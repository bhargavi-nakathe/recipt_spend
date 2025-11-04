# Receipt Spending Classifier

A smart receipt processing system that classifies expenses and provides spending insights.

## Features
- 📷 Receipt image processing with OCR
- 🏷️ Automatic expense categorization
- 💰 Spending analytics and visualization
- 💡 Money-saving recommendations

## Quick Start

### Prerequisites
- Python 3.8+
- Tesseract OCR

### Installation

1. **Clone the repository**
# Receipt Spending Classifier

A smart receipt processing system that classifies expenses and provides spending insights.

## Features
- 📷 Receipt image processing with OCR
- 🏷️ Automatic expense categorization
- 💰 Spending analytics and visualization
- 💡 Money-saving recommendations

## Quick Start

### Prerequisites
- Python 3.8+
- Tesseract OCR

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd receipt-classifier
```

## Tesseract OCR (Windows)

This project uses Tesseract OCR via `pytesseract`. You must install the Tesseract binary on Windows and ensure the executable is accessible (either on PATH or configured in the app).

1) Install Tesseract (pick one):

	 - Using winget (recommended on Windows 10/11):

	 ```powershell
	 winget install UB-Mannheim.Tesseract
	 ```

	 - Using Chocolatey:

	 ```powershell
	 choco install tesseract
	 ```

	 - Or download the installer (UB Mannheim builds are common):
		 https://github.com/UB-Mannheim/tesseract/wiki

2) Verify Tesseract is available in a new PowerShell session:

```powershell
tesseract --version
# should print version info, e.g. 'tesseract 5.3.1'
```

3) If `tesseract` is not found after install, add the install folder to your PATH. Typical folder:

```
C:\Program Files\Tesseract-OCR\
```

Add that directory to your user PATH (Environment Variables → Path → Edit) and restart the terminal.

4) Advanced: Without modifying PATH you can set the executable path for this app before starting it. In PowerShell:

```powershell
# $env:TESSERACT_PATH = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
# then start the app in the same shell
D:/recipt_spend/.venv/Scripts/python.exe app.py
```

The code attempts to auto-detect `tesseract.exe` in PATH and common Program Files locations; if it still can't be found, follow the steps above.

If you want, I can add an explicit environment-variable check (TESSERACT_PATH) to the app so it honors $env:TESSERACT_PATH automatically — tell me and I'll add it.