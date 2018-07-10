
# ---------- SYNCHRONIZING THREADS ----------
# You can lock other threads from executing
 
# If we try to model a bank account we have to make sure
# the account is locked down during a transaction so
# that if more then 1 person tries to withdrawal money at
# once we don't give out more money then is in the account

import threading
import time
import random


class BankAccount (threading.Thread):
 
    acctBalance = 100
 
    def __init__(self, name, moneyRequest):
        threading.Thread.__init__(self)
        self.name = name
        self.moneyRequest = moneyRequest
        self.testvar = 34
 
    def run(self):
        # Get lock to keep other threads from accessing the account
        threadLock.acquire()
 
        # Call the static method
        BankAccount.getMoney(self)
 
        # Release lock so other thread can access the account
        threadLock.release()
 
    @staticmethod
    def getMoney(customer):
        print("{} tries to withdrawal ${} at {} - TESTVAR={}".format(customer.name,
                customer.moneyRequest,
                time.strftime("%H:%M:%S", time.gmtime()), customer.testvar))
 
        if BankAccount.acctBalance - customer.moneyRequest > 0:
            BankAccount.acctBalance -= customer.moneyRequest
            print("New account balance is : ${}".format(BankAccount.acctBalance))
        else:
            print("Not enough money in the account")
            print("Current balance : ${}".format(BankAccount.acctBalance))
 
        time.sleep(3)
 
# Create a lock to be used by threads
threadLock = threading.Lock()
 
# Create new threads
doug = BankAccount("Doug", 1)
paul = BankAccount("Paul", 100)
sally = BankAccount("Sally", 50)
 
# Start new Threads
doug.start()
paul.start()
sally.start()
 
# Have threads wait for previous threads to terminate
doug.join()
paul.join()
sally.join()
 
 
xbee = ZigBee(ser=ser, escaped=True, callback=persist_data)
digi = DigiMesh(ser=ser)

# 
	
xbee.halt()
ser.close()


 
 
 
print("Execution Ends")
