props = {
    "A": -1,
    "B": 1,
    "C": -1,
    "D": -1,
    "E": 0
}

clauses = [["A", "B", "-C"], ["-E", "C"]]

def find_unit_clause(props, clauses):
    for clause in clauses:
        num_unsat = 0
        unknown = []
        for prop in clause:
            print(num_unsat, unknown)
            if "-" in prop:
                if props[prop.strip("-")] == -1:
                    break
                elif props[prop.strip("-")] != 0:
                    num_unsat += 1
            else:
                if props[prop] == 1:
                    break
                elif props[prop] != 0:
                    num_unsat += 1
            if props[prop.strip("-")] == 0:
                unknown.append(prop)
        if num_unsat == len(clause) - 1:
            if "-" in unknown[0]:
                return unknown[0], -1
            else:
                return unknown[0], 1
            
print(find_unit_clause(props, clauses))

