import param
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.document_loaders import PyPDFLoader, CSVLoader


class DatabaseLoader:
    """
    The class loads documents from PDF and CSV files, create a document retriever, and generate a conversational 
    question-answering (QA) chain.

    Attributes:
        pdf_file (str, optional): The file path to the PDF file to be loaded. Defaults to None.
        csv_file (str, optional): The file path to the CSV file to be loaded. Defaults to None.
        chain_type (str): The type of chain used for question-answering. Defaults to "stuff".
        k (int): The number of documents to retrieve during similarity search. Defaults to 4.
        documents (list): A list of loaded documents from the PDF and CSV files.
        retriever (object): A retriever object that performs similarity search using vector embeddings.
        qa (object): The question-answering chain object. Initialized via `initialize_qa()`.

    Methods:
        load_documents():
            Loads documents from the specified PDF and CSV files.
            Returns a list of documents containing the text content from the loaded files.

        process_documents():
            Extracts text content from the loaded documents and splits them into smaller chunks.
            Returns a list of chunked text documents for processing.

        create_retriever():
            Creates a retriever object using document embeddings for similarity search.
            Returns a retriever configured for similarity-based searches with the specified number of results (k).

        create_qa_chain():
            Creates a conversational retrieval-based QA chain using an LLM from Hugging Face.
            Returns a conversational retrieval chain with an integrated language model and document retriever.

        initialize_qa():
            Initializes the question-answering (QA) chain by calling the `create_qa_chain()` method.
        
        get_qa():
            Retrieves the initialized QA chain object for external use.
    """

    def __init__(self, pdf_file=None, csv_file=None, chain_type="stuff", k=4):
        self.pdf_file = pdf_file
        self.csv_file = csv_file
        self.chain_type = chain_type
        self.k = k
        self.documents = self.load_documents()
        self.retriever = self.create_retriever()
        self.qa = None

    def load_documents(self):
        # Load PDF and CSV files
        documents = []
        if self.pdf_file:
            pdf_loader = PyPDFLoader(self.pdf_file, extract_images=False)
            documents.extend(pdf_loader.load())
        if self.csv_file:
            csv_loader = CSVLoader(file_path=self.csv_file)
            documents.extend(csv_loader.load())
        return documents

    def process_documents(self):
        # Extract text content and split into chunks
        texts = [doc.page_content for doc in self.documents]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        return text_splitter.create_documents(texts)

    def create_retriever(self):
        # Define embeddings and create a vector database retriever
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        docs = self.process_documents()
        db = DocArrayInMemorySearch.from_documents(docs, embeddings)
        return db.as_retriever(search_type="similarity", search_kwargs={"k": self.k})

    def create_qa_chain(self):
        # Create the LLM and the conversational retrieval chain
        llm = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            task="text-generation",
            max_new_tokens=512,
            do_sample=False,
            repetition_penalty=1.03,
        )
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatHuggingFace(llm=llm),
            chain_type=self.chain_type,
            retriever=self.retriever,
            return_source_documents=True,
            return_generated_question=True,
        )
        return qa_chain

    def initialize_qa(self):
        # Initialize the QA chain by creating it
        self.qa = self.create_qa_chain()

    def get_qa(self):
        # Return the QA chain object
        return self.qa


class cbfs(param.Parameterized):
    """
    The class handles conversational-based question-answering (QA) with database lookups 
    using the pre-loaded PDF and CSV file. It interacts with a QA system and tracks chat history.

    Attributes:
        chat_history (list): A list to store the conversation history as tuples of (query, answer).
        answer (str): The last answer provided by the QA system.
        db_query (str): The generated query for the database lookup based on the question asked.
        db_response (list): A list to store the documents retrieved from the database as source information.

    Methods:
        __init__(**params):
            Initializes the `cbfs` class with default values for PDF and CSV files and automatically loads the database.

        initialize_db():
            Initializes the data loader by loading the PDF and CSV files and setting up the QA system.

        ask_question(query):
            Takes a query as input, calls the QA system, retrieves the response, and updates the chat history. 
            Returns a dictionary containing the QA system's response and database lookup information.

        clear_history():
            Clears the conversation history and resets the related attributes (answer, db_query, db_response).
    """

    chat_history = param.List([])
    answer = param.String("")
    db_query = param.String("")
    db_response = param.List([])

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        self.data_loader = None
        self.qa = None
        self.loaded_file_pdf = "GEM_Report.pdf"  # Default PDF file
        self.loaded_file_csv = "world_data.csv"  # Default CSV file

        # Automatically load and initialize the load_db class
        self.initialize_db()

    def initialize_db(self):
        # Initialize the DatabaseLoader class and create the QA system
        self.data_loader = DatabaseLoader(pdf_file=self.loaded_file_pdf, csv_file=self.loaded_file_csv)
        self.data_loader.initialize_qa()
        self.qa = self.data_loader.get_qa()

    def ask_question(self, query):
        if not query:
            return "No query provided."
        
        # Call the QA system and retrieve results
        result = self.qa({"question": query, "chat_history": self.chat_history})
        
        # Update chat history and results
        self.chat_history.append((query, result['answer']))
        self.db_query = result['generated_question']
        
        # Convert source documents to a serializable format
        self.db_response = [
            {"page_content": doc.page_content, "metadata": doc.metadata} 
            for doc in result['source_documents']
        ]
        
        self.answer = result['answer']

        # Return the LLM's response and database lookup info
        return {
            "response": self.answer,
            "db_lookup": self.db_response  # Now it's JSON serializable
        }

    def clear_history(self):
        self.chat_history = []
        self.answer = ""
        self.db_query = ""
        self.db_response = []
