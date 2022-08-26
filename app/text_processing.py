from better_profanity import profanity

def fix_headline(headline):
    return censor(capitalize(single_headline(headline)))

def single_headline(headline):
    return headline.split('\n')[0]

def capitalize(headline):
    return headline.title()

def censor(headline):
    return profanity.censor(headline)

def get_mugshot(headline):
    