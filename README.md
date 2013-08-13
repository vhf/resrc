resrc
=====

### TODO and FIXME everywhere
`grep TODO -R resrc/*` kthxbye

### run the project
1. `python manage.py syncdb && python manage.py migrate && python manage.py loaddata data.json`
2. Say no to superuser creation. Use existing credentials `root:qwer`
3. sample accounts : `victor:qwer` (superuser + user), `foobar:qwer` (user only)

### run the tests
1. `pip install -r requirements_dev.txt --upgrade`
2. `fab test` to run once, `watchmedo.sh` for continuous testing

### temporary priority list
1. links
2. tags
3. lists
4. templates

## basic features
- **links**
- a **link** can be commented
- a **user** can create **lists** of **links**
- a **list** can be commented
- a **list** can be either public or private
- a **link** is tagged
- a **user** has two default **lists** : `favorites` (star ?) and `toread` (check mark ?)
- a user create **lists** is freeform
- default **lists** are not freeform
- user can filter a **list** according to criteria
- a **link** can be flagged dead
- **user** can `fav`, `toread` a **link**, **list**
- **user** can suggest **link** to **list**

## feature requests

- **links** are cached (?)
- **lists** can be collaborative work (various owners)
- **links** have TL;DR

## meta tags
- level (101 / intermediate / expert)
- resource type (book, try online, articule, ...)
- language ?
