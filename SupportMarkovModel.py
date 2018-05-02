import InputData as Data
import scr.FormatFunctions as Format
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, screening):

    # mean and CI text of discounted total cost
    cost_mean_CI_text = Format.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Data.ALPHA),
        deci=2
    )

    # mean and CI text of discounted utility
    utility_mean_CI_text = Format.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Data.ALPHA),
        deci=2
    )

    # print outcomes
    print(screening)

    print(" Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Data.ALPHA, prec=0),
          cost_mean_CI_text)
    print(" Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Data.ALPHA, prec=0),
          utility_mean_CI_text)


def report_CEA_CBA(simOutputs_US, simOutputs_CT):

    # strategies
    strategy_US = Econ.Strategy(
        name='Ultrasound',
        cost_obs=simOutputs_US.get_costs(),
        effect_obs=simOutputs_US.get_utilities()
    )

    strategy_CT = Econ.Strategy(
        name='Computed Tomography',
        cost_obs=simOutputs_CT.get_costs(),
        effect_obs=simOutputs_CT.get_utilities()
    )

    # CEA
    CEA = Econ.CEA(
        strategies=[strategy_US, strategy_CT],
        if_paired=False
    )

    # report CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2
    )

    # CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label="Additional Discounted Utility",
        y_label='Additional Discounted Cost',
        show_names=True,
        show_legend=True,
        show_clouds=True,
        figure_size=6,
        transparency=0.3
    )
