from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

user_profile_knowledge = TextFileKnowledgeSource(
    file_paths=["../docs/profile.txt"]
)

