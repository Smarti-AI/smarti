# LangChain Framework Overview

## Background
[ChatGPT](https://en.wikipedia.org/wiki/ChatGPT) has impressive general knowledge, it can provide decent answers to various questions. However, when it comes to specific domains, its performance may fall short. But imagine if we could connect LLM to specific data sources, such as organizational databases, PDF documents, books, or other repositories of domain-specific knowledge. This connection would allow LLM to tap into that proprietary information and provide more accurate responses within that particular domain.

[LangChain](https://en.wikipedia.org/wiki/LangChain) is a framework that revolves around LLMs (Language Models) and makes it easy to reference external data sources without copy-pasting them into the LLM's prompt. But it doesn't stop there. LangChain also enables you to take action based on the obtained information, like sending emails, updating databases, or running scripts. Essentially, LangChain streamlines the integration between LLMs and external systems, allowing for dynamic and automated workflows beyond simple data referencing.

We can use LangChain Framework to build chatbots, Generative Question-Answering (GQA), summarization, and much more. LangChain has built-in support for integrations with systems including Amazon, Google, and Microsoft Azure cloud storage; API wrappers for news, movie information, and weather; Bash for summarization, syntax and semantics checking, and execution of shell scripts; multiple web scraping subsystems and templates; few-shot learning prompt generation support; finding and summarizing "todo" tasks in code; Google Drive documents, spreadsheets, and presentations summarization, extraction, and creation; Google Search and Microsoft Bing web search; OpenAI, Anthropic, and Hugging Face language models; iFixit repair guides and wikis search and summarization; MapReduce for question answering, and more.

## Virtual Assistants 
To clarify how LangChain simplifies the development process, let's examine the key components of the framework and apply them to the development of a virtual assistant for students called Smarti. Smarti provides students with a step-by-step explanation of how to solve problems from the student workbook. Essentially, Smarti has two flows: ingest flow, and chat flow. Ingest flow is fairly simple, a student scans and uploads workbooks. Smarti performs the OCR job that translates images to text, parses question and sends each question to ChatGPT. ChatGPT solves the problem and sends the solution back to Smarti. Smarti combines questions and solution to the text file and builds a local [Semantic Index](https://en.wikipedia.org/wiki/Latent_semantic_analysis). Doing so, each new problem solved only once by the ChatGPT. The chat flow begins when the student's input is read and sent to Smarti for problem-solving. On the first attempt Smarti tries to use PrivateGPT that uses a local Semantic Index. If the problem found in the local semantic index, the step-by-step solution is served immediately. If the problem is not solved, Smarti uses ChatGPT to solve the problem and updates the local Semantic Index and then serves the student's request.
<table width="256px">
  <tr>
    <td><img src="./images/sequence-1.png"/></td>
  </tr>
  <tr>
    <td align="center">Smarti's Chat Flow</td>
  </tr>
</table> 


## Design Principles
[TBD]()








