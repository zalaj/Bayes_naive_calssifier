##moj X je class, za katerega iščemo klasifikator

##-------
##Funkcija za branje CSV, ki vrne slovar z vredNostmi
##-------
def read_csv (csv_file):
    
    import csv
    file = open(csv_file, 'rt', encoding = 'ascii')
    read = csv.reader(file)

    rownum=0
    header=[]
    training_data={}
    
    for row in read:
        row=row[0].rsplit(';')
        
        if rownum==0:
            header=row
            colnum=0

            for colnum in range (0, len(header)):
                training_data[header[colnum]]=[]
                colnum=colnum+1
            
        else:
            colnum=0

            for colnum in range (0, len(header)):
                training_data[header[colnum]].append(row[colnum])
                colnum=colnum+1
                
        rownum=rownum+1
    return(training_data)

training_data = read_csv('vaja_podatki.csv') 
##-------
##Funkcija, ki iz slovarja s CSV vrne zalogo unique vredNosti za vsak atribut
##-------

def unique_values(training_data):
    
    keys = list(training_data.keys())
    unique_values={}
    colnum=0
    
    for col in keys:
        ##za vsak ključ naredimo mNožico vredNosti in jo spremenimo nazaj v seznam
        ##tako dobimo unique vredNosti za vsak atribut
        unique_values[col]= list(set(training_data[col]))
    return(unique_values)

unique=unique_values(training_data) 

##-------
##Funkcija, ki izrčuna pogojne verjetNosti za atribute z diskretnimi vredNostmi
##-------

##Tu privzamem, da so pogojne vredNosti lahko samo Yes ali No

def discrete(training_data, atribute, class_variable, test_record):
    
    ##training_data - slovar, kjer so ključi atributi, vredNosti pa so seznam vredNosti
    ##atribute - atrinut za katerega išečmo pogojne verjetNosti
    ##class_variable = atribut glede na katerega iščemo pogojNo verjetNost (DEFAULT BORROWER)
    ##pokličemo funkcijo z unique vredNostmi za atrinute in zaloga vredNosti 
    ##vrednost classa bo že podana kot zadnji stolpec v podatkih
    
    unique=unique_values(training_data)  
    z_vr = unique.get(atribute)

    #podatki za iskani atribut 
    data_a = training_data.get(atribute)

    #podatki za identifikator
    data_i = training_data.get(class_variable)

    #clas je zadnji stolpec v podatkih
    clas = unique.get(class_variable)
        
    p={}
    freq = {} 
    for c in clas:
        p[c] = 0
        freq[c] = 0


    for col in range (0, len(data_a)):
        for c in clas:
            
            if data_i[col]== c:
                freq[c]=freq[c]+1
                
                if data_a[col]==test_record:
                    p[c]=p[c]+1


    ##Laplace: za vsak class dodamo vrednost +1
    for c in clas:
        p[c]=p[c]+1

        freq[c]=freq[c]+ len (z_vr)

    for c in clas:
        p[c] = p[c]/freq[c]

    return(p)

d = discrete(training_data,'Home owner', 'Default borrower', 'No')
e = discrete(training_data,'Home owner', 'Default borrower', 'Yes')
f = discrete(training_data,'Maritual status', 'Default borrower', 'Married')
g= discrete(training_data,'Maritual status', 'Default borrower', 'Divorced')
h = discrete(training_data,'Maritual status', 'Default borrower', 'Single')
##-------
##Funkcija, ki izrčuna upanje vredNosti v nizu
##----
def mean(list):
    
    mean = sum(list)/len(list)
    return(mean)


##-------
##Funkcija, ki izrčuna standardni odklon vredNosti v nizu
##----
def sd(list):
    
    m = mean(list)
    sd=[]
    for i in list:
        sd.append((i-m)**2)
    sd=sum(sd)/(len(sd)-1)
    
    return(sd)

