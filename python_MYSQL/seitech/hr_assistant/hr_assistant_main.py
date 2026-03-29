#!/usr/bin/env python3
"""
HR Assistant - RAG System + Local LLM Integration with Query Preprocessing
Combines hardcoded PDF RAG with Qwen2.5-coder:3b for enhanced answers
Added query preprocessing to fix typos and grammar mistakes
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Optional
import requests
from hardcoded_pdf_rag import PDFRagSystem

class HRAssistant:
    def __init__(self, ollama_model: str = "qwen2.5-coder:7b", ollama_url: str = "http://98.86.11.72:11434"):
        """
        Initialize HR Assistant with RAG system and local LLM
        """
        print("Initializing HR Assistant...")
        
        # Initialize RAG system
        self.rag_system = PDFRagSystem()
        
        # LLM configuration
        self.ollama_model = ollama_model
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
        
        # Check if Ollama is running
        self.check_ollama_status()
        
        # Answer modes
        self.answer_modes = {
            '1': 'detailed',
            '2': 'general',
            '3': 'bullet_points'
        }
        
        print("HR Assistant initialized successfully!")
    
    def check_ollama_status(self) -> bool:
        """
        Check if Ollama is running and the model is available
        """
        try:
            # Test connection to Ollama
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if self.ollama_model not in model_names:
                    print(f"Warning: Model '{self.ollama_model}' not found in Ollama")
                    print(f"Available models: {', '.join(model_names)}")
                    print(f"Please install the model with: ollama pull {self.ollama_model}")
                    return False
                
                print(f"âœ“ Ollama is running with model: {self.ollama_model}")
                return True
            else:
                print(f"âœ— Ollama connection failed with status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"âœ— Ollama is not running or not accessible: {e}")
            print("Please start Ollama with: ollama serve")
            return False
    
    def preprocess_query(self, query: str) -> str:
        """
        Preprocess the query to fix typos and grammar mistakes using LLM
        """
        print("ðŸ”§ Preprocessing query (fixing typos and grammar)...")
        
        preprocessing_prompt = f"""You are a query preprocessing assistant. Your task is to:

1. Fix any spelling mistakes and typos in the given text
2. Correct grammar errors while preserving the original meaning
3. Make the text clear and well-structured for search purposes
4. Keep the same intent and keywords but improve readability
5. Return ONLY the corrected query without any additional text or explanations

Original query: "{query}"

Corrected query:"""

        try:
            payload = {
                "model": self.ollama_model,
                "prompt": preprocessing_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for consistent corrections
                    "top_p": 0.8,
                    "max_tokens": 200,   # Short response needed
                    "num_ctx": 2048
                }
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                corrected_query = result.get('response', query).strip()
                
                # Clean up the response (remove quotes, extra whitespace, etc.)
                corrected_query = corrected_query.strip('"\'').strip()
                
                # If the corrected query is significantly different, show the correction
                if corrected_query.lower() != query.lower():
                    print(f"ðŸ“ Query corrected: '{query}' â†’ '{corrected_query}'")
                else:
                    print("âœ“ Query is already well-formatted")
                
                return corrected_query
            else:
                print(f"âš  Query preprocessing failed, using original query")
                return query
                
        except Exception as e:
            print(f"âš  Query preprocessing error: {e}, using original query")
            return query
    
    def get_rag_context(self, query: str, top_k: int = 3) -> str:
        """
        Get relevant context from RAG system
        """
        print(f"ðŸ” Searching for relevant information...")
        
        # Get relevant chunks from RAG system
        relevant_chunks = self.rag_system.search_similar_chunks(query, top_k)
        
        if not relevant_chunks:
            return "No relevant information found in the database."
        
        # Format the context
        context_parts = []
        for i, chunk in enumerate(relevant_chunks, 1):
            context_parts.append(f"--- Relevant Information {i} ---")
            context_parts.append(f"Source: {chunk['source']}")
            context_parts.append(f"Similarity Score: {chunk['similarity_score']:.3f}")
            context_parts.append(f"Content: {chunk['text']}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def create_prompt(self, query: str, context: str, answer_mode: str = 'detailed') -> str:
        """
        Create the prompt for the LLM based on the answer mode
        """
        base_prompt = (
            "You are an HR Manager assistant.\n"
            "Your goal is to:\n"
            "1. Analyze the user query and the provided context from HR documents.\n"
            "2. Provide accurate, helpful, and professional HR guidance.\n"
            "3. Base your answer strictly on the provided context.\n"
            "4. If the context doesn't contain enough information, clearly state that.\n"
            "\n"
        )
        
        if answer_mode == 'detailed':
            mode_instruction = (
                "Provide a DETAILED answer that:\n"
                "- Explains all relevant policies and procedures\n"
                "- Includes specific requirements, timeframes, and approval processes\n"
                "- Mentions any exceptions or special cases\n"
                "- Uses a professional, comprehensive tone\n"
            )
        elif answer_mode == 'general':
            mode_instruction = (
                "Provide a GENERAL answer that:\n"
                "- Gives a clear, concise overview of the main points\n"
                "- Includes essential information without excessive detail\n"
                "- Adds helpful context and practical advice\n"
                "- Uses a friendly, accessible tone\n"
            )
        elif answer_mode == 'bullet_points':
            mode_instruction = (
                "Provide the answer in BULLET POINTS format that:\n"
                "- Organizes information into clear, scannable bullet points\n"
                "- Uses sub-bullets for detailed requirements when needed\n"
                "- Starts with main categories, then specific details\n"
                "- Makes the information easy to reference quickly\n"
            )
        
        full_prompt = f"""{base_prompt}{mode_instruction}

