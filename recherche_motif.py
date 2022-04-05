import sys

"""Calcul l'esperance de la premiere apparition d'un motif dans une repetition de Pile ou Face"""

"""Le calcul matrciel est tres lent, a optimiser plus tard"""

def construit_automate(motif): # ne fonctionne pas... besoin de KMP ?
	n = len(motif)
	automate = [ [ [False]*(n+1),[False]*(n+1) ] for i in range(n+1)]
	automate[0][0][0] = True
	automate[0][1][0] = True
	for i in range(n):
		if motif[i]=="P":
			automate[i][0][i+1] = True
		else:
			automate[i][1][i+1] = True
	automate[n][0][n] = True
	automate[n][1][n] = True
	return automate


def determinise_automate(automate):
	table = []
	transition = []
	pile = [[0]]
	n = len(automate)
	while pile != []:
		P_accessibles = []
		F_accessibles = []
		q = pile[0]
		pile.pop()
		if (n-1) in q: #on a trouvé un etat final, on le connecte a lui meme
			P_accessibles = [e for e in q]
			F_accessibles = [e for e in q]
		else:
			for e in q:
				for i in range(n):
					if automate[e][0][i]:
						P_accessibles.append(i)
					if automate[e][1][i]:
						F_accessibles.append(i)
		table.append(q)
		transition.append(P_accessibles)
		transition.append(F_accessibles)
		if not P_accessibles in table:
			pile.append(P_accessibles)
		if not F_accessibles in table:
			pile.append(F_accessibles)
	print("table ", table)
	print(transition)
	k = len(table)
	automate_det = [[i,i] for i in range(k)]
	for i in range(k):
		P_transition = transition[2*i]
		automate_det[i][0] = table.index(P_transition)
		F_transition = transition[2*i+1]
		automate_det[i][1] = table.index(F_transition)	

	return automate_det

def construit_matrice(automate):
	n = len(automate)
	mat = [[0]*n for i in range(n)]
	for i in range(n):
		s1,s2=automate[i][0],automate[i][1]
		mat[s1][i] += 0.5
		mat[s2][i] += 0.5
	return mat

def produit_matriciel(a,b):
	n,m = len(a),len(a[0])
	p,q = len(b),len(b[0])
	if m!=p:
		return "Format invalide"
	mat = [[0]*q for i in range(n)]
	for i in range(n):
		for j in range(q):
			for k in range(m):
				mat[i][j]+=a[i][k]*b[k][j]
	return mat

def matrice_extraite(a,i,j): #donne la matrice extraite de A ou on retire la ligne i et la colonne j (indexe a partir de 0)
	n,m = len(a),len(a[0])
	extraite = [[0]*(m-1) for i in range(n-1)]
	for l in range(n):
		if l>i:
			indice_ligne = l-1
		else:
			indice_ligne = l
		for c in range(m):
			if c>j:
				indice_col = c-1
			else:
				indice_col = c
			if i!=l and j!=c:
				extraite[indice_ligne][indice_col] = a[l][c]
	return extraite

def determinant(a):
	det = 0
	n,m = len(a),len(a[0])
	if n!=m:
		return "Dimension invalide"
	if n==1:
		return a[0][0]
	for i in range(n): #dev C1
		det += (-1)**(i)*a[i][0]*determinant(matrice_extraite(a,i,0))
	return det

def inverse(a):
	if determinant(a)==0:
		return "matrice non inversible"
	d=determinant(a)
	n = len(a)
	tcomat = [[0]*(n) for i in range(n)]
	for i in range(n):
		for j in range(n):
			tcomat[j][i] = (-1)**(i+j)*determinant(matrice_extraite(a,i,j))/d
	return tcomat

def identite(n):
	mat = [[0]*n for i in range(n)]
	for i in range(n):
		mat[i][i] = 1
	return mat

def moins(A,B):
	n = len(A)
	return [[A[i][j]-B[i][j] for j in range(n)]for i in range(n)]

def calcul_esperance(motif):
	automate = determinise_automate(construit_automate(motif))
	A = construit_matrice(automate)
	n = len(A)
	print("matrice: ", A)
	B = matrice_extraite(moins(identite(len(A)),A),len(A)-1,len(A)-1)
	print(B)
	if determinant(B)==0:
		return "Det nul..."
	print("inverse: ", inverse(B))
	X0 = [[0] for i in range(len(A)-1)]
	X0[0][0] = 1
	U = [[1]*(len(A)-1)]
	print(U,X0)
	print(produit_matriciel(inverse(B),X0))
	return produit_matriciel(produit_matriciel(U,inverse(B)), X0)


motif = input("Motif: ")
E = calcul_esperance(motif)[0][0]
print("Temps moyen avant la premiere apparition du motif: ", E )