from crewai_tools import (TXTSearchTool,
                          ArxivPaperTool,
                          TavilyExtractorTool,
                          SerperDevTool,
                          FileReadTool,
                          FileWriterTool)
# from langchain.embeddings import SentenceTransformerEmbeddings
# from dotenv import load_dotenv

# import os

## userhistory, search engine, research paper, report pdf

user_medical_search_tool = TXTSearchTool(txt = '../docs/profile.txt'
    #                                      config=dict(
    #                                             llm=dict(
    #                                                 provider="ollama", # or google, openai, anthropic, llama2, ...
    #                                                 config=dict(
    #                                                     model="llama2",
    #                                                     # temperature=0.5,
    #                                                     # top_p=1,
    #                                                     # stream=true,
    #                                                 ),
    #                                             ),
    #                                             embedder=dict(
    #                                                 provider="ollama", # or openai, ollama, ...
    #                                                 config=dict(
    #                                                     model="llama2",
    #                                                     # task_type="retrieval_document",
    #                                                     # title="Embeddings",
    #                                                 ),
    #                                             ),
    # )
                                         )

# add_user_data_tool_perfortnight = PDFTextWritingTool()

research_paper_reader_tool = ArxivPaperTool(
    download_pdfs=False,
    # save_dir="../arxiv_pdfs",
    # max_results = 3
)

medical_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth = "basic",
    urls = ["https://www.medicalnewstoday.com/","https://www.medscape.com/", "https://www.webmd.com/", "https://medicalxpress.com/","https://www.who.int/news"]
)

general_search_tool = SerperDevTool(
    country = "Singapore",
    n_results = 5,
    save_file = True
)

report_format_reader_tool = FileReadTool(
    pdf = '../docs/ reportformat.txt',
    )


past_search_data_tool = TXTSearchTool(
    pdf = '../docs/records.txt'
)

warren_update_record_tool = FileWriterTool('../docs/dr_records.txt', '{summary}')
# print(general_search_tool.run(search_query = "Beautiful destinations near me"))