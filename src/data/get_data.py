import pandas as  pd
"""
Function for data import, transformation

Params
    --------
       ind_list: a .csv file which contains all the customer ids
        file_list : filder containing .csv files for each customer, named after its own customer ids
Return
-----------   
train : training  dataframe 


"""
def import_clean_data(ind_list, file_list):
    for ind in ind_list:
        sub = pd.read_csv(ind, index_col='actor_account_id')
    train = pd.DataFrame( index=sub.index)
    for actor_account_id in train.index:
        seg = pd.read_csv('file_list/' + actor_account_id + '.csv')
    
    log = seg['logid'].values
    #time = seg['time'].values
    
    train.loc[actor_account_id, 'log_cnt'] = len(log)
    train.loc[actor_account_id, 'con_cnt']= seg.loc[seg['logid']== 1003, 'actor_account_id'].count()
    train.loc[actor_account_id, 'exp_amt'] = seg.loc[seg['logid']== 1016, 'use_value1_num'].sum()
    train.loc[actor_account_id, 'exp_mastery_amt'] = seg.loc[seg['logid']== 1016, 'use_value3_num'].sum()
    train.loc[actor_account_id, 'exhaust_cnt'] = seg.loc[seg['logid']== 1201, 'actor_account_id'].count()
    train.loc[actor_account_id, 'die_cnt'] = seg.loc[seg['logid']== 1202, 'actor_account_id'].count()
    train.loc[actor_account_id, 'quest_cnt'] = seg.loc[seg['logid']== 5004, 'actor_account_id'].count()
    train.loc[actor_account_id, 'party_join_cnt'] = seg.loc[seg['logid']== 1102, 'actor_account_id'].count()
    train.loc[actor_account_id, 'party_kick_cnt'] = seg.loc[seg['logid']== 1106, 'actor_account_id'].count()
    train.loc[actor_account_id, 'guild_join_cnt'] = seg.loc[seg['logid']== 6005, 'actor_account_id'].count()
    train.loc[actor_account_id, 'guild_withdraw_cnt'] = seg.loc[seg['logid']== 6009, 'actor_account_id'].count()
    train.loc[actor_account_id, 'teleport_cnt'] =seg.loc[seg['logid']== 1010, 'actor_account_id'].count()
    train.loc[actor_account_id, 'pve_cnt']= seg.loc[seg['logid']==  1208, 'actor_account_id'].count()
    train.loc[actor_account_id, 'pvp_cnt']= seg.loc[seg['logid']==  1209, 'actor_account_id'].count()
    train.loc[actor_account_id, 'ducel_end_cnt']= len(set(seg[(seg.logid ==1404) & (seg.logid ==1406)].count()))
    train.loc[actor_account_id, 'spent_money']= seg.loc[seg['logid']==  1010, 'use_value2_num'].sum()
    train.loc[actor_account_id, 'increased_money']= seg.loc[seg['logid']==  1017, 'use_value2_num'].sum()
    train.loc[actor_account_id, 'decreased_money']= seg.loc[seg['logid']==  1018, 'use_value2_num'].sum()
    train.loc[actor_account_id, 'increased_money2']= seg.loc[seg['logid']==  2006, 'use_value2_num'].sum()
    train.loc[actor_account_id, 'increased_money3']= seg.loc[seg['logid']==  2016, 'use_value2_num'].sum()
    train.loc[actor_account_id, 'decreased_money2']= seg.loc[seg['logid']==  2105, 'use_value2_num'].sum()
    #train.loc[actor_account_id, 'total_increase_money']= train['increased_money']+ train['increased_money2']+ train['increased_money3']
    #train.loc[actor_account_id, 'total_decrease_money']= train['decreased_money']+train['decreased_money2']
    train.loc[actor_account_id, 'increased_experience']= seg.loc[seg['logid']==  1016, 'use_value1_num'].sum()
    train.loc[actor_account_id, 'total_experience']= seg.loc[seg['logid']==  1016, 'new_value2_num'].sum()
    train.loc[actor_account_id, 'in_item']= seg.loc[seg['logid']==  1022, 'use_value1_num'].count()   
    train.loc[actor_account_id, 'decreased_item']= seg.loc[seg['logid']==  1023, 'use_value1_num'].count()
    train.loc[actor_account_id, 'increased_item1']= seg.loc[seg['logid']==  1022, 'new_value2_num'].sum()
    train.loc[actor_account_id, 'decreased_item1']= seg.loc[seg['logid']==  1023, 'new_value2_num'].sum()
    train.loc[actor_account_id, 'del_cnt']= seg.loc[seg['logid']== 1012, 'actor_account_id'].count()
    train.loc[actor_account_id, 'guild_create_cnt']= seg.loc[seg['logid']== 6001, 'actor_account_id'].count() 
    #train[actor_account_id, 'guild_destroy_cnt']= seg.loc[seg['logid']== 6002, 'actor_account_id'].count()    
    train.loc[actor_account_id, 'min_time'] =time.min()
    train.loc[actor_account_id, 'max_time'] = time.max()
    train['min_time'] = train['min_time'].astype('datetime64[ns]')
    train['max_time'] = train['max_time'].astype('datetime64[ns]')
    train.insert(32, "cutof", "05-11-2016")
    train['cutof'] = train['cutof'].astype('datetime64[ns]')
    train['difference_days'] = (train['cutof']- train['max_time']).dt.days
    train.to_csv('train.csv', index = True)
    return train