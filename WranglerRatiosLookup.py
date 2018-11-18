def tj_auto_trans_ratios():
    tj_automatic_transmission_ratio = [
        2.21,  #reverse
        2.84  #1st

    ]
def jk_2012_auto_trans_ratios():
    jk_automatic_transmission_ratio = [
        3.16,  # reverse
        3.59,  # 1st
        2.19,  # 2nd
        1.41,  # 3rd
        1.0,  # 4th
        0.83,  # 5th
    ]
    return jk_automatic_transmission_ratio


def jk_2012_manual_trans_ratios():
    jk_manual_transmission_ratio = [
        4.06,  # reverse
        4.46,  # 1st
        2.61,  # 2nd
        1.72,  # 3rd
        1.25,  # 4th
        1.0,  # 5th
        0.797,  # 6th
    ]
    return (jk_manual_transmission_ratio)

def jk_2007_auto_trans_ratios():
    jk_automatic_transmission_ratio = [
        2.21,  # reverse
        2.84,  # 1st
        1.57,  # 2nd
        1.00,  # 3rd
        0.69,  # 4th
    ]
    return jk_automatic_transmission_ratio


def jk_2007_manual_trans_ratios():
    jk_manual_transmission_ratio = [
        4.06,  # reverse
        4.46,  # 1st
        2.61,  # 2nd
        1.72,  # 3rd
        1.25,  # 4th
        1.0,  # 5th
        0.84,  # 6th
    ]
    return (jk_manual_transmission_ratio)


def jl_automatic_trans_ratios():
    jl_automatic_transmission_ratio = [
        3.30,  # reverse
        4.71,  # 1st
        3.14,  # 2nd
        2.10,
        1.67,
        1.29,
        1.00,
        0.84,  # 7th
        0.67   # 8th
    ]
    return jl_automatic_transmission_ratio

def jl_manual_trans_ratios():
    jl_manual_transmission_ratio = [
        4.49,  # reverse
        5.13,  # 1st
        2.63,  # 2nd
        1.54,
        1.00,
        0.81,  # 5th
        0.72   # 6th
    ]
    return jl_manual_transmission_ratio

def wrangler_diff_ratios():
    wrangler_avail_diff_ratios = [
        3.23,
        3.73,
        4.10,
        4.56,
        4.88,
        5.13,
        5.38
    ]
    return wrangler_avail_diff_ratios


def jeep_model_dict():
    jeep_models = {
        'Jeep JK (2007 - 2011)': 'jk_2007',
        'Jeep JK (2012 - 2018)': 'jk_2012',
        'Jeep JL': 'jl'
    }
    return jeep_models
