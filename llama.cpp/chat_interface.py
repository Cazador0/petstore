import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from llama_cpp import Llama
import tkinter.ttk as ttk
import os
import pandas as pd
from tkinter import filedialog

class MultiModelChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatty")
        self.root.geometry("900x700")
        
        # Configure colors
        self.bg_color = "#1e1e2e"
        self.text_color = "#cdd6f4"
        self.input_bg = "#313244"
        self.accent_color = "#cba6f7"
        self.user_bg = "#45475a"
        self.assistant_bg = "#585b70"
        
        self.root.configure(bg=self.bg_color)
        
        # Model configurations
        self.models = {
            "Nomic-Embed-Text": "./models/nomic-embed-text-v1.5.Q5_K_M.gguf",
            "Coder-33B": "./models/deepseek-coder-33b-instruct.Q4_K_M.gguf",
        }
        
        # Initialize attributes first
        self.model_status = "No model loaded"
        self.status_var = tk.StringVar(value=self.model_status)
        self.history = [
            {"role": "system", "content": "You are an expert coding assistant. Be concise and accurate."}
        ]
        self.llm = None
        self.current_model = None
        self.chat_display = None
        self.user_input = None
        self.model_selector = None
        
        # Chunking parameters
        self.max_context_length = 3000  # Maximum tokens for context
        self.chunk_size = 1000  # Size of chunks for processing
        self.summary_threshold = 2000  # When to create a summary
        
        # Setup UI components
        self.create_widgets()
    
    def create_widgets(self):
        """Create all UI components"""
        # Top panel with model selector
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Model selection
        model_label = tk.Label(
            top_frame,
            text="Select Model:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("SF Mono", 10, "bold")
        )
        model_label.pack(side="left", padx=(0, 10))
        
        self.model_selector = ttk.Combobox(
            top_frame,
            values=list(self.models.keys()),
            state="readonly",
            width=25
        )
        self.model_selector.pack(side="left", padx=(0, 10))
        self.model_selector.bind("<<ComboboxSelected>>", self.on_model_selected)
        
        # Load model button
        load_button = tk.Button(
            top_frame,
            text="Load Model",
            command=self.load_selected_model,
            bg=self.accent_color,
            fg="#11111b",
            activebackground="#f5c2e7",
            font=("SF Mono", 10, "bold"),
            padx=10
        )
        load_button.pack(side="left", padx=(0, 10))
        
        # Clear conversation button
        clear_button = tk.Button(
            top_frame,
            text="Clear Chat",
            command=self.clear_conversation,
            bg="#f38ba8",
            fg="#11111b",
            activebackground="#f5c2e7",
            font=("SF Mono", 10, "bold"),
            padx=10
        )
        clear_button.pack(side="left", padx=(0, 10))
        
        # Context stats button
        stats_button = tk.Button(
            top_frame,
            text="Context Stats",
            command=self.show_context_stats,
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#f5c2e7",
            font=("SF Mono", 10, "bold"),
            padx=10
        )
        stats_button.pack(side="left", padx=(0, 10))
        
        # Import file button
        import_button = tk.Button(
            top_frame,
            text="Import File",
            command=self.import_file,
            bg="#fbb82d",
            fg="#11111b",
            activebackground="#f5c2e7",
            font=("SF Mono", 10, "bold"),
            padx=10
        )
        import_button.pack(side="left", padx=(0, 10))
        
        # Status bar
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            anchor="w",
            bg=self.bg_color,
            fg=self.accent_color,
            font=("SF Mono", 10)
        )
        status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
        # Chat display (scrollable)
        self.chat_display = ScrolledText(
            self.root,
            wrap="word",
            state="disabled",
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("SF Mono", 12),
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_display.tag_config("user", background=self.user_bg, lmargin1=20)
        self.chat_display.tag_config("assistant", background=self.assistant_bg, lmargin1=20)
        self.chat_display.tag_config("system", foreground="#a6e3a1", lmargin1=20)
        
        # Input panel
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.user_input = tk.Entry(
            input_frame,
            width=50,
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("SF Mono", 12)
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)
        self.user_input.bind("<Up>", self.load_previous_message)
        self.user_input.bind("<Down>", self.load_next_message)
        # Bind keyboard shortcuts
        self.root.bind("<Control-Shift-C>", lambda e: self.clear_conversation())
        self.root.bind("<Control-Shift-S>", lambda e: self.show_context_stats())
        
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg=self.accent_color,
            fg="#11111b",
            activebackground="#f5c2e7",
            font=("SF Mono", 10, "bold"),
            padx=15
        )
        send_button.pack(side="right")
        
        # Add initial message
        self.add_message("system", "Welcome to the Multi-Model Chat Interface! Please select and load a model to begin.")
        
        # Message history for up/down arrow navigation
        self.message_history = [""]
        self.history_index = 0
    
    def on_model_selected(self, event=None):
        """Handle model selection from dropdown"""
        selected_model = self.model_selector.get()
        if selected_model in self.models:
            self.status_var.set(f"Selected: {selected_model} | Click 'Load Model' to initialize")
        else:
            self.status_var.set("Please select a valid model")
    
    def load_selected_model(self):
        """Load the selected model in a background thread"""
        selected_model = self.model_selector.get()
        if not selected_model:
            self.status_var.set("❌ Please select a model first")
            return
            
        if selected_model not in self.models:
            self.status_var.set("❌ Invalid model selected")
            return
            
        model_path = self.models[selected_model]
        
        # Check if model file exists
        if not os.path.exists(model_path):
            self.status_var.set(f"❌ Model file not found: {model_path}")
            return
            
        self.model_status = f"Loading {selected_model}..."
        self.status_var.set(self.model_status)
        
        # Load model in background thread
        self.model_thread = threading.Thread(
            target=self._load_model_background, 
            args=(selected_model, model_path), 
            daemon=True
        )
        self.model_thread.start()
    
    def _load_model_background(self, model_name, model_path):
        """Actually load the model - runs in background thread"""
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=4096,  # Reduced context for better performance
                n_threads=8,
                n_gpu_layers=-1,  # Use all available GPU layers
                verbose=False
            )
            self.current_model = model_name
            self.model_status = f"✅ {model_name} loaded successfully!"
        except Exception as e:
            self.llm = None
            self.current_model = None
            self.model_status = f"❌ Model error: {str(e)}"
        self.update_status()
    
    def add_message(self, role, content):
        """Add a message to the chat display"""
        self.chat_display.configure(state="normal")
        
        # Add avatar and role indicator
        prefix = "👤 You: " if role == "user" else "🤖 Assistant: "
        prefix = "🖥️ System: " if role == "system" else prefix
        
        if role == "user":
            self.chat_display.insert("end", prefix, "user")
        elif role == "assistant":
            self.chat_display.insert("end", prefix, "assistant")
        else:
            self.chat_display.insert("end", prefix, "system")
        
        # Add content
        self.chat_display.insert("end", content + "\n\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.yview("end")
    
    def update_status(self):
        """Update the status bar text"""
        self.status_var.set(self.model_status)
    
    def load_previous_message(self, event=None):
        """Load previous message from history using up arrow"""
        if len(self.message_history) > 1:
            self.history_index = min(self.history_index + 1, len(self.message_history) - 1)
            self.user_input.delete(0, "end")
            self.user_input.insert(0, self.message_history[self.history_index])
        return "break"  # Prevent default behavior
    
    def load_next_message(self, event=None):
        """Load next message from history using down arrow"""
        if self.history_index > 0:
            self.history_index -= 1
            self.user_input.delete(0, "end")
            self.user_input.insert(0, self.message_history[self.history_index])
        else:
            self.user_input.delete(0, "end")
        return "break"  # Prevent default behavior
    
    def send_message(self, event=None):
        """Process and send user message"""
        message = self.user_input.get().strip()
        if not message:
            return
            
        # Add to message history if it's a new message
        if message != self.message_history[-1]:
            self.message_history.append(message)
        self.history_index = 0  # Reset history index
        
        self.user_input.delete(0, "end")
        self.add_message("user", message)
        
        # Add to conversation history
        self.history.append({"role": "user", "content": message})
        
        # Check if model is loaded
        if self.llm is None:
            self.add_message("system", "❌ Please load a model first!")
            return
        
        # Generate response in a background thread
        threading.Thread(target=self.generate_response, daemon=True).start()

    def generate_response(self):
        """Generate assistant response - runs in background thread"""
        # Disable input during processing
        self.user_input.configure(state="disabled")
        self.status_var.set(f"🤖 {self.current_model} is thinking...")
        
        try:
            # Manage context using chunking or summarization
            managed_context = self.manage_context(self.history)
            
            # Generate response using the loaded model with managed context
            response = self.llm.create_chat_completion(
                messages=managed_context,
                temperature=0.7,
                max_tokens=1024,
                stream=False
            )['choices'][0]['message']['content']
            
            # Add to history and UI
            self.history.append({"role": "assistant", "content": response})
            self.add_message("assistant", response)
            
            # Check if we need to manage context after adding this response
            total_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in self.history)
            if total_tokens > self.max_context_length * 1.5:
                self.add_message("system", f"ℹ️ Context management active: {len(self.history)} messages, ~{total_tokens} tokens")
        except Exception as e:
            self.add_message("system", f"⚠️ Error: {str(e)}")
        
        # Restore UI
        self.user_input.configure(state="normal")
        self.status_var.set(f"✅ {self.current_model} ready for input")
        self.user_input.focus()
    
    def estimate_tokens(self, text):
        """Estimate token count using the model's tokenizer for accuracy"""
        if self.llm is not None:
            # Use the model's tokenizer for accurate token count
            return len(self.llm.tokenize(text.encode('utf-8')))
        # Fallback to rough estimation if no model is loaded
        return len(text) // 4
    
    def chunk_conversation(self, messages):
        """Chunk conversation history for better context management"""
        if not messages:
            return messages
            
        # Calculate total tokens
        total_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in messages)
        
        # If within limit, return as is
        if total_tokens <= self.max_context_length:
            return messages
            
        # If too long, we need to chunk or summarize
        # Keep system message and most recent messages
        system_msg = [msg for msg in messages if msg["role"] == "system"]
        non_system_msgs = [msg for msg in messages if msg["role"] != "system"]
        
        # Keep the most recent messages within chunk size
        chunked_messages = system_msg.copy()
        current_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in chunked_messages)
        
        # Add messages from newest to oldest until we hit the limit
        for msg in reversed(non_system_msgs):
            msg_tokens = self.estimate_tokens(msg.get("content", ""))
            if current_tokens + msg_tokens <= self.max_context_length:
                chunked_messages.append(msg)
                current_tokens += msg_tokens
            else:
                # If we can't fit the whole message, try to chunk it
                if current_tokens < self.max_context_length:
                    available_tokens = self.max_context_length - current_tokens
                    # Truncate the message to fit
                    max_chars = available_tokens * 4
                    truncated_content = msg.get("content", "")[:max_chars] + " [truncated]"
                    truncated_msg = msg.copy()
                    truncated_msg["content"] = truncated_content
                    chunked_messages.append(truncated_msg)
                break
        
        # Reverse to maintain chronological order (oldest first, then newest)
        non_system_chunked = [msg for msg in chunked_messages if msg["role"] != "system"]
        chunked_messages = system_msg + list(reversed(non_system_chunked))
        
        return chunked_messages
    
    def create_context_summary(self, messages):
        """Create a summary of the conversation context"""
        if not self.llm or len(messages) <= 3:
            return messages
            
        # Only summarize if we have a substantial conversation
        try:
            summary_prompt = [
                {"role": "system", "content": "You are a concise summarizer. Create a brief summary of the conversation so far."},
                {"role": "user", "content": f"Summarize this conversation in one sentence:\n\n{self.format_messages_for_summary(messages)}"}
            ]
            
            summary_response = self.llm.create_chat_completion(
                messages=summary_prompt,
                temperature=0.3,
                max_tokens=150,
                stream=False
            )['choices'][0]['message']['content']
            
            # Replace conversation history with summary
            return [
                {"role": "system", "content": messages[0]["content"]},  # Keep original system message
                {"role": "assistant", "content": f"Previous conversation summary: {summary_response}"}
            ]
        except Exception as e:
            # If summarization fails, fall back to chunking
            return self.chunk_conversation(messages)
    
    def format_messages_for_summary(self, messages):
        """Format messages for summary generation"""
        formatted = []
        for msg in messages:
            if msg["role"] != "system":
                formatted.append(f"{msg['role'].title()}: {msg.get('content', '')}")
        return "\n".join(formatted)
    
    def manage_context(self, messages):
        """Manage conversation context using chunking or summarization"""
        total_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in messages)
        
        # If context is too long, either chunk or summarize
        if total_tokens > self.summary_threshold:
            # For very long conversations, create a summary
            if total_tokens > self.max_context_length * 2:
                return self.create_context_summary(messages)
            else:
                # For moderately long conversations, chunk
                return self.chunk_conversation(messages)
        
        return messages
    
    def clear_conversation(self):
        """Clear the conversation history"""
        # Keep only the system message
        self.history = [self.history[0]] if self.history else [
            {"role": "system", "content": "You are an expert coding assistant. Be concise and accurate."}
        ]
        
        # Clear the chat display
        self.chat_display.configure(state="normal")
        self.chat_display.delete(1.0, "end")
        self.chat_display.configure(state="disabled")
        
        # Add initial message
        self.add_message("system", "Conversation cleared. How can I help you?")
        
        self.status_var.set(f"✅ {self.current_model or 'No model'} ready for input")
    
    def show_context_stats(self):
        """Display context statistics"""
        total_messages = len(self.history)
        total_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in self.history)
        system_tokens = self.estimate_tokens(self.history[0].get("content", "")) if self.history else 0
        user_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in self.history if msg["role"] == "user")
        assistant_tokens = sum(self.estimate_tokens(msg.get("content", "")) for msg in self.history if msg["role"] == "assistant")
        
        stats_message = f"""Context Statistics:
- Total Messages: {total_messages}
- Total Tokens: ~{total_tokens}
- System Tokens: {system_tokens}
- User Tokens: {user_tokens}
- Assistant Tokens: {assistant_tokens}
- Model: {self.current_model or 'None'}"""
        
        self.add_message("system", stats_message)
    
    def import_file(self):
        """Import Excel spreadsheet with model analysis"""
        file_path = filedialog.askopenfilename(
            title="Select Excel Spreadsheet",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            self.add_message("system", "❌ No file selected.")
            return
        
        try:
            df = pd.read_excel(file_path)
            self.add_message("system", f"✅ File '{os.path.basename(file_path)}' imported successfully.")
            # Process the DataFrame as needed (e.g., display some data)
            self.add_message("assistant", str(df.head()))
        except Exception as e:
            self.add_message("system", f"❌ Error importing file: {str(e)}")
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiModelChatUI(root)
    root.mainloop()