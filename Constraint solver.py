#Note: Requires 'pip install python-constraint'

from constraint import AllDifferentConstraint, InSetConstraint, Problem

# variables
jobs       = "FA EA PA RO AC".split()
deskcolor = "Aqua Maroon Pink Cream Purple".split()
travel    = "Fiji France Canada Japan Thailand".split()
drinks     = "Peppermint GreenTea Chamomile EarlGrey EnglishBreakfast".split()
suburb    = "Brunswick, Werribee, Frankston, Oakleigh, StKilda".split(", ")

# There are five houses.
minn, maxn = 1, 5
problem = Problem()
# value of a variable is the number of a house with corresponding property
variables = jobs + deskcolor + travel + drinks + suburb
problem.addVariables(variables, range(minn, maxn+1))

# All jobs, colors, travel, drinks, and suburb are unique to each person
for vars_ in (jobs, deskcolor, travel, drinks, suburb):
    problem.addConstraint(AllDifferentConstraint(), vars_)

# RULE 4: The cream desk is to the left of the purple desk.
#NOTE: interpret it as 'cream desk number' < 'purple desk number'
problem.addConstraint(lambda a,b: a < b, ["Cream", "Purple"])

# RULE 8: In the middle desk the drink is Chamomile
#NOTE: interpret "middle" in a numerical sense (not geometrical)
problem.addConstraint(InSetConstraint([(minn + maxn) // 2]), ["Chamomile"])

# RULE 9: The leftmost desk's job is Financial analyst.
#NOTE: interpret "the first" as the desk number.
problem.addConstraint(InSetConstraint([minn]), ["FA"])


def add_constraints(constraint, statements, variables=variables, problem=problem):
    for stmt in (line for line in statements if line.strip()):
        problem.addConstraint(constraint, [v for v in variables if v in stmt])

#Rules 1, 2, 3, 5, 6, 7, 12, 13

and_statements = """
The jobs PA deskcolor is Pink
The jobs RO travel is Japan
The jobs EA drinks is GreenTea
The deskcolor Cream drinks is EarlGrey
The suburb Werribee travel is France
The deskcolor Maroon suburb is Brunswick
The suburb StKilda drinks is EnglishBreakfast
The jobs AC suburb is Frankston
""".split("\n")
add_constraints(lambda a,b: a == b, and_statements)

#Rules 10, 11, 14, 15
nextto_statements = """
The suburb Oakleigh is next to the travel Fiji
The travel Canada is next to the suburb Brunswick
The jobs FA is next to deskcolor Aqua
The suburb Oakleigh is next to the drinks Peppermint
""".split("\n")
#XXX: what is "next to"? (linear, circular, two sides, 2D house arrangment)
add_constraints(lambda a,b: abs(a - b) == 1, nextto_statements)

def solve(variables=variables, problem=problem):
    from itertools  import groupby
    from operator   import itemgetter

    # find & print solutions
    for solution in problem.getSolutionIter():
        for key, group in groupby(sorted(solution.items(), key=itemgetter(1)), key=itemgetter(1)):
            print(key), 
            for v in sorted(dict(group).keys(), key=variables.index):
                print(v.ljust(9)),
            print()

if __name__ == '__main__':
    solve()
