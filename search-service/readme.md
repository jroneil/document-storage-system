```
search-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── services/
│   │   └── elasticsearch_client.py
│   ├── utils/
│   │   └── search_utils.py
│   └── tests/
│       └── test_search.py
├── requirements.txt
└── Dockerfile
```
docker-compose build --no-cache search-service
