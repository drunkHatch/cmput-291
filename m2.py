import sqlite3
import itertools
import random
from operator import itemgetter, attrgetter
from random import *

database ='p1.db'
#basket= dict()
basket={"p10 20":110,}

conn = sqlite3.connect(database)

c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

current_id = -11


def search(id):
    global c, conn
    global basket
    
    print("search")
    keywords =[]
    keyword = input("please enter your keywords,\n separate each keyword by whitespace:\n")
    keywords = str.split(keyword)
    parent_list = []
    # query 1 begins
    for each in keywords:
        #each = "'"+"%"+each+"%"+"'"
        
        c.execute("select p.pid, p.name,p.unit,count(p.pid),count(c.sid)from \
        products p ,carries c WHERE p.name LIKE ? and p.pid = c.pid group \
        by p.pid order by count(p.pid) DESC;", ('%'+each+'%',))
         
        child_tuple = c.fetchall()
        for i in range(0,len(child_tuple)):
            parent_list.append(list(child_tuple[i]))
    
    numLines=len(parent_list)
    #print(parent_list)
    output1_list = []
    for i in range(len(parent_list)):  
        for j in range (i+1,len(parent_list)):           
            if (parent_list[i][0] == parent_list[j][0]):  
                #print("parent_list item",parent_list[i-1])
                parent_list[i][3] += parent_list[j][3]
                parent_list[j][3] = 0
    
    for i in range(len(parent_list)):  
        if (parent_list[i][3] != 0):
            output1_list.append (parent_list[i])

    #for each in output1_list:
            #print(each)
    numLines=len(parent_list)
    #print("length is "+str(numLines))      
    # query 1 ends, keywords lists
    
    #query 2 beings, last 7 days
    output2_list = []
    c.execute("SELECT olines.pid, sum(qty) FROM orders LEFT JOIN olines ON orders.oid = olines.oid WHERE date(odate, '+7 day') >= date('now') GROUP BY olines.pid;")
    child_tuple = c.fetchall()
    for i in range(0,len(child_tuple)):
        output2_list.append(list(child_tuple[i]))  
    #print(output2_list)
    #query 2 ends, last 7 days
    
    # query 3 begins, in stock #
    output3_list = []
    c.execute("SELECT c.pid, COUNT(s.sid) FROM carries c, stores s WHERE c.sid=s.sid AND qty>0 GROUP BY c.pid")
    child_tuple = c.fetchall()
    for i in range(0,len(child_tuple)):
        output3_list.append(list(child_tuple[i]))   
        
    #print(output3_list)
    # query 3 ends, in stock #
    
    # query 4 begins, min among all
    output4_list = []
    
    c.execute("SELECT DISTINCT c.pid, uprice FROM carries c, stores s WHERE c.sid=s.sid AND uprice <= (select min(uprice) FROM carries c2 WHERE c.pid=c2.pid);")
    child_tuple = c.fetchall()
    for i in range(0,len(child_tuple)):
        output4_list.append(list(child_tuple[i]))    
    # query 4 ends, min among all
    
    # query 5 begins, min among in stock
    output5_list = []
    
    c.execute("SELECT DISTINCT c.pid, c.uprice FROM carries c, stores s WHERE c.qty > 0 AND c.uprice <= (select min(uprice) FROM carries c2 WHERE c.pid=c2.pid AND c2.qty>0);")
    child_tuple = c.fetchall()
    for i in range(0,len(child_tuple)):
        output5_list.append(list(child_tuple[i]))    

    # query 5 ends, min among in stock
    merge(output1_list, output3_list)
    merge(output1_list, output4_list)
    merge(output1_list, output5_list)
    merge(output1_list, output2_list)
    
    output1_list = sorted(output1_list, key=itemgetter(3), reverse=True)
    
    
    count = 0  
    length = len(output1_list)
    current = []
    for n in range(length):
        count += 1
        current.append(output1_list[n])
        print(n, output1_list[n])
        if count == 5 or n == length - 1:
            ope = "wrong operations"
            while(ope == "wrong operations"):
                ope = operations()
                if ope ==  "select":
                    chosen_pid = input("Please enter product id :")
                    for item in current:
                        if item[0] == chosen_pid:
                            # details begins
                            c.execute("SELECT * FROM products WHERE pid=:id;", {"id":chosen_pid})
                            elet1 = c.fetchall()
                            print("Product id:",elet1[0][0], "\nName:",elet1[0][1], "\nUnit:",elet1[0][2],"\nCategory: ",elet1[0][3])
                            
                            c.execute("SELECT s.sid, s.name, c.qty, c.uprice FROM carries c, stores s WHERE c.sid=s.sid AND c.pid=:id GROUP BY s.sid;", {"id":chosen_pid})
                            elet2=[]
                            child_tuple = c.fetchall()
                            for i in range(0,len(child_tuple)):
                                elet2.append(list(child_tuple[i]))
                                
                            c.execute("SELECT olines.sid, sum(qty) FROM orders LEFT JOIN olines ON orders.oid = olines.oid WHERE date(odate, '+7 day') >= date('now') AND olines.pid=:id GROUP BY olines.sid;", {"id":chosen_pid})
                            elet3=[]
                            child_tuple = c.fetchall()
                            for i in range(0,len(child_tuple)):
                                elet3.append(list(child_tuple[i]))   
                            merge2(elet2, elet3)
                            firstTemp = []
                            secondTemp = []
                            
                            for i in range (len(elet2)):
                                if elet2[i][2]!= 0:
                                    firstTemp.append(elet2[i])
                                elif elet2[i][2]== 0:   
                                    secondTemp.append(elet2[i])
                                    
                            firstTemp=sorted(firstTemp,key=itemgetter(3), reverse=False)
                            secondTemp=sorted(secondTemp,key=itemgetter(3), reverse=False)
                            final = firstTemp + secondTemp
                            print(final)
                            
                            endsearch =input("Wana add this item yes/y,no/n./n")
                            if endsearch =="y":
                                store_id=input("Where are you gona buy it from?, Plz enter store id/n")
                                newqty = input("How much are you gona buy it/n")
                                if newqty == None:
                                    newqty =1
                                newItem={chosen_pid + ' '+ str(store_id):newqty}
                                basket.update(newItem)
                                return
                            if endsearch =="n":
                                customer(id)
                                return
                            #details ends
                        elif item == current[-1]:
                            print("no matching")
                            ope = "wrong operations" 
            count = 0
            current = []

