import tkinter as tk
from tkinter import *
from tkinter import messagebox
from functools import partial
from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount
from sys import exc_info

window = tk.Tk()
# Set window size here to '440x640' pixels
window.geometry("440x640")
# Set window title here to 'FedUni Banking'
window.title("FedUni Banking")
# The account number entry and associated variable
account_label = tk.Label(window, text='Account number/Pin')
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(window, textvariable=account_number_var)
account_number_entry.focus_set()
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(window, text='PIN Number', textvariable=pin_number_var, show="*")
pin_number_var.set("")
# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')

balance_label = tk.Label(window, textvariable=balance_var)
# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(window)
# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(window, height=10, width=48)
# The bank account object we will work with
account = BankAccount()
# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    pin_number_var.set("")

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    

    pinNumber = pin_number_var.get()+event
    # Limit to 4 chars in length
    if len(pinNumber) >= 4:
        pin_number_var.set("")
        print("pin length can't be more than 4 characters!")
        messagebox.showinfo("Pin Charcter "," 4 characters length pin only cab be enterered " )

    pin_number_var.set(pinNumber)

def log_in():
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_number_entry
    global pin_number
    # Create the filename from the entered account number with '.txt' on the end

    file_name=str(account_number_entry.get())+".txt"
    # Try to open the account file for reading
    try:
        global account_file
        account_file=open(file_name,"r")
        # Open the account file for reading
        file_content=account_file.read().split('\n')
        # First line is account number
        account.account_number=file_content[0]
        if account_number_entry.get() != file_content[0]:
            messagebox.showinfo('Login Failed', 'Invalid Account Number ')
            account_number_var.set("")
            pin_number_var.set("")
            raise Exception("Invalid login  Please check Account number  ")
        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
        if account_pin_entry.get()== file_content[1]:
            pin_number=file_content[1]
            print ("login Successful")
        else:
            pin_number_var.set("")
            messagebox.showinfo("Invalid User","Invlaid login Pin")
            raise Exception("Invalid Details for pin")
        # Read third and fourth lines (balance and interest rate)
        account.balance=file_content[2]
        account.interest=file_content[3]
        
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        index=4
        #x=len(file_content)-4
        while(index<len(file_content)):
            if file_content[index]=='Deposit':
                account.transaction_list.append(('Deposit',file_content[index+1]))
            elif file_content[index]=='Withdrawl':
                account.transaction_list.append(('Withdrawl',file_content[index+1]))
            index=index+2
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list            
        account.get_transaction_string()
        # Close the file now we're finished with it
        account_file.close()
        remove_all_widgets()
        create_account_screen()
        
    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except IOError as er:
        print( "I/O error({0}): {1}".format(er.errno, er.strerror))
         # Show error messagebox and & reset BankAccount object to default...
        messagebox.showinfo('Login Failed', 'Please check your Account Number ')
        #  ...also clear PIN entry and change focus to account number entry
        account_number_var.set("")
        pin_number_var.set("")
    except ValueError:
        print ("Not converting to number")
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise        
# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account
    # Save the account with any new transactions Reset the bank acount object
    account.save_to_file(pin_number)
    account=BankAccount()

    # Reset the account number and pin to blank
    account_number_var.set("")
    pin_number_var.set("")

    # Remove all widgets and display the login screen again

    remove_all_widgets()
    create_login_screen()
def deleteItemsListBox():  
    transaction_text_widget.delete(0,END) ##delete all contents
    for line in account.get_transaction_string().split('\n'):
        transaction_text_widget.insert(END, line)  # Change the balance label to reflect the new balance
  

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    # Try to increase the account balance and append the deposit to the account file
    account.deposit_funds(amount_entry.get()) 
    
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method

        # Deposit funds
        
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
    account.transaction_list.append(('Deposit',amount_entry.get()))
    ##need to add delete items from  listBox
    deleteItemsListBox()
    balance_var.set(account.balance)
        # Clear the amount entry
    amount_var.set('')
        # Update the interest graph with our new balance
    plot_interest_graph()

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
        
def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
   # Try to increase the account balance and append the deposit to the account file
    
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        
        # Withdraw funds
    account.withdraw_funds(amount_entry.get())

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
    account.transaction_list.append(('Withdrawl',amount_entry.get()))
    
    deleteItemsListBox()
        # Change the balance label to reflect the new balance

        # Change the balance label to reflect the new balance
    balance_var.set(account.balance)
        # Clear the amount entry
    amount_var.set("")
        # Update the interest graph with our new balance
    plot_interest_graph()
    # Catch and display any returned exception as a messagebox 'showerror'
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global window
    for widget in window.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''
    try:
        if float(account.balance)<float(0) or float(account.balance)<float(0.0):
            print('Error: Balance is negative or zero')
        else:
            print("account.balance start plotting", account.balance)
            # YOUR CODE to generate the x and y lists here which will be plotted
            x=[]
            y=[]
            x.append(0)
            x.append(1)
            y.append(0)
            ##need to work on this ### y.append(float(account.balance[:len(account.balance)-2]))
            y.append(float(account.balance))
            for i in range(2,13):
                x.append(i)
                y.append((y[i-1]+y[i-1]*float(account.interest))/12)
            
            # This code to add the plots to the window is a little bit fiddly so you are provided with it.
            # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
            figure = Figure(figsize=(5,2), dpi=100)
            figure.suptitle('Cumulative Interest 12 Months')
            a = figure.add_subplot(111)
            a.plot(x, y, marker='o')
            a.grid()
            
            canvas = FigureCanvasTkAgg(figure, master=window)
            canvas.draw()
            graph_widget = canvas.get_tk_widget()
            graph_widget.grid(row=4, column=0, columnspan=6, sticky='nsew')            
    except:
        print(" error in plotting")
        raise 

# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
   
    '''Function to create the login screen.'''    
    # ----- Row 0 ----- ('FedUni Banking' label here. Font size is 32.)
    windows_title = tk.Label(window, text="FedUni Banking",font=("Comic Sans MS", 32)).grid(row=0,column=0, columnspan=5,sticky="nsew")
     # ----- Row 1 ----- (Acount Number / Pin label here)
    account_label.grid(row=1,column=0,columnspan=2,sticky="NWNESWSE")
    # Account number entry here
    account_number_entry.grid(row=1,column=2,columnspan=2,sticky="NWNESWSE")
    # Account pin entry here
    account_pin_entry.grid(row=1,column=4,columnspan=2,sticky="NWNESWSE")
    # ----- Row 2 -----
    pin_number_var.set("")
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    
    numberbtn1 = Button(window, text="1", command=partial(handle_pin_button,'1')).grid(row=2,column=0,columnspan=2,sticky="NWNESWSE")
    numberbtn2 =  Button(window, text="2",  command=partial(handle_pin_button,'2')).grid(row=2,column=2,columnspan=2,sticky="NWNESWSE")
    numberbtn3 = Button(window, text="3",command=partial(handle_pin_button,'3')).grid(row=2,column=4,columnspan=2,sticky="NWNESWSE")

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.

    numberbtn4 = Button(window, text="4", command=partial(handle_pin_button,'4')).grid(row=3,column=0,columnspan=2,sticky="NWNESWSE")
    numberbtn5 = Button(window, text="5", command=partial(handle_pin_button,'5')).grid(row=3,column=2,columnspan=2,sticky="NWNESWSE")
    numberbtn6 = Button(window, text="6", command=partial(handle_pin_button,'6')).grid(row=3,column=4,columnspan=2,sticky="NWNESWSE")

    

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.

    numberbtn7 = Button(window, text="7", width=10,height=4, command=partial(handle_pin_button,'7')).grid(row=4,columnspan=2,sticky="NWNESWSE")
    numberbtn8 = Button(window, text="8", width=10,height=4, command=partial(handle_pin_button,'8')).grid(row=4,column=2,columnspan=2,sticky="NWNESWSE")
    numberbtn9 = Button(window, text="9", width=10,height=4, command=partial(handle_pin_button,'9')).grid(row=4,column=4,columnspan=4,sticky="NWNESWSE")
    # ----- Row 5 ----- Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    cancel = Button(window, text="Cancel/Clear", width=10,height=4,bg='red',activebackground='red', command=partial(clear_pin_entry,"")).grid(row=5,columnspan=2,sticky="NWNESWSE")
    numberbtn0 = Button(window, text="0", width=10,height=4, command=partial(handle_pin_button,'0')).grid(row=5,column=2,columnspan=2,sticky="NWNESWSE")
    login = Button(window, text="Login", width=10,height=4,bg='green',activebackground='green', command=log_in).grid(row=5,column=4,columnspan=2,sticky="NWNESWSE")

    
    # Button 0 here
    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    window.rowconfigure(5, weight=1)
    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=1)
    window.columnconfigure(2,weight=1)
    window.columnconfigure(3,weight=1)
    window.columnconfigure(4,weight=1)
    window.columnconfigure(5,weight=1)
  
def create_account_screen():
    '''Function to create the account screen.'''
    global amount_entry
    global amount_label
    global transaction_text_widget
    global balance_var
    global amount_var
    # ----- Row 0 -----  FedUni Banking label here. Font size should be 24.

    windows_label1= tk.Label(window, text="FedUni Banking",font=("Comic Sans MS", 24)).grid(row=0,column=0, columnspan=5,sticky="nsew")
    # ----- Row 1 -----  Account number label here
    account_label = tk.Label(window, text='Account number   '+account_number_var.get()).grid(row=1,column=0,sticky="nsew",columnspan=2)
    # Balance label here
    balance_var.set('Balance:$'+account.balance)    
    w = balance_label.grid(row=1,column=2,sticky="nsew",columnspan=2)
    # Log out button here   
    Log_out = Button(window, text="Log Out", command=save_and_log_out).grid(row=1,column=4,sticky="nsew",columnspan=2)
   # ----- Row 2 ----- Amount label here
    account_label = tk.Label(window, text='Amount').grid(row=2,column=0,sticky="nsew",columnspan=2)

    # Amount entry here
    amount_var = tk.StringVar()
    amount_entry = tk.Entry(window, textvariable=amount_var)
    amount_entry.grid(row=2,column=2,sticky="nsew",columnspan=2)
    # Deposit button here
    DepositButton = Button(window, text="Deposit", command=perform_deposit).grid(row=2,column=4,sticky="nsew")
    # Withdraw button here
    WithdrawlButton = Button(window, text="Withdraw", command=perform_withdrawal).grid(row=2,column=5,sticky="nsew")

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----  Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    scrollbar = Scrollbar(window)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited

    # Now add the scrollbar and set it to change with the yview of the text widget
    
    transaction_text_widget = Listbox(window, yscrollcommand = scrollbar.set )
    transaction_text_widget.grid(row =3, column=0, columnspan=6,sticky="nsew")
    for line in account.get_transaction_string().split('\n'):
        transaction_text_widget.insert(END, line) 
    scrollbar.grid(sticky="nsw", row = 3,column=6)
    scrollbar['command']=transaction_text_widget.yview
    
    # ----- Row 4 - Graph -----
    # Call plot_interest_graph() here to display the graph
    
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
   
    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=1)
    window.columnconfigure(2,weight=1)
    window.columnconfigure(3,weight=1)
    window.columnconfigure(4,weight=1)

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
window.mainloop()
