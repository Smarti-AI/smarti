# LangChain Framework

## Background
By now, we all know that ChatGPT has impressive general knowledge - you can ask it about anything, and you will get a pretty good answer. When you go deeper to a specific domain you quickly realize that answers are not as good as you would expect. What if we could connect LLM to proprietary data, like an organizational DB, a pdf document, a book, or any other data source containing domain-specific knowledge? LangChain allows referencing an external data source without copy-pasting it to the ChatGPT prompt. And not only that, ChatGPT allows you to take action once you get the information that you need as sending an email, updating a database, running scripts, etc.

At its core, LangChain is a framework built around LLMs. We can use it for chatbots, Generative Question-Answering (GQA), summarization, and much more. The LangChain framework simplifies dramatically the creation of the application using LLMs. It has built-in support for integrations with systems including Amazon, Google, and Microsoft Azure cloud storage; API wrappers for news, movie information, and weather; Bash for summarization, syntax and semantics checking, and execution of shell scripts; multiple web scraping subsystems and templates; few-shot learning prompt generation support; finding and summarizing "todo" tasks in code; Google Drive documents, spreadsheets, and presentations summarization, extraction, and creation; Google Search and Microsoft Bing web search; OpenAI, Anthropic, and Hugging Face language models; iFixit repair guides and wikis search and summarization; MapReduce for question answering, and more.

## Design Principles 
To clarify how LangChain simplifies the development process, let's examine the key components of the framework and apply them to the development of a virtual assistant for students. The flow of the virtual assistant is simple - it asks the student what course assignment he wants to get help on and then looks for existing assignments in the DB and provides a step-by-step explanation of the solution. If the assignment doesn't exist in the internal DB, Virtual Assistant will use 








