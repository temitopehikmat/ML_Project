import sys
import logging

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
    file_name, exc_tb.tb_lineno,str(error)) # to get the line number, log in using execution tab
    
    return error_message
      

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):# def __init__ is the constructor
        super().__init__(error_message) # this to inherit the init function
        self.error_message=error_message_detail(error_message, error_detail=error_detail)
        
        # inhering another functionality in custom exception
    def __str__(self):
        return self.error_message
    
