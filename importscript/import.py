import psycopg2
import json

def importar_json_para_postgres():
    # Conectar ao banco de dados PostgreSQL
    conn = psycopg2.connect(
        dbname='rickandmorty',
        user='postgres',
        password='22910922',
        host='localhost',
        port='5432'
    )

    # postgresql://postgres:22910922@localhost:5432/rickandmorty

    # Abrir um cursor para executar comandos SQL
    cur = conn.cursor()

    # Carregar o arquivo JSON
    with open(r"C:\Users\felip\OneDrive\Documents\DEV\Rick and Morty\Rick e Morty-back\importscript\allCharsUpdated.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Ordenar os dados pelo campo 'id'
    sorted_data = sorted(data, key=lambda x: x['id'])

    # Criar a tabela 'characters'
    cur.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            status VARCHAR(100),
            species VARCHAR(100),
            type VARCHAR(100),
            gender VARCHAR(100),
            origin_name VARCHAR(100),
            location_name VARCHAR(100),
            image VARCHAR(500)
        )
    ''')

    conn.commit()

    # Iterar sobre os dados e inseri-los no PostgreSQL
    for item in sorted_data:
        # Substitua 'sua_tabela' pelo nome da tabela no seu banco de dados
        cur.execute("INSERT INTO characters (name, status, species, type, gender, origin_name, location_name, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item['name'], item['status'], item['species'], item['type'], item['gender'], item['origin']['name'], item['location']['name'], item['image']))


    # Commit para salvar as alterações no banco de dados
    conn.commit()

    # Fechar o cursor e a conexão
    cur.close()
    conn.close()

if __name__ == "__main__":
    importar_json_para_postgres()
