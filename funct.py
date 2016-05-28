import re, codecs, os


def m_l(matchObj8):
    matchObj1 = re.search( r'(the) (another)', matchObj8, re.I)
    if matchObj1:
        yield "Art_choice \t %s %s" % (matchObj1.start(), matchObj1.end()) + '\t' + matchObj1.group(1) + '\n'

def ind_art(matchObj8, plurals):
    matchObj = re.search( r'(a|an) [a-z]*[\s]?([a-z]+s)', matchObj8, re.I)#поиск неправильных неопределенных артиклей
    if matchObj:
    
        yield "Art_form \t %s %s" % (matchObj.start(), matchObj.end()) + '\t' + matchObj.group(1) + '\n'
    
    else:
        for i in plurals:#поиск неправильных арткилей с нестандартным множественным числом
            matchObj = re.search(r'(a|an) ' + i, line, re.I)
            if matchObj:
                yield "Art_choice \t %s %s" % (matchObj.start(), matchObj.end()) + '\t' + matchObj.group(1) + '\n'

def s_f(matchObj8):
    matchObj2 = re.search( r'([a-z]*)\s?([a-z]+est)', matchObj8, re.I)#поиск отсутствующего артикля перед превосходной степенью прилагательного
    if matchObj2:
        try:
            word1 = matchObj2.group(1)
            matchObj3 = re.search( r'[^the]+', word1, re.I)
            if matchObj3:
                yield "Superlative_adj \t %s %s" % (matchObj2.start(), matchObj2.end()) + '\t' + matchObj2.group(2) + '\n'
        except:
            yield "Superlative_adj \t %s %s" % (matchObj2.start(), matchObj2.end()) + '\t' + matchObj2.group() + '\n'

def c_a(matchObj8, countries):
    for i in countries:#поиск неправильных артиклей в названии стран
        matchObj4 = re.search( r'([a-z]+[\s])?[a-z]+ ' + i, matchObj8, re.I)
        if matchObj4:
            word1 = matchObj4.group()
            matchObj5 = re.search( r'[^the]+ [^the]*\s?' + i, word1, re.I)
            if matchObj5:
                yield "Art_choice \t %s %s" % (matchObj4.start(), matchObj4.end()) + '\t' + i + '\n'

    
def u_a(matchObj8, unique):
    for i in unique:
        matchObj6 = re.search( r'([a-z]+ )?' + i, matchObj8, re.I)
        if matchObj6:
            try:
                word1 = matchObj6.group(1)
                matchObj7 = re.search( r'[^the ]', word1, re.I)
                if matchObj7:
                    yield "Art_choice \t %s %s" % (matchObj6.start(), matchObj6.end()) + '\t' + i + '\n'
            except:
                yield "Art_choice \t %s %s" % (matchObj6.start(), matchObj6.end()) + '\t' + i + '\n'

def adj_n(matchObj8, adj):
    for i in adj:#конструкции прилагательных с существительными
        matchObj9 = re.search( r'(([a-z]+\s)?([a-z]+\s)?([a-z]+\s))?' + i, matchObj8, re.I)
        if matchObj9:
            if matchObj9.group(1) is not None:
                try:
                    word1 = matchObj9.group(2)
                except:
                    word1 = None
                try:
                    word2 = matchObj9.group(3)
                except:
                    word2 = None
                try:
                    word3 = matchObj9.group(4)
                except:
                    word3 = None

                
                if word1 != 'the ':
                    if word2 != 'the ':
                        if word3 != 'the ':
                            yield "Art_choice \t %s %s" % (matchObj9.start(), matchObj9.end()) + '\t' + i + '\n'

                
            else:
                yield "Art_choice \t %s %s" % (matchObj9.start(), matchObj9.end()) + '\t' + i + '\n'

def main():
    with open(u'essay.txt') as work:
        line = work.read().decode('utf-8')        
        matchObj8 = re.sub('\.', '.\n', line)
    result = codecs.open(u'result.ann', 'w', 'utf-8-sig')

    plurals = ["feet", "geese", "mice", "lice", "oxen", "children", "women", "men", "teeth", "phenomena", "formulae"]
    countries = ["UK", "USA", "Kingdom", "Republic", "States", "Islands", "Federation", "Empire"]
    unique = ["Arctic", "Antartic", "Americas", "Netherlands", "Philippines", "equator", "North Pole", "Moon", "Earth", "Nothern Star", "sky", "Internet"]
    adj = ["following", "former", "latter", "initial", "starting", "next", "final", "last", "main", "opposite", "same"]
    art_m = m_l(matchObj8)
    for i in art_m:
        result.write(i)
    indef = ind_art(matchObj8, plurals)
    for i in indef:
        result.write(i)
    superlative = s_f(matchObj8)
    for i in superlative:
        result.write(i)
    country = c_a(matchObj8, countries)
    for i in country:
        result.write(i)
    uniqueObj = u_a(matchObj8, unique)
    for i in uniqueObj:
        result.write(i)
    adjNoun = adj_n(matchObj8, adj)
    for i in adjNoun:
        result.write(i)
    
main()
