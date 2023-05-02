import csv

prob_cold = [0.95, 0.05]
prob_cat = [0.98, 0.02]
prob_allergic_reaction_given_cat = {
    (0, 0): 0.95, (0, 1): 0.25, (1, 0): .05, (1, 1): 0.75}
prob_sneeze_given_cold_allergic_reaction = {(0, 0, 0): .99, (1, 0, 0): .01, (
    0, 0, 1): 0.30, (1, 0, 1): .70, (0, 1, 0): .2, (1, 1, 0): .8, (0, 1, 1): .1, (1, 1, 1): .9}
prob_scratches_given_cat = {
    (0, 0): 0.95, (0, 1): 0.50, (1, 0): .05, (1, 1): 0.50}

joint_probabilities = []

for cold in range(2):
    for cat in range(2):
        for allergy in range(2):
            for sneeze in range(2):
                for scratches in range(2):
                    joint_probability = (
                        prob_cold[cold]
                        * prob_cat[cat]
                        * prob_allergic_reaction_given_cat[(allergy, cat)]
                        * prob_sneeze_given_cold_allergic_reaction[(sneeze, cold, allergy)]
                        * prob_scratches_given_cat[(scratches, cat)]
                    )
                    joint_probabilities.append(
                        (
                            cold,
                            sneeze,
                            allergy,
                            scratches,
                            cat,
                            joint_probability,
                        )
                    )

with open('jpt.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    header = ["Cold", "Sneeze", "Allergy", "Scratch", "Cat", "Joint_Prob"]
    csv_writer.writerow(header)

    for entry in joint_probabilities:
        csv_writer.writerow(list(entry[:-1]) + [format(round(entry[-1], 6), '.6f')])
