def comm_func_ticker_match(ticker, amfi_rank_dict, dematsum_list):
    if (ticker in amfi_rank_dict and amfi_rank_dict[ticker] <= 500) \
            or ticker in dematsum_list:
        return True
    else:
        return False
