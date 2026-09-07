# Source Code Tokenizer & Lexical Analyzer

A complete, interactive Academic Compiler Design project developed in Python using Streamlit. This application tokenizes programming source code (C/C++, Java, and Python) into a formatted token stream, displays statistics and interactive type distributions, and flags unknown lexical errors.

---

## 📖 Table of Contents
1. [How It Works](#⚙️-how-it-works)
2. [Features](#-features)
3. [Technologies Used](#-technologies-used)
4. [Project Architecture](#-project-architecture)
5. [Installation & Setup](#-installation--setup)
6. [Running the Application](#-running-the-application)
7. [Example Output](#-example-output)
8. [Future Improvements](#-future-improvements)


## ⚙️ How It Works

The Tokenizer loops sequentially through the characters of the source code. At each cursor position to process:
1. **Whitespace Scanning:** It skips whitespaces, counts newlines `\n` to advance line numbers, and tracks column alignment.
2. **Deterministic Rules Matching:** It iterates through the ordered rule patterns. If a pattern matches *exactly* at the current character offset (`pattern.match(code, pos)`), the matched substring is extracted.
3. **Keyword Validation:** If the token is classification `IDENTIFIER`, the lexer checks if it belongs to the configured **Keywords set**. If yes, it is reclassified as `KEYWORD`.
4. **Error Isolation:** If no pattern matches, the char is recorded as an `UNKNOWN` token type and pushed to a separate lexical errors list.
5. **Preserving Context:** Both correct tokens and errors keep line and column location metadata.

---

## 🌟 Features

* **Dual Input Modes:** Upload a code file (`.c`, `.cpp`, `.java`, `.py`, `.txt`) or paste directly into the paste card editor.
* **Configurable Keywords:** Edit the comma-separated keywords list on the sidebar to adapt tokenization instantly.
* **Preserved Line and Column Offsets:** Track coordinates for every token, critical for compiler diagnostic purposes.
* **Extended Multi-Language Parsers:** Out-of-the-box configurations for C/C++, Java, and Python.
* **Analytical Dashboard:** View statistics cards for Keywords, Identifiers, Operators, Numbers, Comments, and Errors.
* **Visual Token Distribution:** Display interactive plotly bar charts illustrating frequency counts of each token type.
* **Tabular Search & Filter:** Filter tokens easily via live keyword typing.
* **CSV & TXT Downloader:** Export token streams to spreadsheet formats and readable text streams.

---

## 💻 Technologies Used

* **Python 3** (Core logic and patterns)
* **Streamlit** (Interactive frontend dashboard)
* **Plotly** (Dynamic graphical charts)
* **Pandas** (Dataframe structures for tables)
* **Pytest** (Automated unit tests)

---

## 📁 Project Architecture

```text
source-code-tokenizer/
│
├── app.py                     # Streamlit frontend application
│
├── tokenizer/                 # Tokenizer Module
│   ├── __init__.py            # Exposes core classes (Tokenizer, Token)
│   ├── tokenizer.py           # Lexer engine implementation
│   ├── token.py               # Token class with coordinate attributes
│   ├── patterns.py            # Language regex rules in match priority order
│   ├── keywords.py            # Static keyword storage lists
│   └── errors.py              # Lexical error tracking class
│
├── utils/                     # Utility Helper Functions
│   ├── __init__.py
│   ├── file_handler.py        # Reading uploads/local files with fallback encodings
│   └── exporter.py            # Formatted CSV and TXT writing utility
│
├── tests/                     # Automated Test Suites
│   ├── test_tokenizer.py      # Core parser structure tests
│   ├── test_numbers.py        # Int, float, scientific notation tests
│   ├── test_strings.py        # String, character, multiline quotes tests
│   ├── test_comments.py       # Single-line, multi-line comment inclusion tests
│   └── test_operators.py      # Double operator longest-match tests
│
├── sample_code/               # Prepared Input Demonstrators
│   ├── sample.c
│   ├── sample.cpp
│   └── sample.java
│
├── requirements.txt           # External project dependencies
├── README.md                  # Comprehensive Documentation & Viva guide
└── .gitignore                 # Untracked files list
```

---

## 💽 Installation & Setup

1. **Clone or Navigate to the project folder:**
   ```bash
   cd "CD Project"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   * **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   * **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

5. **Install all required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Application

### 1. Launch the Streamlit Dashboard
To run the interactive compiler UI:
```bash
streamlit run app.py
```
This command spins up a local server. A browser window will automatically open (usually at `http://localhost:8501`).

### 2. View and Run Unit Tests
To execute the suite of unit tests verifying lexer behavior:
```bash
pytest
```
*You should see all test assertions pass successfully!*

---

## 📋 Example Output

For the following input code:
```c
int main() {
    int sum = 10 + 20;
    return 0;
}
```

The exported **TXT Token Stream** is formatted as:
```text
Line     Token Type                Lexeme
1        KEYWORD                   int
1        IDENTIFIER                main
1        LEFT_PAREN                (
1        RIGHT_PAREN               )
1        LEFT_BRACE                {
2        KEYWORD                   int
2        IDENTIFIER                sum
2        ASSIGNMENT_OPERATOR       =
2        INTEGER                   10
2        ARITHMETIC_OPERATOR       +
2        INTEGER                   20
2        SEMICOLON                 ;
3        KEYWORD                   return
3        INTEGER                   0
3        SEMICOLON                 ;
4        RIGHT_BRACE               }
```

---

## 🔮 Future Improvements

For a thesis or further academic upgrades on top of this analyzer:
1. **Abstract Syntax Tree (AST) Generation:** Integrate a parser using grammar specifications (LL/LR parsers) to generate syntax trees.
2. **Syntax Error Detection:** Validate matching brackets, braces, and missing semicolons in addition to lexical scanner errors.
3. **Symbol Table Module:** Map declared variables, tracking their scope, memory offset, and data type.
4. **Intermediate Code Generation (ICG):** Output three-address code (TAC) representations for compilation backends.
5. **Interactive Flowchart Node Graph:** Display a DAG (Directed Acyclic Graph) of program flow within Streamlit.
