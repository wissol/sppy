from settings import language as lang

def mylang(var):
    try:
        if lang == "en":
            raise Exception("English")
        elif lang == "es":
            from language.spanish import dic as mytext 
            mytext[var]
# to add language, follow the next example and add the file language:
        #elif lang == "ru":
        #    from language.russian import dic as mytext 
        #    mytext[var]
            
    except: # If don find the value will show it in english
        from language.english import dic as mytext
    var = mytext[var]
    return var
  

  
