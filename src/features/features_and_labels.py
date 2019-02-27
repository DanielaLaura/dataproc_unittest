import pandas as  pd
import numpy as np

def get_features_and_labels():
     train = pd.read_csv('train.csv', index=True)
     test= pd.read_csv('test.csv', index=True)
     label_times= pd.read_csv('label_times.csv', index=True)
     train= train.merge(label_times, on = 'actor_account_id', how = 'left')
     train=train[~train['label'].isna()].sort_values(['actor_account_id', 'cutoff_time'])
     train.drop(columns=['cutoff_time', 'actor_account_id'])
     train= pd.get_dummies(train.drop(columns=['cutoff_time', 'actor_account_id']))
     test= pd.get_dummies(test.drop(columns=[ 'actor_account_id']))
     y, test_y = np.array(train.pop('label')), np.array(test.pop('label'))
     y_reg, test_y_reg = np.array(train.pop('days_to_churn')), np.array(test.pop('days_to_churn'))
     return (y, test_y, y_reg, test_y_reg)
  
