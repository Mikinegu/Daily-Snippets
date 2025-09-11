# Text File Analyzer 📊

A comprehensive Python tool for analyzing text files with detailed statistics, readability scores, and insights. Perfect for writers, editors, students, and anyone who wants to understand their text better.

## Features ✨

- **Basic Statistics**: Word count, character count, line count, sentence analysis
- **Reading Time Estimation**: Calculate how long it takes to read your text
- **Readability Analysis**: Flesch Reading Ease and Flesch-Kincaid Grade Level scores
- **Word Frequency Analysis**: Find the most common words and phrases
- **Text Insights**: Detailed analysis of word lengths, sentence structures, and more
- **Multiple Input Methods**: Analyze files or direct text input
- **Export Results**: Save analysis results to JSON format
- **Interactive Mode**: User-friendly command-line interface

## Installation 🚀

1. Clone or download this repository
2. Navigate to the project directory
3. No external dependencies required! Uses only Python standard library

```bash
cd "Text file analyzer"
```

## Usage 📖

### Command Line Usage

#### Analyze a text file:
```bash
python text_analyzer.py sample_text.txt
```

#### Save analysis results:
```bash
python text_analyzer.py sample_text.txt --save
```

#### Specify output file:
```bash
python text_analyzer.py sample_text.txt --output my_analysis.json
```

#### Interactive mode:
```bash
python text_analyzer.py --interactive
```

### Python API Usage

```python
from text_analyzer import TextAnalyzer

# Create analyzer instance
analyzer = TextAnalyzer()

# Load text from file
analyzer.load_file("document.txt")

# Or load text directly
analyzer.load_text("Your text here...")

# Perform analysis
results = analyzer.analyze()

# Print formatted results
analyzer.print_analysis()

# Save results to JSON
analyzer.save_analysis("analysis.json")
```

## Sample Output 📋

```
============================================================
TEXT ANALYSIS REPORT: sample_text.txt
Analysis Date: 2024-01-15T10:30:45.123456
============================================================

📊 BASIC STATISTICS
──────────────────────────────
Total Characters: 1,234
Characters (no spaces): 1,045
Total Words: 198
Unique Words: 156
Total Sentences: 12
Total Lines: 8
Non-empty Lines: 6
Avg Words/Sentence: 16.5
Avg Characters/Word: 5.3

⏱️  READING TIME
──────────────────────────────
Estimated Reading Time: 1.0 minutes
Estimated Reading Time: 59 seconds

📖 READABILITY ANALYSIS
──────────────────────────────
Flesch Reading Ease: 65.2
Reading Level: Standard
Grade Level: 8.5
Avg Sentence Length: 16.5 words
Avg Syllables/Word: 1.8

🔤 MOST COMMON WORDS
──────────────────────────────
text             :  12
analysis         :   8
words            :   6
file             :   5
content          :   4

📝 MOST COMMON PHRASES
──────────────────────────────
'text analysis' : 3
'file analyzer' : 2
'reading time' : 2

💡 TEXT INSIGHTS
──────────────────────────────
• Average word length: 5.3 characters
• Longest word: 'comprehensive' (13 characters)
• Shortest word: 'a' (1 characters)
• Longest sentence: 25 words
• Shortest sentence: 8 words
• Number of paragraphs: 3
• Average paragraph length: 66.0 words
============================================================
```

## File Structure 📁

```
Text file analyzer/
├── text_analyzer.py      # Main analyzer script
├── requirements.txt      # Dependencies (none required!)
├── README.md            # This file
├── sample_texts/        # Example text files
│   ├── sample1.txt
│   ├── sample2.txt
│   └── sample3.txt
└── examples/           # Usage examples
    ├── basic_usage.py
    └── advanced_usage.py
```

## Analysis Features Explained 🔍

### Basic Statistics
- **Total Characters**: All characters including spaces and punctuation
- **Characters (no spaces)**: Characters excluding spaces
- **Total Words**: Number of words (alphanumeric sequences)
- **Unique Words**: Number of distinct words
- **Sentences**: Number of sentences (split by . ! ?)
- **Lines**: Total lines in the file
- **Non-empty Lines**: Lines with actual content

### Reading Time
- Based on average reading speed of 200 words per minute
- Provides both minutes and seconds estimates

### Readability Scores
- **Flesch Reading Ease**: 0-100 scale (higher = easier to read)
- **Flesch-Kincaid Grade Level**: U.S. grade level required to understand
- **Reading Level Categories**: Very Easy, Easy, Fairly Easy, Standard, Fairly Difficult, Difficult, Very Difficult

### Word Frequency
- Shows most common words (excluding common stop words)
- Configurable number of top words to display
- Filters out words shorter than 3 characters

### Phrase Analysis
- Finds most common 2-word phrases
- Useful for identifying recurring concepts

## Examples 📚

### Example 1: Analyzing a Blog Post
```bash
python text_analyzer.py blog_post.txt --save
```

### Example 2: Interactive Analysis
```bash
python text_analyzer.py --interactive
```

### Example 3: Batch Analysis Script
```python
import os
from text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
text_files = [f for f in os.listdir('.') if f.endswith('.txt')]

for file in text_files:
    print(f"\nAnalyzing {file}...")
    analyzer.load_file(file)
    analyzer.analyze()
    analyzer.print_analysis()
    analyzer.save_analysis(f"{file}_analysis.json")
```

## Customization 🛠️

### Modifying Stop Words
Edit the `stop_words` set in the `word_frequency()` method to customize which words are filtered out.

### Changing Reading Speed
Modify the reading speed constant in `reading_time()` method (default: 200 words/minute).

### Adding New Metrics
Extend the `TextAnalyzer` class with new methods and integrate them into the `analyze()` method.

## Contributing 🤝

Contributions are welcome! Here are some ideas for enhancements:

- GUI interface using tkinter
- Web interface using Flask or Streamlit
- Support for more file formats (PDF, DOCX, etc.)
- Advanced readability metrics
- Language detection
- Sentiment analysis
- Export to different formats (CSV, HTML, etc.)

## License 📄

This project is open source and available under the MIT License.

## Troubleshooting 🔧

### Common Issues

1. **File not found error**: Make sure the file path is correct and the file exists
2. **Unicode decode error**: Ensure the file is a text file with proper encoding
3. **Empty analysis**: Check that the file contains actual text content

### Performance Notes

- Large files (>10MB) may take longer to process
- Memory usage scales with file size
- Consider splitting very large files for analysis

## Future Enhancements 🚀

- [ ] GUI interface
- [ ] Web interface
- [ ] PDF and DOCX support
- [ ] Batch processing
- [ ] Advanced readability metrics
- [ ] Language detection
- [ ] Sentiment analysis
- [ ] Export to multiple formats
- [ ] Real-time analysis
- [ ] Comparison between texts

---

**Happy Analyzing!** 📊✨
