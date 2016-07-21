MySQL Tunneling
---------------

ssh -fN root@209.126.121.94 -L 3306:localhost:3306

Solr Build
----------

http://209.126.121.94:8983/solr/calls/update?stream.body=<delete><query>*:*</query></delete>
http://209.126.121.94:8983/solr/calls/update?stream.body=<commit/>

http://209.126.121.94:8983/solr/callsfailed/update?stream.body=<delete><query>*:*</query></delete>
http://209.126.121.94:8983/solr/callsfailed/update?stream.body=<commit/>