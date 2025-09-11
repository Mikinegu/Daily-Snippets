#!/usr/bin/env python3
"""
Basic Usage Examples for Text Analyzer
This file demonstrates simple ways to use the TextAnalyzer class.
"""

from text_analyzer import TextAnalyzer

def example_1_analyze_file():
    """Example 1: Analyze a text file"""
    print("Example 1: Analyzing a text file")
    print("=" * 40)
    
    analyzer = TextAnalyzer()
    
    # Load and analyze a sample file
    if analyzer.load_file("sample_texts/sample1.txt"):
        analyzer.analyze()
        analyzer.print_analysis()
    else:
        print("Could not load the file")

def example_2_analyze_text():
    """Example 2: Analyze text directly"""
    print("\nExample 2: Analyzing text directly")
    print("=" * 40)
    
    analyzer = TextAnalyzer()
    
    sample_text = """
    This is a sample text for analysis. It contains several sentences 
    with different lengths and complexity levels. The text analyzer will 
    provide detailed statistics about this content.
    """
    
    analyzer.load_text(sample_text)
    analyzer.analyze()
    analyzer.print_analysis()

def example_3_save_results():
    """Example 3: Save analysis results"""
    print("\nExample 3: Saving analysis results")
    print("=" * 40)
    
    analyzer = TextAnalyzer()
    
    if analyzer.load_file("sample_texts/sample2.txt"):
        analyzer.analyze()
        analyzer.print_analysis()
        
        # Save results to JSON file
        analyzer.save_analysis("sample2_analysis.json")
        print("Analysis saved successfully!")

def example_4_get_specific_stats():
    """Example 4: Get specific statistics"""
    print("\nExample 4: Getting specific statistics")
    print("=" * 40)
    
    analyzer = TextAnalyzer()
    
    if analyzer.load_file("sample_texts/sample3.txt"):
        analyzer.analyze()
        results = analyzer.analysis_results
        
        # Access specific statistics
        basic_stats = results['basic_stats']
        readability = results['readability_scores']
        
        print(f"Word count: {basic_stats['total_words']}")
        print(f"Reading time: {results['reading_time']['estimated_reading_time_minutes']} minutes")
        print(f"Readability score: {readability['flesch_reading_ease']}")
        print(f"Grade level: {readability['flesch_kincaid_grade_level']}")

def example_5_batch_analysis():
    """Example 5: Analyze multiple files"""
    print("\nExample 5: Batch analysis of multiple files")
    print("=" * 40)
    
    import os
    
    analyzer = TextAnalyzer()
    sample_files = [
        "sample_texts/sample1.txt",
        "sample_texts/sample2.txt", 
        "sample_texts/sample3.txt"
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            print(f"\nAnalyzing {file_path}...")
            analyzer.load_file(file_path)
            analyzer.analyze()
            
            # Just show basic stats for batch processing
            stats = analyzer.analysis_results['basic_stats']
            print(f"Words: {stats['total_words']}, "
                  f"Sentences: {stats['total_sentences']}, "
                  f"Reading time: {analyzer.analysis_results['reading_time']['estimated_reading_time_minutes']:.1f} min")

if __name__ == "__main__":
    print("Text Analyzer - Basic Usage Examples")
    print("=" * 50)
    
    # Run all examples
    example_1_analyze_file()
    example_2_analyze_text()
    example_3_save_results()
    example_4_get_specific_stats()
    example_5_batch_analysis()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
