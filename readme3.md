Resume lancement : 

Dans chaque terminal distinct : 

Docker pipeline : 
   docker compose up --build

Docker API : 
   docker compose up --build api

Front : 
   cd .\frontend\
   python -m http.server 5500
   link : http://localhost:5500