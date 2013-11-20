##moj X je class, za katerega iščemo klasifikator

##-------
##Funkcija za branje CSV, ki vrne slovar z vrednostmi
##-------
def read_csv (csv_file):
    
    import csv
    file = open(csv_file, 'rt', encoding = 'ascii')
    read = csv.reader(file)

    rownum=0
    header=[]
    values={}
    
    for row in read:
        row=row[0].rsplit(';')
        
        if rownum==0:
            header=row
            colnum=0

            for colnum in range (0, len(header)):
                values[header[colnum]]=[]
                colnum=colnum+1
            
        else:
            colnum=0

            for colnum in range (0, len(header)):
                values[header[colnum]].append(row[colnum])
                colnum=colnum+1
                
        rownum=rownum+1
    return(values)


##-------
##Funkcija, ki iz slovarja s CSV vrne zalogo unique vrednosti za vsak atribut
##-------

def unique_values(values):
    
    keys = list(values.keys())
    unique_values={}
    colnum=0
    
    for col in keys:
        ##za vsak ključ naredimo množico vrednosti in jo spremenimo nazaj v seznam
        ##tako dobimo unique vrednosti za vsak atribut
        unique_values[col]= list(set(values[col]))
    return(unique_values)


##-------
##Funkcija, ki izrčuna pogojne verjetnosti za atribute z diskretnimi vrednostmi
##-------

##Tu privzamem, da so pogojne vrednosti lahko samo Yes ali No

def discrete(values, atribute, identificator):
    
    ##values - slovar, kjer so ključi atributi, vrednosti pa so seznam vrednosti
    ##atribute - atrinut za katerega išečmo pogojne verjetnosti
    ##identificator je tisti atribut glede na katerega gledaš pogojno verjetnost
    ##- DEFAULT BORROWER

    ##funkcija z uniwue vrednostmi za atrinute in zaloga vrednosti 
    unique=unique_values(values)  
    z_vr = unique.get(atribute)

    #podatki za iskani atribut 
    data_a = values.get(atribute)

    #podatki za identifikator
    data_i = values.get(identificator)
    
    p_yes={}
    p_no={}    
    frek_no=0
    frek_yes=0
    
    for col in z_vr:
        p_yes[col]=0
        p_no[col]=0
 
    for col in range (0, len(data_a)):
        
        if data_i[col]=='Yes':
            p_yes[data_a[col]] = p_yes[data_a[col]]+1
            frek_yes=frek_yes+1
            
        if data_i[col]=='No':
            p_no[data_a[col]] = p_no[data_a[col]]+1
            frek_no=frek_no+1
            
    for col in z_vr:
        p_yes[col]=p_yes[col]/frek_yes
        p_no[col]=p_no[col]/frek_no
    
    return(p_yes, p_no)

##-------
##Funkcija, ki izrčuna upanje vrednosti v nizu
##----
def mean(list):
    
    mean = sum(list)/len(list)
    return(mean)


##-------
##Funkcija, ki izrčuna standardni odklon vrednosti v nizu
##----
def sd(list):
    
    m = mean(list)
    sd=[]
    for i in list:
        sd.append((i-m)**2)
    sd=sum(sd)/(len(sd)-1)
    
    return(sd)

##-------
##Funkcija, ki izrčuna verjetnost za normalno porazdeljene podatke
##----
def p_normal (ident, mean, sd):
    ##ident je identifikator za katerega računamo verjetnost

    import math
    
    p = 1/(math.sqrt(2*math.pi*sd))*math.exp(-(ident-mean)**2/(2*sd))
    return(p)
    

##-------
##Funkcija, ki izrčuna pogojne verjetnosti za atribute z normalno porazdelitvijo
##----

def normal(values, atribute, identificator, clas):
    
    ##values - slovar, kjer so ključi atributi, vrednosti pa so seznam vrednosti
    ##atribute - atrinut za katerega išečmo pogojne verjetnosti
    ##identificator je tisti atribut glede na katerega gledaš pogojno verjetnost
    ##- DEFAULT BORROWER
    ##clas - tisti razred za katerega delamo posterior 

    ##funkcija z uniwue vrednostmi za atrinute in zaloga vrednosti 
    unique=unique_values(values)  
    z_vr = unique.get(atribute)

    #podatki za iskani atribut 
    data_a = values.get(atribute)

    #podatki za identifikator
    data_i = values.get(identificator)
    z_vr_i = unique.get(identificator)
    
    p={}
    frek_yes=0
    frek_no=0

    for i in z_vr_i:
        p[i]=[]

    for col in range(0, len(data_a)):
        
        if data_i[col]=='Yes':
            p['Yes'].append(int(data_a[col]))
            frek_yes = frek_yes + 1
        if data_i[col]=='No':
            p['No'].append(int(data_a[col]))
            frek_no = frek_no + 1

    for i in z_vr_i:
        m = int(mean(p[i]))
        s = int(sd(p[i]))
        p = p_normal(clas,m,s)
        return(p)


def bayes_naive_class (csv_file, Class, identificator):

    data = read_csv(csv_file)    
    print(data)

s = {'Home owner':['No'],'Maritual status': ['Single'], 'Annual income': [120]}
X='Default borrower'
bayes_naive_class ('vaja_podatki.csv',s,X)

    
    


            
