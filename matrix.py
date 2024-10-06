import os
import re  # Make sure to import the re module

class SparseMatrix:
    """
    Represents a sparse matrix.
    """

    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols
        self.elements = {}  # Initialize the elements dictionary

    @classmethod
    def from_file(cls, matrix_file_path):
        ...
        
        try:
            with open(matrix_file_path, "r") as file:
                lines = file.readlines()

            if len(lines) < 2:
                raise ValueError(
                    f"File {matrix_file_path} does not contain enough lines for matrix dimensions"
                )

            # Parse dimensions
            row_match = re.match(r'rows=(\d+)', lines[0].strip())  # Use re.match()
            col_match = re.match(r'cols=(\d+)', lines[1].strip())  # Use re.match()

            if not row_match or not col_match:
                raise ValueError(
                    f"Invalid dimension format in file {matrix_file_path}. Expected 'rows=X' and 'cols=Y'"
                )

            total_rows = int(row_match[1])
            total_cols = int(col_match[1])

            sparse_matrix = cls(total_rows, total_cols)

            # Parse elements
            for i in range(2, len(lines)):
                line = lines[i].strip()
                if line == "":
                    continue  # Skip empty lines

                match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                if not match:
                    raise ValueError(
                        f"Invalid format at line {i + 1} in file {matrix_file_path}: {line}"
                    )

                row = int(match[1])
                col = int(match[2])
                value = int(match[3])

                sparse_matrix.set_element(row, col, value)

            return sparse_matrix
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {matrix_file_path}")
        except Exception as e:
            raise e

    def get_element(self, row, col):
        """
        Retrieves the value of an element at a specific row and column.

        :param row: The row index of the element.
        :param col: The column index of the element.
        :return: The value at the specified position, or 0 if not set.
        """
        key = (row, col)
        return self.elements.get(key, 0)  # Return the value or 0 if not found

    def set_element(self, row, col, value):
        """
        Sets the value of an element at a specific row and column.

        :param row: The row index where the value should be set.
        :param col: The column index where the value should be set.
        :param value: The value to set at the specified position.
        """
        if row >= self.rows:
            self.rows = row + 1  # Update rows if needed
        if col >= self.cols:
            self.cols = col + 1  # Update columns if needed

        key = (row, col)
        self.elements[key] = value  # Set the value in the dictionary

    # Rest of your class methods remain unchanged...

    def add(self, other):
        """
        Adds two sparse matrices.

        :param other: The other SparseMatrix to add.
        :return: A new SparseMatrix that is the sum of the two matrices.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = SparseMatrix(self.rows, self.cols)

        # Add elements from the first matrix
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)

        # Add elements from the second matrix
        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value + value)

        return result

    def subtract(self, other):
        """
        Subtracts one sparse matrix from another.

        :param other: The other SparseMatrix to subtract.
        :return: A new SparseMatrix that is the result of the subtraction.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result = SparseMatrix(self.rows, self.cols)

        # Subtract elements from the second matrix from the first matrix
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)

        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value - value)

        return result

    def multiply(self, other):
        """
        Multiplies two sparse matrices.

        :param other: The other SparseMatrix to multiply.
        :return: A new SparseMatrix that is the product of the two matrices.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns of first matrix must equal number of rows of second matrix.")

        result = SparseMatrix(self.rows, other.cols)

        # Multiply matrices
        for (row, col), value in self.elements.items():
            for k in range(other.cols):
                other_value = other.get_element(col, k)
                if other_value != 0:
                    current_value = result.get_element(row, k)
                    result.set_element(row, k, current_value + value * other_value)

        return result

    def __str__(self):
        """
        Converts the SparseMatrix to a string representation.

        :return: The string representation of the SparseMatrix.
        """
        result = f"rows={self.rows}\ncols={self.cols}\n"
        for key, value in self.elements.items():
            result += f"({key[0]}, {key[1]}, {value})\n"
        return result.strip()  # Return trimmed string

    def save_to_file(self, file_path):
        """
        Saves the SparseMatrix to a file.

        :param file_path: The path to save the matrix file.
        """
        content = str(self)  # Get string representation
        with open(file_path, "w") as file:
            file.write(content)  # Write to file

def performCalculations():
    """
    Performs a matrix operation based on user input.
    """
    try:
        # Define available operations
        matrix_operations = {
            '1': {"name": "addition", "method": "add"},
            '2': {"name": "subtraction", "method": "subtract"},
            '3': {"name": "multiplication", "method": "multiply"},
        }

        # Display the operations menu
        print("Available operations:")
        for key, operation in matrix_operations.items():
            print(f"{key}: {operation['name']}")

        matrix_file_path1 = input("Enter the file path for the first matrix: ")
        matrix1 = SparseMatrix.from_file(matrix_file_path1)
        print("First matrix loading........\n")

        matrix_file_path2 = input("Enter the file path for the second matrix: ")
        matrix2 = SparseMatrix.from_file(matrix_file_path2)
        print("Second matrix loading.......\n")

        operation_choice = input("Choose an operation (1, 2, or 3): ")
        operation = matrix_operations.get(operation_choice)

        if not operation:
            raise ValueError("Invalid operation choice.")

        result_matrix = getattr(matrix1, operation["method"])(matrix2)
        print(f"Output of {operation['name']}........\n")

        output_file_path = input("Enter the file path to save the result: ")
        result_matrix.save_to_file(output_file_path)
        print(f"Output file saved to {output_file_path}")

    except Exception as error:
        print("Error:", error)

# Run the matrix operation function
performCalculations()
