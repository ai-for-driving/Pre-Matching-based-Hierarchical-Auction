from typing import List
import numpy as np
from player import buyer, seller

def init_bids_and_asks(
    buyers: List[buyer],
    sellers: List[seller],
) -> tuple[List[buyer], List[seller]]:
    buyer_num = len(buyers)
    random_bids = np.random.uniform(0, 1, buyer_num)
    for buyer in buyers:
        buyer.set_bid(random_bids[buyer.get_index()])
    sorted_buyers = sorted(buyers, key=lambda x: x.get_bid(), reverse=True)
    seller_num = len(sellers)
    random_asks = np.random.uniform(0, 1, seller_num)
    for seller in sellers:
        seller.set_ask(random_asks[seller.get_index()])
    sorted_sellers = sorted(sellers, key=lambda x: x.get_ask())
    return sorted_buyers, sorted_sellers

def find_key_index(
    sorted_buyers: List[buyer],
    sorted_sellers: List[seller],
):
    max_buyer_number = 0
    buyer_key_index = 0
    seller_key_index = 0
    
    for buyer in sorted_buyers:
        buyer_number = buyer.get_index()
        for seller in sorted_sellers:
            seller_number = seller.get_index()
            buyer_bid = buyer.get_bid()
            seller_ask = seller.get_ask()
            if buyer_bid < seller_ask:
                continue
            else:
                if (buyer_number == len(sorted_buyers) - 1) or (seller_number == len(sorted_sellers) - 1) \
                    or ((buyer_number < len(sorted_buyers) - 1) and \
                        (seller_number < len(sorted_sellers) - 1) and \
                        (sorted_buyers[buyer_number + 1].get_bid() < sorted_sellers[seller_number + 1].get_ask())):
                    offered_computing_resource_sum = 0
                    offered_storage_resource_sum = 0
                    for _ in range(seller_number - 1):
                        offered_computing_resource_sum += sorted_sellers[_].get_offered_computing_resources()
                        offered_storage_resource_sum += sorted_sellers[_].get_offered_storage_resources()
                    for buyer_prime_index in range(buyer_number - 1):
                        offered_computing_resource_sum -= sorted_buyers[buyer_prime_index].get_requested_computing_resources()
                        offered_storage_resource_sum -= sorted_buyers[buyer_prime_index].get_requested_storage_resources()
                        if offered_computing_resource_sum < 0 or offered_storage_resource_sum < 0:
                            if buyer_prime_index > max_buyer_number + 1:
                                max_buyer_number = buyer_prime_index - 1
                                buyer_key_index = buyer_prime_index - 1
                                seller_key_index = seller_number
                                break
    return buyer_key_index, seller_key_index

def resource_allocation_of_edge_cloud_auction(
    sorted_buyers: List[buyer],
    sorted_sellers: List[seller],
    buyer_key_index: int,
    seller_key_index: int,
    buyer_num: int,
    seller_num: int,
) -> np.ndarray: 
    new_buyers = sorted_buyers[0:buyer_key_index + 1]
    new_sellers = sorted_sellers[0:seller_key_index + 1]
    
    offloading_decision = np.zeros((buyer_num, seller_num))
    
    for seller in new_sellers:
        offered_computing_resources = seller.get_offered_computing_resources()
        offered_storage_resources = seller.get_offered_storage_resources()
        for buyer in new_buyers:
            requested_computing_resources = buyer.get_requested_computing_resources()
            requested_storage_resources = buyer.get_requested_storage_resources()
            if offered_computing_resources < requested_computing_resources or offered_storage_resources < requested_storage_resources:
                seller_key_index = seller.get_index() - 1
                break
        for buyer in new_buyers:
            requested_computing_resources = buyer.get_requested_computing_resources()
            requested_storage_resources = buyer.get_requested_storage_resources()
            if offered_computing_resources >= requested_computing_resources and offered_storage_resources >= requested_storage_resources:
                offloading_decision[buyer.get_index()][seller.get_index()] = 1
                new_buyers.remove(buyer)
                seller.set_offered_computing_resources(offered_computing_resources - requested_computing_resources)
                seller.set_offered_storage_resources(offered_storage_resources - requested_storage_resources)
    
    return offloading_decision

def payment_pricing(
    buyers: List[buyer],
    sellers: List[seller],
    buyer_key_index: int,
    seller_key_index: int,
    offloading_decision: np.ndarray,
):
    for buyer in buyers:
        if offloading_decision[buyer.get_index()].sum() == 1:
            bid_high = buyer.get_bid()
            bid_low = buyers[buyer.get_index() + 1].get_bid()
            bid_temp = buyer.get_bid()
            while bid_high - bid_low > 0.0001:
                bid_now = (bid_high + bid_low) / 2
                buyer.set_bid(bid_now)
                sorted_buyers = sorted(buyers, key=lambda x: x.get_bid(), reverse=True)
                buyer_key_index, seller_key_index = find_key_index(sorted_buyers, sellers)
                offloading_decision = resource_allocation_of_edge_cloud_auction(sorted_buyers, sellers, buyer_key_index, seller_key_index, len(buyers), len(sellers))
                if offloading_decision[buyer.get_index()].sum() == 1:
                    bid_low = bid_now
                else:
                    bid_high = bid_now
                buyer.set_payment(bid_now)
                bid_now = bid_temp
                
    for seller in sellers:
        if offloading_decision[:, seller.get_index()].sum() > 0:
            seller.set_payment(sellers[seller_key_index + 1].get_ask())