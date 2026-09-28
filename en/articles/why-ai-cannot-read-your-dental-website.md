---
titre: How AI reads a dentist website, and why yours may be invisible
titre_court: Dentist website invisible to AI: why it happens
description: ChatGPT can't find my practice: why a dentist website stays invisible to AI, the four walls you can check yourself and how to fix each one.
accroche: An AI does not visit your website the way a patient does. It sends a crawler, reads the raw text, cross-checks it with other sources, then cites you or not. This article follows that path step by step and shows the four walls that make a dentist website invisible to AI, with a two-minute test for each one.
date: 2026-09-12
lecture: 7 min
sujets: AI search, practice website
resume: The path an AI crawler takes to your website, and the four walls that make it invisible: scripts, blocking, vague text, no outside sources, with the test and the fix for each.
fr: ia-lisent-site-dentiste-invisible
---

You followed the method in our article [Is your dental practice on ChatGPT?](https://en.developpia.fr/blog/is-my-dental-practice-on-chatgpt-ten-minute-check/) and the result is in: ChatGPT does not find your practice, or cites it with Doctolib (France's leading online booking platform) and never with your website. You have the number. The question left is why.

The answer lies in the path an AI travels to reach your website. That path is short, but it goes through four doors. If one of them is closed, the AI turns back and cites another dentist. Here is that path in plain words, then each wall, with a two-minute test and the fix that goes with it.

## The path an AI takes to your website

When a patient types "dentist for an implant in Nantes" into ChatGPT, the tool does not answer from memory. It runs a search, just as you would on Google, and gets a list of pages. Then it sends a crawler to read the ones it is interested in.

That crawler has a name. For ChatGPT, it is OAI-SearchBot, not GPTBot: GPTBot collects text to train the models, while OAI-SearchBot looks for pages to cite in answers. [OpenAI's page about its crawlers](https://platform.openai.com/docs/bots) describes both. At Anthropic, the company behind Claude, the crawler is called ClaudeBot. At Perplexity, PerplexityBot.

The crawler requests the page from your server, the computer that hosts your website. The server sends back a text file: the page as it leaves the server, before anything is displayed. The crawler reads that file as is. It does not run scripts, those small programs that build the page in the patient's browser. It does not "see" the page, it reads the text that arrives.

Next, the AI cross-checks. It compares what it read on your website with your Google Business Profile, Doctolib and the directory of the French Dental Council (Ordre national des chirurgiens-dentistes). If everything matches and answers the patient's question, it cites you, with the source. Otherwise, it moves on to the next practice. Our guide [How ChatGPT chooses the dentist it recommends](https://en.developpia.fr/guides/how-ai-chooses-a-dentist/) details that final choice. Here, we look at what happens before: the four walls that stop the crawler along the way.

## First wall: your text is built by scripts

Many recent websites are delivered almost empty. The file sent by the server contains a shell, and scripts written in JavaScript fetch the text and the hours, then assemble them in the browser. For a patient, everything shows up in a second. For the crawler, the page stays empty: no treatment, no city, no name. The crawlers of OpenAI, Anthropic and Perplexity do not read JavaScript. A website that displays its content through scripts is invisible to them.

The test takes two minutes. In your browser settings, search for "JavaScript" and turn it off, then reload your website. What you see then is what the crawler sees. A blank page, or a heading alone without the treatments, confirms the problem. Another way to do it: right-click on the page, choose "View page source", then search for a sentence from your homepage with the browser's find function. If it is missing, it arrives through a script.

The fix does not require rebuilding the website. The text needs to leave the server already written into the page: this is called "server-side rendering", and modern tools can do it. Ask the person who manages your website: "Is the text of my pages present in the source code, without the scripts?". It is one of the basics of a [dental practice website](https://en.developpia.fr/dental-practice-website/) that machines can read.

## Second wall: a gatekeeper blocks the crawler at the door

Before it can even read the page, the crawler has to pass two checks.

The first is Cloudflare, a protection service used by many hosting providers to filter unwanted traffic. Since July 2025, Cloudflare has blocked AI crawlers by default, often without you knowing. The crawler requests the page and finds the door shut.

The second is the robots.txt file, a small text file at the root of your website that tells each crawler what it is allowed to read. A "Disallow: /" line, which means "forbidden: everything", placed under a crawler's name shuts the whole website to it. Some agencies add GPTBot there to keep the text from being used for training, and lump OAI-SearchBot in with it. The result: ChatGPT can no longer cite you.

To check:

- Type your website address followed by /robots.txt in the browser's address bar. Look for the names OAI-SearchBot, ClaudeBot, PerplexityBot, or the asterisk "*" that stands for all crawlers. The line right below decides: "Disallow: /" blocks, "Allow: /", which means "allowed", lets them through.
- If your website goes through Cloudflare, open its dashboard, in the section for AI crawlers called "AI Crawl Control". There you can see which crawlers are blocked and which are allowed, one by one.
- Without that access, ask your hosting provider: "Are the OAI-SearchBot, ClaudeBot and PerplexityBot crawlers allowed to read my website?".

The fix is a choice, not a technical feat: allow the AI search crawlers. You can keep GPTBot blocked if you do not want your text used for training. The two settings are independent.

## Third wall: the crawler reads, but does not understand who you are

The crawler got in and has text. That text still has to answer the patient's question. "A modern practice, a caring team": none of these words names a treatment, a city or a name. The AI does not guess. It looks in the text for the word "implant", the word "Nantes", the exact name of the practice.

Then it cross-checks with your Google Business Profile and Doctolib. Take a fictional practice: "Cabinet du Parc" on the website, "Docteur Martin" on Google, "SELARL du Parc" on Doctolib, a treatment listed here and missing there. The AI is no longer sure it is talking about the same practice. It prefers another dentist whose information is clean.

The test: read the first lines of your homepage as a stranger would. Do you find the practice name, the city and a treatment? Then open your [Google Business Profile](https://en.developpia.fr/google-business-profile-dentist/) and your Doctolib page side by side. Compare the name, the address, the phone number and the treatments, line by line.

The fix: an identical name everywhere, down to the character. One page per treatment, with the city in the title and in the first lines, the steps and the fees. Schema markup (structured data), an invisible record that describes the practice to machines, helps the AI understand the page. It does not raise your ranking, it prevents a misreading.

> **The takeaway**
> An AI cites what it has been able to read, understand and cross-check. Text that arrives through scripts, a gatekeeper that blocks the crawler, a page that names neither the treatment nor the city, a single source: any one of these four walls is enough to make a practice invisible.

## Fourth wall: nobody else talks about you

The last check: the AI looks for traces of your practice beyond your own website. A website alone, however well made, only has its own word. The Dental Council directory, your Google Business Profile, Doctolib, reputable health directories: every outside page that repeats the same name, the same address and the same treatments builds trust.

The test: type the exact name of your practice in quotation marks into Google, followed by your city. Count the pages that are neither your website nor your Google Business Profile. If you find none, or if they give an old address, the AI sees the same thing you do.

The fix: check that each directory exists and says the same thing as your website, without churning out new listings. One up-to-date directory is worth more than ten contradictory listings.

## What changes nothing, and what has changed

Two ideas get repeated a lot. The first: an llms.txt file, a plain-text introduction page meant for AI, would be enough to get read. That file has no proven effect on rankings. It does no harm, and it replaces nothing. The second: schema markup would push a website up. It helps machines understand the page, nothing more.

On the other hand, one thing really has changed. Since [July 22, 2026](https://blog.google/intl/fr-fr/nouveautes-produits/explorez-obtenez-des-reponses/recherche-ia-apercus-mode/), Google has shown AI Overviews and AI Mode in France: a written answer placed above the list of websites. Google states on its [page about AI features](https://developers.google.com/search/docs/appearance/ai-features) that no separate setting is required. The same walls apply: a page Google cannot read appears neither in the regular results nor in the AI Overview.

The four walls can be checked in one evening. Taking them down is the job of [AI search for dentists](https://en.developpia.fr/ai-search-dentist/), which starts with the same work as regular SEO: a readable website, identical information everywhere, pages that answer questions. That work is one of the five levers described in our article on [what the code allows in dental marketing](https://en.developpia.fr/blog/dental-marketing-what-the-code-allows/). Once the walls are down, the next question is which page to write for each treatment.

## Frequently asked questions

### Does blocking GPTBot make my practice disappear from ChatGPT?

No. GPTBot collects text to train the models, OAI-SearchBot looks for pages to cite in answers. You can shut out the first and let the second through. Check that your robots.txt file and Cloudflare do make the distinction between the two.

### My website looks fine on my phone, so AI can read it, right?

Not necessarily. Your phone runs the scripts that build the page; the crawler does not. The only reliable test is to view the source code, or the page without scripts, and look for your text there.

### Does the practice website need an llms.txt file?

It does no harm, and it has no proven effect on rankings. The time spent writing it is better spent opening the website to crawlers and aligning your information everywhere. If your agency offers it on top of everything else, let them.
