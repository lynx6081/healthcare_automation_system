from crewai_tools import (
    TXTSearchTool,
    ArxivPaperTool,
    TavilyExtractorTool,
    SerperDevTool,
    FileReadTool,
    FileWriterTool
)

# User medical profile search tool
user_medical_search_tool = TXTSearchTool(txt='../docs/profile.txt')


# Research paper reader tool
research_paper_reader_tool = ArxivPaperTool(download_pdfs=False)

# Medical web data extractor tool
medical_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth="basic",
    urls=[
        "https://www.medicalnewstoday.com/",
        "https://www.medscape.com/",
        "https://www.webmd.com/",
        "https://medicalxpress.com/",
        "https://www.who.int/news"
    ]
)

# General search tool
general_search_tool = SerperDevTool(
    country="Singapore",
    n_results=5,
    save_file=True
)

# Report format reader tool
report_format_reader_tool = FileReadTool(file_path='../docs/reportformat.txt')

# Warren Past search data tool
warren_past_search_data_tool = TXTSearchTool(txt='../docs/dr_records.txt')

# Warren update record tool - FIX: FileWriterTool takes no parameters in constructor
warren_update_record_tool = FileWriterTool()

# Advic search data tool
advic_search_data_tool = TXTSearchTool(txt='../docs/advic_records.txt')

# Advic data update tool - FIX: FileWriterTool takes no parameters in constructor
advic_data_update_tool = FileWriterTool()

# Carla past search data tool
carla_past_search_data_tool = TXTSearchTool(txt='../docs/carla_records.txt')

# Carla update record tool - FIX: FileWriterTool takes no parameters in constructor
carla_update_record_tool = FileWriterTool()

# Nutrition web data extractor tool
nutrition_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth="basic",
    urls=[
        "https://www.nutrition.gov/",
        "https://www.myfooddata.com/",
        "https://www.nutritionix.com/"
    ]
)

# Rachel past search data tool
rachel_past_search_data_tool = TXTSearchTool(txt='../docs/rachel_records.txt')

# Movement web data extractor tool
movement_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth="basic",
    urls=[
        "https://www.apta.org/",
        "https://www.webmd.com/a-to-z-guides/what-is-a-physiotherapist",
        "https://www.nhs.uk/tests-and-treatments/physiotherapy/"
    ]
)

# Rachel update record tool - FIX: FileWriterTool takes no parameters in constructor
rachel_update_record_tool = FileWriterTool()

# Ruby progress data search
ruby_progress_data_tool = TXTSearchTool(txt='../docs/ruby_records.txt')

# Ruby update record tool - FIX: FileWriterTool takes no parameters in constructor
ruby_update_record_tool = FileWriterTool()
