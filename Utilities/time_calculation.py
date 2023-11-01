import numpy as np
import time

def compute_V2I_SINR(
    white_gaussian_noise: int,
    channel_gain: float,
    transmission_power: float,
    intra_edge_interference: float,
    inter_edge_interference: float
) -> float:
    return (1.0 / (cover_dBm_to_W(white_gaussian_noise) + intra_edge_interference + inter_edge_interference)) * \
        (np.abs(channel_gain) ** 2) * cover_mW_to_W(transmission_power)

def compute_V2V_SINR(
    white_gaussian_noise: int,
    channel_gain: float,
    transmission_power: float,
    intra_vehicle_interference: float,
    inter_vehicle_interference: float
) -> float:
    return (1.0 / (cover_dBm_to_W(white_gaussian_noise) + intra_vehicle_interference + inter_vehicle_interference)) * \
        (np.abs(channel_gain) ** 2) * cover_mW_to_W(transmission_power)


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

def obtain_wired_transmission_time(
    transmission_rate: float,
    data_size: float
) -> float:
    """
    :param transmission_rate: bit/s
    :param data_size: bit
    :return: transmission time measure by s
    """
    return data_size / cover_Mbps_to_bps(transmission_rate)

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


def transform_str_data_time_into_timestamp(data_time: str) -> int:
    """
    :param data_time: a string of data time time e.g., "2019-01-01 00:00:00"
    :return: a timestamp
    """
    # US time zone
    return int(time.mktime(time.strptime(data_time, "%Y-%m-%d %H:%M:%S")) + 3600 * 15)

def transform_timestamp_into_str_data_time(timestamp: int) -> str:
    """
    :param timestamp: a timestamp
    :return: a string of data time time e.g., "2019-01-01 00:00:00"
    """
    # US time zone
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp - 3600 * 15))

def transform_str_data_time_into_timestamp_ms(data_time: str) -> int:
    """
    :param data_time: a string of data time time e.g., "2019-01-01 00:00:00"
    :return: a timestamp
    """
    # US time zone
    return int(time.mktime(time.strptime(data_time, "%Y-%m-%d %H:%M:%S"))) * 1000 + 3600 * 15 * 1000

def transform_timestamp_ms_into_str_data_time(timestamp: int) -> str:
    """
    :param timestamp: a timestamp
    :return: a string of data time time e.g., "2019-01-01 00:00:00"
    """
    # US time zone
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000 - 3600 * 15))
