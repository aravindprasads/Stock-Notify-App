from flask import Flask, render_template, request
import subprocess                                                                                   
import stock_library as SL


app = Flask(__name__)                                                                               
app.config['DEBUG'] = True         
data_file = 'data' 

## Main page                                                                                        
@app.route('/', methods=['GET', 'POST'])                                                            
def index():         
    #Create data file if not existing already
    bashCommand = "touch " + data_file
    subprocess.check_output(['bash','-c', bashCommand])           
    ret_value = 0

    print "Entering main"
    if [request.method == 'POST']:
        stock_name = request.form.get('stock-name')                                                         
        min_value = request.form.get('min-value')                                                  
        mail_id = request.form.get('mail-id')    
        if(stock_name and min_value and mail_id):
            ret_value = SL.flask_fun(stock_name, min_value, mail_id)
        else:
            if(stock_name):
                return "Enter all 3 details - Name, Minimum value and Mail-ID"
        if(1 == ret_value):
            error_str = "The NSE Stock details are retreived from Alpha vantage website. Currently"
            error_str += " the website seems unavailable. Kindly try after some time." 
            return error_str
        elif(2 == ret_value):
            error_str = "Company name "+ stock_name +" is not supported in  NSe Stock exchange. "
            error_str += "Kindly try a different Company name"
            return error_str

        stock_name_del = request.form.get('stock-name-del')                                                         
        if(stock_name_del):
            SL.delete_company_from_readfile(stock_name_del)

        stock_data = SL.read_and_fill_info_from_datafile()

    return render_template('stock.html', stock_data=stock_data)                
    
if __name__ == '__main__':
    app.run()

