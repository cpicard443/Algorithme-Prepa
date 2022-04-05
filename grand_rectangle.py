import sys

def pre_calcul(tab):
	n = len(tab)
	m = len(tab[0])
	col = [[(tab[i][j]+1)%2 for j in range(m)]for i in range(n)]
	for j in range(m):
		for i in range(1,n):
			if tab[i][j] == 1:
				col[i][j] = 0
			else:
				col[i][j] = col[i-1][j]+1
	return col

def calculL(histo):
	n = len(histo)
	L = [0]*n
	for i in range(n):
		j = i
		while j!=0 and histo[j-1]>=histo[i]:
			j = L[j-1]
		if j==0:
			L[i] = 0
		else:
			L[i] = j
	return L

def calculR(histo):
	n = len(histo)
	R = [0]*n
	for i in range(n-1,-1,-1):
		j = i
		while j!=(n-1) and histo[j+1]>=histo[i]:
			j = R[j+1]
		if j==(n-1):
			R[i] = n-1
		else:
			R[i] = j
	return R 

def plusGrandRectangleHisto(histo,L,R):
	n = len(histo)
	airemax = histo[n-1]
	cotemax = 0
	for i in range(n):
		l=L[i]
		h = histo[i]
		r = R[i]
		airemax = max(airemax, (r-l+1)*h)
		cotemax = max(cotemax,min(r-l+1,h))
	return (airemax,cotemax)

def cotemax(tab):
	col = pre_calcul(tab)
	#print(col)
	maxi = 0
	for lig in col:
		R = calculR(lig)
		L = calculL(lig)
		(a,c)=plusGrandRectangleHisto(lig,L,R)
		#print("RESULTAT: ", lig,a,c)
		#print(R,L)
		#print("__________")
		maxi = max(maxi,c)
	return maxi

n,m = map(int, sys.stdin.readline().split())
tab = [list(map(int, sys.stdin.readline().split()))for i in range(n)]
print(cotemax(tab))


