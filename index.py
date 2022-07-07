from threading import Thread
from reach_rpc import mk_rpc
import time

def main():
    rpc, rpc_callbacks = mk_rpc()

    starting_balance = rpc("/stdlib/parseCurrency", 100)
    User_1 = input("Enter your name player1: ")
    User_2 =input("Enter your name player2: ")
    acc_user1 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_user2 = rpc("/stdlib/newTestAccount", starting_balance)

    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))
    def get_address(s):
        return(rpc("/acc/getAddress", s))
    before_user1 = get_balance(acc_user1)
    before_user2 = get_balance(acc_user2)
    acc1 =  get_address(acc_user1)
    acc2 = get_address(acc_user2)
    print("%s starting balance is %s algo" %(User_1,before_user1))
    print("%s starting balance is %s algo"%(User_2,before_user2))
    print("%s's address is %s"%(User_1,acc1))
    print("%s's address is %s"%(User_2,acc2))

    ctc_user1 = rpc("/acc/contract", acc_user1)

    def Usr1():
        fund = input("Enter amount you want to swap: ")
        def getadd():
            return acc2
        rpc_callbacks(
            "/backend/User1",
            ctc_user1,
            dict(funds=rpc("/stdlib/parseCurrency", fund), getaddress = getadd)
        )

    user1 = Thread(target = Usr1)
    user1.start()

    def Usr2():
        fund = input("Enter amount you want to swap user2: ")
        ctc_user2 =  rpc("/acc/contract", acc_user2, rpc("/ctc/getInfo", ctc_user1))

        rpc_callbacks(
            "/backend/User2",
            ctc_user2,
            dict(funds=rpc("/stdlib/parseCurrency", fund))
        )
        rpc("/forget/ctc")

    user2 = Thread(target= Usr2)
    user2.start()
    user1.join()
    user2.join()

    after_user1 = get_balance(acc_user1)
    after_user2 = get_balance(acc_user2)

    print("%s went from %s to %s" % (User_1,before_user1, after_user1))
    print("%s went from %s to %s" % (User_2,before_user2, after_user2))

    rpc("/forget/acc", acc_user1, acc_user2)
    rpc("/forget/ctc", ctc_user1)

if __name__ == "__main__":
    main()
