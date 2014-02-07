

"""
Formulae for calculating DraftScores
"""
def kdascore(k, d, a, role):
    if role in ('top', 'mid', 'adc'):
        score = 0.5 * ((2 * k + a) / (d + 10))
    elif role == 'jungle':
        score = 0.5 * ((2 * k + 2 * a) / (d + 10))
    elif role == 'support':
        score = 0.5 * ((1.5 * k + 2 * a) / (d + 10))
    return score

def partscore(k, a, tk):
    if tk == 0:
        return 0
    score = (k + a) / tk

    return score

def goldscore(gold, oppgold, gamegold):
    score = 5 * (2 * gold - oppgold) / gamegold
    return score

def csscore(cs, oppcs, role):
    if role in ('top', 'jungle', 'mid'):
        score = cs / (200 + oppcs)
    elif role in ('adc', 'support'):
        score = cs / (75 + oppcs)
    return score

def winscore(win):
    if win == 1:
        score = 0.2
    else:
        score = 0
    return score

def deathscore(d):
    if d == 0:
        score = 0.2
    else:
        score = 0
    return score

scoreformuladict = {
    'kdascore': kdascore,
    'partscore': partscore,
    'goldscore': goldscore,
    'csscore': csscore,
    'winscore': winscore,
    'deathscore': deathscore,
}