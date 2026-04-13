import json
import random
import string
from pathlib import Path


class Bank:
    database='data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("no such file exist ")
    except Exception as err:
          print(f"an exception occured as {err}")  
    @classmethod
    def __update(cls):
        with open(cls.database,'w')as fs:
            fs.write(json.dumps(Bank.data))
    
    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return"".join(id)

    def createaccount(self):
        info={
            "name":input("tell your name :-"),
            "age":int(input("tell your age:-")),
            "email":input("tell your email:-"),
            "pin":input("create a pin of 4 digit:-"),
            "accountNo":Bank.__accountgenerate(),
            "balance":0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("Sorry you cannot create your account")
        else:
            print("Account has been created successfully")
        for i in info:
            print(f"{i}:{info[i]}")
        print("please note down your account number")
        Bank.data.append(info)
        Bank.__update()
    def depositmoney(self):
        accnumber=input("tell your account no:-")
        pin=input("tell your pin no:-")
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]

        if userdata==False:
            print("no data found")
        else:
            amount=int(input("how much you want to deposit"))
            if amount>10000 and amount<0:
                print("Sorry the amount is too much you can deposit below 10 thousand")
            else:
                print(userdata)
                userdata[0]['balance']+=amount
                Bank.__update()
                print("Amount deposit successfully")
       
    def withdrawmoney(self):
        accnumber=input("tell your account no:-")
        pin=input("tell your pin no:-")
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]

        if userdata==False:
            print("no data found")
        else:
            amount=int(input("how much you want to withdraw"))
            if userdata[0]['balance'] <amount:
                print("Sorry you dont't have that much money")
            else:
                print(userdata)
                userdata[0]['balance']-=amount
                Bank.__update()
                print("Amount withdrew successfully") 

    def showdetails(self):
        accnumber=input("Enter your account number:-")
        pin=input("tell your pin number:-")
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]
        print("your information are \n\n\n")
        for i in userdata[0]:
            print(f"{i}:{userdata[0][i]}")
    

    def updatedetails(self):
        accnumber=input("Enter your account number:-")
        pin=input("tell your pin number:-")
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]

        if userdata==False:
            print("no such user found")
        else:
            print("you cannot change the age,accountnumber,balance")

            print("Fill the details for change or leave it empty if no change")
            newdata={

                "name":input("please tell your name or press enter:- "),
                "email":input("please tell your new Email or press enter to skip:-"),
                "pin":input("enter new pin or press enter to skip:-")
            }
            if newdata["name"]=="":
                newdata["name"]=userdata[0]["name"]
            if newdata["email"]=="":
                newdata["email"]=userdata[0]["email"]
            if newdata["pin"]=="":
                newdata["pin"]=userdata[0]["pin"]
            
            newdata['age']=userdata[0]['age']
            newdata['accountNo']=userdata[0]['accountNo']
            newdata['balance']=userdata[0]['balance']
            if type(newdata['pin'])==str:
                newdata['pin']=int(newdata['pin'])
            
            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            Bank.__update()
            print("detailed update successfully.")
    
    def delete(self):
        accnumber=input("Enter your account number:-")
        pin=input("tell your pin number:-")
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]
        if userdata == False:
            print("sorry no such data found.")
        else:
            check=input("press y if you actually want to delete the account or press n")
            if check=='n' or check=='N':
                print("bypassed")
            else:
                index=Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully")
                Bank.__update()



user=Bank()
print("Press 1. For creating a bank account")
print("Press 2. For deposit money")
print("Press 3. Withdraw the money")
print("Press 4. For Details")
print("Press 5. For updating the details")
print("Press 6. For delete your account")

check = int(input("Enter your choice: "))

if check==1:
    user.createaccount()

if check==2:
    user.depositmoney()

if check==3:
    user.withdrawmoney()

if check==4:
    user.showdetails()

if check==5:
    user.updatedetails()

if check == 6:
    user.delete()