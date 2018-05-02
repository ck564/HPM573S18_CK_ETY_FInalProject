import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# create a cohort for ultrasound
cohort = MarkovCls.Cohort(
    id=0,
    screening=P.Screening.US)

simOutputs = cohort.simulate()


# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs, 'Ultrasound:')


# print(simOutputs.get_costs())
