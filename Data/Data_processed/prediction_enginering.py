def label_customer(customer_id,logins, prediction_date, churn_days,   return_trans = False):
    """
    Make label times for a single customer. Returns a dataframe of labels with times, the binary label, 
    and the number of days until the next churn.
       
    Params
    --------
        customer_id (str): unique id for the customer
        customer_logs (dataframe): logs dataframe for the customer
        prediction_date (str): time at which predictions are made. Either "MS" for the first of the month
                               or "SMS" for the first and fifteenth of each month 
        churn_days (int): integer number of days without an active membership required for a churn. A churn is
                          defined by exceeding this number of 5 weeks  without being an active player.
        lead_time (int): number of periods in advance to make predictions for. 3 weeks
        prediction_window(int): number of periods over which to consider churn. 5 weeks
        return_trans (boolean): whether or not to return the transactions for analysis. Defaults to False.
        
    Return
    --------
        label_times (dataframe): a table of customer id, the cutoff times at the specified frequency, the 
                                 label for each cutoff time, the number of days until the next churn for each
                                 cutoff time, and the date on which the churn itself occurred.
        transactions (dataframe): [optional] dataframe of customer transactions if return_trans = True. Useful
                                  for making sure that the function performed as expected
    
       """
    
    assert(prediction_date in ['MS', 'SMS']), "Prediction day must be either 'MS' or 'SMS'"
    assert(logins['actor_account_id'].unique() == [customer_id]), "Transactions must be for only customer"
    
    # Don't modify original
    logs = logins.copy()
    
    #Range for cutoff times is from first to last  log
    first_log = logs['min_time']
    last_log = logs['max_time']
    start_date = first_log
   # pd.datetime(first_log.month, first_log.day)
   
    # Find number of days between last log and cutoff
    
    logs['difference_days'] = logs['cutof']- logs['max_time']
    # Determine which actor are associated with a churn
    logs['churn'] = logs['difference_days'].astype('timedelta64[D]') > churn_days
    logs['last_day_active']=last_log
    
    # Find date of each churn
    logs.loc[logs['churn'] == True, 
                     'churn_date'] = logs.loc[logs['churn'] == True, 
                                                      'last_day_active'] + pd.Timedelta(churn_days, 'd')
    
    #time labels
    label_times=pd.DataFrame({'actor_account_id':[customer_id]})
    label_times.insert(1, "cutoff_time", "05-11-2016")
    label_times['cutoff_time'] = label_times['cutoff_time'].astype('datetime64[ns]')


    lead_time=21
    prediction_window=35
    # Use the lead time and prediction window parameters to establish the prediction window 
    # Prediction window is for each cutoff time
    label_times['prediction_window_start'] = label_times['cutoff_time'] + pd.Timedelta(lead_time, 'd')
    label_times['prediction_window_end'] = label_times['cutoff_time'] + pd.Timedelta(lead_time, 'd') + pd.Timedelta(prediction_window, 'd')
    
    previous_churn_date = None
    
    #when no churn
    if (logs['churn']==False).all():
        label_times['label']=0
        label_times['days_to_churn']=np.nan
        label_times['churn_date']=np.nan
        if return_trans:
            return label_times[['actor_account_id', 'cutoff_time', 'label', 'days_to_churn', 'churn_date']], logs
        return label_times[['actor_account_id', 'cutoff_time', 'label', 'days_to_churn', 'churn_date']]

    # Iterate through every cutoff time
    for i, row in label_times.iterrows():
        
        # Default values if unknown
        churn_date = pd.NaT
        label = np.nan
        # Find the window start and end
        window_start = row['prediction_window_start']
        window_end = row['prediction_window_end']
        # Determine if there were any churns during the prediction window
        churns = logs.loc[(logs['churn_date'] >= window_start) & 
                                  (logs['churn_date'] < window_end), 'churn_date']

        # Positive label if there was a churn during window
        if not churns.empty:
            label = 1
            churn_date = churns.values[0]

            # Find number of days until next churn by 
            # subsetting to cutoff times before current churn and after previous churns
            if not previous_churn_date:
                before_idx = label_times.loc[(label_times['cutoff_time'] <= churn_date)].index
            else:
                before_idx = label_times.loc[(label_times['cutoff_time'] <= churn_date) & 
                                             (label_times['cutoff_time'] > previous_churn_date)].index

            # Calculate days to next churn for cutoff times before current churn
            label_times.loc[before_idx, 'days_to_churn'] = (churn_date - label_times.loc[before_idx, 
                                                                                         'cutoff_time']).\
                                                            dt.total_seconds() / (3600 * 24)
            previous_churn_date = churn_date
        # No churns, but need to determine if an active member
        else:
            # Find transactions before the end of the window that were not cancelled ### here the carracter deleted
            logs_before = logs.loc[(logs['time'] < window_end)].copy()
            # If the membership expiration date for this membership is after the window start, the custom has not churned
            if np.any(logs_before['time'] >= window_start):
                label = 0

        # Assign values
        label_times.loc[i, 'label'] = label
        label_times.loc[i, 'churn_date'] = churn_date
        
        # Handle case with no churns
        if not np.any(label_times['label'] == 1):
            label_times['days_to_churn'] = np.nan
            label_times['churn_date'] = pd.NaT
        
    if return_trans:
        return label_times.drop(columns = ['actor_account_id']), logs
    
    return label_times[['actor_account_id', 'cutoff_time', 'label', 'days_to_churn', 'churn_date']].copy()


