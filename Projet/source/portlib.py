from datetime import date

import pandas as pd
import numpy as np

from typing import Union

NB_JOURS_ANNEE = 253  # Trading day https://en.wikipedia.org/wiki/Trading_day


def courbe_taux(date: float) -> float:
    date = date if date > 0 else 0.0001
    beta_0 = 0.0509387294135403
    beta_1 = -0.0300728704714689
    beta_2 = 0.0198996013841474
    beta_3 = -0.0834749661479616
    tau_0 = 0.109427785737843
    tau_1 = 0.241789711613793
    
    return beta_0 + beta_1 * ((1 - np.exp(-date / tau_0)) / (date / tau_0)) + beta_2 * (((1 - np.exp(-date / tau_0)) / (date / tau_0)) - np.exp(-date / tau_0)) + beta_3 * (((1 - np.exp(-date / tau_1)) / (date / tau_1)) - np.exp(-date / tau_1))


def discount_factor(t_0: int, grand_t: int) -> float:
    x = (1 + courbe_taux(grand_t))**grand_t
    y = (1 + courbe_taux(t_0))**(-t_0)
    return y/x


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

def rebase_df(df: pd.DataFrame, cm: bool = True) -> pd.DataFrame:
    """
    Rebasing values on 1. If cm is True it's comparing each day with the previous one, if it False it's comparing with the first day.
    """
    if cm:
        returns = df / df.shift(1)
    
        length = returns.shape[0]

        def rebase_series(serie: pd.Series) -> pd.Series:
            s = [0] * length
            s[0] = 1

            for i in range(1, length):
                s[i] = s[i - 1] * (serie[i] + 0 if cm else 1)
            return pd.Series(s)

        return returns.apply(lambda x: rebase_series(x), axis=0)
    else:
        returns = df / df.iloc[0]
        
        return returns.reset_index(drop=True)

def clean_df_time_series(df: pd.DataFrame, name: str = 'value', start_date: date = None) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date']).dt.date
    if start_date:
        df = df[df['date'] > start_date]
    return df.set_index('date').rename(columns={'value': name})

def garantie_max(nav):
    x = 1
    y = 0.85
    return max(y * np.max(nav), x)