import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# create and cohort without drug
cohort_US = MarkovCls.Cohort(
    id=0,
    screening=P.Screening.US)

simOutputs_US = cohort_US.simulate()


# create and simulate cohort with drug
cohort_CT = MarkovCls.Cohort(
    id=1,
    screening=P.Screening.CT)

simOutputs_CT = cohort_CT.simulate()


# report CEA results
SupportMarkov.report_CEA_CBA(simOutputs_US, simOutputs_CT)