def operations():
    a_input = input("Please enter command :")
    if a_input == "nextpage":
        return "nextpage"
    elif a_input == "select":
        return "select"
    else:
        print("wrong operations")
        return "wrong operations"
        
    #return 0
def merge(output, adder):
    for i in range(len(output)):  
        for j in range (len(adder)):           
            if (output[i][0] == adder[j][0]):  
                output[i].append(adder[j][1])
def merge2(output, adder):
    for i in range(len(output)):  
        for j in range (len(adder)):           
            if (output[i][0] == adder[j][0]):  
                output[i].append(adder[j][1])
    for i in range(len(output)): 
        if len(output[i]) != 5:
            output[i].append(0) 
def place_order(id):
    global c, conn, basket
    valid = True
    oid = randint(1, 1000)
    c.execute("SELECT oid FROM olines;")
    oids = c.fetchall()
    while ( oid in oids):
        oid = randint(1, 1000)
    if oid not in oids:
        c.execute("SELECT address FROM customers WHERE cid =:id;", {"id":id})
        tempaddress = c.fetchone()    
        address = tempaddress[0]
    while(valid ):
        # CHECK QTY AND WARNING 
        for item in basket:
            tempt = str.split(item, ' ')

            value = basket[item]

            c.execute("SELECT qty FROM carries WHERE pid =? AND sid =?;", (tempt[0], tempt[1]))
            qty = c.fetchone()
            qty=list(qty)
           
            # CHANGE QTY, DELETE PRODUCT
            new_qty = 0
            while (qty[0] < int(value)):
                new_qty = input("Not enough quantity in stock for "+ tempt[0] +" please enter new quantity to buy(0 means delete):\n")             
                valid = False
                basket[item] = new_qty
                value = new_qty         
    # UPDATE DB
            booked = qty[0]-int(new_qty)           
            c.execute("UPDATE carries SET qty=? WHERE sid=? and pid=?;",(booked,tempt[1], tempt[0]))
            conn.commit() 
            c.execute("SELECT uprice FROM carries WHERE pid =? AND sid =?;", (tempt[0], tempt[1]))
            uprice = c.fetchone()
            uprice=list(uprice)
            print("oid",oid)
            print("id",id)
            print("sid",tempt[1])
            print("pid",tempt[0])
            print("qty",new_qty)
            print("uprice",uprice[0])
            
            c.execute("INSERT INTO orders VALUES (?,?,odate= datetime('now'), ?);" (oid,id,address))
            conn.commit()             
            c.execute("insert into olines values (?, ?, ?, ?, ?);",(int(oid),int(tempt[1]),str(tempt[0]),int(new_qty),float(uprice[0])))
            conn.commit() 
    # CLEAR BASKET and commit all the changes

        basket={}
