import sys
sys.setrecursionlimit(10**5)


""""
13 9 12 3
4 11 1 10
8 2 -1 5
0 6 7 14
"""

""""
0 1 2 3
4 5 6 7
8 9 10 11
12 13 -1 14
"""



print("Les nombres doivent etre donnees de 0 à 14 et -1 indique la case vide")
grille = [list(map(int,sys.stdin.readline().split())) for  i in range(4)]
deplacement = list()
mini = 0
li=0
lj=0
h = 0
mini = 0

def position_vide():
	global li,lj
	for i in range(4):
		for j in range(4):
			if grille[i][j] == -1:
				li = i
				lj = j
				return None
	return None


def heuristique():
	s=0
	for i in range(4):
		for j in range(4):
			if grille[i][j] != -1:
				s+= abs(i-grille[i][j]//4) + abs(j-(grille[i][j]%4))
	return s


def final():
	for i in range(4):
		for j in range(4):
			if not (j==3 and i==3) and (grille[i][j]//4 != i or grille[i][j]%4 != j) :
				return False
	return True

def move(i,j):
	global h,grille,li,lj
	h += - abs(i-grille[i][j]//4) - abs(j-(grille[i][j]%4)) + abs(li-grille[i][j]//4) + abs(lj-(grille[i][j]%4))
	grille[li][lj] = grille[i][j]
	grille[i][j] = -1
	li = i
	lj = j

#deplace la case libre vers la gauche
def tente_gauche():
	if (deplacement == [] or deplacement[-1] != "droite") and lj != 0:
		move(li,lj-1)
		deplacement.append("gauche")
		return True
	else:
		return False

def tente_droite():
	if (deplacement == [] or deplacement[-1] != "gauche") and lj != 3:
		move(li,lj+1)
		deplacement.append("droite")
		return True
	else:
		return False

def tente_haut():
	if (deplacement == [] or deplacement[-1] != "bas") and li != 0:
		move(li-1,lj)
		deplacement.append("haut")
		return True
	else:
		return False

def tente_bas():
	if (deplacement == [] or deplacement[-1] != "haut") and li != 3:
		move(li+1,lj)
		deplacement.append("bas")
		return True
	else:
		return False	

def dfs(lim,p):
	global mini
	#print(grille)
	c = p + h
	if c > lim:
		if mini == -1 or c <= mini:
			mini = c
		return False
	if final():
		return True
	if tente_gauche():
		if not dfs(lim,p+1):
			deplacement.pop()
			move(li,lj+1)
		else:
			return True
	if tente_droite():
		if not dfs(lim,p+1):
			deplacement.pop()
			move(li,lj-1)
		else:
			return True
	if tente_bas():
		if not dfs(lim,p+1):
			deplacement.pop()
			move(li-1,lj)
		else:
			return True
	if tente_haut():
		if not dfs(lim,p+1):
			deplacement.pop()
			move(li+1,lj)
		else:
			return True
	return False
	

position_vide()


h = heuristique()
m = h
r = final()

while not r:
	mini = -1
	r = dfs(m,0)
	m = mini

print(deplacement)	
