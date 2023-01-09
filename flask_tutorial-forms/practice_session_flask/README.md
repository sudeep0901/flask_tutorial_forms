
# auto reload code

```python
export FLASK_ENV=development # deprecated
export FLASK_DEBUG=1 

```
![](2023-01-07-09-52-05.png)

# Using Bootstap
```shell
(venv) $ pip install flask-bootstrap
```

### issue
TemplateNotFound
jinja2.exceptions.TemplateNotFound: bootstrap/base.html


#Links
url_for() helper function
url_for('index') would return /, the root URL of the application. 

Calling url_for('index', _external=True) would instead return an absolute URL, which in this example is http://localhost:5000/.

# static files
url_for('static', filename='css/styles.css', _external=True) would return http://localhost:5000/static/css/styles.css.


```sql
create table customer(fname varchar(50), lname varchar(50));
create user 'admin'@'localhost' identified by 'admin';
alter table customer add column id int auto_increment primary key;

grant all privileges on *.* to 'admin'@'localhost' identified by 'admin' with grant option;
```
```shell
pip install pymysql

pip install mysql-connector-python

```