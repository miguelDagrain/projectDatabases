# Programmeer project databases 2019: ESP
# Script voor extractie van tags
#
# Auteur: Len Feremans
# Datum: 14 Maart
from collections import defaultdict, Counter
import math
import codecs
import csv
import re
# =========================================================
# Data uit ESP
file1 = './projects.csv'
file2 = './people.csv'
file3 = './connections.csv'
promotors_filter = set(['Bart Goethals', 'Toon Calders', 'Kris Laukens', 'Floris Geerts'])
# =========================================================

# =========================================================
#1. load projects, connections and people
# =========================================================
f = codecs.open(file1, encoding='utf-8')
reader = csv.reader(f , delimiter=',', quotechar='\'')
lines = []
project_ids = {}
for line in reader:
    active = line[5]
    if active == 'y': #filter active projects
        lines.append(line)
    project_ids[len(lines)-1] = line[0]
print('number of projects:{}'.format(len(lines)))
print('first line:{}'.format(lines[0]))

f = codecs.open(file2, encoding='utf-8')
reader = csv.reader(f , delimiter=',', quotechar='\'')
people = {}
name_tokens = set()
for line in reader:
    id = line[0]
    name = line[1]
    people[id] = name
    for name_token in name.lower().split(): #filter professor names from texts
        name_tokens.add(name_token)
    
f = codecs.open(file3, encoding='utf-8')
reader = csv.reader(f , delimiter=',', quotechar='\'')
promoters = {}
for line in reader:
    project_id = line[1]
    people_id = line[2]
    if line[3] == 'p':
        promoters[project_id] = people[people_id] #join connections with people
        
#Join connections and projects, and store promotor for each project
for i,line in enumerate(lines):
    line[0] = promoters.get(project_ids[i],None)

# =========================================================
#2. clean HTML tags from description
# =========================================================
def parse_description(line):
    #verwijder html tags en entities en URL's met regex
    regex_remove_list = [r'<[^>]*>', r'&[^;]+;', r'http(s)?://[a-zA-Z0-9_\-\.]+$]']
    for item in regex_remove_list:
        line = re.sub(item, ' ', line)
    #verwijder common seperators
    remove_lst = ['\\n','\\r','\\','/',
                  '(',')','.',',','!','-','\'',':','"','[',']']
    for item in remove_lst:
        line = line.replace(item, ' ')
    #lower case
    return line.lower() 

for line in lines:
    line[2] = parse_description(line[2])
    line[1] = parse_description(line[1])

print('first line after processing:{}'.format(lines[0]))

# =========================================================
#3. Natural language processing: stopwoorden verwijderen  +  numerieke tekens en lower case
# stopwoorden uit nltk
# =========================================================
stopwords_nl  = [u'de', u'en', u'van', u'ik', u'te', u'dat', u'die', u'in', u'een', u'hij', u'het', u'niet', u'zijn', u'is', u'was', u'op', u'aan', u'met', u'als', u'voor', u'had', u'er', u'maar', u'om', u'hem', u'dan', u'zou', 
 u'of', u'wat', u'mijn', u'men', u'dit', u'zo', u'door', u'over', u'ze', u'zich', u'bij', u'ook', u'tot', u'je', u'mij', u'uit', u'der', u'daar', u'haar', u'naar', u'heb', u'hoe', u'heeft', u'hebben', u'deze',
 u'u', u'want', u'nog', u'zal', u'me', u'zij', u'nu', u'ge', u'geen', u'omdat', u'iets', u'worden', u'toch', u'al', u'waren', u'veel', u'meer', u'doen', u'toen', u'moet', u'ben', u'zonder', u'kan', u'hun',
 u'dus', u'alles', u'onder', u'ja', u'eens', u'hier', u'wie', u'werd', u'altijd', u'doch', u'wordt', u'wezen', u'kunnen', u'ons', u'zelf', u'tegen', u'na', u'reeds', u'wil', u'kon', u'niets', u'uw', 
 u'iemand', u'geweest', u'andere']

stopwords_en = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself',
 u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were',
 u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of',
 u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on',
 u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other',
 u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now', u'd', u'll', u'm', u'o',
 u're', u've', u'y', u'ain', u'aren', u'couldn', u'didn', u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn', u'shan', u'shouldn', u'wasn', u'weren', u'won', u'wouldn']

