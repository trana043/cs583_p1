
import itertools
import re
from sys import argv



def mis(elem):
   global my_mis
   if elem in my_mis:
      return my_mis[elem]
   return 0

def sup(elem):
   global item_count
   if elem in item_count:
      return float(item_count[elem])/len(T)
   return 0

def level2_candidate_gen(L, phi):
   global  T
   C2 = [] #initialize the set of candidates
   for i in range (0, len(L)-1):  #for each item l in L in the same order
      if float(item_count[L[i]])/len(T) >= mis(L[i]):
         for j in range(i, len(L)):
            if j>i:
               if float(item_count[L[j]])/len(T)- mis(L[i]) >= 0.00005 and abs(sup(L[j]) - sup(L[i])) <= phi:
                  C2.append([L[i],L[j]])
   return C2


def MScandidate_gen(f_k0, phi):
   c_k1 = []
   #print f_k0
   for i in range(0, len(f_k0)):
      for j in range(0,len(f_k0)):
         if i == j:
            continue
         #copy transactions into 2 temp variable
         tmp1 = f_k0[i][0:len(f_k0[i])-1]
         tmp2 = f_k0[j][0:len(f_k0[j])-1]
         if cmp(tmp1, tmp2) != 0:
            continue
         
         #get the last item of the 2 transctions
         tmp3 = f_k0[i][len(f_k0[i])-1]
         tmp4 = f_k0[j][len(f_k0[j])-1]
         if tmp3 < tmp4 and abs(sup(tmp3) - sup(tmp4)) <= phi:
            #add the last item of transaction 2 to transaction 1 to make
            #new transaction
            c = (f_k0[i][:])
            c.append(tmp4)
            c_k1.append(c)
            for k in range(0, len(c)-1):
               s= c[:]
               del s[k]
               flag = 0
               if c[0] in s or (mis(c[1]) == mis(c[0])):
                  for fk in f_k0:
                     if in_transaction(s,fk):
                        flag = 1
                        break
                  # s is not in f_k0
                  if flag == 0:
                     c_k1.pop()
                     break
   return c_k1

def subset(itemset1, itemset2):
   t = False
   sub = []
   sub_result = True
   for i in itemset1:
      for j in itemset2:
         if i == j:
            t = True or t
      sub_result = sub_result and t
      t = False
   return sub_result

def count_itemset(Ck):
   count = 0
   global T
   for t in T:
      if subset(Ck, t):
         count = count+1
   return count

#read data from input file
def initialize_data(parameter, input_file):
   a = False
   file_handle = open(parameter, 'r')
   # parse the file to fill up MIS and SUP dictionary
   for line in file_handle:
      # parse MIS(10) = 0.
      if '=' in line and 'mis' in line.lower():
         tmp = line.split('=')
         elem = tmp[0]
         elem = elem.strip()
         elem = elem[4:]
         elem = elem[:-1]
         my_mis[elem] = float(tmp[1])
      elif '=' in line:
         tmp = line.split('=')
         global constrain
         constrain = float((tmp[1]).strip())
      elif 'cannot_be_together' in line:
         tmp = line[len('cannot_be_together:'):].split("{")
         tmp2 = []
         for t in tmp[1:]:
            tmp2.append(t.split('}')[0])
         tmp3 = []
         for e in tmp2:
            tmp3.append(e.split(','))
         tmp4 = []
         for arr in tmp3:
            tmp5 = []
            for elem in arr:
               if elem[0] == ' ':
                  tmp5.append(elem[1:]) # string to int => tmp5.append(int(elem[1:]))
               else:
                  tmp5.append(elem)
            tmp4.append(tmp5)
         global not_together
         not_together = tmp4
         #print 'cannot_be_together:'+str(tmp4)

      elif 'must-have' in line:
         global tempor
         tempor = line.split(': ')[1].split(" or ")
         a = True
   if not a:
      if not a:
         tempor = my_mis.keys()

   file_handle = open(input_file, 'r')
   my_hash = {}
   for line in file_handle:
      a = line.strip()
      tmp = a[1:len(a)-1]
      temp = tmp.split(',')
      seq = []
      for i in temp:
         y = i.strip()
         if y in item_count:
            item_count[y] += 1
         else:
            item_count[y] = 1
         seq.append(y)
      T.append(seq)
   #print item_count
   for k in my_hash.keys():
      my_sup[k] = my_hash[k]

