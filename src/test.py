import psycopg2


DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

c.execute('insert into stocks (ticker, stock, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s)', ["AMC", "AMC THEATRES", "https", "0", "0", "0"])
conn.commit()

c.execute('select * from stocks')
records = c.fetchall()
print(records)
