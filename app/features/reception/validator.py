# this file to validate user input in reception feature


class ReceptionValidator : 

    @staticmethod
    def request_validator (national_code , battalion_option , company_option):

        #check all three fiels is not empty 
        if not national_code:
            return False, national_code,"کد ملی وارد نشده است."

        if not battalion_option:
            return False, national_code,"گردان انتخاب نشده است."

        if not company_option:
            return False, national_code,"گروهان انتخاب نشده است."


        return (True, national_code,None )
                        
    # function: validate national_code value
    @staticmethod
    def national_code_validator (national_code): 
                
        #validate national_code == 10 digit 
        national_code = str(national_code)
        if len(national_code) != 10:
            return False,national_code, "کد ملی باید ۱۰ رقم باشد."
        
        return (True, national_code, None )
    
   


        