import pandas as pd
import numpy as np

from typing import Union

NB_JOURS_ANNEE = 253  # Trading day https://en.wikipedia.org/wiki/Trading_day


def get_rendements(nav: Union[pd.Series, list], benchmark: Union[pd.Series, list]) -> pd.DataFrame:
    """
    Get rendements for the NAV and the benchmark on usuals times interval.
    """
    df_rendement = pd.DataFrame(columns=['3M', '6M', '1Y', '3Y', 'ALL'])

    # NAV
    T_nav = len(nav) - 1
    
    df_rendement.loc["NAV"] = {
        "ALL": (nav[T_nav]/nav[0]) - 1,
        "3Y": (nav[T_nav]/nav[T_nav - 3 * NB_JOURS_ANNEE]) - 1,
        "1Y": (nav[T_nav]/nav[T_nav - NB_JOURS_ANNEE]) - 1,
        "6M": (nav[T_nav]/nav[round(T_nav - 4.345 * 6 * 6)]) - 1,
        "3M": (nav[T_nav]/nav[round(T_nav - 4.345 * 3 * 5)]) - 1,
    }

    df_rendement.loc["NAV Annualisé"] = {
        "ALL": (nav[T_nav]/nav[0])**(NB_JOURS_ANNEE/(T_nav)) - 1,
        "3Y": (nav[T_nav]/nav[T_nav - 3 * NB_JOURS_ANNEE])**(NB_JOURS_ANNEE/(3*NB_JOURS_ANNEE)) - 1,
        "1Y": (nav[T_nav]/nav[T_nav - NB_JOURS_ANNEE])**(NB_JOURS_ANNEE/NB_JOURS_ANNEE) - 1,
        "6M": (nav[T_nav]/nav[round(T_nav - 4.345 * 6 * 6)])**(NB_JOURS_ANNEE/(4.345 * 6 * 5)) - 1,
        "3M": (nav[T_nav]/nav[round(T_nav - 4.345 * 3 * 5)])**(NB_JOURS_ANNEE/(4.345 * 3 * 5)) - 1,
    }

    # Benchmark
    T_benchmark = len(benchmark) - 1
    
    df_rendement.loc["Benchmark"] = {
        "ALL": (benchmark[T_benchmark]/benchmark[0]) - 1,
        "3Y": (benchmark[T_benchmark]/benchmark[T_benchmark - 3 * NB_JOURS_ANNEE]) - 1,
        "1Y": (benchmark[T_benchmark]/benchmark[T_benchmark - NB_JOURS_ANNEE]) - 1,
        "6M": (benchmark[T_benchmark]/benchmark[round(T_benchmark - 4.345 * 6 * 6)]) - 1,
        "3M": (benchmark[T_benchmark]/benchmark[round(T_benchmark - 4.345 * 3 * 5)]) - 1,
    }

    df_rendement.loc["Benchmark Annualisé"] = {
        "ALL": (benchmark[T_benchmark]/benchmark[0])**(NB_JOURS_ANNEE/(T_benchmark)) - 1,
        "3Y": (benchmark[T_benchmark]/benchmark[T_benchmark - 3 * NB_JOURS_ANNEE])**(NB_JOURS_ANNEE/(3*NB_JOURS_ANNEE)) - 1,
        "1Y": (benchmark[T_benchmark]/benchmark[T_benchmark - NB_JOURS_ANNEE])**(NB_JOURS_ANNEE/NB_JOURS_ANNEE) - 1,
        "6M": (benchmark[T_benchmark]/benchmark[round(T_benchmark - 4.345 * 6 * 6)])**(NB_JOURS_ANNEE/(4.345 * 6 * 5)) - 1,
        "3M": (benchmark[T_benchmark]/benchmark[round(T_benchmark - 4.345 * 3 * 5)])**(NB_JOURS_ANNEE/(4.345 * 3 * 5)) - 1,
    }

    return df_rendement


def get_vol(nav_rendement: Union[pd.Series, list], benchmark_rendement: Union[pd.Series, list]):
    """
    Get annualized volatiliy for the NAV and the Benchmark
    """
    df_vol = pd.DataFrame(columns=['Vol. Annualisé'])

    # NAV
    T_nav = len(nav_rendement) - 1
    
    r_barre = np.mean(nav_rendement)
    vol_port = (1 / (T_nav - 1)) * sum([(r - r_barre)**2 for r in nav_rendement])
    df_vol.loc["NAV"] = vol_port * np.sqrt(NB_JOURS_ANNEE)

    # Benchmark
    T_benchmark = len(benchmark_rendement) - 1
    
    b_barre = np.mean(benchmark_rendement)
    vol_benchmark = (1 / (T_benchmark - 1)) * sum([(bb - b_barre)**2 for bb in benchmark_rendement])
    df_vol.loc["Benchmark"] = vol_benchmark * np.sqrt(NB_JOURS_ANNEE)

    return df_vol