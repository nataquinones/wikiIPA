---
layout: page
title: About
permalink: /about/
nav_order: 3
---
Last update: 2021-04-17
{: .label .label-nqo }

Version 0.01
{: .label .label-nqo }

# About

## Why?
A linguist friend was looking for pronunciation data for a class, and I tried to help by writing a quick script to scrape Wiktionary. After playing with that, I thought it would be interesting to have this information indexed by language, so I decided to build this website. Might be useful for someone else?

## How?
All this information was extracted from [Wiktionary](https://www.wiktionary.org)!

You can check out how the _code_ part works by checking the [Github repository](https://github.com/nataquinones/wikiIPA/) for this project. Briefly, there's this list called: [Terms with IPA pronunciation by language](https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language), I go one by one, and save 1) the term and 2) the pronunciation written with the International Phonetic Alphabet (IPA). That goes into tables, which are later on read and converted into markdown files to make this website.

You can **download** the tables with these results from [here](https://github.com/nataquinones/wikiIPA/tree/main/code/data/CURRENT/tables), or browse the [glossaries](../glossaries/). 

## Who?
- This project was made by [Natalia Quinones-Olvera](https://nataquinones.github.io)
- All the data comes from [Wiktionary](https://www.wiktionary.org)
- Website theme is [Just the Docs](https://github.com/just-the-docs/just-the-docs)

## Issues and contributions
The way the pronunciation data is submitted into Wiktionary is not standard, so there are a bunch of errors in the glossaries. If you let me know of an error by submitting an [issue](https://github.com/nataquinones/wikiIPA/issues), I'll do my best to get it fixed!

## Versions
- **0.01**: *2021-04-17* Incomplete first version to test the site.
