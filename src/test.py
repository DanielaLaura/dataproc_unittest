class TestInput(unittest.TestCase):
  
    @classmethod
    def setUpClass(cls):
        # print('setupClass')   
        pass

    @classmethod
    def tearDownClass(cls): 
        # print('teardownClass')
        pass


    def setUp(self):
        print('setUp') 
        self.y, self.test_y, self.y_reg, self.test_y_reg = get_features_and_labels()
         
        self.roc = 0
        self.f1_score=0
        self.recall_score=0
        self.precision_score=0
        self.rmsle=0



    def tearDown(self):
        # print('tearDown')
        pass


    def test_classification(self):     
        np.random.seed(31337)
        self.ta = TheAlgorithm(self.y, self.test_y, self.y_reg, self.test_y_reg)
        self.assertEqual(self.ta.evaluate_classification(), self. classification) 
        self.assertEqual(self.ta.roc.tolist(), self.roc.tolist())
        self.assertEqual(self.ta.f1_score(), self.f1_score.tolist())
        self.assertEqual(self.ta.recall_score(), self.recall_score.tolist())
        self.assertEqual(self.ta.precision_score(), self.precision_score.tolist())
        
  
    def test_regression(self):
        
        self.ta = TheAlgorithm(self.y, self.test_y, self.y_reg, self.test_y_reg)
        self.assertEqual(self.ta.evaluate_regression(), self. regression)  
        self.assertEqual(self.ta.rmsle.tolist(), self.rmsle.tolist())

if __name__ == '__main__':
  
    #run tests 
    unittest.main(argv=['first-arg-is-ignored'], exit=False)