User Query: {query}

Context from HR Documents:
{context}

Please provide your answer:"""
        
        return full_prompt
    
    def query_llm(self, prompt: str) -> str:
        """
        Send prompt to local LLM and get response with enhanced error handling
        """
        try:
            print("ðŸ¤– Generating enhanced answer...")
            
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "max_tokens": 800,  # Reduced from 1000
                    "num_ctx": 4096,    # Context window
                    "num_predict": 800  # Max prediction tokens
                }
            }
            
            # Try with extended timeout first
            try:
                response = requests.post(
                    self.api_endpoint,
                    json=payload,
                    timeout=360  # Extended timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', 'No response received from LLM')
                else:
                    return f"Error: LLM request failed with status {response.status_code}"
                    
            except requests.exceptions.Timeout:
                # If still timeout, try with streaming
                print("Timeout occurred, trying streaming response...")
                return self.query_llm_streaming(prompt)
                
        except requests.exceptions.RequestException as e:
            # Fallback to RAG-only answer
            print(f"LLM unavailable: {e}")
            return self.get_fallback_answer(prompt)
    
    def query_llm_streaming(self, prompt: str) -> str:
        """
        Try streaming response for better timeout handling
        """
        try:
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "max_tokens": 500,  # Reduced for streaming
                    "num_ctx": 2048
                }
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=30,  # Shorter timeout for streaming
                stream=True
            )
            
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if 'response' in data:
                                full_response += data['response']
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
                
                return full_response if full_response else "No response received from streaming LLM"
            else:
                return f"Streaming request failed with status {response.status_code}"
                
        except Exception as e:
            return self.get_fallback_answer(prompt)
    
    def get_fallback_answer(self, prompt: str) -> str:
        """
        Provide fallback answer when LLM is unavailable
        """
        # Extract the query from the prompt
        query_start = prompt.find("User Query: ") + len("User Query: ")
        query_end = prompt.find("\n", query_start)
        query = prompt[query_start:query_end] if query_end != -1 else "the query"
        
        # Get raw RAG answer
        raw_answer = self.rag_system.answer_question(query)
        
        if raw_answer != "Sorry, this information is not provided in the documents.":
            return f"ðŸ“„ **RAG-Only Answer** (LLM unavailable):\n\n{raw_answer}\n\n*Note: This is the raw information from our documents. For enhanced formatting, please ensure Ollama is running properly.*"
        else:
            return "âŒ **No Information Found**: The query couldn't be answered from the available documents, and the LLM is currently unavailable for enhanced processing."
    
    def get_enhanced_answer(self, query: str, answer_mode: str = 'detailed') -> Dict:
        """
        Get enhanced answer combining query preprocessing, RAG and LLM
        """
        # Step 1: Preprocess query to fix typos and grammar
        corrected_query = self.preprocess_query(query)
        
        # Step 2: Get RAG context using the corrected query
        rag_context = self.get_rag_context(corrected_query)
        
        # Step 3: Create LLM prompt using the original query (for context) but search was done with corrected query
        prompt = self.create_prompt(query, rag_context, answer_mode)
        
        # Step 4: Get LLM response
        llm_response = self.query_llm(prompt)
        
        # Step 5: Get raw RAG answer using corrected query for comparison
        raw_answer = self.rag_system.answer_question(corrected_query)
        
        return {
            'original_query': query,
            'corrected_query': corrected_query,
            'answer_mode': answer_mode,
            'rag_context': rag_context,
            'raw_answer': raw_answer,
            'enhanced_answer': llm_response,
            'query_was_corrected': corrected_query.lower() != query.lower()
        }
    
    def display_answer(self, result: Dict) -> None:
        """
        Display the formatted answer
        """
        print("\n" + "="*80)
        print(f"ORIGINAL QUERY: {result['original_query']}")
        if result['query_was_corrected']:
            print(f"CORRECTED QUERY: {result['corrected_query']}")
        print(f"ANSWER MODE: {result['answer_mode'].upper()}")
        print("="*80)
        
        print("\nðŸ“ ENHANCED ANSWER:")
        print("-" * 40)
        print(result['enhanced_answer'])
        
        print(f"\nðŸ“Š RAG CONTEXT SUMMARY:")
        print("-" * 40)
        # Count relevant chunks
        context_lines = result['rag_context'].split('\n')
        chunk_count = len([line for line in context_lines if line.startswith('--- Relevant Information')])
        print(f"Found {chunk_count} relevant document sections")
        
        # Show query preprocessing info
        if result['query_was_corrected']:
            print("âœ“ Query was preprocessed and corrected")
        else:
            print("âœ“ Query was already well-formatted")
        
        # Show if raw answer was available
        if result['raw_answer'] != "Sorry, this information is not provided in the documents.":
            print("âœ“ Direct information found in documents")
        else:
            print("âš  Limited direct information - answer enhanced with LLM reasoning")
        
        # Show fallback options if LLM failed
        if "LLM unavailable" in result['enhanced_answer'] or "Error communicating with LLM" in result['enhanced_answer']:
            print("\nðŸ”§ TROUBLESHOOTING:")
            print("- Check if Ollama is running: ollama serve")
            print("- Verify model is installed: ollama pull qwen2.5-coder:3b")
            print("- Try a shorter, simpler question")
            print("- Consider using a smaller model like llama2:7b")
    
    def show_menu(self) -> None:
        """
        Display the main menu
        """
        print("\n" + "="*60)
        print("ðŸ¤– HR ASSISTANT - RAG + LLM POWERED (with Query Preprocessing)")
        print("="*60)
        print("Features:")
        print("â€¢ Automatic typo and grammar correction")
        print("â€¢ Smart document search")
        print("â€¢ Enhanced answer generation")
        print("\nAnswer Modes:")
        print("1. Detailed Answer (comprehensive with all details)")
        print("2. General Answer (concise with practical advice)")
        print("3. Bullet Points (organized, scannable format)")
        print("\nCommands:")
        print("â€¢ 'info' - Show database information")
        print("â€¢ 'help' - Show this menu")
        print("â€¢ 'quit' or 'exit' or 'bye' - Exit the program")
        print("="*60)
    
    def run(self) -> None:
        """
        Main interactive loop
        """
        self.show_menu()
        
        while True:
            try:
                # Get user query
                query = input("\nðŸ’¬ Enter your HR question: ").strip()
                
                # Handle commands
                if query.lower() in ['quit', 'exit', 'q','bye']:
                    print("\nðŸ‘‹ Goodbye!")
                    break
                
                if query.lower() == 'help':
                    self.show_menu()
                    continue
                
                if query.lower() == 'info':
                    info = self.rag_system.get_database_info()
                    if info:
                        print(f"\nðŸ“Š Database Information:")
                        print(f"Total chunks: {info['total_chunks']}")
                        print(f"Sources: {', '.join(info['sources'])}")
                        print(f"Total words: {info['total_words']:,}")
                        print(f"Average chunk length: {info['avg_chunk_length']:.1f} characters")
                        print(f"Accuracy threshold: {info['threshold']}")
                    continue
                
                if not query:
                    continue
                
                # Get answer mode
                print("\nðŸŽ¯ Select answer mode:")
                print("1. Detailed  2. General  3. Bullet Points")
                mode_choice = input("Choose (1-3) or press Enter for detailed: ").strip()
                
                if mode_choice not in self.answer_modes:
                    mode_choice = '1'  # Default to detailed
                
                answer_mode = self.answer_modes[mode_choice]
                
                # Get enhanced answer with preprocessing
                print(f"\nðŸš€ Processing your question in {answer_mode} mode...")
                result = self.get_enhanced_answer(query, answer_mode)
                
                # Display result
                self.display_answer(result)
                
            except KeyboardInterrupt:
                print("\n\nðŸ‘‹ Goodbye!")
                break
            except Exception as e:
                print(f"\nâŒ Error: {e}")
                print("Please try again or type 'help' for assistance.")

def main():
    """
    Main entry point
    """
    try:
        # Initialize HR Assistant
        assistant = HRAssistant()
        
        # Run the interactive session
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n\nðŸ‘‹ Goodbye!")
    except Exception as e:
        print(f"âŒ Failed to initialize HR Assistant: {e}")
        print("\nPlease ensure:")
        print("1. Ollama is running (ollama serve)")
        print("2. qwen2.5-coder:3b model is installed (ollama pull qwen2.5-coder:3b)")
        print("3. hardcoded_pdf_rag.py is in the same directory")

if __name__ == "__main__":
    print("""
    ðŸ“‹ REQUIREMENTS:
    pip install requests sentence-transformers torch pandas numpy
    
    ðŸš€ OLLAMA SETUP:
    1. Install Ollama: https://ollama.ai/
    2. Start Ollama: ollama serve
    3. Install model: ollama pull qwen2.5-coder:3b
    
    ðŸ†• NEW FEATURES:
    - Automatic query preprocessing to fix typos and grammar
    - Enhanced search accuracy through corrected queries
    - Improved user experience with better query understanding
    """)
    
    main()