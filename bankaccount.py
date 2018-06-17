from tkinter import messagebox
class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number=0
        self.pin_number=""
        self.balance=0.0
        self.interest=0.0
        self.transaction_list=[]
        
    def isNumber(self, amountNum):
        isNumber = True
        try:
            number = float(amountNum)
            if(number<0):
                isNumber = False
            else:
                isNumber =  number == number
        except ValueError:
            isNumber = False
        return isNumber

    def deposit_funds(self, fund):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        if self.isNumber(fund) :
            self.balance= float(self.balance) + float(fund)
        else:
            messagebox.showinfo('Transaction Error', 'Illegal numeric value entered in depositing') 
            raise ValueError('Illegal numeric value entered in depositing')


    def withdraw_funds(self, fund):
        ''' Raises an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        if self.isNumber(fund) :
            if float(fund)<=float(self.balance):
                self.balance = float(self.balance) -float(fund) 
            
            if float(fund)>float(self.balance):
                messagebox.showinfo('Transaction Error', 'Withdraw amount exceeds available funds')
                raise ValueError('Withdraw amount exceeds available funds')
        else:
            messagebox.showinfo('Transaction Error', 'Illegal numeric value entered in withdrawing')
            raise ValueError('Illegal numeric value entered in withdrawing')  

    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Eext line.'''
        get_transaction_string=""
        #save_to_file()
        for i in self.transaction_list:
            get_transaction_string+=i[0]
            get_transaction_string+="\n"
            get_transaction_string+=i[1]
            get_transaction_string+="\n"
        #print("in another file account.get_transaction ",get_transaction_string)    
        return get_transaction_string

    def save_to_file(self,pinno):
        '''Function to overwrite the account text file with the current account
           details. '''
        self.pinNumber=pinno
        fileName=str(self.account_number)+".txt"
        f=open(fileName,"w")
        content=self.get_transaction_string()
        f.write(''+self.account_number+'\n')
        f.write(self.pinNumber+'\n')
        f.write(str(self.balance)+'\n')
        f.write(str(self.interest)+'\n')
        f.write(content)
        f.close 
