#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wsgiref import simple_server
import datetime
import csv
from urllib.parse import parse_qs

HTML_FILE = 'index.html'
CSV_FILE = 'board.csv'
CONTENT_TYPE_HTML = 'text/html; charset=utf-8'

def read_html_file():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def save_message(post_data):
    parsed_data = parse_qs(post_data)
    name = parsed_data.get('name', [''])[0]
    message = parsed_data.get('message', [''])[0]
    dtm = datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        board = csv.writer(f)
        board.writerow([dtm, name, message])

def read_messages():
    messages = ''
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            messages += line.strip() + '<br>'
    return messages

def application(environ, start_response):
    headers = [('Content-type', CONTENT_TYPE_HTML)]
    status = '200 OK'
    method = environ.get('REQUEST_METHOD')

    if method == 'GET':
        body = read_html_file()
    elif method == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
        save_message(post_data)
        body = read_messages()
        body += '<a href="/index.html"><button>投稿画面へ戻る</button></a>'
    else:
        body = 'Unsupported method'

    start_response(status, headers)
    return [body.encode('utf-8')]

if __name__ == '__main__':
    host = ''
    port = 8000
    server = simple_server.make_server(host, port, application)
    server.serve_forever()
