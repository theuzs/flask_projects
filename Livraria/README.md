# Modelo Entidade-Relacionamento (MER)

 ## Entidades:
Livro: Representa um livro na papelaria.

Atributos:
id_livro (PK)
titulo
isbn
edicao
editora
ano_publicacao
preco_capa
categoria
Autor: Representa um autor de livros.

Atributos:
id_autor (PK)
nome
nacionalidade
biografia
Estoque: Representa o controle de entrada e saída de livros no estoque.

Atributos:
id_estoque (PK)
id_livro (FK)
quantidade
data_entrada
data_saida
Venda: Representa uma venda realizada de um livro.

Atributos:
id_venda (PK)
id_livro (FK)
quantidade
data_venda
valor_total
Relacionamentos:
Livro-Autor: Um livro pode ter um ou mais autores, e um autor pode escrever vários livros.

Relacionamento M:N entre Livro e Autor (resolvido por uma tabela de junção chamada Livro_Autor).
Atributos da tabela de junção:
id_livro
id_autor
Livro-Estoque: Um livro pode ter múltiplas entradas e saídas de estoque.

Relacionamento 1:N entre Livro e Estoque.
Livro-Venda: Um livro pode ser vendido várias vezes.

Relacionamento 1:N entre Livro e Venda.


# Diagrama de Caso de Uso
               +--------------------+
               |    Funcionário      |
               +--------------------+
                        |
         +--------------+-------------------+
         |                                  |
   +-------------------+          +----------------------+
   | Cadastrar Livro   |          | Cadastrar Autor      |
   +-------------------+          +----------------------+
         |                                  |
   +-------------------+          +----------------------+
   | Registrar Entrada |          | Registrar Saída      |
   | de Estoque        |          | de Estoque           |
   +-------------------+          +----------------------+
         |                                  |
   +-------------------+          +----------------------+
   | Realizar Venda    |<-------->| Estoque              |
   +-------------------+          +----------------------+



# Diagrama Entidade-Relacionamento (DER)

+-----------------+        +-----------------------+       +-----------------+
|     Livro      |        |       Livro_Autor      |       |     Autor       |
+-----------------+        +-----------------------+       +-----------------+
| id_livro (PK)  |<-----> | id_livro (FK)          |       | id_autor (PK)   |
| titulo         |        | id_autor (FK)          |       | nome            |
| isbn           |        +-----------------------+        | nacionalidade   |
| edicao         |                                         | biografia       |
| editora        |                                         +-----------------+
| ano_publicacao |
| preco_capa     |
| categoria      |
+-----------------+    

         |
         | 1:N
         |
+-----------------+
|     Estoque     |
+-----------------+
| id_estoque (PK) |
| id_livro (FK)   |
| quantidade      |
| data_entrada    |
| data_saida      |
+-----------------+

         |
         | 1:N
         |
+-----------------+
|     Venda       |
+-----------------+
| id_venda (PK)   |
| id_livro (FK)   |
| quantidade      |
| data_venda      |
| valor_total     |
+-----------------+


![image](https://github.com/user-attachments/assets/b180a6f8-fbac-41fa-a30b-8400a34a8d48)

