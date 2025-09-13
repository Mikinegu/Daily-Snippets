#!/usr/bin/env python3
"""
Typing Speed Tester Program
A comprehensive typing speed tester that measures WPM, accuracy, and provides detailed statistics.
"""

import time
import random
import string
from typing import List, Tuple, Dict
import os
import sys


class TypingSpeedTester:
    """
    A comprehensive typing speed tester that measures:
    - Words Per Minute (WPM)
    - Characters Per Minute (CPM)
    - Accuracy percentage
    - Error analysis
    """
    
    def __init__(self):
        """Initialize the typing speed tester with default settings."""
        self.text_samples = [
            "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
            "Python is a powerful programming language that is easy to learn and fun to use.",
            "Practice makes perfect when it comes to typing. The more you type, the better you become.",
            "Technology has revolutionized the way we communicate and work in the modern world.",
            "Learning to type efficiently can significantly improve your productivity and reduce fatigue.",
            "The art of typing is not just about speed, but also about accuracy and consistency.",
            "Every keystroke matters when you're trying to achieve the perfect typing rhythm.",
            "Consistent practice and proper technique are the keys to becoming a proficient typist.",
            "The digital age demands fast and accurate typing skills for success in many careers.",
            "Typing speed tests help you identify areas for improvement and track your progress over time."
        ]
        
        self.current_text = ""
        self.start_time = 0
        self.end_time = 0
        self.user_input = ""
        self.errors = []
        
    def clear_screen(self):
        """Clear the terminal screen for better user experience."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        self.clear_screen()
        print("=" * 60)
        print("           TYPING SPEED TESTER")
        print("=" * 60)
        print("\nInstructions:")
        print("• You will be given a text to type")
        print("• Type the text exactly as shown")
        print("• Press ENTER when you're done")
        print("• Your speed and accuracy will be calculated")
        print("\nPress ENTER to start the test...")
        input()
    
    def select_text(self) -> str:
        """
        Select a random text sample for the typing test.
        
        Returns:
            str: The selected text for typing
        """
        return random.choice(self.text_samples)
    
    def display_text(self, text: str):
        """
        Display the text to be typed with proper formatting.
        
        Args:
            text (str): The text to display
        """
        self.clear_screen()
        print("=" * 60)
        print("           TYPING SPEED TEST")
        print("=" * 60)
        print("\nType the following text:")
        print("-" * 60)
        print(text)
        print("-" * 60)
        print("\nPress ENTER when you're ready to start typing...")
        input()
        
        # Clear screen and show text again for typing
        self.clear_screen()
        print("=" * 60)
        print("           TYPING IN PROGRESS")
        print("=" * 60)
        print("\nType the following text:")
        print("-" * 60)
        print(text)
        print("-" * 60)
        print("\nStart typing now!")
        print("(Press ENTER when finished)\n")
    
    def get_user_input(self) -> str:
        """
        Get user input for the typing test.
        
        Returns:
            str: The user's typed input
        """
        return input()
    
    def calculate_statistics(self, original_text: str, user_input: str, 
                           start_time: float, end_time: float) -> Dict:
        """
        Calculate comprehensive typing statistics.
        
        Args:
            original_text (str): The original text to type
            user_input (str): What the user actually typed
            start_time (float): When typing started
            end_time (float): When typing ended
            
        Returns:
            Dict: Dictionary containing all calculated statistics
        """
        # Basic calculations
        time_taken = end_time - start_time
        minutes = time_taken / 60
        
        # Character and word counts
        original_chars = len(original_text)
        user_chars = len(user_input)
        
        # Split into words (5 characters = 1 word for WPM calculation)
        original_words = len(original_text.split())
        user_words = len(user_input.split())
        
        # Calculate WPM and CPM
        wpm = (user_chars / 5) / minutes if minutes > 0 else 0
        cpm = user_chars / minutes if minutes > 0 else 0
        
        # Calculate accuracy
        errors = self.find_errors(original_text, user_input)
        total_chars = max(original_chars, user_chars)
        correct_chars = total_chars - len(errors)
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        
        # Calculate error rate
        error_rate = (len(errors) / total_chars) * 100 if total_chars > 0 else 0
        
        return {
            'time_taken': time_taken,
            'wpm': wpm,
            'cpm': cpm,
            'accuracy': accuracy,
            'error_rate': error_rate,
            'total_chars': total_chars,
            'correct_chars': correct_chars,
            'errors': errors,
            'original_words': original_words,
            'user_words': user_words
        }
    
    def find_errors(self, original: str, user_input: str) -> List[Tuple[int, str, str]]:
        """
        Find and categorize errors in the user's input.
        
        Args:
            original (str): The original text
            user_input (str): The user's input
            
        Returns:
            List[Tuple[int, str, str]]: List of (position, expected, actual) tuples
        """
        errors = []
        min_length = min(len(original), len(user_input))
        
        # Check character by character
        for i in range(min_length):
            if original[i] != user_input[i]:
                errors.append((i, original[i], user_input[i]))
        
        # Check for extra or missing characters
        if len(user_input) > len(original):
            for i in range(len(original), len(user_input)):
                errors.append((i, '', user_input[i]))
        elif len(original) > len(user_input):
            for i in range(len(user_input), len(original)):
                errors.append((i, original[i], ''))
        
        return errors
    
    def display_results(self, stats: Dict):
        """
        Display the typing test results in a formatted manner.
        
        Args:
            stats (Dict): Dictionary containing typing statistics
        """
        self.clear_screen()
        print("=" * 60)
        print("           TYPING TEST RESULTS")
        print("=" * 60)
        
        print(f"\n⏱️  Time Taken: {stats['time_taken']:.2f} seconds")
        print(f"📊 Words Per Minute (WPM): {stats['wpm']:.1f}")
        print(f"📈 Characters Per Minute (CPM): {stats['cpm']:.1f}")
        print(f"🎯 Accuracy: {stats['accuracy']:.1f}%")
        print(f"❌ Error Rate: {stats['error_rate']:.1f}%")
        
        print(f"\n📝 Text Statistics:")
        print(f"   • Original words: {stats['original_words']}")
        print(f"   • Your words: {stats['user_words']}")
        print(f"   • Total characters: {stats['total_chars']}")
        print(f"   • Correct characters: {stats['correct_chars']}")
        print(f"   • Errors: {len(stats['errors'])}")
        
        # Display errors if any
        if stats['errors']:
            print(f"\n🔍 Error Analysis:")
            for i, (pos, expected, actual) in enumerate(stats['errors'][:10]):  # Show first 10 errors
                if expected == '':
                    print(f"   Position {pos}: Extra character '{actual}'")
                elif actual == '':
                    print(f"   Position {pos}: Missing character '{expected}'")
                else:
                    print(f"   Position {pos}: Expected '{expected}', got '{actual}'")
            
            if len(stats['errors']) > 10:
                print(f"   ... and {len(stats['errors']) - 10} more errors")
        
        # Performance rating
        print(f"\n🏆 Performance Rating:")
        if stats['wpm'] >= 70 and stats['accuracy'] >= 95:
            print("   Excellent! Professional level typing speed.")
        elif stats['wpm'] >= 50 and stats['accuracy'] >= 90:
            print("   Good! Above average typing speed.")
        elif stats['wpm'] >= 30 and stats['accuracy'] >= 80:
            print("   Fair. Keep practicing to improve.")
        else:
            print("   Needs improvement. Focus on accuracy first, then speed.")
    
    def run_test(self):
        """Run a complete typing speed test."""
        try:
            # Display welcome
            self.display_welcome()
            
            # Select and display text
            self.current_text = self.select_text()
            self.display_text(self.current_text)
            
            # Start timing and get input
            self.start_time = time.time()
            self.user_input = self.get_user_input()
            self.end_time = time.time()
            
            # Calculate and display results
            stats = self.calculate_statistics(
                self.current_text, 
                self.user_input, 
                self.start_time, 
                self.end_time
            )
            
            self.display_results(stats)
            
            # Ask if user wants to try again
            print("\n" + "=" * 60)
            try_again = input("Would you like to try again? (y/n): ").lower().strip()
            if try_again in ['y', 'yes']:
                self.run_test()
            else:
                print("\nThank you for using the Typing Speed Tester!")
                print("Keep practicing to improve your typing skills! 🚀")
                
        except KeyboardInterrupt:
            print("\n\nTest interrupted. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


def main():
    """Main function to run the typing speed tester."""
    tester = TypingSpeedTester()
    tester.run_test()


if __name__ == "__main__":
    main()
