# ASP2(C)NL 

ASP2(C)NL is composed by two novel and open-source tools, namely ASP2CNL and CNL2NL.

With ASP2CNL, ASP rules are converted into Controlled Natural Language (CNL) sentences in
the format supported by the tool CNL2ASP [1].

Subsequently, CNL2NL translate the obtained CNL sentences into natural language sentences 
using the state-of-the-art LLM tool ChatGPT. 

Finally, the two tools, can be combined together in a pipeline, referred to as ASP2NL, 
that transforms a given ASP program into a set of sentences expressed in a natural language.

[1]: Caruso, Simone & Dodaro, Carmine & Maratea, Marco & Mochi, Marco & 
 		Riccio, Francesco. (2023). CNL2ASP: Converting Controlled Natural Language Sentences into ASP. 
 		Theory and Practice of Logic Programming. 24. 1-31. 10.1017/S1471068423000388. [Link](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/cnl2asp-converting-controlled-natural-language-sentences-into-asp/AF5901FADC579E49C583CFD5A10C0192).


#### Python request libraries

Python version 3.10 is required.

`lark inflect multipledispatch` are the only required libraries. Optionally, `openai` should be also installed if you plan to use it.
```
pip install lark inflect multipledispatch openai 
```

## ASP2CNL

A prototype for automatic converting ASP rules into Controlled Natural Language (CNL) 
sentences in the format supported by the tool CNL2ASP.

## CNL2NL 

### Access to a LLM  is required

In order to convert CNL into plan natural language the CNL2NL tool needs access to a Large Language Model. 
We suggest to use an open source library called Ollama which download and run pre-trained LLMs locally. 
Alternatively, OpenAI's ChatGPT can be also invoked but a valid api key is required. The api key must be stored in the environment variable `OPENAI_API_KEY`

#### Install Ollama on Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

For installation on other systems, please refer to [Download Ollama](https://ollama.com/download)

Note:By default Ollama launch itself as system service. If you do not want such behaviour, please, run the following command to disable automatic Ollama serving 
```
sudo systemctl disable ollama.service
```

Once completed the installation process we have to download the model we want to use.
The simplest way to complete this task is by running the following command  

```
ollama run <LLM MODEL NAME>
```
Where `<LLM MODEL NAME>` is any model present in the Ollama library, an update list can be found at [Ollama - Model List](https://ollama.com/library) 

We suggest to use [openChat](https://ollama.com/library/openchat) as alternative to ChatGPT:

```
ollama run openchat
```


### Getting start

#### ASP2CNL

Syntax to convert an ASP program into Controlled Natural Language (CNL).

``` 
python asp2cnl/asp2cnl.py -f <ASP PROGRAM FILE> -d <DEFINITION FILE> [-o <OUTPUT JSON FILE>]
```

The result will be printed to the standard output as a list of CNL sentences. In the case where 
a JSON format is needed, the option -o can be used, allowing to save the results to a file. 

A simple example is
```
python asp2cnl/asp2cnl.py -f example/maxclique/maxclique.asp -d example/maxclique/schema.cnl
```

#### CNL2NL

Syntax to convert a list of CNL sentences into natural language using a LLM

```
python cnl2nl/cnl2nl.py -f <CNL JSON FILE> -m <LLM MODEL NAME> -o <OUTPUT JSON FILE>
```

The default value `<LLM MODEL NAME>` is set to  `openchat` and can be omitted. Results will be stored into a json file whose default name is `cnl2nl.json`

A simple example is
```
python cnl2nl/cnl2nl.py -f examples/cnl_example.json
```

#### ASP2NL

Syntax to convert an asp program into natural language via CNL

```
python asp2nl/asp2nl.py -f <ASP PROGRAM FILE> -d <DEFINITION FILE> -m <LLM MODEL NAME> -o <OUTPUT JSON FILE>
```

The default value `<LLM MODEL NAME>` is set to  `openchat` and can be omitted. Results will be stored into a json file whose default name is `asp2cnl2nl.json`

A simple example is
```
python asp2nl/asp2nl.py -f example/maxclique/maxclique.asp -d example/maxclique/schema.cnl
```

