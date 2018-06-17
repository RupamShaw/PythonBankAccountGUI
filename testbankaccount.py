import unittest 
from  bankaccount import BankAccount
class TestBankAcount(unittest.TestCase):
    def setUp(self):
            # Create a test BankAccount object
                self.account = BankAccount()     
            # Provide it with some property values        
                self.account.balance= 1000.0
    def test_legal_deposit_works(self):
        # deposit amount + into current balance.
       result = self.account.deposit_funds(500.0)
       self.assertEqual(self.account.balance,1500.0)
    def test_illegal_deposit_raises_exception(self):
        # deposit amount illegal amount like negative amount  
        self.assertRaises(ValueError ,self.account.deposit_funds,'fantastic')
        self.assertRaises(ValueError ,self.account.deposit_funds,'-145.0')
    def test_legal_withdrawal(self):
        #withdraw amount from current balance 
        self.account.withdraw_funds(100.0)
        self.assertEqual(self.account.balance,900.0)
    def test_illegal_withdrawal(self):
        # Your code here to test that withdrawing an illegal amount (like 'bananas'none)
         self.assertRaises(ValueError ,self.account.withdraw_funds,'anything')
         self.assertRaises(ValueError ,self.account.withdraw_funds,'-4.44')
    def test_insufficient_funds_withdrawal(self):
        #withdrawal fund is not more balance amount 
        self.assertRaises(ValueError ,self.account.withdraw_funds,3100.0)
        self.assertRaises(ValueError ,self.account.withdraw_funds,3100.78)        
# Run the unit tests in the above test case
if __name__ == '__main__' :
    unittest.main()       