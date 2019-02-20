import re                                                                                         
import urllib2                                                                                      
import subprocess                                                                                   
import time
import smtplib                                                                                      
from email.MIMEMultipart import MIMEMultipart                                                       
from email.MIMEText import MIMEText          

web_file = 'alphavantage_data.txt'
data_file = 'data' 
temp_output_file = 'temp_data'
first_time = True
mail_dic = {}
zero_val = "{:.4f}".format(float(0))


#Get the company info and write it to "data" file
def get_company_info_from_website(company):
    my_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE:" + company + "&interval=1min&apikey=<alphavantage-key>"
    #Write the company info to "data" file
    dn_file = urllib2.urlopen(my_url)
    with open(web_file, 'wb') as output:
        output.write(dn_file.read())


def extract_info_from_data_file(line):
    match = re.search('(\w+)\s(.*)\s(.*)\s(.*)\s(.*)\s(.*)\s(.*)', line)
    if match:
        company =  match.group(1)
        temp = (float)(match.group(2))
        actual_val = "{:.4f}".format(temp)
        temp = (float)(match.group(3))
        min_val = "{:.4f}".format(temp)
        temp = (float)(match.group(4))
        max_val = "{:.4f}".format(temp)
        email_id = match.group(5)
        min_mail_status = match.group(6)
        max_mail_status = match.group(7)
        return (match, company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status)
    else:
        return (match, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL")


def extract_info_from_web_file(line):
    match = re.search('(\"1. open\"\:\s\")(\w+.*)(\",)', line)
    return match


def search_invalid_response_from_data_file(line):
    match = re.search('Invalid', line)
    return match


def write_line_to_data_file(fp, new_comp, new_comp_val, min_val, max_val, email_id, min_mail_status, max_mail_status):
    write_str = new_comp + " " + new_comp_val + " " + min_val + " " + max_val + " " + email_id 
    write_str += " " + str(min_mail_status) + " " + str(max_mail_status) + "\n"  
    fp.write(write_str)


def print_data_file_contents():
    print ("\nData file contents")
    print ("===================================================")
    fp = open(data_file,"r")
    lines = fp.readlines()
    for line in lines:
        line = line.rstrip('\n')
        (match, company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status) = extract_info_from_data_file(line)
        print (company,actual_val,min_val,max_val,email_id,min_mail_status,max_mail_status)
    print ("===================================================")


def check_datafile(data_dic, new_comp):
    if new_comp in data_dic:
        return True
    return False        


def get_comp_info_from_datafile():
    fp = open(data_file,"r")                                                      
    lines = fp.readlines()
    data_dic = {}
    for line in lines:
        line = line.rstrip('\n')
        (match, company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status) = extract_info_from_data_file(line)
        print (company,actual_val,min_val,max_val,email_id)
        data_dic[company] = actual_val
    fp.close()
    return data_dic


def send_mail(company, cur_val, min_val, max_val, email_id, is_lesser):
    print ("Sending mail to " + email_id + " about company " + company)
    
    if(True == is_lesser):
        comp_str = " has decreased below " + str(min_val) 
    else:
        comp_str = " has increased above " + str(max_val)
    subj_msg = "STOCK VALUE OF " + company + " CHANGED !!!"                                             
    body_msg = "Hi User,\n\nThis mail is from Stock-Notify Website.\n\nThe stock value of Company "     
    body_msg += company + comp_str +". Current value is " + str(cur_val)   
    body_msg += ".\n\nHappy to assist you always.\n\nThanks,\nStock-Notify-App team"         
                                                                                                        
    fromaddr = "<email-id>"
    toaddr = email_id
    msg = MIMEMultipart()                                                                               
    msg['From'] = fromaddr                                                                              
    msg['To'] = toaddr                                                                                  
    msg['Subject'] = subj_msg                                                                           
                                                                                                        
    msg.attach(MIMEText(body_msg, 'plain'))                                                             
                                                                                                        
    server = smtplib.SMTP('smtp.gmail.com', 587)                                                        
    server.starttls()                                                                                   
    server.login(fromaddr, "<password>")
    text = msg.as_string()                                                                              
    server.sendmail(fromaddr, toaddr, text)                                                             
    server.quit()                                 


def replace_contents(new_comp, new_comp_val, min_val, max_val, email_id, min_mail_status, max_mail_status):
    bashCommand = "touch " + temp_output_file
    subprocess.check_output(['bash','-c', bashCommand])
    old_fp = open(data_file, "r") 
    new_fp = open(temp_output_file, "w")

    lines = old_fp.readlines()
    for line in lines:
        line = line.rstrip('\n')
        (match, old_comp, old_comp_val, r_min_val, r_max_val, r_email_id, r_min_mail_status, r_max_mail_status) = extract_info_from_data_file(line)
        if(old_comp != new_comp):
            new_fp.write(line+'\n')
        else:    
            print ("\nOld value " + str(old_comp_val) + " New value " + str(new_comp_val))
            write_line_to_data_file(new_fp, new_comp, new_comp_val, min_val, max_val, email_id, min_mail_status, max_mail_status)
    old_fp.close()           
    new_fp.close()           
    bashCommand = "rm " + data_file
    subprocess.check_output(['bash','-c', bashCommand])           
    bashCommand = "mv " + temp_output_file + " " + data_file
    subprocess.check_output(['bash','-c', bashCommand])           
   

def read_and_fill_info_from_datafile():
    stock_data = []                                                                               

    print ("\nData file contents")
    print ("===================================================")
    fp = open(data_file,"r")                                                      
    lines = fp.readlines()
    for line in lines:
        line = line.rstrip('\n')
        (match, company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status) = extract_info_from_data_file(line)
        print (company,actual_val,min_val,max_val,email_id,min_mail_status,max_mail_status)
        global zero_val
        if(min_val == zero_val):
            min_val_str = "NOT-SET BY USER"
        else:
            min_val_str = str(min_val)
        if(max_val == zero_val):
            max_val_str = "NOT-SET BY USER"
        else:
            max_val_str = str(max_val)
        stock = {                                                                                 
            'name' : company,
            'actual_value' : str(actual_val),
            'min_value' : min_val_str,
            'max_value' : max_val_str,
            'email_id' : email_id
        }                                                                                           
        stock_data.append(stock)                                                                
    print ("===================================================")
    fp.close()
    return stock_data


def delete_company_from_readfile(new_comp):
    bashCommand = "touch " + temp_output_file
    subprocess.check_output(['bash','-c', bashCommand])
    print ("Company to delete = "+ new_comp)
    old_fp = open(data_file, "r") 
    new_fp = open(temp_output_file, "w")

    lines = old_fp.readlines()
    for line in lines:
        line = line.rstrip('\n')
        (match, old_comp, old_comp_val, min_val, max_val, email_id, min_mail_status, max_mail_status) = extract_info_from_data_file(line)
        if(old_comp != new_comp):
            new_fp.write(line+'\n')
    old_fp.close()           
    new_fp.close()           
    bashCommand = "rm " + data_file
    subprocess.check_output(['bash','-c', bashCommand])           
    bashCommand = "mv " + temp_output_file + " " + data_file
    subprocess.check_output(['bash','-c', bashCommand])           


def process_data_write_to_op_file(company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status):
    bashCommand = "touch " + temp_output_file
    subprocess.check_output(['bash','-c', bashCommand])
    data_written = False
    #Read the data file
    with open(web_file) as fp_web:
        lines = fp_web.readlines()
    fp_web.close()
    fp_temp = open(temp_output_file, "a")
    for line in lines:
        match = extract_info_from_web_file(line)
        #if success, read the stock value
        if match:
            temp = (float)(match.group(2))
            new_comp_val = "{:.4f}".format(temp)
            print (company +" Current value " + str(new_comp_val))
            print (company +" Min value " + str(min_val))

            if(float(min_val) != float(zero_val)):
                if(float(new_comp_val) < float(min_val)):
                    print ("Found the Value to be lesser")
                    if(False == min_mail_status):
                        print ("Trying to send mail to about company " + company + " to " + email_id)
                        send_mail(company, new_comp_val, min_val, max_val, email_id, True)
                    else:
                        print ("Not sending mail now. Mail already sent")
                    min_mail_status = True                        
            if(float(max_val) != float(zero_val)):
                if(float(new_comp_val) > float(max_val)):
                    print ("Found the Value to be higher")
                    if(False == max_mail_status):
                        print ("Trying to send mail to about company " + company + " to " + email_id)
                        send_mail(company, new_comp_val, min_val, max_val, email_id, False)
                    else:
                        print ("Not sending mail now. Mail already sent")
                    max_mail_status = True                        
            write_line_to_data_file(fp_temp, company, new_comp_val, min_val, max_val, email_id, min_mail_status, max_mail_status)
            fp_temp.close()
            data_written = True
            break
    #if data retreival from website failed, reqwrite old data of company back to output file            
    if(False == data_written):
        print ("\nSomething failed in retreving contents from Web file")
        with open(web_file) as fp_web:
            lines = fp_web.readlines()
            print (lines)
        write_line_to_data_file(fp_temp, company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status)
        fp_web.close()            
    fp_temp.close()


def thread_fun():
    #Create data file if not existing already
    bashCommand = "touch " + data_file
    subprocess.check_output(['bash','-c', bashCommand])
    bashCommand = "touch " + temp_output_file
    subprocess.check_output(['bash','-c', bashCommand])

    print ("\nReading contents from Data file")
    fp_data = open(data_file, "r")
    lines = fp_data.readlines()
    data_dic = {}
    data_written = False
    for line in lines:
        line = line.rstrip('\n')
        (match, company, actual_val, min_val, max_val, email_id, min_mail_status_str, max_mail_status_str) = extract_info_from_data_file(line)
        if match:
            print ("\n"+company)
            print (company,actual_val,min_val,max_val,email_id)
            #Get the company info and write it to "data" file
            print ("\nGet the company info and write it to data file")
            get_company_info_from_website(company)
            #Get val from web_file and update val in data_file/output_file
            print ("\nGet val from web_file and update val in data_file/output_file")
            print ("mail-status - " + min_mail_status_str)
            if("True" == min_mail_status_str):
                min_mail_status = True
            else:
                min_mail_status = False
            if("True" == max_mail_status_str):
                max_mail_status = True
            else:
                max_mail_status = False
            #print "mail-status-val " + str(min_mail_status) 
            process_data_write_to_op_file(company, actual_val, min_val, max_val, email_id, min_mail_status, max_mail_status)

    #Make the temporary file as new file
    bashCommand = "mv " + temp_output_file + " " + data_file
    subprocess.check_output(['bash','-c', bashCommand])
    fp_data.close()

    print_data_file_contents()
    print ("\n!!!!!!!!!!NEXT LOOP!!!!!!!!!!!!!!!!!!!!!!!!")


def flask_fun(stock_name, min_value, max_value, mail_id):
    #Read the inputs
    new_comp = stock_name
    temp = (float)(min_value)
    min_val = "{:.4f}".format(temp)
    temp = (float)(max_value)
    max_val = "{:.4f}".format(temp)
    email_id = mail_id
    
    print ("\nCompany given = " + new_comp)
    print ("\nMin Value given = " + str(min_val))
    print ("\nMax Value given = " + str(max_val))
    print ("\nemail-id given = " + email_id)

    #Extract a dic of company-names
    data_dic = {}
    data_dic = get_comp_info_from_datafile()
    company_found = False
    no_of_retries = 0
    ret_value = 0

    while(no_of_retries < 3):
        print ("Getting company info of " + new_comp + " from website")
        get_company_info_from_website(new_comp)	
        #Read the data file
        with open(web_file) as fp:                                                                      
            lines = fp.readlines()
        for line in lines:
            match = extract_info_from_web_file(line)
            #if success, read the stock value
            if match:         
                company_found = True
                temp = (float)(match.group(2))
                new_comp_val = "{:.4f}".format(temp)
                print ("\nCompany current value " + str(new_comp_val))
                #Check if the company name provided byy User already exists in data file
                if(check_datafile(data_dic, new_comp) == False):
                    print ("\nNew Company provided")
                    fp = open(data_file,"a")                                                      
                    write_line_to_data_file(fp, new_comp, new_comp_val, min_val, max_val, email_id, False, False)
                    fp.close()
                else:
                    print ("\nCompany already exists. Replacing contents in data file")
                    replace_contents(new_comp, new_comp_val, min_val, max_val, email_id, False, False)
                ret_value = 0                    
                break
            else:
                match = search_invalid_response_from_data_file(line)
                if match:         
                    print ("\nCompany not found in Website. Return")
                    company_found = True
                    ret_value = 2
                    break
        if(True == company_found):
            break
        no_of_retries += 1            
        time.sleep(2)

    if(no_of_retries >= 3):        
        ret_value = 1

    return ret_value        
                                
