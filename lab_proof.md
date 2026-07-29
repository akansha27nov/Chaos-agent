# Lab Proof: Chaos Agent

## 1. Code / Workflow
Implemented a modern `create_agent` (LangChain v1.0) with four creative tools. The system takes a complaint, routes it to the appropriate Hawkins or Upside Down tool, retrieves hardcoded context, and synthesizes a chaotic final response.

## 2. Execution Trace
**INPUT (Query):** 
*The electricity in my house is flickering and my compass is pointing the wrong way!*

**DECIDE (Tool Path):** 
*consult_demogorgon | Args: {'complaint': 'flickering electricity and compass malfunction'}*

**VERIFY (Tool Evidence):** 
*Gurgle... *screech*! Translation: The Demogorgon finds 'flickering electricity and compass malfunction' hilarious and wants to turn it into slime.
Record #412: Unexplained magnetic and electrical fluctuations reported town-wide.*

**BUILD (Final Output):** 
*Ah, it seems we have a delightful conundrum on our hands! The Demogorgon, our resident expert on the Upside Down, finds your flickering electricity and misbehaving compass to be quite the joke—so much so that it wants to transform them into gooey slime! How charming.

But not to worry, as I dug through the Hawkins municipal records and unearthed some juicy tidbits! Record #412 reveals that there have been town-wide reports of unexplained magnetic and electrical fluctuations. Sounds like the Upside Down may be leaking into our reality, causing your electrical chaos and compass confusion.

Here's the grand plan: I suggest you light a scented candle, perhaps something floral, and channel the energy of the Demogorgon’s laughter. Then, cast an interdimensional spell to stabilize your electrical system, while simultaneously enchanting your compass to point towards the nearest snack bar—because who wouldn't want a snack during a supernatural crisis?

Would you like me to cast that enchanting spell for you? Just say the word!*

## 3. Explain: Grounding Risk / Failure Mode
**Failure Mode:** *"Creative Hallucination Overriding Evidence." Because the system prompt instructs the agent to be "highly creative" and "slightly unhinged," there is a high risk that the LLM will embellish the final output with entities or facts that were *not* present in the tool's returned evidence (e.g., adding scented candles and snack bars). This breaks strict grounding.*

---

## 4. AI Reviewer Output (Prompt Discipline)

**Three Grounding Risks:**
1. *System prompt encourages "unhinged" responses, which actively degrades factual adherence to the tool payload.*
2. *The agent chose to invoke `consult_demogorgon` based on user input rather than utilizing an archive record first, leading to a fictional translation instead of an initial factual anchor.*
3. The LLM combined parametric memory of the *Stranger Things* universe with the tool context rather than relying *only* on the retrieved tool text.

**Two Trace Checks:**
1. Did the tool call arguments directly map to the user's explicit keywords?
2. Is every factual claim in the final output directly traceable back to the raw string returned in `VERIFY (Tool Evidence)`?

**One Simplification:**
Remove the "highly creative" instruction from the system prompt if strict grounding verification is the primary goal; separate the "retrieval" step from the "creative writing" step into two distinct nodes.

**Verification:**
The final response is tied to the source via the specific detail of `Record #412: Unexplained magnetic and electrical fluctuations reported town-wide`, which originated directly from the tool's hardcoded dictionary.