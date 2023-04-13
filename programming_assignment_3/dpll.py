import sys
import copy

# Define constants
count = 0
uch = False


class Model:
    """Represents a Model which has some clauses and propositions. Strictly speaking,
    this is not the definition of a propositional 'model' which we talked about in class since
    it also holds the propositions, but it was easier to package everything in this one class."""

    def __init__(self, filename, values=None) -> None:
        """By default, the Model is initialized to have all propositions (represented by
        a dictionary) set to unknown (0). If the user specified a certain value in the command
        line argument, we set that proposition to the specified value. Each model also has a 
        list of each clause."""

        self.props = {}
        self.clauses = []

        # Read the KB from the *.cnf file specified
        with open(filename, "r") as cnf:
            for line in cnf.readlines():
                if line == '\n':
                    continue
                line_props = line.split(" ")
                # Removes newline character
                line_props[-1] = line_props[-1].strip()

                line_props_temp = []
                for prop in line_props:
                    if prop == " " or prop == "":
                        continue
                    elif "#" in prop:
                        break
                    else:
                        line_props_temp.append(prop.replace(" ", ""))

                if len(line_props_temp) > 0:
                    self.clauses.append(line_props_temp)
                for prop in line_props_temp:
                    # Redundant check but whatever
                    if prop.strip("-") not in self.props.keys():
                        self.props[prop.strip("-")] = 0

        if values != None:
            for val in values:
                # This condition is ubiquitous throughout the program. If the proposition
                # specified is negated, then we must make the truth value for the proposition
                # in the dictionary FALSE (-1), this is because we do not store the state of
                # each negated literal, just the naked literal.
                if "-" in val:
                    self.props[val.strip("-")] = -1
                else:
                    self.props[val] = 1

    def __str__(self) -> str:
        """Prints the state of each proposition, one on each line."""

        ret = ''
        for prop in self.props:
            ret += prop + ": " + str(self.props[prop]) + "\n"
        return ret

    def print_true(self) -> str:
        """Prints only the satisfied propositions, all one one line."""

        ret = 'just the Satisfied (true) propositions:\n'
        for prop in self.props:
            if self.props[prop] == 1:
                ret += prop + " "

        return ret


def find_unit_clause(model):
    """For each clause in a model, find the first unit clause (if one exists)
    and return the literal and the appropriate value to set it to in
    order to satisfy the unit clause as a tuple."""

    for clause in model.clauses:
        # Represents the number of unsatisfied propositions in a clause
        num_unsat = 0
        # A list of all the unknown (0 value) propositions in a clause
        unknown = []
        for prop in clause:
            # If at least one proposition in the clause is true, then we break
            # since the clause is not unit. However, the clause is unsatisfied,
            # we increment num_unsat and continue checking all props in the clause.
            if "-" in prop:
                if model.props[prop.strip("-")] == -1:
                    break
                elif model.props[prop.strip("-")] != 0:
                    num_unsat += 1
            else:
                if model.props[prop] == 1:
                    break
                elif model.props[prop] != 0:
                    num_unsat += 1
            if model.props[prop.strip("-")] == 0:
                unknown.append(prop)
        # After checking all props in the clause, if the number of unsatisfied propositions
        # is one less than total number of clauses, then we know there must be exactly
        # one unknown proposition (this is the only way a proposition is added to the unknown
        # list). Then, we set this proposition to TRUE (or FALSE) based on whether or not it
        # is negated. This will make the unit clause true.
        if num_unsat == len(clause) - 1 and len(unknown) == 1:
            if "-" in unknown[0]:
                return unknown[0], -1
            else:
                return unknown[0], 1
    return None, None


def all_clauses_true(model):
    """Checks if all clauses in a Model's list of clauses are true. Returns
    True if they are, and False otherwise."""

    for clause in model.clauses:
        contains_true = False
        for prop in clause:
            if "-" in prop:
                if model.props[prop.strip("-")] == -1:
                    contains_true = True
                    break
            else:
                if model.props[prop] == 1:
                    contains_true = True
                    break
        # Once we find a clause that is false, return False
        if not contains_true:
            return False
    return True


def some_clause_false(model):
    """Returns True if at least one clause in a Model's list of clauses is False,
    and returns False if none of the clauses are false."""

    for clause in model.clauses:
        all_false = True
        for prop in clause:
            if model.props[prop.strip("-")] == 0:
                all_false = False
                break
            if "-" in prop:
                if model.props[prop.strip("-")] == -1:
                    all_false = False
                    break
            else:
                if model.props[prop] == 1:
                    all_false = False
                    break
        if all_false:
            return True
    # Fail safe, should never reach this point
    return False


def dpll(model, var, value):
    """The main DPLL function. Based on Figure 7.7 from the Textbook. Note, the parameters
    are slightly different than in the book's implementation. Here, all of the clauses, propositions,
    and corresponding values are stored in a Model object. In our implementation, 'var' and 'value'
    represents the proposition that was changed in the most recent call as well as the truth value
    it was set to (this allows us to print which variable/value we are 'trying' at any step)."""

    global uch, count

    if var == "":
        print("model: ")
        print(model.props)
    else:
        print("trying " + var + "=" + value)
        print(model.props)

    # Each time DPLL is called, increment count
    count += 1

    if all_clauses_true(model):
        print("solution:")
        print(model)
        print(model.print_true())
        return True
    if some_clause_false(model):
        print("backtracking")
        return False
    # In the case where +UCH is specified, use this heuristic
    if uch:
        prop, value = find_unit_clause(model)
        if prop is not None:
            mdl_UC = copy.deepcopy(model)
            if "-" in prop:
                mdl_UC.props[prop.strip("-")] = -1
                return dpll(mdl_UC, prop.strip("-"), "F")
            else:
                mdl_UC.props[prop] = 1
                return dpll(mdl_UC, prop, "T")

    p = 0
    for prop in model.props:
        if model.props[prop] == 0:
            p = prop
            break

    # Once we find the next unknown value in the CURRENT model (the model passed in),
    # we make two DEEP copies of the CURRENT model. In one of them, set the value of
    # the appropriate proposition to FALSE and in the other, set the value to TRUE. Then,
    # call DPLL on BOTH of them to determine which one potentially satisfies the constraints.
    mdl_T = copy.deepcopy(model)
    mdl_T.props[p] = 1

    mdl_F = copy.deepcopy(model)
    mdl_F.props[p] = -1

    return dpll(mdl_T, p, "T") or dpll(mdl_F, p, "F")


def main():
    """Main function. Parse user arguments, call DPLL, etc."""

    global count, uch

    args = sys.argv[1:]
    literals = []
    filename = ""
    uch = False

    # Not very thorough in error checking here
    if len(args) == 1 and args[0] == "-h":
        print("usage: python3 DPLL.py <filename> <literal>* [+UCH]")
    elif ".cnf" not in args[0]:
        print("Error: must specify .cnf file")
    elif len(args) >= 1:
        filename = args[0]
        for arg in args[1:]:
            if arg == "+UCH":
                uch = True
                break
            literals.append(arg)

    mdl = None
    if len(literals) != 0:
        mdl = Model(filename, literals)
    else:
        mdl = Model(filename)

    # If the model is not satisfiable, print "unsatisfiable"
    if not dpll(mdl, "", None):
        print("Unsatisfiable")
    print("total DPLL calls:", count)
    print("UCH=" + str(uch))


if __name__ == "__main__":
    main()
