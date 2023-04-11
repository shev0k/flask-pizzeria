from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request
import csv
from flask import render_template
from flask import redirect
import smtplib
from msilib.schema import Billboard
import email
import string

# Variables on for the indexpage
username = "Account"

# admin accounts
marioIsLoggedin = False
messageLoginMario = ""

# Log in user
userLoggedIn = False

# Order
pizzaOrderList=[]
pastaOrderList = []
drinkOrderList=[]
desserOrderList=[]

orderTotal = 0
roundedOrderTotal = 0

# (order) lists to text to add to html
pizzaListText = ""

#Hardedcoded pizzas :(
amountPizzamar = 0
costPizzamar = 0
addPizzamar = False
amountPizzasi = 0
costPizzasi = 0
amountPizzabbq = 0
costPizzabbq = 0
amountPizzapar = 0
costPizzapar = 0
amountPizzacap = 0
costPizzacap = 0
amountPizzache = 0
costPizzache = 0

#Hardcoded drinks
amountWater = 0
costWater = 0
amountWine = 0
costWine = 0
amountMoretti = 0
costMoretti = 0

#Hardcoded pastas
amountPastatomato = 0
costPastatomato = 0
amountBolognese = 0
costBolognese = 0
amountCarbonara = 0
costCarbonara = 0

#Hardcoded desserts
amountLavacake = 0
costLavacake = 0
amountPancakes = 0
costPancakes = 0
amountCookie = 0
costCookie = 0

# Kitchen order
orderIdsDictionary={} #dictionary

#ratings
ratingsList=[]
reviewList=[]

statusA = ""
statusB = ""

error = ""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def landingpage():
    global username, messageLoginMario, marioIsLoggedin
    return render_template("index.html", name=username, hellomario = messageLoginMario, mariologin = marioIsLoggedin) #orderpizza

@app.route("/index.html")
def redirectToLandingpage():
    return redirect("/")

@app.route("/about.html")
def about():
    global marioIsLoggedin, username #orderpizza
    return render_template("about.html", mariologin=marioIsLoggedin, name=username) #orderpizza=orderpizza,

