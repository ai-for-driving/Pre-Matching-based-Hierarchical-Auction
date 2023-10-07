import numpy as np


    
def compute_channel_condition(
    channel_fading_gain: float,
    distance: float,
    path_loss_exponent: int,
) -> float:
    """
    Compute the channel condition
    """
    return np.power(np.abs(channel_fading_gain), 2) * \
        1.0 / (np.power(distance, path_loss_exponent))

def compute_V2I_SINR(
    white_gaussian_noise: int,
    channel_condition: float,
    transmission_power: float,
    intra_edge_interference: float,
    inter_edge_interference: float
) -> float:
    """
    Compute the SINR of a vehicle transmission
    Args:
        white_gaussian_noise: the white gaussian noise of the channel, e.g., -70 dBm
        channel_fading_gain: the channel fading gain, e.g., Gaussion distribution with mean 2 and variance 0.4
        distance: the distance between the vehicle and the edge, e.g., 300 meters
        path_loss_exponent: the path loss exponent, e.g., 3
        transmission_power: the transmission power of the vehicle, e.g., 10 mW
    Returns:
        SNR: the SNR of the transmission
    """
    return (1.0 / (cover_dBm_to_W(white_gaussian_noise) + intra_edge_interference + inter_edge_interference)) * \
        np.power(np.absolute(channel_condition), 2) * cover_mW_to_W(transmission_power)

def compute_V2V_SINR(
    white_gaussian_noise: int,
    channel_condition: float,
    transmission_power: float,
    other_vehicle_interference: float,
) -> float:
    return (1.0 / (cover_dBm_to_W(white_gaussian_noise) + other_vehicle_interference)) * \
        channel_condition * cover_mW_to_W(transmission_power)

def compute_transmission_rate(SINR, bandwidth) -> float:
    """
    :param SINR:
    :param bandwidth:
    :return: transmission rate measure by bit/s
    """
    return float(cover_MHz_to_Hz(bandwidth) * np.log2(1 + SINR))

def cover_bps_to_Mbps(bps: float) -> float:
    return bps / 1000000

def cover_Mbps_to_bps(Mbps: float) -> float:
    return Mbps * 1000000

def cover_MHz_to_Hz(MHz: float) -> float:
    return MHz * 1000000

def cover_ratio_to_dB(ratio: float) -> float:
    return 10 * np.log10(ratio)

def cover_dB_to_ratio(dB: float) -> float:
    return np.power(10, (dB / 10))

def cover_dBm_to_W(dBm: float) -> float:
    return np.power(10, (dBm / 10)) / 1000

def cover_W_to_dBm(W: float) -> float:
    return 10 * np.log10(W * 1000)

def cover_W_to_mW(W: float) -> float:
    return W * 1000

def cover_mW_to_W(mW: float) -> float:
    return mW / 1000

def obtain_transmission_time(transmission_rate, data_size) -> float:
    """
    :param transmission_rate: bit/s
    :param data_size: bit
    :return: transmission time measure by s
    """
    return data_size / transmission_rate

def obtain_computing_time(
    data_size: float,
    per_cycle_required: float,
    computing_capability: float
) -> float:
    return data_size * per_cycle_required / computing_capability
