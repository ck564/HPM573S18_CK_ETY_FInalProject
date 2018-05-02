import InputData as Data
import ParameterClasses as Parameters
import scr.EconEvalClasses as EconCls
import scr.RandomVariantGenerators as RndCls
import scr.StatisticalClasses as StatCls


class Patient:
    def __init__(self, id, parameters):

        self._id = id
        self._rng = None  # random number generated
        self._parameters = parameters
        self._stateMonitor = PatientStateMonitor(parameters)
        self._delta_t = parameters.get_delta_t()

    def simulate(self, sim_length):
        """ simulate patient over specified simulation length """

        # random number generated for patient
        self._rng = RndCls.RNG(self._id)

        k = 0  # current time step

        # while patient is alive and simulation length not yet reached
        while self._stateMonitor.get_if_alive() and k * self._delta_t < sim_length:

            # find the transition probabilities of the future states
            trans_probs = self._parameters.get_transition_prob(self._stateMonitor.get_current_state())
            # create empirical distribution
            empirical_dist = RndCls.Empirical(trans_probs)
            # sample from empirical distribution to get new state (returns an integer)
            new_state_index = empirical_dist.sample(self._rng)

            # update health state
            self._stateMonitor.update(k, Parameters.HealthStates(new_state_index))

            # increment time step
            k += 1

    def get_total_discounted_cost(self):
        return self._stateMonitor.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._stateMonitor.get_total_discounted_utility()


class PatientStateMonitor:

    def __init__(self, parameters):

        self._currentState = parameters.get_initial_health_state()
        self._delta_t = parameters.get_delta_t()

        # monitoring cost and utility outcomes
        self._costUtilityOutcomes = PatientCostUtilityMonitor(parameters)

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state

        """

        # update state of patient (if patient died, do nothing)
        if not self.get_if_alive():
            return

        # collect cost and utility outcomes
        self._costUtilityOutcomes.update(k, self._currentState, next_state)

        self._currentState = next_state

    def get_current_state(self):
        return self._currentState

    def get_if_alive(self):
        result = True
        if self._currentState in [Parameters.HealthStates.Dead]:
            result = False
        return result

    def get_total_discounted_cost(self):
        return self._costUtilityOutcomes.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._costUtilityOutcomes.get_total_discounted_utility()


class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        self._parameters = parameters
        self._totalDiscountedCost = 0  # total cost
        self._totalDiscountedUtility = 0  # total utility

    def update(self, k, current_state, next_state):

        # update cost
        cost = 0.5 * (self._parameters.get_annual_state_cost(current_state) +
                      (self._parameters.get_annual_state_cost(next_state))) * self._parameters.get_delta_t()

        # update utility
        utility = 0.5 * (self._parameters.get_annual_state_utility(current_state) +
                         (self._parameters.get_annual_state_utility(next_state))) * self._parameters.get_delta_t()

        # add cost of screening
        if current_state == Parameters.HealthStates.Well:
            cost += self._parameters.get_screening_cost()
        else:
            cost += 0

        # update total discounted cost and utility (corrected for half-cycle effect)
        self._totalDiscountedCost += \
            EconCls.pv(cost, self._parameters.get_adj_discount_rate() / 2, 2*k+1)
        self._totalDiscountedUtility += \
            EconCls.pv(utility, self._parameters.get_adj_discount_rate()/2, 2*k+1)

    def get_total_discounted_cost(self):
        return self._totalDiscountedCost

    def get_total_discounted_utility(self):
        return self._totalDiscountedUtility


class Cohort:

    def __init__(self, id, screening):
        """ create a cohort of patients """

        self._initial_pop_size = Data.POP_SIZE
        self._patients = []

        # populate cohort
        for i in range(self._initial_pop_size):
            # create a new patient
            patient = Patient(id * self._initial_pop_size + i, Parameters.ParametersFixed(screening))
            # add patient to cohort
            self._patients.append(patient)

    def simulate(self):

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from simulated cohort """

        self._costs = []
        self._utilities = []

        for patient in simulated_cohort.get_patients():

            # cost and utility
            self._costs.append(patient.get_total_discounted_cost())
            self._utilities.append(patient.get_total_discounted_utility())

        # summary statistics
        self._sumStat_cost = StatCls.SummaryStat('Patient discounted cost', self._costs)
        self._sumStat_utility = StatCls.SummaryStat('Patient discounted utility', self._utilities)

    def get_costs(self):
        return self._costs

    def get_utilities(self):
        return self._utilities

    def get_sumStat_discounted_cost(self):
        return self._sumStat_cost

    def get_sumStat_discounted_utility(self):
        return self._sumStat_utility
