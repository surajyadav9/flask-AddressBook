######   Understanding Python's request library (https://realpython.com/python-requests/)   #####

1. Install Python requests module
    $ pip install requests


2. Python shell (#GET)
    >> from requests import get, put, post, delete
    >> 
    >> res = get('http://localhost:5000/address/') 
    >>
    >> # status code
    >> res.status_code #200
    >>
    >> # header
    >> res.headers # {'Server': 'Werkzeug/2.2.2 Python/3.11.0', 'Date': 'Sat, 10 Dec 2022 14:19:05 GMT', 
                        'Content-Type': 'application/json', 'Content-Length': '169', 'Connection': 'close'}
    >>

    >> #received data --> deserialize using json
    >> res.json() # [{'_type': 'both', 'id': 1, 'isBusiness': True, 'isPermanent': True, 'mobile': 7980991768, 'name': 'suraj yadav', 'pincode': 10001}]
    >> 


3. Python shell (#POST - Success Example)
    >>
    >> # here we are passing a form type data i.e (text/html)
    >> res = post('http://localhost:5000/address/', data={'name':'surya bhai', 'mobile':7980991768, 'pincode':712123, '_type':'both'})
    >>
    >> res.status_code #201
    >>
    >> res.json() # {'_type': 'both', 'id': 2, 'isBusiness': True, 'isPermanent': True, 'mobile': 7980991768, 'name': 'surya bhai', 'pincode': 712123}


4. Python shell (#POST - Error Example --> returning text/html data)
    >> get('http://localhost:5000/address/').json() # [{'_type': 'both', 'id': 1, 'isBusiness': True, 'isPermanent': True, 'mobile': 7980991768, 'name': 'suraj yadav', 'pincode': 10001}, 
        {'_type': 'both', 'id': 2, 'isBusiness': True, 'isPermanent': True, 'mobile': 7980991768, 'name': 'surya bhai', 'pincode': 712123}]
    >> 
    >> 
    >>
    >> #posting data with duplicate name that will result in error according to our logic
    >> res = post('http://localhost:5000/address/', data={'name':'surya bhai', 'mobile':7980991768, 'pincode':712123, '_type':'both'})
    >>
    >> res.status_code # 400
    >>
    >> # GIVE A LOOK AT RETURN-TYPE
    >> res.headers # {'Server': 'Werkzeug/2.2.2 Python/3.11.0', 'Date': 'Sat, 10 Dec 2022 14:47:09 GMT', 
                        'Content-Type': 'text/html; charset=utf-8', 'Content-Length': '26', 'Connection': 'close'}

    >> 
    >> # returned content in bytes
    >> res.content # b'duplicate name not allowed'
    >>
    >> # return text data
    >> res.text # 'duplicate name not allowed'


5. Python shell (#POST - Error Example --> returning text/html data)
    >>
    >> # Passing Empty data
    >> res = post('http://localhost:5000/address/', data={  })
    >>
    >> res.status_code # 400
    >>
    >> res.content # b'incomplete data passed'
    >>
    >> res.text # 'incomplete data passed'


(BONUS)
6. Python shell (#POST - Passing JSON data)
    >> 
    >> res = post('http://localhost:5000/address/', json={ 'name':'hello world' }) # using json={} instead of data={}
    >>
    >> res.status_code # 201
    >> 
    >> res.headers # {'Server': 'Werkzeug/2.2.2 Python/3.11.0', 'Date': 'Sat, 10 Dec 2022 15:27:21 GMT', 
                        'Content-Type': 'application/json', 'Content-Length': '28', 'Connection': 'close'}
    >>
    >> res.json() # {'name': 'hello world'}
