resrc
=====

# run the project
- python manage.py syncdb && python manage.py migrate
- accounts : root:qwer (superuser only), victor:qwer (superuser + user), foobar:qwer (user only)

# temporary priority list
1. lists
2. tags
3. template

# basic features
- **links**
- a **link** can be commented
- a **user** can create **lists** of **links**
- a **list** can be commented
- a **list** can be either public or private
- a **link** is tagged
- a **link**, a **list**, a comment can be up/down voted, have karma
- a **user** holds karma of his own published **links**, **lists**, comments
- a **user** has two default **lists** : `favorites` (star ?) and `toread` (check mark ?)
- a **list** is ordered or not (**list** owner has the choice)
- user can filter a **list** according to criteria
- a **list** is (un)ordered
- a **link** can be flagged dead
- **user** can `fav`, `toread` a **link**, **list**
- **user** can suggest **link** to **list**

## feature requests

- **links** are cached (?)
- **lists** can be collaborative work (various owners)
- **links** have TL;DR

# Templates
## Public
### Frontpage
- Tag tree
- Featured lists

### Lists
- List of public **lists**

### Search
- Elaborate search engine

### Tags
- Browse links/lists by tag
- Browse tag tree

## Private (user)
- My **lists**
- My comments

# Tag implementation ideas and examples
> http://12devs.co.uk/articles/204/
>
> Middleman IS_IN Ruby
>
> Ruby IS_A Programming Language
>
> Middleman IS_A Static site generator
>
> link#1 IS_ABOUT Middleman
>
> -> hence filing shows :
>
> Ruby (Language) > Middleman (Static site generator)
>
> Link title : Building static websites(TAG) with Middleman(TAG), deploying to Heroku(TAG)

howto, guide, course

