# get all attrition records
get_attrition = function(dt) {
    dt = dt[(no_quote_reason == 'refused_to_provide_quote') | 
                (no_quote_reason == 'failed_callback') | 
                (no_quote_reason == 'unable_to_provide_quote')]
    return(dt)
}

# parse comments for 'other' no_quote_reason and update no_quote_reason accordingly
parse_comment = function(dt) {
    nqr_other_na_ids = get_called_no_quote_records(dt)[(no_quote_reason == 'other') | is.na(no_quote_reason), id]
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'additional_context'), 'no_quote_reason'] = 'refused_to_provide_quote'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'does_not_perform_service'), 'no_quote_reason'] = 'does_not_provide_this_service'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'failed_callback'), 'no_quote_reason'] = 'failed_callback'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'no_phone_contact'), 'no_quote_reason'] = 'no_contact_after_2_tries'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'returned_call_with_quote_without_quote'), 'no_quote_reason'] = 'refused_to_provide_quote'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'shop_no_longer_operating'), 'no_quote_reason'] = 'no_contact_after_2_tries'
    dt[(id %in% nqr_other_na_ids) & (analyzed_comment == 'unable_to_provide_quote'), 'no_quote_reason'] = 'unable_to_provide_quote'
    
    return(dt)
}

# get all records with a quote / quote range
get_quote_records = function(dt) {
    return (dt[
        !is.na(quote_point) | 
            (
                !is.na(quote_range_low) & !is.na(quote_range_high)
            ), ])
}

# get all records with the shop not called
get_no_called_records = function(dt) {
    return (dt[
        is.na(quote_point) & 
            is.na(quote_range_low) & 
            is.na(quote_range_high) &
            is.na(no_quote_reason) &
            is.na(notes),])
}

# get all records with the shop called but no quote is given
get_called_no_quote_records = function(dt) {
    return (dt[
        !(
            is.na(quote_point) & 
                is.na(quote_range_low) & 
                is.na(quote_range_high) &
                is.na(no_quote_reason) &
                is.na(notes)
        ) &
        !(
            !is.na(quote_point) | 
                (
                    !is.na(quote_range_low) & 
                        !is.na(quote_range_high)
                )
        ), ])
}

# function to print out stats required for the flow chart
print_flow_chart_stats = function(dt) {
    # no call
    no_call_dt = get_no_called_records(dt)
    n_no_call = no_call_dt[, .N]
    n_no_call_county = no_call_dt[, uniqueN(county)]
    n_no_call_chain = no_call_dt[, uniqueN(chain)]
    
    # called, but no response
    no_quote_dt = get_called_no_quote_records(dt)
    n_no_quote = no_quote_dt[, .N]
    n_no_quote_county = no_quote_dt[, uniqueN(county)]
    n_no_quote_chain = no_quote_dt[, uniqueN(chain)]
    
    # called, with results
    quotes_dt = get_quote_records(dt)
    n_quote = quotes_dt[, .N]
    n_quote_county = quotes_dt[, uniqueN(county)]
    n_quote_chain = quotes_dt[, uniqueN(chain)]
    
    cat(paste0('n_no_call: ', n_no_call, '\n'))
    cat(paste0('n_no_call_county: ', n_no_call_county, '\n'))
    cat(paste0('n_no_call_chain: ', n_no_call_chain, '\n'))
    cat(paste0('n_no_quote: ', n_no_quote, '\n'))
    cat(paste0('n_no_quote_county: ', n_no_quote_county, '\n'))
    cat(paste0('n_no_quote_chain: ', n_no_quote_chain, '\n'))
    cat(paste0('n_quote: ', n_quote, '\n'))
    cat(paste0('n_quote_county: ', n_quote_county, '\n'))
    cat(paste0('n_quote_chain: ', n_quote_chain, '\n'))
}
