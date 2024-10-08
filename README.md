
# Simple Language Compiler for Kids

This project is a simple compiler for a language designed to help kids create calculator programs. The language is heavily inspired by Pascal but with limited keywords for simplicity, making it ideal for beginner programmers.

## Features

- **Supported Keywords**:
  - `var`: Variable declaration
  - `for`: Looping construct
  - `read`: Reading user input
  - `write`: Outputting values to the console
  - `to`, `do`, `endfor`: Loop control
- **Arithmetic Operations**: Supports addition, subtraction, multiplication, and division.
- **Variable Assignment**: Assign values to variables using `:=`.
- **Simple Compiler**: The compiler parses, compiles, and executes code directly.

## Example Program

Here’s an example of a simple program written in this language:

```pascal
var x, y;
read(x);
read(y);
write(x + y);
```

## Project Structure

- **`Tokenizer.py`**: Responsible for tokenizing the input source code.
- **`Parser.py`**: Parses the tokens generated by the tokenizer and builds the abstract syntax tree (AST).
- **`Compiler.py`**: Translates the AST into executable code.
- **`main.py`**: Entry point for running the compiler.
- **`sum.sm`**: Example source file containing code to test.

## Requirements

- **Python 3.x** is required to run this project.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Jacob-Vu/sumolang.git
   cd sumolang
   ```

2. Ensure you have Python installed on your system. You can download it [here](https://www.python.org/downloads/).

3. Install any necessary Python dependencies (if any, such as `argparse`, etc.). You can use `pip` to install them:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run a program written in the simple language, follow these steps:

1. Write your code in a `.sm` file (e.g., `sum.sm`).
2. Compile and execute the program using the following command:

   ```bash
   python main.py sum.sm
   ```

This will compile the code in `sum.sm` and execute it, displaying any output to the console.

### Example

Here’s how you can run the `sum.sm` file:

```bash
python main.py sum.sm
```

If the file contains the following code:

```pascal
var x, y;
read(x);
read(y);
write(x + y);
```

The program will prompt you to input two values and output their sum.

## How It Works

- **Tokenizer**: Breaks the input code into tokens (keywords, operators, numbers, etc.).
- **Parser**: Takes the tokens and constructs an Abstract Syntax Tree (AST).
- **Compiler**: Translates the AST into executable code or directly interprets it for execution.

## Future Improvements

- Support for more complex expressions and control structures (e.g., `if`, `while`).
- Error handling and reporting improvements.
- A graphical interface for kids to write and run their programs more easily.
- Self-executable compiled files instead of interpreted execution.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests if you’d like to improve the project.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
