# from ngrams import weightedBigrams
import operator
import codecs
import re
import sys
import RegPattern
from Regemotest import sample_match
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def tokens(str1): 
    # print (str1.strip().split(' '))
    return str1.strip().split(' ')

# to remove url
def del_url(line): #return re.sub(r'https?:\/\/.*', "", line).lower()
    result = ''
    p_list = ["s'","'s"]
    for i in re.sub(r'https?:\/\/.*', "", line).lower().split(' '):
        if "s'" in i:
            result += i.replace("s'","") + " "
        elif "'s" in i:
            result += i.replace("'s","") + " "
        else:
            result += i + " "
        # for p in p_list:
        #     if p in i:
        #         result += i.replace(p,'')+ ' '
        # result += i + ' '
                

    return result

def checktag(tweet):
    result = ''
    for i in tweet.split(' '):
        if i.startswith('#'): #remove @ amd #
            result += '<HASHTAG>'
            result += ' '
        elif i.startswith('@'):
            result += '<USER>'
            result += ' '
        elif 'pm' in i:
            result += i.replace('pm',' <PM>')#change the time format and add 'space' to be tokenized
            result += ' '
        else:
            result += i
            result += ' '
    return result

def removeRT(tweet): #if RT: then discard this tweet
    result = ''
    for i in tweet.split(' '):
        if i.startswith('rt') or i.startswith('RT'): #remove @ amd #
            break
        else:
            result += i
            result += ' '
    return result

reg = RegPattern.RegPattern()

def regTime(tweet):
    finalResult1 = ''
    result = (reg.get_pattern(tweet,'re_time'))
    # print reg.re_time
    # print result
    for i in result:
        finalResult1 += str(i) + ' '
    return finalResult1

def regPatterns(tweet):
    finalResult = ''
    result = (reg.get_pattern(tweet,'re_all'))
    # print result
    for i in result:
        finalResult += i + ' '
    return finalResult  

def minusNetworks(word_list):
	
	# Get edges for the subjective graph
    	edges1 = sample_match(word_list)

        edges = {}
        for edge in edges1:
                value = edges1[edge]
                edges[edge] = value        

        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)
        words = {}
        netEdges = {}
        countWords = 0
        for (edge, value) in sorted_edges:
            print "%s\t%f"%(edge,value)
            tokens = edge.split("\t")
            if tokens[0] not in words:
                countWords = countWords + 1
                words[tokens[0]] = countWords
            if tokens[1] not in words:
                countWords = countWords + 1
                words[tokens[1]] = countWords
            netEdge = unicode(words[tokens[0]]) + " " + unicode(words[tokens[1]])
            netEdges[netEdge] = value

        saveNetwork(words,netEdges)

#def processTweets(path):


#def tokenize:

def saveNetwork(words, edges):
        out = codecs.open("./minused.net","w", "utf-8-sig")
        out2 = codecs.open("./minused.vertices","w", "utf-8-sig")
        out3 = codecs.open("./minused.edges","w", "utf-8-sig")
        #Write the vertices names
        out.write("*Vertices "+ unicode(len(words)) + "\n")
            
        sorted_words = sorted(words.items(), key=operator.itemgetter(1))
        for (word, value) in sorted_words:
            line = unicode(value) + " \"" + word.replace("\"","\\\"") + "\" 0.0 0.0 0.0";

            out.write(line+"\n");
            out2.write(unicode(value) + "\t" + word +"\n")
        #Write the Edges
        out.write("*Arcs \n");
        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)
        for (edge, value) in sorted_edges:
           
           out.write(edge + " " + unicode(value)+"\n");
           out3.write(edge + " " + unicode(value)+"\n")
        out.close();
        out2.close()
        out3.close()


def replaceWordByTag(word):

        # If HT
        if word[0] == '#':
            word = "<hashtag>";
        

        #If URL
        if "http" in word or "https" in word:
            word = "<url>";
        

        #If mini URL
        if len(word) > 3 and "co/" in word[0, 3]:
            word = "<minurl>";


        #If user mention
        if word[0] == '@':
            word = "<usermention>";
        

        return word;

