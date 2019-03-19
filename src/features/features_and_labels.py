import pandas as  pd
import numpy as np

def get_features_and_labels():
     train = pd.read_csv('train.csv', index=True)
     test= pd.read_csv('test.csv', index=True)
     label_times= pd.read_csv('label_times.csv', index=True)
     train= train.merge(label_times, on = 'actor_account_id', how = 'left')
     train=train[~train['label'].isna()].sort_values(['actor_account_id', 'cutoff_time'])
     #clean train set
     missing_train= train.isnull().sum() / len(train)
     to_drop = list((missing_train[missing_train > 0.9]).index)
     to_drop = [x for x in to_drop if x != 'days_to_churn']
     train.drop(columns=to_drop, inplace=True)
     one_unique = train.apply(lambda x: x.nunique() == 1, axis=0)
     unique_drop = list(one_unique[one_unique == True].index)
     train.drop(columns=to_drop, inplace=True)
     train.drop(columns=['cutoff_time', 'actor_account_id'])
     train= pd.get_dummies(train.drop(columns=['cutoff_time', 'actor_account_id']))
     #clean test set
     missing_test= test.isnull().sum() / len(test)
     to_drop1 = list((missing_test[missing_test > 0.9]).index)
     to_drop1 = [x for x in to_drop1 if x != 'days_to_churn']
     test.drop(columns=to_drop1, inplace=True)
     test= pd.get_dummies(test.drop(columns=[ 'actor_account_id']))

     y, test_y = np.array(train.pop('label')), np.array(test.pop('label'))
     y_reg, test_y_reg = np.array(train.pop('days_to_churn')), np.array(test.pop('days_to_churn'))
     return (y, test_y, y_reg, test_y_reg)
  
