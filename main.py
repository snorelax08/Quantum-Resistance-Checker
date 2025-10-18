import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Import the scoring function
try:
    from quantum_scorer import calculate_quantum_vulnerability_score
    from quantum_recommendations import get_recommendations, get_batch_recommendations
except ImportError:
    messagebox.showerror("Error", "quantum_scorer.py or quantum_recommendations.py not found!")

class QuantumResistanceChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Resistance Checker")
        self.root.geometry("800x900")
        self.root.configure(bg="#1a1a2e")
        
        # Title
        title_label = tk.Label(
            root, 
            text="⚛️ Quantum Resistance Checker ⚛️", 
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            root,
            text="Analyze encrypted files for quantum vulnerability",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#888888"
        )
        subtitle.pack(pady=5)
        
        # File selection button
        self.file_button = tk.Button(
            root,
            text="📁 Select Single File",
            command=self.select_file,
            font=("Arial", 12, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.file_button.pack(pady=10)
        
        # Multiple files button
        self.multi_file_button = tk.Button(
            root,
            text="📂 Select Multiple Files",
            command=self.select_multiple_files,
            font=("Arial", 12, "bold"),
            bg="#ffa500",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.multi_file_button.pack(pady=10)
        
        # File name display
        self.file_label = tk.Label(
            root,
            text="No file selected",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        self.file_label.pack()
        
        self.selected_file = None
        self.selected_files = []
        
        # Button frame for Analyze and Save buttons
        button_frame = tk.Frame(root, bg="#1a1a2e")
        button_frame.pack(pady=15)
        
        # Analyze button
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍 Analyze File",
            command=self.analyze_file,
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.analyze_button.pack(side="left", padx=10)
        
        # Save button
        self.save_button = tk.Button(
            button_frame,
            text="💾 Save Results",
            command=self.save_results,
            font=("Arial", 12, "bold"),
            bg="#51cf66",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.save_button.pack(side="left", padx=10)
        
        # Analyze Multiple button
        self.analyze_multi_button = tk.Button(
            button_frame,
            text="📊 Analyze Multiple",
            command=self.analyze_multiple_files,
            font=("Arial", 12, "bold"),
            bg="#9c27b0",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.analyze_multi_button.pack(side="left", padx=10)
        
        # Recommendations button
        self.rec_button = tk.Button(
            button_frame,
            text="💡 Recommendations",
            command=self.show_recommendations,
            font=("Arial", 12, "bold"),
            bg="#ff9800",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )
        self.rec_button.pack(side="left", padx=10)
        
        # Results area - using Text widget
        self.results_text = tk.Text(
            root,
            font=("Courier", 10),
            bg="#0f3460",
            fg="#00d4ff",
            height=30,
            width=95,
            relief="flat",
            borderwidth=2
        )
        self.results_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.results_text.insert("1.0", "Select a file and click 'Analyze File' to see results here...")
        self.results_text.config(state="disabled")
        
        # Store latest results for saving
        self.latest_results = None
        self.latest_result_text = None
        
    def select_file(self):
        """Let user pick a single file"""
        file_path = filedialog.askopenfilename(
            title="Select an encrypted file"
        )
        if file_path:
            self.selected_file = file_path
            self.selected_files = []
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"Selected: {file_name}")
    
    def select_multiple_files(self):
        """Let user pick multiple files"""
        file_paths = filedialog.askopenfilenames(
            title="Select multiple encrypted files"
        )
        if file_paths:
            self.selected_files = list(file_paths)
            self.selected_file = None
            self.file_label.config(text=f"Selected: {len(file_paths)} files")
    
    def create_progress_bar(self, score):
        """Create a visual progress bar"""
        max_score = 100
        filled = int((score / max_score) * 40)
        empty = 40 - filled
        
        if score >= 80:
            bar_char = "█"
            color_indicator = "🟢"
        elif score >= 60:
            bar_char = "▓"
            color_indicator = "🟡"
        elif score >= 40:
            bar_char = "▒"
            color_indicator = "🟠"
        else:
            bar_char = "░"
            color_indicator = "🔴"
        
        progress_bar = bar_char * filled + "░" * empty
        return f"[{progress_bar}] {score}/100  {color_indicator}"
    
    def analyze_file(self):
        """Analyze the selected file"""
        if self.selected_file is None:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        self.analyze_button.config(state="disabled")
        self.analyze_button.config(text="⏳ Analyzing...")
        self.root.update()
        
        try:
            results = calculate_quantum_vulnerability_score(self.selected_file)
            
            score = results['total_score']
            if score >= 80:
                risk_text = "✓ LOW RISK - Excellent quantum resistance"
                risk_emoji = "🟢"
            elif score >= 60:
                risk_text = "⚠ MEDIUM RISK - Good quantum resistance"
                risk_emoji = "🟡"
            elif score >= 40:
                risk_text = "⚠⚠ HIGH RISK - Vulnerable to quantum attacks"
                risk_emoji = "🟠"
            else:
                risk_text = "✗ CRITICAL RISK - Very vulnerable to quantum attacks"
                risk_emoji = "🔴"
            
            progress_bar = self.create_progress_bar(score)
            
            result_text = f"""
{'='*80}
{risk_emoji} QUANTUM RESISTANCE ANALYSIS {risk_emoji}
{'='*80}

FILE INFORMATION:
  • File Name:    {results['file_name']}
  • File Size:    {results['file_size']} bytes
  • File Type:    {results['file_extension']}

ENCRYPTION ALGORITHM DETECTED:
  • Algorithm:         {results['algorithm']}
  • File Type Info:    {results['description']}
  • Quantum Safe:      {'YES ✓' if results['is_quantum_safe'] else 'NO ✗'}
  • Threat Level:      {results['risk_level']}

SECURITY SCORE BREAKDOWN:
  • Algorithm Score:   {results['algorithm_score']:>2}/30  {'█' * (results['algorithm_score']//3)} {'░' * (10 - results['algorithm_score']//3)}
  • Key Length Score:  {results['key_length_score']:>2}/40  {'█' * (results['key_length_score']//4)} {'░' * (10 - results['key_length_score']//4)}
  • File Type Score:   {results['file_type_score']:>2}/20  {'█' * (results['file_type_score']//2)} {'░' * (10 - results['file_type_score']//2)}
  • Entropy Score:     {results['entropy_score']:>2}/10  {'█' * (results['entropy_score'])} {'░' * (10 - results['entropy_score'])}

{'='*80}

OVERALL QUANTUM RESISTANCE SCORE:

  {progress_bar}

  Risk Assessment: {risk_text}

{'='*80}

WHAT DOES THIS MEAN?

  Score < 40:   🔴 CRITICAL - Very vulnerable to quantum computers
  Score 40-60:  🟠 HIGH - Vulnerable but acceptable for now
  Score 60-80:  🟡 MEDIUM - Good quantum resistance
  Score > 80:   🟢 LOW - Excellent quantum resistance

A higher score means better protection against quantum attacks!

{'='*80}
"""
            
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", result_text)
            self.results_text.config(state="disabled")
            
            self.latest_results = results
            self.latest_result_text = result_text
            
        except Exception as e:
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"❌ ERROR: {str(e)}\n\nPlease make sure:\n  1. The file exists\n  2. You have permission to read it\n  3. quantum_scorer.py is in the same folder")
            self.results_text.config(state="disabled")
            messagebox.showerror("Analysis Error", f"Error: {str(e)}")
        
        finally:
            self.analyze_button.config(state="normal")
            self.analyze_button.config(text="🔍 Analyze File")
    
    def analyze_multiple_files(self):
        """Analyze multiple files and compare them"""
        if not self.selected_files:
            messagebox.showerror("Error", "Please select multiple files first!")
            return
        
        self.analyze_multi_button.config(state="disabled")
        self.analyze_multi_button.config(text="⏳ Analyzing...")
        self.root.update()
        
        try:
            print(f"DEBUG: Starting analysis of {len(self.selected_files)} files")
            results_list = []
            
            for file_path in self.selected_files:
                print(f"DEBUG: Analyzing {file_path}")
                results = calculate_quantum_vulnerability_score(file_path)
                results_list.append(results)
            
            results_list.sort(key=lambda x: x['total_score'], reverse=True)
            
            best_file = results_list[0]
            worst_file = results_list[-1]
            avg_score = sum([r['total_score'] for r in results_list]) / len(results_list)
            
            result_text = f"""
{'='*80}
📊 QUANTUM RESISTANCE COMPARISON ANALYSIS 📊
{'='*80}

SUMMARY:
  • Total Files Analyzed: {len(results_list)}
  • Average Score: {avg_score:.1f}/100
  • Best Score: {best_file['total_score']}/100 ({best_file['file_name']})
  • Worst Score: {worst_file['total_score']}/100 ({worst_file['file_name']})

{'='*80}
DETAILED RESULTS (sorted by security score):
{'='*80}

"""
            
            for i, results in enumerate(results_list, 1):
                score = results['total_score']
                if score >= 80:
                    emoji = "🟢"
                    risk = "LOW"
                elif score >= 60:
                    emoji = "🟡"
                    risk = "MEDIUM"
                elif score >= 40:
                    emoji = "🟠"
                    risk = "HIGH"
                else:
                    emoji = "🔴"
                    risk = "CRITICAL"
                
                progress_bar = self.create_progress_bar(score)
                
                result_text += f"""{i}. {emoji} {results['file_name']}
   Algorithm: {results['algorithm']}
   Quantum Safe: {'YES ✓' if results['is_quantum_safe'] else 'NO ✗'}
   Score: {progress_bar}
   Risk: {risk}
   Details: {results['description']}

"""
            
            result_text += f"""{'='*80}
SECURITY RANKING:
{'='*80}

"""
            
            for i, results in enumerate(results_list, 1):
                result_text += f"{i}. {results['file_name']:40} {results['total_score']:>3}/100\n"
            
            result_text += f"""
{'='*80}
RECOMMENDATIONS:
{'='*80}

Most Secure: {best_file['file_name']} (Score: {best_file['total_score']}/100)
Least Secure: {worst_file['file_name']} (Score: {worst_file['total_score']}/100)

Files needing upgrade: {len([r for r in results_list if r['total_score'] < 60])}
Files with good security: {len([r for r in results_list if r['total_score'] >= 60])}

{'='*80}
"""
            
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", result_text)
            self.results_text.config(state="disabled")
            
            self.latest_results = {'multiple': True, 'count': len(results_list)}
            self.latest_result_text = result_text
            
            print(f"DEBUG: Analysis complete!")
            
        except Exception as e:
            print(f"DEBUG: ERROR - {str(e)}")
            import traceback
            traceback.print_exc()
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"❌ ERROR: {str(e)}\n\nPlease make sure all files are valid.")
            self.results_text.config(state="disabled")
            messagebox.showerror("Analysis Error", f"Error: {str(e)}")
        
        finally:
            self.analyze_multi_button.config(state="normal")
            self.analyze_multi_button.config(text="📊 Analyze Multiple")
    
    def show_recommendations(self):
        """Show recommendations based on latest analysis"""
        if self.latest_results is None:
            messagebox.showerror("Error", "Please analyze a file first!")
            return
        
        try:
            # Check if it's a batch analysis or single file
            if isinstance(self.latest_results, dict) and 'multiple' in self.latest_results:
                # This is batch analysis - need to re-analyze to get results list
                messagebox.showinfo("Info", "Batch recommendations coming soon! Analyze files first.")
                return
            else:
                # Single file analysis
                algorithm = self.latest_results['algorithm']
                score = self.latest_results['total_score']
                rec_text = get_recommendations(algorithm, score)
            
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", rec_text)
            self.results_text.config(state="disabled")
            
            # Store for saving
            self.latest_result_text = rec_text
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating recommendations:\n{str(e)}")
    
    def save_results(self):
        """Save the latest analysis results to a file"""
        if self.latest_result_text is None:
            messagebox.showerror("Error", "Please analyze a file first before saving!")
            return
        
        print(f"DEBUG: Saving results. Text length: {len(self.latest_result_text)}")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=f"quantum_analysis_results.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.latest_result_text)
                
                print(f"DEBUG: File saved to {file_path}")
                messagebox.showinfo("Success", f"Results saved successfully!\n\nFile: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumResistanceChecker(root)
    root.mainloop()