def subsets(s):
	# base case
	if len(s) == 0:
		return [[]]
	# the input set is not empty, divide and conquer!
	h, t = s[0], s[1:]
	ss_excl_h = subsets(t)
	ss_incl_h = [([h] + ss) for ss in ss_excl_h]
	return ss_incl_h + ss_excl_h


def in_transaction(c, trans):
   if len(c) > len(trans):
      return 0
   
   for i in c:
      if i not in trans:
         return 0
   return 1

def selection_sort(my_list):
   flag = 0
   for index in range(len(my_list)):
       for location in range(index+1,len(my_list)):
           flag = 0
           if mis(my_list[location])<mis(my_list[index]):
               flag = 1
           if mis(my_list[location])==mis(my_list[index]) and my_list[location]<(my_list[index]):
               flag = 1
           if flag ==1:
              temp = my_list[index]
              my_list[index] = my_list[location]
              my_list[location] = temp


                           
constrain = 0
T = []
my_mis = {}   # the dictionary that contains mis of all items
my_sup = {}   # the dictionary contains sup of all items
item_count = {}
not_together = {}
not_together = []
tempor = []

initialize_data('parameter.txt', 'input.txt')
M = (item_count.keys())
#sort M based on mis values
selection_sort(M)
flag = 0
first_item_mis = 0
L = []
#first pass overt T
for item in M:
   if flag == 0 and sup(item) > mis(item):
      L.append(item)
      flag = 1
      first_item_mis = mis(item)
      continue
   if flag == 1:
      if sup(item) >= first_item_mis:
         L.append(item)
f1 = []
for item in L:
   if float(item_count[item])/len(T) >= mis(item):
      f1.append([item])

k = 2
ck = []
all_f = f1

while len(f1)!= 0:
   if k==2:
      ck = level2_candidate_gen(L, constrain)
   else:
      #print "ms gen"
      ck = MScandidate_gen(f1, constrain)
   if len(ck) == 0:
      break
   k+=1
   tmp_count = {}
   for transaction in T:
      for c in ck:
         if in_transaction(c,transaction):
            if ",".join(c) in tmp_count:
               tmp_count[",".join(c)] += 1
            else:
               tmp_count[",".join(c)] = 1
         tmp = c[1:]
         if in_transaction(tmp, transaction):
            if ",".join(tmp) in tmp_count:
               tmp_count[",".join(tmp)] += 1
            else:
               tmp_count[",".join(tmp)] = 1
   f1 = []

   for c in ck:
      if ",".join(c) not in tmp_count:
         continue
      if tmp_count[",".join(c)]/float(len(T)) >= mis(c[0]):
         f1.append(c)


   all_f = all_f + f1


res = []
for seq in all_f:
   flag = 0
   for item in tempor:
      if item in seq:
         flag = 1
         break
   if flag == 1:
      for item in not_together:
         if in_transaction(item, seq):
            flag = 0
            break
   if flag == 1:
      res.append(seq)

result={}
for seq in res:
   if len(seq)==0:
      continue
   l = len(seq)
   if l not in result:
      result[l] = {}
   result[l][','.join(seq)]= count_itemset(seq)

if len(result):
  for length in result:
    print "Frequent ", length, "-itemsets"
    for seq in result[length]:
      tmp = (seq.strip()).split(',')
      if len(tmp) > 1:
         selection_sort(tmp)
      print "   ", result[length][seq], ":{", ','.join(tmp), "}"
      tmp = seq.split(',')

      if len(tmp[1:])!= 0:
         print "tail_count = ", count_itemset(tmp[1:])
    print("\n")
    print "   Total number of Frequent ", length, "-itemsets", len(result[length])
    print "\n"
else:
  print "Frequent 1-itemsets"
  print "  Total number of Frequent 1-itemsets = 0"
