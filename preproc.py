import os
import re
import sys

sent_ids = []

def extract_sent_id(file):
	temp_ids = [-1]	# base 1 indexing
	with open(file) as  raw_file:
		for line in raw_file:
			if(line.startswith("<Sentence id=")):
				temp_ids.append(int(re.findall(r'[0-9]+',line)[0]))
	return temp_ids

data = {}

# {
#     'text' : String form of chunk
#     'name' : Unique Chunk name in a sent (NP2)
#     'tag' : General Chunk name (NP)
#     'drel' :  {
#                        'head' : 'name' of head chunk
#                        'rel' : Relation b/w head and child
#                  }
# }

def load_text(file, sent_ids):

	with open(file) as  text_file:
		for sentence in text_file:
			sentence = sentence.rstrip('\n').split('\t')
			i = 0
			sent_num = chunk_num = -1
			while i in range(len(sentence)):
				word = sentence[i]

				if(re.match(r'[0-9]+\.[0-9]+@#',word)):

					if(sent_num >= 0):
						data[sent_num][chunk_num]['text'] = data[sent_num][chunk_num]['text'].rstrip(' ')

					indices = word.rstrip('@#').split('.')
					sent_num = sent_ids[int(indices[1])]
					chunk_num = sent_ids[int(indices[0])]

					if(sent_num not in data):
						data[sent_num] = {}
					if(chunk_num not in data[sent_num]):
						data[sent_num][chunk_num] = {}
						data[sent_num][chunk_num]['text'] = ""

				else:
					data[sent_num][chunk_num]['text'] += (word+" ")

				i+=1
			data[sent_num][chunk_num]['text'] = data[sent_num][chunk_num]['text'].rstrip(' ')


def load_attr(file, sent_ids):

	with open(file) as  attr_file:
		for sentence in attr_file:
			sentence = sentence.rstrip('\n').split('\t')
			i = 0
			sent_num = chunk_num = -1
			while i in range(len(sentence)):
				word = sentence[i]

				if(re.match(r'[0-9]+\.[0-9]+@#',word)):

					indices = word.rstrip('@#').split('.')
					sent_num = sent_ids[int(indices[1])]
					chunk_num = sent_ids[int(indices[0])]

					if(chunk_num not in data[sent_num]):
						data[sent_num][chunk_num] = {}
						data[sent_num][chunk_num]['text'] = 'UNK' 

					data[sent_num][chunk_num]['drel'] = {}
					data[sent_num][chunk_num]['drel']['rel'] = None
					data[sent_num][chunk_num]['drel']['head'] = None

				else:
					if(word.startswith("name=")):
						data[sent_num][chunk_num]['name'] = word.split("'")[1]
					elif(word.startswith("drel=")):
						drel = word.split("'")[1]
						data[sent_num][chunk_num]['drel'] = {}
						data[sent_num][chunk_num]['drel']['rel'] = drel.split(':')[0]
						data[sent_num][chunk_num]['drel']['head'] = drel.split(':')[1]
					elif(data[sent_num][chunk_num]['text'] == 'UNK' and word.startswith("af=")):
						data[sent_num][chunk_num]['text'] = word.split("='")[1].split(',')[0]

				i+=1


def basic_format(text_file, attr_file):

	load_text(text_file, sent_ids)
	load_attr(attr_file, sent_ids)
	return data

def chunk_format(sent_ids, text_file, attr_file):

	load_text(text_file, sent_ids)
	load_attr(attr_file, sent_ids)
	alter = {}
	for sentence in data:
		for chunk in data[sentence]:
			if(sentence not in alter):
				alter[sentence] = {}
			alter[sentence][data[sentence][chunk]['name']] = data[sentence][chunk]
	return alter

def preprocess(raw_file, text_file, attr_file, save_folder):

	sent_ids = extract_sent_id(raw_file)
	data = chunk_format(sent_ids, text_file, attr_file)
	save_path = "Dependency_Graphs/"+save_folder

	try:  
	    os.mkdir("Dependency_Graphs")  
	except OSError as error:
		pass

	try:
	    os.mkdir("Dependency_Graphs/"+save_folder)  
	except OSError as error:
		pass

	for s in data:
		dot_list = []
		dot_list.append("digraph {\n")
		sentence = data[s]

		for c in sentence:
			chunk = sentence[c]
			chunk_string = '\t'+chunk['name']
			chunk_string += ' '+'[label="'+chunk['text']+' ('+re.sub(r'[0-9]','',chunk['name'])+')'+'"]\n'
			dot_list.append(chunk_string)

		for c in sentence:
			chunk = sentence[c]
			if(chunk['drel']['head'] != None):
				rel_string = '\t'+chunk['drel']['head'] + ' -> ' + chunk['name'] + ' [label="'
				rel_string += chunk['drel']['rel'] + '"]\n'
				dot_list.append(rel_string)
			
		dot_list.append('}\n')

		file = open(save_path+"/sent_"+str(s)+".dot",'w')
		file.writelines(dot_list)
		file.close()

def check_input_files(inp):
	if(len(inp)!=4):
		print("Error: Incorrect number of arguments")
	for file in inp:
		if(os.path.exists(file)==False):
			print("Error: path does not exist [",file,"]")
			exit()

def main():
	inp = sys.argv
	check_input_files(inp[:-1])
	raw_file, text_file, attr_file, save_folder = inp[1], inp[2], inp[3], inp[4]
	preprocess(raw_file, text_file, attr_file, save_folder)

#-----------------------------

if __name__== "__main__":
   main()