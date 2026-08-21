# Source Code Tokenizer & Lexical Analyzer

A complete, interactive Academic Compiler Design project developed in Python using Streamlit. This application tokenizes programming source code (C/C++, Java, and Python) into a formatted token stream, displays statistics and interactive type distributions, and flags unknown lexical errors.

---

## 📖 Table of Contents
1. [Academic Explanation & Viva Prep](#-academic-explanation--viva-prep)
2. [How It Works](#⚙️-how-it-works)
3. [Features](#-features)
4. [Technologies Used](#-technologies-used)
5. [Project Architecture](#-project-architecture)
6. [Installation & Setup](#-installation--setup)
7. [Running the Application](#-running-the-application)
8. [Example Output](#-example-output)
9. [Future Improvements](#-future-improvements)

---

## 🎓 Academic Explanation & Viva Prep

This project is tailored for System Programming and Compiler Design laboratories. Below are the key interview (viva-voce) questions explained in beginner-friendly language:

### What is Lexical Analysis?
Lexical analysis is the **first phase of a compiler**. Its main job is to scan the characters of the source code from left to right and group them into logical sequences called *lexemes*.

### What is a Lexer (or Tokenizer)?
A **lexer** is the module/program that performs lexical analysis. It takes raw text as input, removes whitespace and comments, and produces a structured stream of tokens.

### What is a Token?
A **token** is an abstract category of lexical elements. It acts as an identifier for syntax analysis (parsing). Examples: `KEYWORD`, `IDENTIFIER`, `INTEGER`, `ARITHMETIC_OPERATOR`, `SEMICOLON`.

### What is a Lexeme?
A **lexeme** is the actual concrete text string in the source code that matches the pattern of a token.
* *Example:* In `int count = 10;`, the string `int` is a lexeme matching token `KEYWORD`, and the string `count` is a lexeme matching token `IDENTIFIER`.

### What is a Token Stream?
A **token stream** is the ordered sequence of tokens produced by the lexer. This stream is passed directly to the next phase of the compiler: the **Syntax Analyzer (Parser)** to build the Abstract Syntax Tree (AST).

### Why are Regular Expressions (Regex) used?
Regular expressions are mathematical representations of regular languages. Since programming language tokens can be defined using regular grammars (represented by Regular Expressions), we can use regex patterns to efficiently match and categorize characters into lexemes.

### What is the Longest-Match Principle (Maximal Munch)?
When scanning source code, if multiple regex patterns match the input text, the lexer must choose the pattern that matches the **longest sequence of characters**.
* *Example:* For the lexeme `>=`, if the lexer did not follow the longest-match principle, it might split it into `>` (relational operator) and `=` (assignment operator). Standard lexers ensure `>=` is recognized as a single relational operator.
* *How it's solved here:* Patterns are carefully sorted and compiled so that multi-character operators (e.g. `++`, `>=`, `&&`, `||`) are matched first, followed by single-character options (e.g. `+`, `>`, `&`, `|`).

### How are Lexical Errors handled?
A lexical error occurs when the character sequence cannot be matched to any valid token pattern of the programming language.
* *Example:* In `int x = 10 @ 20;`, the character `@` is not valid in C.
* *Handling:* The tokenizer categorizes it as `UNKNOWN`, reports a descriptive message, and continues tokenization. It logs the line, column, and character to prevent compiler crash.

---

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
