class Faculdade:
	def __init__(self, nome):
		self.nome = nome
		self.professores = []
		self.alunos = []

	def add_aluno(self, aluno):
		self.alunos.append(aluno)

	def get_total_alunos(self):
		return len(self.alunos)

	def is_aluno(self, aluno):
		if (aluno in self.alunos):
			return True
		else:
			return False

class Aluno:
	def __init__(self, nome, idade, curso):
		self.nome = nome
		self.idade = idade
		self.curso = curso