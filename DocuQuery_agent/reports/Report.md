
Running:
 - search_knowledge_base(query=memory and retrievers in agentic system)

In the context of an agentic system, memory and retrievers play a crucial role in shaping the behavior of generative agents. Here's a detailed overview of how these components function:

### Memory in Agentic Systems
The memory of a generative agent is structured as a **memory stream**. This stream maintains a comprehensive, organized record of all of the agent’s experiences in natural language, and its architecture is composed of several essential features:

- **Memory Objects**: Each piece of memory has a text description, a creation timestamp, and a most recent access timestamp.
- **Observations**: Observations are the fundamental units in the memory stream, representing events either performed by the agent or noticed by them.
- **Embedded Memories**: Generative agents use embedded text descriptions as memory objects, which help compare and relate different memories using metrics like cosine similarity.

### Retrieval Mechanism
Given the constraints of context windows in language models, it is impractical to recall the entire memory stream simultaneously. Instead, relevant parts of the memory are retrieved and fed into the language model to condition the agent's responses and actions. The retrieval system functions using key considerations:

- **Recency**: Recent events are considered more relevant. Recency is calculated using an exponential decay function, simulating how distant events fade away.
- **Importance**: Memories deemed significant, either due to their emotional weight or impact on the agent's goals, are scored higher.
- **Relevance**: Based on the current situation, memories that are pertinent receive higher scores, calculated as the similarity between the current context and past experiences.

### Scoring and Selection
All memory objects are scored based on the recency, importance, and relevance. A weighted combination of these scores determines which memories are retrieved at any given time, utilizing min-max scaling for normalization.

### Reflection
Reflection synthesizes individual memories into broader inferences about oneself and others, allowing agents to form and adjust high-level beliefs and guidance for future behavior. This process leads to abstracting patterns from specific instances, which can be crucial for advanced decision-making or planning.

### Planning
The planning component of the system involves utilizing reflections and current environmental inputs to devise action plans. These are broken down into recursive, moment-to-moment behaviors and staged into future planning tasks, adding context and depth to the decision-making process.

### Challenges
One of the key challenges is ensuring the system hasn't retrieved irrelevant or incomplete memories, which could lead to incorrect behavior or suboptimal interactions. Another challenge is balancing between maintaining coherence with long-term objectives and reacting to the immediate environment.

### Conclusion
Together, memory storage, retrieval mechanisms, reflection, and planning allow generative agents to simulate human-like behavior effectively. They help these agents showcase emergent and interactive social dynamics in computationally rich environments.