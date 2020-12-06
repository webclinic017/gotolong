

1> NSE 
Download following

https://www.nseindia.com/content/indices/ind_nifty500list.csv

https://www.nseindia.com/products/content/equities/indices/nifty_500.htm


2> BSE

Download following

https://www.bseindia.com/sensexview/IndicesWatch_weight.aspx?iname=BSE500&index_Code=17


click on excel icon on right hand side.


3> It is useful to get unique industries

ISIN DB

1. Get unique industries  from ISIN db. It would be useful to know portfolio distribution.

MariaDB [gotolong]> select distinct comp_industry from global_isin;
+--------------------------+
| comp_industry            |
+--------------------------+
| Industry                 |
| SERVICES                 |
| IT                       |
| INDUSTRIAL MANUFACTURING |
| CEMENT & CEMENT PRODUCTS |
| METALS                   |
| FINANCIAL SERVICES       |
| CHEMICALS                |
| ENERGY                   |
| CONSUMER GOODS           |
| PHARMA                   |
| AUTOMOBILE               |
| HEALTHCARE SERVICES      |
| CONSTRUCTION             |
| PAPER                    |
| TELECOM                  |
| TEXTILES                 |
| FERTILISERS & PESTICIDES |
| MEDIA & ENTERTAINMENT    |
+--------------------------+
19 rows in set (0.021 sec)

MariaDB [gotolong]>