from flask import Flask, render_template, request, redirect
from whoosh import index
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import *
app = Flask(__name__)
ix = open_dir("indexdir/")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    cancer=request.form['cancer']
    gene=request.form['gene']
    query_b = MultifieldParser(['Title','content'], ix.schema).parse('{} OR {}'.format(cancer, gene))
    with ix.searcher() as srch:
        res_b = srch.search(query_b, limit=20)
        results=[(i['Title'],i['name'],i['content'].split('.')[:3]) for i in res_b]
        return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run()
