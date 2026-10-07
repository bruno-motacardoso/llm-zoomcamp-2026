INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()

class RAGBase:
    def __init__(
            self,
            index,
            llm_client,
            instructions=INSTRUCTIONS,
            prompt_template=PROMPT_TEMPLATE,
            course="llm-zoomcamp",
            model="google/gemma-4-31B-it"
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.course = course
        self.model = model

    def search(self, query, num_results=5):
        filter_dict = {"course": self.course}
        boost_dict = {"question": 3.0, "section": 0.5}

        return self.index.search(
            query,
            filter_dict=filter_dict,
            boost_dict=boost_dict,
            num_results=num_results
        )

    def build_context(self, search_results):
        lines = []
        for doc in search_results:
            lines.append(f"{doc['section']}")
            lines.append(f"Q: {doc['question']}")
            lines.append(f"A: {doc['answer']}")
            lines.append("")  # Add an empty line for better readability

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query,
            context=context
        )

    def llm(self, prompt):
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "developer", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        return self.llm(prompt)