def findEmotionWords(pathEdges, pathNodes, pathPWs):
    out = codecs.open("network/hws_bi.csv","w", "utf-8-sig")

    f1 = codecs.open(pathEdges,"r", "utf-8")
    f2 = codecs.open(pathNodes,"r", "utf-8")
    f3 = codecs.open(pathPWs,"r", "utf-8")
    #Add eigen
    #f4 = codecs.open(pathEigen,"r","utf-8")

    #Read the edges
    edges = []
    for line in f1:
        edges.append(line)

    #Read the nodes
    nodes = {}
    for line in f2:
        #print line
        tokens = line.split("\t")
        nodes[tokens[0]] = tokens[1].strip()

    #Add Read eigen
    #eigen = {}
    #for line in f4:
    #    tokens = line.split("\t")
    #    eigen[tokens[0]] = tokens[1].strip()

    for line in f3:
        tokens = line.split("\t")
        index = tokens[0]
        word = tokens[1]
        print line
        for edge in edges:
            tokens = edge.split(" ")
            index1 = tokens[0]
            index2 = tokens[1]
            value = tokens[2].strip()
            if index1 in nodes and index2 in nodes:
                if index1 == index:
                    #if float(value) > 0.0001:
                    #    print word+": "+nodes[index1]+nodes[index2]+" - "+value
                    #    out.write(nodes[index1]+nodes[index2]+"\t"+value+"\n")
                    print word+": "+nodes[index1]+nodes[index2]+" - "+value
                    out.write(nodes[index1]+nodes[index2]+"\t"+value+"\n")
                elif index2 == index:
                    #if float(value) > 0.0001:
                    #    print word+": "+nodes[index1]+nodes[index2]+" - "+value
                    #    out.write(nodes[index1]+nodes[index2]+"\t"+value+"\n")
                    print word+": "+nodes[index1]+nodes[index2]+" - "+value
                    out.write(nodes[index1]+nodes[index2]+"\t"+value+"\n")
    out.close()
def findEmotionWordsTriGram(pathEdges, pathNodes, pathPWs):
	out = codecs.open("network/hws_tri.csv","w", "utf-8-sig")
	out2 = codecs.open("network/hws_bi_list","w", "utf-8-sig")
	f1 = codecs.open(pathEdges,"r", "utf-8")
	f2 = codecs.open(pathNodes,"r", "utf-8")
	f3 = codecs.open(pathPWs,"r", "utf-8")
	edges = []
	print "Loading Edges..."
	for line in f1:
		edges.append(line)
	nodes = {}
	print "Loading Nodes..."
	for line in f2:
		#print line
		tokens = line.split("\t")
		nodes[tokens[0]] = tokens[1].strip()
		#print nodes[1]
	result = []
	print "Appending Result..."
	for line in f3:
		tokens = line.split("\t")
		index = tokens[0]
		word = tokens[1]

		for edge in edges:
			tokens = edge.split(" ")
			index1 = tokens[0]
			index2 = tokens[1]
			value = tokens[2].strip()
			if index1 in nodes and index2 in nodes:
				if index1 == index or index2 == index:
					result.append(index1 + " " +index2)
					out2.write(index1 + " " + index2 + " " + value + "\n")
	print "Matching..."
	for i in range(0,len(result),1):
		tokens = result[i].split(" ")
		index1 = tokens[0]
		index2 = tokens[1]
		for j in range(0,len(result),1):
			temp_tokens = result[j].split(" ")
			temp_index1 = temp_tokens[0]
			temp_index2 = temp_tokens[1]
			temp_value = temp_tokens[2].strip()
			if index2 == temp_index1:
				print nodes[index1]+nodes[index2]+nodes[temp_index2]+" - "+temp_value
				out.write(nodes[index1]+nodes[index2]+nodes[temp_index2]+"\t"+temp_value+"\n")
					#for i in range(0,len(edges),1):
					#	temp_tokens = edges[i].split(" ")
					#	temp_index1 = temp_tokens[0]
					#	temp_index2 = temp_tokens[1]
					#	print index1 + index2 + temp_index2
					#	temp_value = temp_tokens[2].strip()
					#	print nodes
					#	if index2 == temp_index1:
					#		print nodes[index1]+nodes[index2]+nodes[temp_index2]+" - "+temp_value
					#		out.write(nodes[index1]+nodes[index2]+nodes[temp_index2]+"\t"+temp_value+"\n")
	out.close()
#findEmotionWords("network/dropped","network/pws")
#findEmotionWords("network/minused.edges","network/minused.vertices","network/hws")
#findEmotionWords("network/minused.edges","network/minused.vertices","network/pws")
#minusNetworks("Murmur/total/all", "Twitter/News/all")
#minusNetworks("Murmur/total/moods/angry.json", "")
#minusNetworks("network/emo","network/all")
#findEmotionWordsTriGram("network/minused.edges","network/minused.vertices","network/hws")



word_list = ["TODAY","IS","GOOD","!"]
T_test = []
with open("dumper_portal_musicALL.txt",'r') as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split('\t')
        if len(split_line) != 2: continue
        uid, text = split_line
        for i in tokens(regPatterns(checktag(removeRT(del_url(text))))):
            T_test.append(i)
minusNetworks(T_test)

# print tokens(regPatterns(checktag(removeRT(del_url("today is good!")))))