stop_words = set(stopwords_nl + stopwords_en)

def get_normal_tokens(line):
    tokens = line.split()
    tokens_copy = []
    for token in tokens:
        if re.match('[a-z][a-z][a-z]+',token) and not(token in stop_words) and not(token in name_tokens):
            tokens_copy.append(token)
    return tokens_copy

# =========================================================
#4. Enumerate bi-grams, and count global frequency     
# Count number of occurences of each token/work and each bigram
# =========================================================
def enumerate_bigrams(line):
    tokens = get_normal_tokens(line[1]) + get_normal_tokens(line[2])
    bigrams = set()
    for i in range(0, len(tokens)-1):
        token = tokens[i]
        token_next = tokens[i + 1]
        bigram = token + '_' + token_next
        bigrams.add(bigram)
    return bigrams

cnt_bigrams = Counter()
for line in lines:
    bigrams = enumerate_bigrams(line)
    for bigram in bigrams:
        cnt_bigrams[bigram] +=1
        
print('common bigrams:{}'.format(cnt_bigrams.most_common(10)))
print('number of bigrams:{}'.format(len(cnt_bigrams)))
print('top-10 frequent bigrams')
for i in range(0,10):
    print(cnt_bigrams.most_common(10)[i])
 
# =========================================================   
#5. Count frequency for each bigram, for each promotor
# Count frequency for each bigram in title or description
# =========================================================
cnt_bigrams_promotor = defaultdict(lambda: Counter())
for i,line in enumerate(lines):
    if(line[0] == None): #no promotor
        continue
    bigrams = enumerate_bigrams(line)
    for bigram in bigrams:
        cnt_bigrams_promotor[line[0]][bigram] +=1

for promotor in cnt_bigrams_promotor.keys():
    if not(promotor in promotors_filter):
        continue
    print('top-5 frequent bigrams for {}'.format(promotor))
    all = cnt_bigrams_promotor[promotor].most_common()
    all = sorted(all, key= lambda pair: pair[1], reverse=True)
    for i in range(0,5):
        print(all[i])

def frequency(idx, lines):
    line = lines[idx]
    cnt_bigrams_line = Counter()
    #count occurrences, title occurences count double
    title_tokens = tokens = get_normal_tokens(line[1])
    for i in range(0, len(title_tokens)-1):
        bigram_current = title_tokens[i] + '_' + title_tokens[i + 1]
        cnt_bigrams_line[bigram_current] +=2
    descr_tokens = get_normal_tokens(line[2])
    for i in range(0, len(descr_tokens)-1):
        bigram_current = descr_tokens[i] + '_' + descr_tokens[i + 1]
        cnt_bigrams_line[bigram_current] +=1
    return cnt_bigrams_line

# =========================================================
#6. Extract tags for promotors
# =========================================================
lines = sorted(lines, key=lambda tuple: str(tuple[0]) + str(tuple[1])) #sort on promoter, than title

def score_bigram_tf_idf(promotor, bigram, count_line):
    count_all_projects = cnt_bigrams[bigram] 
    count_promotor_projects = cnt_bigrams_promotor[promotor][bigram]
    return (count_promotor_projects * count_line) / math.log(count_all_projects + 1)
            

print('Search results')
prev_promotor = None
for i,line in enumerate(lines):
    promotor = line[0]
    if not(promotor in promotors_filter):
        continue
    #compute bigrams
    bigrams = frequency(i,lines).most_common()
    bigrams_with_score = []
    for (bigram, count_line) in bigrams:
        bigrams_with_score.append([bigram, score_bigram_tf_idf(promotor,bigram,count_line)])
                  
    #best bigrams have highest promotor-frequency * term-frequency/log(document frequence)
    bigrams_with_score_sorted = sorted(bigrams_with_score, key=lambda tuple: tuple[1], reverse=True)
    tags = ''
    for i in range(0, min(len(bigrams_with_score_sorted), 3)):
        tags += '#' + bigrams_with_score_sorted[i][0] + ' '
    #print
    if promotor != prev_promotor:
        print(promotor)
        prev_promotor  = promotor
    print('    {}\n            {}'.format(line[1], tags))
    
    