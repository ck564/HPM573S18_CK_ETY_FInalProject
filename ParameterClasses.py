from enum import Enum
import InputData as Data


class HealthStates(Enum):
    Well = 0
    Appendicitis_norup = 1
    Appendicitis_rup = 2
    PostAppendicitis = 3
    Cancer = 4
    Dead = 5


class Screening(Enum):
    US = 0  # Ultrasound
    CT = 1  # Computed Tomography


class ParametersFixed:
    def __init__(self, screening):

        self._screening = screening
        self._delta_t = Data.DELTA_T
        self._initialHealthState = HealthStates.Well

        # transition probability matrix
        self._prob_matrix = []

        # compose matrix depending selected screening
        if screening == Screening.US:
            self._prob_matrix = Data.TRANS_MATRIX_US
        if screening == Screening.CT:
            self._prob_matrix = Data.TRANS_MATRIX_CT

        # cost and utility matrix
        self._annualStateCosts = []
        self._annualStateUtilities = []

        # compose costs depending selected screening and utilities
        if screening == Screening.US:
            self._annualStateCosts = Data.COST_STATES_US
        if screening == Screening.CT:
            self._annualStateCosts = Data.COST_STATES_CT

        self._annualStateUtilities = Data.UTIL_STATES

        # screening costs
        if self._screening == Screening.US:
            self._screenCost = Data.COST_US
        if screening == Screening.CT:
            self._screenCost = Data.COST_CT

        # adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT_RATE * Data.DELTA_T

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        return self._annualStateUtilities[state.value]

    def get_screening_cost(self):
        return self._screenCost

    def get_adj_discount_rate(self):
        return self._adjDiscountRate
