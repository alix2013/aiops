from base import ask
import os

def chat():
    show_source=True
    while True:
        question = input("\nEnter a query: ")
        if question == "exit":
            break

        res = ask(question)
        answer, sourceDocs = res["result"], res["source_documents"]

        # Print the result
        qna = f""""Question: {question}
Answer: {answer}

        """
        print(qna)
        if show_source: 
            print("----------------------------------SOURCE DOCUMENTS---------------------------")
            for document in sourceDocs:
                # print("\n> " + document.metadata["source"] + ":")
                print("\n> " + os.path.basename(str(document.metadata["source"])) + ":")
                print(document.page_content)
            print("----------------------------------SOURCE DOCUMENTS---------------------------")

if __name__ == "__main__":
    chat()




