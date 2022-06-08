import unittest
from ensino import *

class tester(unittest.TestCase):

	def setUp(self):
		self.f1 = Faculdade("Universidade Federal da Bahia")
		self.a1 = Aluno('Fulano da Silva', 20, 'Ciência da Computação')
		self.a2 = Aluno('Cicrano de Souza', 17, 'Sistemas de Informação')

		self.f1.add_aluno(self.a1)
		self.f1.add_aluno(self.a2)

	def test_adicao_de_aluno(self):
		self.assertEqual(self.f1.get_total_alunos() , 2)
		#self.assertEqual('foo'.upper(), 'FOO')
		#self.assertTrue()
		#self.assertFalse()

	# def test_se_aluno_pertence_faculdade1(self):
	# 	self.assertTrue(self.f1.is_aluno(self.a1))

	def test_se_aluno_pertence_faculdade2(self):
		self.assertTrue(self.f1.is_aluno(self.a2))

	def verifying_se_aluno_pertence_faculdade2(self):
		self.assertTrue(self.f1.is_aluno(self.a2))

	def test_useless(self):
		pass

if __name__ == '__main__':
    unittest.main()