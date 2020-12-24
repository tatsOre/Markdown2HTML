# Markdown to HMTL
Script that takes two arguments and parsing Markdown syntax for generating HTML:
* First argument is the name of the Markdown file
* Second argument is the output file name

## Headings:
| Markdown  | HTML generated |
| ------------- | ------------- |
| `# Heading level 1` | `<h1>Heading level 1</h1>` |
| `## Heading level 2` | `<h2>Heading level 2</h2>` |
| `### Heading level 3` | `<h3>Heading level 3</h3>` |
| `#### Heading level 4` | `<h4>Heading level 4</h4>` |
| `##### Heading level 5` | `<h5>Heading level 5</h5>` |
| `###### Heading level 6` | `<h6>Heading level 6</h6>` |

## Unordered listing:
**Markdown:**
```
- Hello
- Bye
```
**HTML generated:**
```
<ul>
    <li>Hello</li>
    <li>Bye</li>
</ul>
```

## Ordered listing:
**Markdown:**
```
* Hello
* Bye
```
**HTML generated:**
```
<ol>
    <li>Hello</li>
    <li>Bye</li>
</ol>
```

## Simple text:
**Markdown:**
```
Hello

I'm a text
with 2 lines
```
**HTML generated:**
```
<p>
    Hello
</p>
<p>
    I'm a text
        <br />
    with 2 lines
</p>
```

## Bold and emphasis text :
| Markdown  | HTML generated |
| ------------- | ------------- |
| `**Hello**` | `<b>Hello</b>` |
| `__Hello__` | `<em>Hello</em>` |


## Extra:
| Markdown  | HTML generated | description |
| ------------- | ------------- | ------------- |
| `[[Hello]]` | `8b1a9953c4611296a827abf8c47804d7` | convert in MD5 (lowercase) the content |
| `((Hello Chicago))` | `Hello hiago` | remove all `c` (case insensitive) from the content |

### Author:
* Tatiana Orejuela Zapata | [Github](https://github.com/tatsOre)
##### December, 2020. 
