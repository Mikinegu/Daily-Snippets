#!/usr/bin/env python3
"""
Text File Analyzer
A comprehensive tool for analyzing text files with various metrics including:
- Word count, character count, line count
- Reading time estimation
- Readability scores (Flesch Reading Ease, Flesch-Kincaid Grade Level)
- Most common words and phrases
- Text statistics and insights
"""

import os
import re
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
import math

class TextAnalyzer:
    def __init__(self):
        self.text = ""
        self.filename = ""
        self.analysis_results = {}
        
    def load_file(self, filepath):
        """Load text from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.text = file.read()
            self.filename = os.path.basename(filepath)
            return True
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            return False
        except UnicodeDecodeError:
            print(f"Error: Unable to decode file '{filepath}'. Please ensure it's a text file.")
            return False
    
    def load_text(self, text):
        """Load text directly from string"""
        self.text = text
        self.filename = "Direct Input"
        return True
    
    def basic_stats(self):
        """Calculate basic text statistics"""
        # Remove extra whitespace and split into words
        words = re.findall(r'\b\w+\b', self.text.lower())
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Character counts
        total_chars = len(self.text)
        chars_no_spaces = len(self.text.replace(' ', ''))
        chars_no_punctuation = len(re.sub(r'[^\w\s]', '', self.text))
        
        # Line counts
        lines = self.text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            'total_characters': total_chars,
            'characters_no_spaces': chars_no_spaces,
            'characters_no_punctuation': chars_no_punctuation,
            'total_words': len(words),
            'unique_words': len(set(words)),
            'total_sentences': len(sentences),
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'average_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'average_characters_per_word': chars_no_spaces / len(words) if words else 0
        }
    
    def reading_time(self):
        """Estimate reading time (average 200 words per minute)"""
        words = len(re.findall(r'\b\w+\b', self.text.lower()))
        minutes = words / 200
        return {
            'estimated_reading_time_minutes': round(minutes, 2),
            'estimated_reading_time_seconds': round(minutes * 60, 0)
        }
    
    def readability_scores(self):
        """Calculate readability scores"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {'error': 'Insufficient text for readability analysis'}
        
        # Count syllables (approximate)
        def count_syllables(word):
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in word:
                if char in vowels:
                    if not prev_was_vowel:
                        syllable_count += 1
                    prev_was_vowel = True
                else:
                    prev_was_vowel = False
            
            # Handle silent 'e'
            if word.endswith('e'):
                syllable_count -= 1
            
            return max(1, syllable_count)
        
        total_syllables = sum(count_syllables(word) for word in words)
        
        # Flesch Reading Ease Score
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Flesch-Kincaid Grade Level
        fk_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        
        # Reading level interpretation
        def interpret_flesch(score):
            if score >= 90:
                return "Very Easy"
            elif score >= 80:
                return "Easy"
            elif score >= 70:
                return "Fairly Easy"
            elif score >= 60:
                return "Standard"
            elif score >= 50:
                return "Fairly Difficult"
            elif score >= 30:
                return "Difficult"
            else:
                return "Very Difficult"
        
        return {
            'flesch_reading_ease': round(flesch_score, 2),
            'flesch_reading_level': interpret_flesch(flesch_score),
            'flesch_kincaid_grade_level': round(fk_grade, 2),
            'average_sentence_length': round(avg_sentence_length, 2),
            'average_syllables_per_word': round(avg_syllables_per_word, 2)
        }
    
    def word_frequency(self, top_n=20):
        """Find most common words"""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        words = re.findall(r'\b\w+\b', self.text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        word_counts = Counter(words)
        return dict(word_counts.most_common(top_n))
    
    def phrase_frequency(self, phrase_length=2, top_n=10):
        """Find most common phrases"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        phrases = []
        
        for i in range(len(words) - phrase_length + 1):
            phrase = ' '.join(words[i:i + phrase_length])
            phrases.append(phrase)
        
        phrase_counts = Counter(phrases)
        return dict(phrase_counts.most_common(top_n))
    
    def text_insights(self):
        """Generate text insights"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        insights = []
        
        # Word length analysis
        word_lengths = [len(word) for word in words]
        if word_lengths:
            avg_word_length = sum(word_lengths) / len(word_lengths)
            longest_word = max(words, key=len)
            shortest_word = min(words, key=len)
            
            insights.append(f"Average word length: {avg_word_length:.1f} characters")
            insights.append(f"Longest word: '{longest_word}' ({len(longest_word)} characters)")
            insights.append(f"Shortest word: '{shortest_word}' ({len(shortest_word)} characters)")
        
        # Sentence analysis
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            longest_sentence = max(sentences, key=lambda x: len(x.split()))
            shortest_sentence = min(sentences, key=lambda x: len(x.split()))
            
            insights.append(f"Longest sentence: {len(longest_sentence.split())} words")
            insights.append(f"Shortest sentence: {len(shortest_sentence.split())} words")
        
        # Paragraph analysis
        paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        if paragraphs:
            paragraph_lengths = [len(p.split()) for p in paragraphs]
            insights.append(f"Number of paragraphs: {len(paragraphs)}")
            insights.append(f"Average paragraph length: {sum(paragraph_lengths) / len(paragraph_lengths):.1f} words")
        
        return insights
    
    def analyze(self):
        """Perform complete text analysis"""
        if not self.text:
            return {'error': 'No text loaded'}
        
        self.analysis_results = {
            'filename': self.filename,
            'analysis_timestamp': datetime.now().isoformat(),
            'basic_stats': self.basic_stats(),
            'reading_time': self.reading_time(),
            'readability_scores': self.readability_scores(),
            'most_common_words': self.word_frequency(),
            'most_common_phrases': self.phrase_frequency(),
            'text_insights': self.text_insights()
        }
        
        return self.analysis_results
    
    def print_analysis(self):
        """Print formatted analysis results"""
        if not self.analysis_results:
            print("No analysis results available. Run analyze() first.")
            return
        
        results = self.analysis_results
        
        print(f"\n{'='*60}")
        print(f"TEXT ANALYSIS REPORT: {results['filename']}")
        print(f"Analysis Date: {results['analysis_timestamp']}")
        print(f"{'='*60}")
        
        # Basic Statistics
        stats = results['basic_stats']
        print(f"\n📊 BASIC STATISTICS")
        print(f"{'─'*30}")
        print(f"Total Characters: {stats['total_characters']:,}")
        print(f"Characters (no spaces): {stats['characters_no_spaces']:,}")
        print(f"Total Words: {stats['total_words']:,}")
        print(f"Unique Words: {stats['unique_words']:,}")
        print(f"Total Sentences: {stats['total_sentences']:,}")
        print(f"Total Lines: {stats['total_lines']:,}")
        print(f"Non-empty Lines: {stats['non_empty_lines']:,}")
        print(f"Avg Words/Sentence: {stats['average_words_per_sentence']:.1f}")
        print(f"Avg Characters/Word: {stats['average_characters_per_word']:.1f}")
        
        # Reading Time
        reading_time = results['reading_time']
        print(f"\n⏱️  READING TIME")
        print(f"{'─'*30}")
        print(f"Estimated Reading Time: {reading_time['estimated_reading_time_minutes']:.1f} minutes")
        print(f"Estimated Reading Time: {reading_time['estimated_reading_time_seconds']:.0f} seconds")
        
        # Readability Scores
        readability = results['readability_scores']
        if 'error' not in readability:
            print(f"\n📖 READABILITY ANALYSIS")
            print(f"{'─'*30}")
            print(f"Flesch Reading Ease: {readability['flesch_reading_ease']}")
            print(f"Reading Level: {readability['flesch_reading_level']}")
            print(f"Grade Level: {readability['flesch_kincaid_grade_level']}")
            print(f"Avg Sentence Length: {readability['average_sentence_length']:.1f} words")
            print(f"Avg Syllables/Word: {readability['average_syllables_per_word']:.2f}")
        
        # Most Common Words
        common_words = results['most_common_words']
        print(f"\n🔤 MOST COMMON WORDS")
        print(f"{'─'*30}")
        for word, count in list(common_words.items())[:10]:
            print(f"{word:<15} : {count:>3}")
        
        # Most Common Phrases
        common_phrases = results['most_common_phrases']
        print(f"\n📝 MOST COMMON PHRASES")
        print(f"{'─'*30}")
        for phrase, count in list(common_phrases.items())[:5]:
            print(f"'{phrase}' : {count}")
        
        # Text Insights
        insights = results['text_insights']
        print(f"\n💡 TEXT INSIGHTS")
        print(f"{'─'*30}")
        for insight in insights:
            print(f"• {insight}")
        
        print(f"\n{'='*60}")
    
    def save_analysis(self, output_file=None):
        """Save analysis results to JSON file"""
        if not self.analysis_results:
            print("No analysis results to save. Run analyze() first.")
            return False
        
        if not output_file:
            base_name = os.path.splitext(self.filename)[0]
            output_file = f"{base_name}_analysis.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
            print(f"Analysis saved to: {output_file}")
            return True
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Text File Analyzer - Comprehensive text analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python text_analyzer.py document.txt
  python text_analyzer.py document.txt --save
  python text_analyzer.py document.txt --output analysis.json
  python text_analyzer.py --interactive
        """
    )
    
    parser.add_argument('file', nargs='?', help='Text file to analyze')
    parser.add_argument('--save', '-s', action='store_true', help='Save analysis to JSON file')
    parser.add_argument('--output', '-o', help='Output file for analysis results')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    analyzer = TextAnalyzer()
    
    if args.interactive:
        print("Text Analyzer - Interactive Mode")
        print("=" * 40)
        
        while True:
            print("\nOptions:")
            print("1. Analyze a file")
            print("2. Analyze text input")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                filepath = input("Enter file path: ").strip()
                if analyzer.load_file(filepath):
                    analyzer.analyze()
                    analyzer.print_analysis()
                    
                    save_choice = input("\nSave analysis to file? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        analyzer.save_analysis()
            
            elif choice == '2':
                print("Enter your text (press Ctrl+D or Ctrl+Z when done):")
                try:
                    text_lines = []
                    while True:
                        line = input()
                        text_lines.append(line)
                except EOFError:
                    text = '\n'.join(text_lines)
                    if text.strip():
                        analyzer.load_text(text)
                        analyzer.analyze()
                        analyzer.print_analysis()
                        
                        save_choice = input("\nSave analysis to file? (y/n): ").strip().lower()
                        if save_choice == 'y':
                            analyzer.save_analysis()
                    else:
                        print("No text entered.")
            
            elif choice == '3':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    elif args.file:
        if analyzer.load_file(args.file):
            analyzer.analyze()
            analyzer.print_analysis()
            
            if args.save or args.output:
                analyzer.save_analysis(args.output)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
