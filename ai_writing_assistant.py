import openai
import os
import json
import random
import textwrap

class AIWritingAssistant:
    def __init__(self, api_key, model='text-davinci-003'):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def generate_text(self, prompt, max_tokens=150):
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        text = response.choices[0].text.strip()
        return text

    def edit_text(self, text, instructions):
        prompt = f"Edit the following text based on these instructions: '{instructions}'\n\nText: {text}\n\nEdited Text:"
        return self.generate_text(prompt)

    def summary_text(self, text):
        prompt = f"Please summarize the following text:\n\n{text}\n\nSummary:"
        return self.generate_text(prompt)

    def get_random_prompt(self):
        prompts = [
            "What would happen if humans could communicate with animals?",
            "Describe a futuristic city where technology and nature coexist.",
            "Write a short story about a time traveler who visits ancient Rome.",
            "Outline the main themes in the book '1984' and their relevance today.",
            "Create conversation dialogue between two poets discussing their craft."
        ]
        return random.choice(prompts)

    def format_text(self, text, width=70):
        return textwrap.fill(text, width)

    def save_to_file(self, text, filename):
        with open(filename, 'w') as file:
            file.write(text)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def create_outline(self, topic):
        prompt = f"Create an outline for an article about {topic}."
        return self.generate_text(prompt)

    def suggest_improvements(self, text):
        prompt = f"Suggest improvements for the following text:\n\n{text}\n\nImprovements:"
        return self.generate_text(prompt)

    def run(self):
        print("Welcome to the AI Writing Assistant! What would you like to do today?")
        while True:
            print("\nOptions:")
            print("1. Generate Text")
            print("2. Edit Text")
            print("3. Summarize Text")
            print("4. Create Outline")
            print("5. Suggest Improvements")
            print("6. Get Random Prompt")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                user_prompt = input("Enter your prompt: ")
                print("\nGenerating text...")
                generated_text = self.generate_text(user_prompt)
                print("\nGenerated Text:\n", generated_text)

            elif choice == '2':
                user_text = input("Enter the text you want to edit: ")
                instructions = input("Enter your editing instructions: ")
                print("\nEditing text...")
                edited_text = self.edit_text(user_text, instructions)
                print("\nEdited Text:\n", edited_text)

            elif choice == '3':
                user_text = input("Enter the text to summarize: ")
                print("\nSummarizing text...")
                summary = self.summary_text(user_text)
                print("\nSummary:\n", summary)

            elif choice == '4':
                topic = input("Enter the topic for the outline: ")
                print("\nCreating outline...")
                outline = self.create_outline(topic)
                print("\nOutline:\n", outline)

            elif choice == '5':
                user_text = input("Enter the text you want improvements for: ")
                print("\nSuggesting improvements...")
                improvements = self.suggest_improvements(user_text)
                print("\nSuggestions:\n", improvements)

            elif choice == '6':
                print("\nRandom Prompt:\n", self.get_random_prompt())

            elif choice == '7':
                print("Exiting the AI Writing Assistant. Goodbye!")
                break

            else:
                print("Invalid choice. Please select an option between 1 and 7.")

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have set your OpenAI API key in your environment variables
    assistant = AIWritingAssistant(api_key)
    assistant.run()