# ASP2(C)NL 

intro

## CNL2NL 

#### Python request libraries

`lark inflect multipledispatch` are the only required libraries. Optionally, `openai` should be also installed if you plan to use it.
```
pip install lark inflect multipledispatch openai 
```

### About LLM  

In order to convert CNL into plan natural language the script needs access to an Large Language Model. 
We suggest to use an open source library called Ollama which download and run pre-trained LLMs locally. 
Alternatively, OpenAI's ChatGPT can be also invoked but a valid api key is required. The api key must be stored in the environment variable `OPENAI_API_KEY`

#### Install Ollama on Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

For installation on other systems, please refer to [Download Ollama](https://ollama.com/download)

Run the following command to disable automatic Ollama serving 
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

#### ASP2NL

Syntax to convert an asp program into natural language via CNL

```
python asp2nl/asp2nl.py <ASP PROGRAM FILE> <DEFINITION FILE> <LLM MODEL NAME>
```

The default value `<LLM MODEL NAME>` is set to  `openchat` and can be omitted. Results will be stored into the json file `asp2cnl2nl.json`

A simple example is
```
python asp2nl/asp2nl.py example/maxclique/maxclique.asp example/maxclique/schema.cnl
```

#### ASP2NL

Syntax to convert an asp program into natural language via CNL

```
python asp2nl/asp2nl.py <ASP PROGRAM FILE> <DEFINITION FILE> <LLM MODEL NAME>
```

The default value `<LLM MODEL NAME>` is set to  `openchat` and can be omitted. Results will be stored into the json file `asp2cnl2nl.json`

A simple example is
```
python asp2nl/asp2nl.py example/maxclique/maxclique.asp example/maxclique/schema.cnl
```

#### CNL2NL

Syntax to convert a list of CNL sentences into natural language using a LLM

```
python cnl2nl/cnl2nl.py <CNL JSON FILE> <LLM MODEL NAME>
```

The default value `<LLM MODEL NAME>` is set to  `openchat` and can be omitted. Results will be stored into the json file `cnl2nl.json`

A simple example is
```
python cnl2nl/cnl2nl.py examples/cnl_example.json
```