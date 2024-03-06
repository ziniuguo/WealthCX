import query_summary
import sentence_analysis
def class_news_analysis(text):
    target_company_RIC = sentence_analysis.analyze_text(text)
    json_result = query_summary.query_combined_table(target_company_RIC)
    prompt = "Please analysis the following news " + json_result
    response = "function"
    return response