##-------
##Funkcija, ki izrčuna verjetNost za NormalNo porazdeljene podatke
##----
def p_Normal (ident, mean, sd):
    ##ident je identifikator za katerega računamo verjetNost

    import math
    
    p = 1/(math.sqrt(2*math.pi*sd))*math.exp(-(ident-mean)**2/(2*sd))
    return(p)
    

##-------
##Funkcija, ki izrčuna pogojne verjetNosti za atribute z NormalNo porazdelitvijo
##----

def Normal(training_data, atribute, class_variable, test_record):
    
    ##values - slovar, kjer so ključi atributi, vredNosti pa so seznam vredNosti
    ##atribute - atrinut za katerega išečmo pogojne verjetNosti
    ##identificator je tisti atribut glede na katerega gledaš pogojNo verjetNost
    ##- DEFAULT BORROWER
    ##clas - tisti razred za katerega delamo posterior 

    ##funkcija z unique vredNostmi za atrinute in zaloga vredNosti 
    unique=unique_values(training_data)  
    z_vr = unique.get(atribute)

    #podatki za iskani atribut 
    data_a = training_data.get(atribute)

    #podatki za identifikator
    data_i = training_data.get(class_variable)
    clas = unique.get(class_variable)


    #slovarja za štetje frekvenc in verjetnosti
    p_data={}
    freq = {}
    
    for c in clas:
        p_data[c] = []
        freq[c] = 0


    for col in range(0, len(data_a)):

        for c in clas:
            
            if data_i[col]==c:
                p_data[c].append(int(data_a[col]))
                freq[c] = freq[c]+ 1

    #izracun verjetnosti za normalno porazdelitev
    p={}
    
    for c in clas:
        m = int(mean(p_data[c]))
        s = int(sd(p_data[c]))
        p[c]=(p_Normal(test_record,m,s))

    return(p)
           
###----
##Funkcija za prior
###---
def prior(training_data, class_variable):

    c_variable= training_data[class_variable]
    clas = unique.get(class_variable)
    
    p={}
    for c in clas:
        
        p[c]= c_variable.count(c)/len(c_variable)

    
    return(p)

p=prior(training_data, 'Home owner')
r = prior(training_data, 'Maritual status')

###----
##Produkt
###

def prod(list):

    p=1
    for i in list:
       p*=i
    return(p)
    
    
#####---
##Funkcija za bayes
####---

def bayes_naive_class (csv_file, test_record, class_variable):

    ##csv_file = csv datoteka, ki vsebuje podatke
    ##test_record = slovar podatkov za katere iščemo napoved
    ##class_variable = class glede na katerega gledamo pogojne verjetNosti


    training_data = read_csv(csv_file)    
    unique = unique_values(training_data)

    prior_distr = prior(training_data, class_variable)
    
    p_Yes=[]
    p_No=[]

    for atribute in test_record:
        
        if len(unique[atribute])<=5:
            x_i = test_record[atribute]
            p = discrete (training_data, atribute, class_variable, x_i)
            p_Yes.append(p['Yes'])
            p_No.append(p['No'])

        else:
            x_i = int(test_record[atribute])
            p = Normal(training_data, atribute, class_variable, x_i)
            p_Yes.append(p['Yes'])
            p_No.append(p['No'])

    ##posteriorna verjetnost je produkt vseh pogojnih verjetnosti in priorne verjetnosti
    post_yes = prod(p_Yes)*prior_distr['Yes']
    post_no = prod(p_No)*prior_distr['No']

    if post_yes > post_no:
        return('Yes')
    else:
        return('No')
    

#########################################   
##test_record_1 = {'Home owner':'No','Maritual status': 'Married', 'Annual income': 120}
##class_variable_1='Default borrower'
##vaja = bayes_naive_class ('vaja_podatki.csv', test_record_1, class_variable_1)

##test_record_2 = {'age':80,'marital':'single','education':'tertiary', 'default':'No', 'balance':3000,'housing':'Yes', 'loan':'No'}
##class_variable_2 = 'y'
##test = vaja = bayes_naive_class ('vaja_bank.csv', test_record_2, class_variable_2)
    
    


            
