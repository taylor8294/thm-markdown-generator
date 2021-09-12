# TryHackMe Room Markdown Generator

_Python script for automatically generating a markdown question-and-answers file for TryHackMe rooms._

[TryHackMe](https://tryhackme.com) is a free online platform for learning cyber security, using hands-on exercises and labs, all through your browser.

When completing the 'rooms' that TryHackMe offers, many users want to take note of their answers and how they solved the room as they go. This can lead to a lot of copying and pasting of the questions from the room webpage into your write-up.

I came across [this blog post](https://burakb.net/tryhackme-tasks-and-questions-to-markdown-snippet/) which presents a way to automatically generate a starting template write-up file (in markdown syntax) by pasting a little javascript into the browser console on the room's webpage. I felt it was a useful little tool when working with TryHackMe, so turned it into a python script for easier use from the command line. 

## Install

### Download

I use [`pdm`](https://github.com/pdm-project/pdm) to manage my python projects.

``` bash
git clone https://github.com/taylor8294/THM-Room-Markdown.git
cd THM-Room-Markdown
pdm sync
pdm run python src/THM-Room-Markdown.py -h
```

To do so just using regular old `pip` (without PEP 582 support)

``` bash
git clone https://github.com/taylor8294/THM-Room-Markdown.git
cd THM-Room-Markdown
pip install -r requirements.txt
python src/THM-Room-Markdown.py -h
```

## Example Usage

You just need to run the script, passing it a room code and an output file.

```
$ pdm run python src\THM-Room-Markdown.py -h
usage: THM-Room-Markdown.py [-h] [-o OUTPUT] [-d] [-v] room

TryHackMe Room Markdown Note Generator

positional arguments:
  room                  Room code (from the room URL)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output to file
  -d, --disable-markdown
                        Disable changing question HTML to markdown format
  -v, --verbose         Verbose output (includes task descriptions)

$ pdm run python src\THM-Room-Markdown.py tutorial -o tutorial.md
Output written to ./tutorial.md

$ 
```

The contents of `tutorial.md` will then be as below.

````markdown
![Tutorial](https://tryhackme.com/img/banners/default_tryhackme.png)

# Tutorial

***Learn how to use a TryHackMe room to start your upskilling in cyber security.***

`#tutorial`

[Link to room](https://tryhackme.com/room/tutorial)

**Author:** *[tryhackme](https://tryhackme.com/p/tryhackme)*

Room published: 2020-06-12 20:40

Room started: 2021-09-12 01:47

Room finished:

## Task 1: Starting your first machine

1) Follow the steps in this task. What is the flag text shown on the website of the machine you started on this task?  
*A flag is just a piece of text that's used to verify you've performed a certain action. In security challenges, users are asked to find flags to prove that they've successfully hacked a machine*

```

```


````

## License

### Commercial license

If you want to use THM-Markdown-Generator as part of a commercial site, tool, project, or application, the Commercial license is the appropriate license. With this option, your source code is kept proprietary. To acquire a THM-Markdown-Generator Commercial License please [contact me](https://www.taylrr.co.uk/).

### Open source license

If you are creating an open source application under a license compatible with the [GNU GPL license v3](https://www.gnu.org/licenses/gpl-3.0.html), you may use THM-Markdown-Generator under the terms of the GPLv3.

---

By [Taylor8294 🌈🐻](https://www.taylrr.co.uk/)