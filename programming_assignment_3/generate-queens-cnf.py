def generate_n_queens_cnf(n):
    # Changes from 0-based indexing to 1-base indexing
    def var(i, j):
        return f"Q{i + 1}{j + 1}"

    # Writes all clauses on one single line, separated by spaces
    def write_clauses(clauses):
        return "\n".join(" ".join(clause) for clause in clauses)

    with open(f"{n}-queens.cnf", "w") as file:
        # At least one queen in a row
        file.write("# At least one queen in each row\n")
        for row in range(n):
            row = [var(row, j) for j in range(n)]
            file.write(write_clauses([row]))
            file.write("\n")

        file.write("\n")

        # At least one queen in a column
        file.write("# At least one queen in each column\n")
        for col in range(n):
            col = [var(i, col) for i in range(n)]
            file.write(write_clauses([col]))
            file.write("\n")

        file.write("\n")

        # At most one queen in a row or column
        file.write("# At most one queen in each column/row\n")
        for row in range(n):
            for col in range(n):
                for k in range(col + 1, n):
                    file.write(f"-{var(row, col)} -{var(row, k)}\n")
                    file.write(f"-{var(col, row)} -{var(k, row)}\n")

        file.write("\n")

        # At most one queen on each diagonal
        file.write("# At most one queen in each diagonal\n")
        for row in range(n):
            for col in range(n):
                for k in range(1, n):
                    if row + k < n and col + k < n:
                        file.write(f"-{var(row, col)} -{var(row + k, col + k)}\n")
                    if row + k < n and col - k >= 0:
                        file.write(f"-{var(row, col)} -{var(row + k, col - k)}\n")
                    if row - k >= 0 and col + k < n:
                        file.write(f"-{var(row, col)} -{var(row - k, col + k)}\n")
                    if row - k >= 0 and col - k >= 0:
                        file.write(f"-{var(row, col)} -{var(row - k, col - k)}\n")



n = int(input("Enter the number of queens: "))
generate_n_queens_cnf(n)
