if __name__ == '__main__': 
  

  y, test_y, y_reg, test_y_reg = get_features_and_labels()
  print ('Test:', test_y.shape, y.shape)
  
 
  ta = TheAlgorithm( y, test_y, y_reg, test_y_reg)
  classification = ta.evaluate_classification()
  print()
  print('ROC AUC, precision score, recall score, and f1 score:', classification,'\n') 
  
  
  regression = ta.evaluate_regression()
  print()
  print('RMSLE:', test_accuracy,'\n') 
  