@app.route("/account.html")
def signuppage():
    global error #gives the user an error when the password or username is incorrect.
    return render_template("account.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    global username, userLoggedIn, error, marioIsLoggedin, messageLoginMario

    username = request.form['username']
    checkPassword = request.form['password']
    marioIsLoggedin=False

    with open("data.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if username in row and checkPassword in row: #if name exists within the csv
                if username == "Mario " and checkPassword == "mario": #log in as Mario (access to reviews)
                    messageLoginMario='Greetings Mario good to see you here'
                    marioIsLoggedin=True
                    userLoggedIn= True
                if username == "Luigi" and checkPassword == "luigi": #log in as Luigi
                    userLoggedIn= True
                    return redirect ("/kitchen-orders.html") #Go to the pizza orders page
                userLoggedIn= True
                return redirect("/")
            
    userLoggedIn= True #how does this work?
    error="login not succesful make sure you spell your name and password correctly."
    return redirect("/account.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    global error,check1,check2,emails,notes,alreadylogino,dp,check3,name

    open("data.csv", 'a').close()
    open("data.csv", 'r').close()
    error=""
    name = request.form['username']
    gmail = request.form['email']
    passwordsign  = request.form['password']
    passwordlist= list(passwordsign)
    
    check1=False
    check2=True
    check3=False
    mcheck1 = False
    mcheck2 = False
    mcheck3 = False
    mcheck4 = False

    
    if len(passwordsign) >= 8: 
        for i in passwordlist:
            if i in acceptcapital:
                mcheck1 = True
        for i in passwordlist:
            if i in acceptlower:
                mcheck2 = True
        for i in passwordlist:
            if i in acceptnumber:
                mcheck3 = True
        for i in passwordlist:
            if i in acceptspecial:
                mcheck4 = True       

    if mcheck1 == True and mcheck2 == True and mcheck3 == True and mcheck4 == True:                                
        check1=True
    
    with open("data.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            dp = row
            if gmail in dp:
                check2=False        

    if "@" in gmail and "." in gmail:
        check3 = True
    

    if check1 == True and check2 == True and check3 == True:
        alreadylogino=True
        with open("data.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow({name:[name],gmail:gmail,passwordsign:[password]})

        return redirect("/")

    
    elif check2 == False and check1 == True and check3 == True:
        error = "The email was already used"

    elif check1 == False and check2 == True and check3 == True:
        error = "The password is not long enough also make sure to add at least one lowercase and uppercase letter one number and one special character"

    elif check3 == False and check2 == True and check1 == True:
        error = "Incorrect email input"

    else:
        error = "Multiple things went wrong try again make sure you put in a valid email and a password of at least 8 characters"

    return redirect("/account.html")

@app.route("/kitchen-orders.html")
def kitchenPage():
    return render_template("luigi-cart.html", order=orderIdsDictionary)

@app.route("/remove", methods=["GET", "POST"])
def removeorder():
    idremover=int(request.form["afval"])
    if idremover in orderIdsDictionary:
        del orderIdsDictionary[idremover]
    return redirect("/luigi-cart.html")

@app.route("/index.html#PIZZA")
def pizzasection():
    return render_template("index.html#PIZZA")

@app.route("/addmar", methods=["GET", "POST"])
def normalpizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzamar, costPizzamar, addPizzamar
    if userLoggedIn== True:
        addPizzamar = True
        orderTotal+=7.99
        costPizzamar+=7.99
        amountPizzamar +=1
        return redirect("/index.html#PIZZA")  
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addsicilian", methods=["GET", "POST"])
def salamipizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzasi, costPizzasi
    if userLoggedIn== True:
        orderTotal+=7.49        
        costPizzasi+=7.49    
        amountPizzasi +=1
        return redirect("/index.html#PIZZA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addbbq", methods=["GET", "POST"])
def hawaiipizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzabbq, costPizzabbq
    if userLoggedIn== True:
        orderTotal+=8.49       
        costPizzabbq+=8.49 
        amountPizzabbq +=1
        return redirect("/index.html#PIZZA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addpar", methods=["GET", "POST"])
def funghipizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzapar, costPizzapar
    if userLoggedIn== True:
        orderTotal+=8.99
        costPizzapar +=8.99
        amountPizzapar +=1
        return redirect("/index.html#PIZZA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addcap", methods=["GET", "POST"])
def tonnopizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzcap, costPizzacap
    if userLoggedIn== True:
        orderTotal +=7.49
        costPizzacap +=7.49
        amountPizzcap +=1
        return redirect("/index.html#PIZZA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/add4chee", methods=["GET", "POST"])
def poyopizza():
    global orderTotal, userLoggedIn, loginfirst, amountPizzache, costPizzache
    if userLoggedIn== True:
        orderTotal+=9.99
        costPizzache +=9.99
        amountPizzache +=1
        return redirect("/index.html#PIZZA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/index.html#DRINKS")
def drinksection():
    return render_template("index.html#DRINKS")

@app.route("/addwater", methods=["GET", "POST"])
def water():
    global orderTotal, userLoggedIn, loginfirst, amountWater, costWater
    if userLoggedIn== True:
        orderTotal+=0.99
        costWater+=0.99
        amountWater +=1
        return redirect("/index.html#DRINKS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addmor", methods=["GET", "POST"])
def bellini(): 
    global orderTotal, userLoggedIn, loginfirst, amountMoretti, costMoretti
    if userLoggedIn== True:
        orderTotal+=2.49
        costMoretti+=2.49
        amountMoretti +=1
        return redirect("/index.html#DRINKS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addwin", methods=["GET", "POST"])
def wine():
    global orderTotal, userLoggedIn, loginfirst, amountWine, costWine
    if userLoggedIn== True:
        orderTotal+=8.99
        costWine+=8.99        
        amountWine +=1
        return redirect("/index.html#DRINKS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")
@app.route("/index.html#PASTA")

def pastasectione():
    return render_template("index.html#PASTA")

@app.route("/addbur", methods=["GET", "POST"])
def carbonaraPasta():
    global orderTotal, userLoggedIn, loginfirst, amountPastatomato, costPastatomato
    if userLoggedIn== True:
        orderTotal+=7.99
        costPastatomato+=7.99
        amountPastatomato +=1
        return redirect("/index.html#PASTA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addbol", methods=["GET", "POST"])
def bolognese():
    global orderTotal, userLoggedIn, loginfirst, amountBolognese, costBolognese
    if userLoggedIn== True:
        orderTotal+=7.49
        costBolognese+=7.49
        amountBolognese +=1
        return redirect("/index.html#PASTA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addcar", methods=["GET", "POST"])
def carbonara():
    global orderTotal, userLoggedIn, loginfirst, amountCarbonara, costCarbonara
    if userLoggedIn== True:
        orderTotal+=8.49
        costCarbonara+=8.49
        amountCarbonara +=1
        return redirect("/index.html#PASTA")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/index.html#DESSERTS")
def dessertssection():
    return render_template("index.html#DESSERTS")

@app.route("/addcho", methods=["GET", "POST"])
def lavacake():
    global orderTotal, userLoggedIn, loginfirst, amountLavacake, costLavacake
    if userLoggedIn== True:
        orderTotal+=2.49
        costLavacake+=2.49
        amountLavacake +=1
        return redirect("/index.html#DESSERTS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/adddut", methods=["GET", "POST"])
def pancakes():
    global orderTotal, userLoggedIn, loginfirst, amountPancakes, costPancakes
    if userLoggedIn== True:
        orderTotal+=2.99
        costPancakes+=2.99
        amountPancakes +=1
        return redirect("/index.html#DESSERTS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")

@app.route("/addgia", methods=["GET", "POST"])
def bigCookie():
    global orderTotal, userLoggedIn, loginfirst, amountCookie, costCookie
    if userLoggedIn== True:
        orderTotal+=1.99
        costCookie+=1.99
        amountCookie +=1
        return redirect("/index.html#DESSERTS")
    else:
        loginfirst="you need to log in first"
    return redirect("/account.html")


@app.route("/shoppingcart.html")
def carty():
    global pizzaListText, pizzaOrderList, costPizzamar, orderTotal, amountPizzamar , amountPizzamar,costPizzamar
    pizzaOrderList.append(("","",""))
    pastaOrderList.append(("","",""))
    drinkOrderList.append(("","",""))
    desserOrderList.append(("","",""))

    for i in range(len(pizzaOrderList)):
        if amountPizzamar > 0:
            if "Pizza margharita di bufala" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza margharita di bufala",costPizzamar,amountPizzamar))
            else:
                pizzaOrderList.append(("Pizza margharita di bufala",costPizzamar,amountPizzamar))
        if amountPizzasi > 0:
            if "Pizza sicilian sausage & salami" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza sicilian sausage & salami",costPizzasi,amountPizzasi))
            else:
                pizzaOrderList.append(("Pizza sicilian sausage & salami",costPizzasi,amountPizzasi))
        if amountPizzabbq > 0:
            if "Pizza BBQ meatlovers" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza BBQ meatlovers",costPizzabbq,amountPizzabbq))
            else:
                pizzaOrderList.append(("Pizza BBQ meatlovers",costPizzabbq,amountPizzabbq))
        if amountPizzapar > 0:
            if "Pizza parmigiana eggplant" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza parmigiana eggplant",costPizzapar,amountPizzapar)) 
            else:
                pizzaOrderList.append(("Pizza parmigiana eggplant",costPizzapar,amountPizzapar)) 
        if amountPizzacap > 0:
            if "Pizza caprese" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza caprese",costPizzacap,amountPizzacap))
            else:
                pizzaOrderList.append(("Pizza caprese",costPizzacap,amountPizzacap))
        if amountPizzache > 0:
            if "Pizza 4 cheese" in pizzaOrderList[i]:
                pizzaOrderList.pop(i)
                pizzaOrderList.append(("Pizza 4 cheese",costPizzache,amountPizzache))
            else:
                pizzaOrderList.append(("Pizza 4 cheese",costPizzache,amountPizzache))

    for i in range(len(pastaOrderList)):
        if amountPastatomato > 0:
            if "Pasta burst tomato" in pastaOrderList[i]:
                pastaOrderList.pop(i)
                pastaOrderList.append(("Pasta burst tomato",costPastatomato,amountPastatomato))
            else:
                pastaOrderList.append(("Pasta burst tomato",costPastatomato,amountPastatomato))
        if amountBolognese > 0:
            if "Spaghetti bolognese" in pastaOrderList[i]:
                pastaOrderList.pop(i)
                pastaOrderList.append(("Spaghetti bolognese",costBolognese,amountBolognese))
            else:
                pastaOrderList.append(("Spaghetti bolognese",costBolognese,amountBolognese))
        if amountCarbonara > 0:
            if "Spaghetti carbonara" in pastaOrderList[i]:
                pastaOrderList.pop(i)
                pastaOrderList.append(("Spaghetti carbonara",costCarbonara,amountCarbonara))
            else:
                pastaOrderList.append(("Spaghetti carbonara",costCarbonara,amountCarbonara))

    for i in range(len(drinkOrderList)):
        if amountMoretti > 0:
            if "Moretti" in drinkOrderList[i]:
                drinkOrderList.pop(i)
                drinkOrderList.append(("Moretti",costMoretti,amountMoretti))
            else:
                drinkOrderList.append(("Moretti",costMoretti,amountMoretti))
        if amountWine > 0:
            if "Wine" in drinkOrderList[i]:
                drinkOrderList.pop(i)
                drinkOrderList.append(("Wine",costWine,amountWine))
            else:
                drinkOrderList.append(("Wine",costWine,amountWine))
        if amountWater > 0:
            if "Water" in drinkOrderList[i]:
                drinkOrderList.pop(i)
                drinkOrderList.append(("Water",costWater,amountWater))
            else:
                drinkOrderList.append(("Water",costWater,amountWater))

    for i in range(len(desserOrderList)):
        if amountLavacake > 0:
            if "Chocolate lava cake" in desserOrderList[i]:
                desserOrderList.pop(i)
                desserOrderList.append(("Chocolate lava cake",costLavacake,amountLavacake))
            else:
                desserOrderList.append(("Chocolate lava cake",costLavacake,amountLavacake))
        if amountPancakes > 0:
            if "Dutch mini pancakes" in desserOrderList[i]:
                desserOrderList.pop(i)
                desserOrderList.append(("Dutch mini pancakes",costPancakes,amountPancakes))
            else:
                desserOrderList.append(("Dutch mini pancakes",costPancakes,amountPancakes))
        if amountCookie > 0:
            if "Giant chocolate chip cookie" in desserOrderList[i]:
                desserOrderList.pop(i)
                desserOrderList.append(("Giant chocolate chip cookie",costCookie,amountCookie))
            else:
                desserOrderList.append(("Giant chocolate chip cookie",costCookie,amountCookie))

    if "" in pizzaOrderList[0] and len(pizzaOrderList) >1:
        pizzaOrderList.pop(0)
    if "" in desserOrderList[0] and len(desserOrderList) >1:
        desserOrderList.pop(0)
    if "" in drinkOrderList[0] and len(drinkOrderList)>1:
        drinkOrderList.pop(0)
    if "" in pastaOrderList[0] and len(pastaOrderList)>1:
        pastaOrderList.pop(0)

    pizzaListText = pizzaOrderList
    orderTotal = round(orderTotal,2)
    return render_template("shoppingcart.html", pizzalust=pizzaListText, pastalust = pastaOrderList, drinklust = drinkOrderList, dessertlust = desserOrderList, totals = orderTotal)

@app.route("/paypal", methods=["GET", "POST"])
def writeCardInfoToCSV():
    global notes
    cardname= request.form['cardholder-name']
    cardNr = request.form['card-number']
    cvvs = request.form['cvv']
    expiMonth  = request.form['month']
    expiYear  = request.form['year']

    with open("transactionInfo.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([cardname, cardNr, cvvs, expiMonth, expiYear])

    return redirect("/combine")

@app.route("/reset", methods=["GET", "POST"])
def remove():
    global orderTotal, pizzaOrderList, pastaOrderList, drinkOrderList, desserOrderList
    pizzaOrderList=[]
    pastaOrderList = []
    drinkOrderList=[]
    desserOrderList=[]
    orderTotal=0
    return redirect("/shoppingcart.html")

@app.route("/resetcash", methods=["GET", "POST"])
def removecash():
    global orderTotal, pizzaOrderList, pastaOrderList, drinkOrderList, desserOrderList
    pizzaOrderList=[]
    pastaOrderList = []
    drinkOrderList=[]
    desserOrderList=[]
    orderTotal=0
    return redirect("/cart_cash.html")

@app.route("/cart_cash.html")
def cash():
    global roundedOrderTotal, orderTotal
    roundedOrderTotal = round(orderTotal,2)
    return render_template("cart_cash.html", pizzalust=pizzaListText, pastalust=pastaOrderList, drinklust=drinkOrderList, dessertlust=desserOrderList, totals=roundedOrderTotal)

@app.route("/paypal", methods=["GET", "POST"])
def paypal():
    global notes
    cardname= request.form['cardholder-name']
    cn = request.form['card-number']
    cvvs = request.form['cvv']
    expim  = request.form['month']
    expiy  = request.form['year']
    notes =request.form["discount-token"]

    with open("transactionInfo.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([cardname, cn, cvvs, expim, expiy])

    return redirect("/combine")

@app.route("/prep.html", methods=["POST", "GET"])
def progress():
    global name,marioIsLoggedin,prep
    
    if request.method == "POST":
        prepeth = request.get_json()
        prep=prepeth["glomp"]
        print(prep)
    if prep == 1:
        return redirect("/oven.html")
    
    return render_template("prep.html", statusA=statusA,statusB=statusB, name=name, mariologin=marioIsLoggedin)

@app.route("/oven.html", methods=["POST", "GET"])
def oven():
    global statusA,statusB,name, marioIsLoggedin,done
    
    if request.method == "POST":
        doneth = request.get_json()
        done=doneth["sjwomp"]
        print(done)
    if done == "T":
        return redirect("/ready.html")
       
    return render_template("oven.html", statusA=statusA,statusB=statusB, name=name, mariologin=marioIsLoggedin)

@app.route("/ready.html", methods=["POST", "GET"])
def ready():
    global statusA,statusB,name,marioIsLoggedin,readitti
    if request.method == "POST":
        revieweth = request.get_json()
        readitti=revieweth["blonk"]
        print(readitti)
    if readitti == 1:
        return redirect("/leave-a-review.html")
        
    return render_template("ready.html", statusA=statusA,statusB=statusB,name=name, mariologin=marioIsLoggedin)

@app.route("/combine")
def combino():
    global notes,orderIdsDictionary,prep,done,readitti
    prep=0
    done=0
    readitti=0
    ids=1
    while ids in orderIdsDictionary:
        ids+=1
    orderIdsDictionary[ids] = {"orderid":ids,"pizza-list":pizzaOrderList,"pasta-list":pastaOrderList,"drink-list":drinkOrderList,"dessert-list":desserOrderList,"notess":notes}

    return redirect("/prep.html")

@app.route("/leave-a-review.html")
def reviewi():
    return render_template("leave-a-review.html")

@app.route("/ratings.html")
def ratingsread():
    global name,marioIsLoggedin,ratingsList,reviewList,averagerating
    if len(ratingsList) != 0:
        averagerating= round( float(sum(ratingsList)/len(ratingsList)) ,2)
    
    return render_template("ratings.html",orderpizza=pizzaOrderList,name=name, mariologin=marioIsLoggedin,avg=averagerating,com=reviewList)

@app.route("/review", methods=["GET", "POST"])
def reviewleave():
    global comment,ratingsList,reviewList
    rating = float(request.form.get("stars"))
    comment = request.form["critic"]
    ratingsList.append(rating)
    reviewList.append(comment)
    if len(reviewList) > 5:
        del reviewList[0]
    print(rating)
    return redirect("/")

@app.route("/info", methods=["GET", "POST"])
def testyget():
    global notes
    notes =request.form["discount-token"]
    
    return redirect("/combine")