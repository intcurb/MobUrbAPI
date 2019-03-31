# MobUrbAPI
Esse repositório contem a API para a integração de dados responsáveis por gerar os dados de simulação.

## Requisitos

|Ferramenta|Instalação (Linux)|Site|
|-------------------|---------------------------|-------------------------------------------------|
|Python 2.7|sudo apt-get install python2.7|https://www.python.org/downloads/ |
|Pip|sudo apt-get install python-pip|https://pip.pypa.io/en/stable/installing/ |
|Git|sudo apt-get install git|https://git-scm.com/downloads |
|SUMO|sudo apt-get install sumo sumo-tools sumo-doc|https://sumo.dlr.de/wiki/Installing |
|Flask|pip install flask|https://pypi.org/project/Flask/ |
|Flask restful|pip install Flask-RESTful|https://pypi.org/project/Flask-RESTful/ |
|Flask Jsonpify|pip install Flask-Jsonpify|https://pypi.org/project/Flask-Jsonpify/ |
|SQLAlchemy|pip install SQLAlchemy|https://pypi.org/project/SQLAlchemy/ |
|pyproj|sudo apt-get install pyproj|https://packages.ubuntu.com/search?keywords=python-pyproj |
|pyproj|pip install pyproj|https://pypi.org/project/pyproj/ |
|lxml|pip install lxml|https://pypi.org/project/lxml/ |
|lxml|sudo apt-get install python-lxml|https://packages.ubuntu.com/search?keywords=python-lxml |

## Instalação

 - Clonar o projeto com o comando: git clone https://github.com/intcurb/MobUrbAPI.git
 
## SUMO
 - A API do MobUrb utiliza recursos básicos das ferramentas do SUMO, apesar do projeto já incorporar a pasta de ferramentas, é recomendado que o colaborador tenha o sumo instalado em sua máquina.

## Utilização do sistema
 - Dentro da pasta do projeto (raiz), executar o seguinte comando para que a API inicie a execução: python InfoTransCtd.py
 
 - A seguinte mensagem será exibida informando que a API está pronta para utilização na porta 5002 do seu localhost:
 
 ```
 * Serving Flask app "InfoTransCtd" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)
 ```