def list_order(id):
    global c, conn
    
    
    print("list_order")
def setup(id):
    global c, conn
    
    print("setup")
def Update(id):
    global c, conn
    
    print("Update")
def add(id):
    global c, conn
    
    print("add")



def customers(id):
    global c, conn
    global bakset
    
    """

    """
    print("Here is current item in your \n", basket)
    
    function_type = input('Here are avaliable functions\n Search for products(Enter s)\n Place an order(Enter p)\n List orders(Enter L)\n')

    if function_type == "s":
        search(id)
        customers(id)
    elif function_type == "p":
        place_order(id)
        customers(id)
    elif function_type == "l":
        list_order(id)
        customers(id)
    elif function_type == "o":
        main()
    # Search for products


def agents (id):
    global c, conn
    
    print('agents function')
    function_type = input('Here are avaliable functions\n Set up a delivery(Enter s)\n \
    Update a delivery(Enter u)\n Add to stock(Enter l)\n')
    if function_type == "s":
        setup(id)
        agents(id)
    elif function_type == "u":
        Update(id)
        agents(id)
    elif function_type == "l":
        add(id)
        agents(id)
    elif function_type == "o":
        main()

def check_exist(c_id, c_pwd):
    # 
    c.execute("SELECT cid FROM customers WHERE cid=:id AND pwd=:pd;", {"id":c_id,"pd":c_pwd}) 
    row = c.fetchone()
    
    if row == None:
        valid = False
    else:
        valid = True
    
    return valid

def check_id(id):
    c.execute("SELECT cid FROM customers WHERE cid=:id;", {"id":id}) 
    row = c.fetchone()
    if row == None:
        valid = True
    else:
        valid = False
    return valid
    
def login(login_type):
    global c, conn
    """
    check login_type
    check sign in/up


    """
    if login_type == "c":
        sign = input("Sign in(i)/Sign up(u): ")
        if sign == "i":
            # complete later
            c_id = input("Please fuking enter your customer id: \n")
            c_pwd = input("Please enter your password: \n")
             # check valid
            valid = check_exist(c_id, c_pwd)
             

            if valid:
                customers(c_id)
            else:
                print("Login failed, Please try again")
                login(login_type)
                #if valid == True:
        elif sign == "u":
            # complete later
            c_id = input("Please fuking enter your new customer id: \n")
            c_pwd = input("Please enter your new password: \n")

            valid = check_id(c_id)
            
            
            if valid:
                name = input("Please enter your name\n")
                address = input("Please enter your address\n")
                
                c.execute("INSERT INTO customers VALUES (?,?,?,?);", (c_id, name, address, c_pwd))
                #c.execute("INSERT INTO Contacts VALUES (?, ?, ?, ?);", (firstname, lastname, phone, email))
                conn.commit()
                print("success registry")
                login(login_type)                
            else:
                print("failed, plz regi again")
                login(login_type)

        else:
            print("login error")
            login(login_type)

    elif login_type == "a":
        a_id = input("Please fuking enter your agent id: \n")
        a_pwd = input("Please enter your password: \n")
        # check valid
        valid = True

        if valid == True:
            agents(a_id)
    else:
        print("error")

def select_type():
    """ argument: None
    cheak login type: customer, agent, error
    exit program
    """
    login_type = input("Choose your login type: customer(c)/agent(a)\nenter e to exit\n")

    if login_type == "c":
        print("customers login")
    elif login_type == "a":
        print("agents login")
    elif login_type == "e":
        exit(1)
    else:
        print("error")
        login_type = select_type()

    return login_type

def main():
 
    #type 1
    #login_type = select_type() # correct!!
    #login(login_type)
    
    customers("c10")


main()
