# webeve

## Domain naming

Append lines from file `hosts` to your `/etc/hosts`. After it sites is avaliable

| Application | URL |
|-------------|-------------------------------|
| secureblog | http://secureblog |
| evilsite | http://evilsite |

## XXS

Contexts:
1. HTML
    * Tag
        <a>user_input</a>
        <a><script></a>

        <script>var login = `{{login}}`;</script>
    * Attribute value
        <a href="user_input">click me</a>
        <a href="javascript:alert(1)">click me</a>
        <a href="user_input">click me</a>
        <a href=""><script>attack</script><img title="a">click me</a>
        <a href=user_input>click me</a>
        <a href=asdf><script><img>click me</a>

        <input value="user_input">

2. DOM
    setTimeout("alert(`hello, {{login}}`)", 3000);
    

