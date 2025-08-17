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
report_format_reader_tool = FileReadTool(pdf='../docs/reportformat.txt')

#warren Past search data tool
warren_past_search_data_tool = TXTSearchTool(pdf='../docs/dr_records.txt')

# Warren update record tool
warren_update_record_tool = FileWriterTool('../docs/dr_records.txt', '{summary}')

#advic search data tool
advic_search_data_tool = TXTSearchTool(pdf='../docs/advic_records.txt')

# Advic data update tool
advic_data_update_tool = FileWriterTool('/docs/advic_records.txt', '{data}')

# Carla past search data tool
carla_past_search_data_tool = TXTSearchTool(pdf='../docs/carla_records.txt')

# carla_update_record_tool 
carla_update_record_tool = FileWriterTool('../docs/carla_records.txt', '{mealpan}')

#nutrition_web_data_extractor_tool
nutrition_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth="basic",
    urls=[
        "https://www.nutrition.gov/",
        "https://www.myfooddata.com/",
        "https://www.nutritionix.com/"
    ]
)

# rachel_past_search_data_tool
rachel_past_search_data_tool = TXTSearchTool(pdf='../docs/rachel_records.txt')

#moverment_web_data_extractor_tool
movement_web_data_extractor_tool = TavilyExtractorTool(
    extract_depth="basic",
    urls=[
        "https://www.apta.org/",
        "https://www.webmd.com/a-to-z-guides/what-is-a-physiotherapist",
        "https://www.nhs.uk/tests-and-treatments/physiotherapy/"
    ]
)

# rachel_update_record_tool 
rachel_update_record_tool = FileWriterTool('../docs/rachel_records.txt', '{exercisepan}')

# ruby progress data search
ruby_progress_data_tool = TXTSearchTool(pdf='../docs/ruby_records.txt')

# ruby update record tool
ruby_update_record_tool = FileWriterTool('../docs/ruby_records.txt', '{quality_assurance_log},{crisis_response_log},{onboarding_data},{weekly_progress_summary},{weekly_progress_report_YYYY_MM_DD}')