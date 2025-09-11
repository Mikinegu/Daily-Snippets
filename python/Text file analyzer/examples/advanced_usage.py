#!/usr/bin/env python3
"""
Advanced Usage Examples for Text Analyzer
This file demonstrates advanced features and customizations.
"""

from text_analyzer import TextAnalyzer
import json
import os

class CustomTextAnalyzer(TextAnalyzer):
    """Extended TextAnalyzer with custom features"""
    
    def __init__(self):
        super().__init__()
        self.custom_stop_words = set()
    
    def add_custom_stop_words(self, words):
        """Add custom stop words to filter out"""
        self.custom_stop_words.update(words)
    
    def word_frequency(self, top_n=20):
        """Override word frequency with custom stop words"""
        # Get default stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Add custom stop words
        stop_words.update(self.custom_stop_words)
        
        words = re.findall(r'\b\w+\b', self.text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        word_counts = Counter(words)
        return dict(word_counts.most_common(top_n))
    
    def compare_texts(self, other_analyzer):
        """Compare this text with another analyzed text"""
        if not self.analysis_results or not other_analyzer.analysis_results:
            return {"error": "Both texts must be analyzed first"}
        
        comparison = {
            "text1": self.filename,
            "text2": other_analyzer.filename,
            "word_count_diff": self.analysis_results['basic_stats']['total_words'] - 
                             other_analyzer.analysis_results['basic_stats']['total_words'],
            "readability_diff": self.analysis_results['readability_scores']['flesch_reading_ease'] - 
                              other_analyzer.analysis_results['readability_scores']['flesch_reading_ease'],
            "reading_time_diff": (self.analysis_results['reading_time']['estimated_reading_time_minutes'] - 
                                other_analyzer.analysis_results['reading_time']['estimated_reading_time_minutes'])
        }
        
        return comparison

def advanced_example_1_custom_stop_words():
    """Example 1: Using custom stop words"""
    print("Advanced Example 1: Custom Stop Words")
    print("=" * 45)
    
    analyzer = CustomTextAnalyzer()
    
    # Add domain-specific stop words
    analyzer.add_custom_stop_words(['text', 'analysis', 'analyzer', 'file'])
    
    if analyzer.load_file("sample_texts/sample1.txt"):
        analyzer.analyze()
        
        print("Most common words (with custom stop words):")
        common_words = analyzer.analysis_results['most_common_words']
        for word, count in list(common_words.items())[:10]:
            print(f"  {word}: {count}")

def advanced_example_2_text_comparison():
    """Example 2: Comparing two texts"""
    print("\nAdvanced Example 2: Text Comparison")
    print("=" * 40)
    
    analyzer1 = CustomTextAnalyzer()
    analyzer2 = CustomTextAnalyzer()
    
    # Analyze two different texts
    analyzer1.load_file("sample_texts/sample1.txt")
    analyzer1.analyze()
    
    analyzer2.load_file("sample_texts/sample2.txt")
    analyzer2.analyze()
    
    # Compare the texts
    comparison = analyzer1.compare_texts(analyzer2)
    
    print(f"Comparing '{comparison['text1']}' vs '{comparison['text2']}':")
    print(f"Word count difference: {comparison['word_count_diff']:+d} words")
    print(f"Readability difference: {comparison['readability_diff']:+.1f} points")
    print(f"Reading time difference: {comparison['reading_time_diff']:+.1f} minutes")

def advanced_example_3_batch_processing():
    """Example 3: Batch processing with detailed reports"""
    print("\nAdvanced Example 3: Batch Processing")
    print("=" * 40)
    
    analyzer = CustomTextAnalyzer()
    sample_files = [
        "sample_texts/sample1.txt",
        "sample_texts/sample2.txt",
        "sample_texts/sample3.txt"
    ]
    
    batch_results = []
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            print(f"Processing {file_path}...")
            analyzer.load_file(file_path)
            analyzer.analyze()
            
            # Extract key metrics
            stats = analyzer.analysis_results['basic_stats']
            readability = analyzer.analysis_results['readability_scores']
            reading_time = analyzer.analysis_results['reading_time']
            
            result = {
                'filename': analyzer.filename,
                'word_count': stats['total_words'],
                'sentence_count': stats['total_sentences'],
                'readability_score': readability['flesch_reading_ease'],
                'grade_level': readability['flesch_kincaid_grade_level'],
                'reading_time_minutes': reading_time['estimated_reading_time_minutes']
            }
            
            batch_results.append(result)
    
    # Save batch results
    with open('batch_analysis_results.json', 'w') as f:
        json.dump(batch_results, f, indent=2)
    
    print(f"\nBatch analysis complete! Results saved to 'batch_analysis_results.json'")
    
    # Display summary
    print("\nSummary:")
    for result in batch_results:
        print(f"  {result['filename']}: {result['word_count']} words, "
              f"Grade {result['grade_level']:.1f}, "
              f"{result['reading_time_minutes']:.1f} min read")

def advanced_example_4_text_insights():
    """Example 4: Deep text insights"""
    print("\nAdvanced Example 4: Deep Text Insights")
    print("=" * 40)
    
    analyzer = TextAnalyzer()
    
    if analyzer.load_file("sample_texts/sample1.txt"):
        analyzer.analyze()
        results = analyzer.analysis_results
        
        print("Deep Analysis Insights:")
        print("-" * 25)
        
        # Word diversity analysis
        basic_stats = results['basic_stats']
        word_diversity = basic_stats['unique_words'] / basic_stats['total_words']
        print(f"Word diversity ratio: {word_diversity:.3f} (higher = more diverse vocabulary)")
        
        # Sentence complexity
        readability = results['readability_scores']
        print(f"Sentence complexity: {readability['average_sentence_length']:.1f} words per sentence")
        
        # Most impactful words (longer words that appear frequently)
        common_words = results['most_common_words']
        impactful_words = [(word, count) for word, count in common_words.items() 
                          if len(word) > 6 and count > 2]
        
        if impactful_words:
            print("Most impactful words (long + frequent):")
            for word, count in impactful_words[:5]:
                print(f"  {word} ({len(word)} chars, {count} times)")

def advanced_example_5_export_formats():
    """Example 5: Export in different formats"""
    print("\nAdvanced Example 5: Export Formats")
    print("=" * 35)
    
    analyzer = TextAnalyzer()
    
    if analyzer.load_file("sample_texts/sample1.txt"):
        analyzer.analyze()
        
        # Export to JSON (already available)
        analyzer.save_analysis("detailed_analysis.json")
        
        # Create a simple text report
        results = analyzer.analysis_results
        basic_stats = results['basic_stats']
        readability = results['readability_scores']
        
        report = f"""
TEXT ANALYSIS REPORT
===================
File: {results['filename']}
Date: {results['analysis_timestamp']}

SUMMARY:
- {basic_stats['total_words']} words
- {basic_stats['total_sentences']} sentences  
- {basic_stats['total_characters']} characters
- Reading time: {results['reading_time']['estimated_reading_time_minutes']:.1f} minutes
- Readability: {readability['flesch_reading_ease']:.1f} ({readability['flesch_reading_level']})
- Grade level: {readability['flesch_kincaid_grade_level']:.1f}

TOP WORDS:
"""
        
        for word, count in list(results['most_common_words'].items())[:10]:
            report += f"- {word}: {count}\n"
        
        with open("text_report.txt", "w") as f:
            f.write(report)
        
        print("Reports exported:")
        print("  - detailed_analysis.json (full data)")
        print("  - text_report.txt (summary report)")

if __name__ == "__main__":
    print("Text Analyzer - Advanced Usage Examples")
    print("=" * 50)
    
    # Run advanced examples
    advanced_example_1_custom_stop_words()
    advanced_example_2_text_comparison()
    advanced_example_3_batch_processing()
    advanced_example_4_text_insights()
    advanced_example_5_export_formats()
    
    print("\n" + "=" * 50)
    print("All advanced examples completed!")
