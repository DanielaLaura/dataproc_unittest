class TheAlgorithm(object):
  
    @my_logger
    @my_timer
    def __init__(self,y, test_y, y_reg, test_y_reg):  
      self.y, self.test_y, self.y_reg, self.test_y_reg = y, test_y, y_reg, test_y_reg

   
    
    @my_logger
    @my_timer
    def evaluate_classification(self):
     """Evaluate a machine learning model on four metrics:
       ROC AUC, precision score, recall score, and f1 score.

       Returns the model and the predictions."""
     self.classifier =RandomForestClassifier(n_estimators=100, max_depth=40,
                                            min_samples_leaf=50,
                                            min_samples_leaf=50,
                                            random_state=50)
     self.classifier.fit(self.train, self.y)
   

    # Predict probabilities and labels
     self.probs = self.classifier.predict_proba(self.test_y)[:, 1]
     self.preds =self.classifier.predict(self.test_y)

    # Calculate metrics
     self.roc = roc_auc_score(self.test_y, self.probs)
     self.f1_score=self.f1_score(self.test_y, self.probs)
     self.recall_score=self.recall_score(self.test_y, self.probs)
     self.precision_score=self.precision_score(self.test_y, self.probs)
     return self.preds, self.roc, self.f1_score,self.recall_score, self.precision_score





    @my_logger
    @my_timer
    def evaluate_regression(self):
     """Evaluate a Regression machine learning model on one metrics:
       RMSLE score.

       Returns the predictions and ."""
     self.regression =lgb.LGBMRegressor(n_estimators=1000, objective = 'regression', 
                                   boosting_type = 'gbdt', learning_rate = 0.1, 
                                   metric= 'rmsle',  max_depth= 6, 
                                   subsample = 0.8, n_jobs = -1, random_state = 50)
     self.regression.fit(self.train, self.y_reg)
   

    # Predict probabilities and labels
     self.probs = self.regression.predict_proba(self.test_y_reg)[:, 1]
     self.preds =self.regression.predict(self.test_y_reg)

    # Calculate metrics
     self.rmsle = rmsle(self.test_y_reg, self.probs)
    
 
     err = rmsle(np.exp(y_valid), preds)
     return self.preds,  self.rmsle









    


