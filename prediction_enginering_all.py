
from prediciton_engineering import label_customer
def make_label_times(logs, prediction_date, churn_days):
    """
    Make labels for an entire series of transactions. 
    
    Params
    --------
        logs (dataframe): table of customer transactions
        prediction_date (str): time at which predictions are made. Either "MS" for the first of the month
                               or "SMS" for the first and fifteenth of each month 
        churn_days (int): integer number of days without an active membership required for a churn. A churn is
                          defined by exceeding this number of days without an active membership.
        lead_time (int): number of periods in advance to make predictions for. Defaults to 1 (preditions for one offset)
        prediction_window(int): number of periods over which to consider churn. Defaults to 1.
    Return
    --------
        label_times (dataframe): a table with customer ids, cutoff times, binary label, regression label, 
                                 and date of churn. This table can then be used for feature engineering.
    """
    
    label_times = []
    logs = logs.sort_values(['actor_account_id'])
    
    # Iterate through each customer and find labels
    for customer_id, logins in logs.groupby('actor_account_id'):
        lt_cust = label_customer(customer_id, logins, prediction_date, churn_days, 
                                                   )
        
        label_times.append(lt_cust)
        
    # Concatenate into a single dataframe
    return pd.concat(label_times)