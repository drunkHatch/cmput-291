#List orders
    #see all orders 
    #orders will be sorted with proper details shown
    #the results are properly shown when there are more than 5 orders
    #can select an order and see the details (as per spec)
    
def list_o():
     #the order id, order date, the number of products ordered and the total price etc
    
    c.execute("SELECT o.oid, o.odate, COUNT(*), SUM(l.qty * l.uprice) FROM orders o LEFT JOIN olines l \
    ON o.oid = l.oid GROUP BY o.oid HAVING o.cid =:cid ORDER BY o.odate;", {"cid":current_cid})
    
    orders_output = c.fetchall()
    
    show_list = []
    for i in range(len(orders_output)):
        show_list.append(orders_output[i])
        if (i + 1) % 5 == 0 or i == len(orders_output):
            valid = False
            while(not valid):
                for j in range(5):
                    print(show_list[j])         
                    
                user_action = input("Please enter detail to select an order to show details\n Please enter nextpage to show more orders: \n Please enter exit to")
                if user_action == "detail":
                    # enter oid
                    chosen_oid = input("Please enter order id: ")
                    #tracking details
                    c.execute("SELECT d.trackingno d.pickUpTime d.dropOffTime od.address FROM deliveries d, orders od WHERE d.oid = o.oid AND o.oid =:oid;", {"oid":chosen_oid})
                    details1 = c.fetchall()
                    # product details
                    c.execute("SELECT l.sid, s.name, l.pid, p.name l.qty, p.unit, l.uprice FROM olines l, products p, stores s WHERE l.sid = s.sid AND l.pid = p.pid AND l.oid =:oid GROUP BYl.pid;", {"oid":chosen_oid})
                    details2 = c.fetchall()
                    
                    print("delivery information")
                    print("trackingno pickUpTime dropOffTime address")
                    print(details1)
                    
                    print("products information")
                    print("sid sname pid pname qty unit uprice")
                    print(details2)
                    
                    valid = False        
                elif user_action == "nextpage":
                    valid = True
                    show_list = []
                elif user_action == "exit":
                    show_list = []
                    return
                else:
                    print("wrong action, please enter command again")
                    valid = False
    