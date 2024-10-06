def seconds_to_HHMMSS(seconds):
    '''
    Function: Converts seconds to HHMMSS format
    '''
    hours, remainder = divmod(seconds, 3600) # divide seconds by 3600, hours=quotient and remainder=remainder
    mins, sec = divmod(remainder, 60) # divide remainder by 60, mins=quotient and sec=remainder
    return f"{int(hours):02}:{int(mins):02}:{int(sec):02}" #return format in HH:MM:SS