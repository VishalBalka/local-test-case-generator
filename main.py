import os
from document_parser import DocumentParser
from testcase_generator import TestCaseGenerator
import datetime

class TestCaseGeneratorApp:
    """Main application for test case generation"""
    
    def __init__(self, model_name="llama3.2:3b"):
        self.parser = DocumentParser()
        self.generator = TestCaseGenerator(model_name)
        self.output_dir = "output/test_cases"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_file(self, file_path):
        """Process a file and generate test cases"""
        print(f"📄 Parsing file: {file_path}")
        requirements = self.parser.parse_file(file_path)
        
        print(f"✓ Extracted {len(requirements)} characters")
        print("🤖 Generating test cases...")
        
        test_cases = self.generator.generate_test_cases(requirements)
        
        self._save_output(test_cases, os.path.basename(file_path))
        return test_cases
    
    def process_text(self, text):
        """Process direct text input"""
        print("🤖 Generating test cases from text...")
        test_cases = self.generator.generate_test_cases(text)
        self._save_output(test_cases, "text_input")
        return test_cases
    
    def process_prompt(self, prompt):
        """Process custom prompt"""
        print("🤖 Generating test cases from prompt...")
        test_cases = self.generator.generate_from_prompt(prompt)
        self._save_output(test_cases, "custom_prompt")
        return test_cases
    
    def _save_output(self, content, source_name):
        """Save generated test cases to file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Test cases saved to: {filepath}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("    LOCAL TEST CASE GENERATOR")
    print("=" * 60)
    
    # Initialize app (change model if needed)
    app = TestCaseGeneratorApp(model_name="llama3.2:3b")
    
    while True:
        print("\nChoose input method:")
        print("1. Process PDF file")
        print("2. Process DOCX file")
        print("3. Process TXT file")
        print("4. Enter text directly")
        print("5. Enter custom prompt")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "6":
            print("Goodbye!")
            break
        
        try:
            if choice in ["1", "2", "3"]:
                file_path = input("Enter file path: ").strip()
                if not os.path.exists(file_path):
                    print("❌ File not found!")
                    continue
                test_cases = app.process_file(file_path)
                print("\n" + "=" * 60)
                print("GENERATED TEST CASES:")
                print("=" * 60)
                print(test_cases)
            
            elif choice == "4":
                print("Enter requirements text (press Ctrl+D or Ctrl+Z when done):")
                lines = []
                while True:
                    try:
                        line = input()
                        lines.append(line)
                    except EOFError:
                        break
                text = "\n".join(lines)
                test_cases = app.process_text(text)
                print("\n" + "=" * 60)
                print("GENERATED TEST CASES:")
                print("=" * 60)
                print(test_cases)
            
            elif choice == "5":
                prompt = input("Enter your prompt: ").strip()
                test_cases = app.process_prompt(prompt)
                print("\n" + "=" * 60)
                print("GENERATED TEST CASES:")
                print("=" * 60)
                print(test_cases)
            
            else:
                print("❌ Invalid choice!")
        
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()