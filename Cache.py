class Cache(object):
	"""
	Desenvolver um cache simples, em memória, para que não seja necessária uma nova
consulta no banco de dados para os alunos recém-acessados. O cache deverá conter no MÁXIMO
10 itens (ou seja, dados de no máximo 10 alunos). O cache também deverá levar em conta dados
recém-cadastrados. Exemplos de comportamento do cache:
1. O endpoint 5 (Buscar aluno) busca por aluno de ra 123. Em seguida, o mesmo endpoint é
acessado também para o aluno de ra 123. Como esse dado já havia sido buscado no banco
recentemente, a aplicação não deve fazer uma nova leitura no banco mas sim ler do cache;
2. O endpoint 4 (Cadastrar aluno) registra aluno de ra 321. Em seguida o endoint 5 (Buscar aluno) é
acessado para o aluno de 321. Como esse aluno acabou de ser registrado, a aplicação não deve fazer
nova leitura no banco mas sim ler do cache.
O critério de evasão (momento em que um dado deve ser removido da cache para dar lugar a
outro mais recente) fica por sua conta.
"""
	def __init__(self, size):
		self.size = size
		self.cache = dict()
		self.keys = []
	
	def set(self,key,value):
		self.cache[key] = value
		self.keys.append(key)
		if len(self.cache) > self.size:
			evade = self.keys.pop(0)
			del self.cache[evade]

	def get(self,key):
		if key not in self.cache:
			return False
		return self.cache[key]

	def dump(self):
		return self.cache
