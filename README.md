# **LLM Verbal Skills Trainer** 🚀  

An **AI-powered** verbal skills training system that leverages **LLMs** with **optimized inference, quantization strategies, and evaluation mechanisms** to enhance **spoken communication and language understanding**.  

---

## 📌 **Table of Contents**  
- [🎯 Project Overview](#-project-overview)  
- [⚙️ Setup Instructions](#️-setup-instructions)  
- [🛠 Model Optimization & Performance Analysis](#-model-optimization--performance-analysis)  
- [🚀 Usage Guide (Examples)](#-usage-guide-examples)  
- [📊 Comprehensive LLM Benchmarking Report](#-comprehensive-llm-benchmarking-report)  
- [🔍 LLM Selection & Implementation Strategy](#-llm-selection--implementation-strategy)  
- [⚙️ Configuration Details](#-configuration-details)  
- [💡 Final Thoughts](#-final-thoughts)  

---

## 🎯 **Project Overview**  
The **LLM Verbal Skills Trainer** is designed to improve **verbal and communication skills** through **real-time AI-based conversation and assessment**.  

### **Key Features:**  
✅ **Conversational AI** – Engages users in real-time dialogues.  
✅ **Presentation Assessment** – Evaluates speech and provides feedback.  
✅ **Skill Training** – Custom learning modules for verbal proficiency.  
✅ **Voice Interface** – AI-driven **text-to-speech** and **speech recognition**.  
✅ **Performance Benchmarking** – Evaluates **inference time, memory usage, accuracy** of different models.  

---

## ⚙️ **Setup Instructions**  
### **1️⃣ Install Dependencies**  
This project requires **Python 3.11**. Ensure it is installed before proceeding.  

```sh
# Install Poetry (for dependency management)
pip install poetry

# Install project dependencies
poetry install
```

### **2️⃣ Download & Install Ollama (for LLM inference)**  
The `src/olla_setup.py` script will **install Ollama, pull required models, and optimize settings**.  

```sh
# Run the setup script to install Ollama and download models
python3.11 src/olla_setup.py
```

This will:  
✅ **Check if Ollama is installed**  
✅ **Download pre-selected LLMs**  
✅ **Apply different quantization and optimization settings**  

📌 **Note:** The models downloaded include:  
- `llama2:7b`  
- `mistral:7b`  
- `deepseek-r1:14b`, `deepseek-r1:7b`, `deepseek-r1:1.5b`  
- `llama3.2:latest`  

---

### **3️⃣ Run Model Performance Evaluation**  
Once models are downloaded, analyze their **performance, memory usage, and inference time** by running:  

```sh
python3.11 src/evaluation_analysis.py
```

This script:  
✅ **Benchmarks models with different quantization strategies**  
✅ **Generates interactive performance graphs**  
✅ **Logs optimal configurations for inference efficiency**  

---

### **4️⃣ Run the Application**  
Start the **Verbal Skills Training AI** by running:  

```sh
python3.11 main.py
```

🎯 **This will launch the AI-driven verbal skills training tool.**  

---

## 🚀 **Usage Guide (Examples)**
### 🎭 **Choose a Skill Module**
**Selected Module:** `Storytelling`

### 🎲 **Get Your Challenge**
🎭 **Your Challenge:** Share a fictional story about overcoming fear.

⏳ **You have 60 seconds! Countdown starts now!** 🚀

**🔥 Challenge:** Tell a captivating story based on the prompt.  
🎯 **Tips:** Focus on **narrative flow, character depth, and audience engagement**.  
🏆 **Evaluation Criteria:** Narrative structure, character development, emotional engagement, creativity, and delivery.

---

### ✍️ **User Response**
```text
Lena had always been terrified of water. As a child, a near-drowning experience left her paralyzed with fear at the mere sight of a swimming pool. But when her friends planned a beach trip, she decided it was time to face her fear. With her heart pounding, she dipped her toes into the ocean. Guided by a patient instructor, she learned to float, then paddle. Each small step built her confidence. Finally, after weeks of practice, she took a deep breath and swam on her own. The fear that once controlled her had faded. Now, the ocean felt like freedom, not danger. Lena realized courage wasn’t the absence of fear—it was moving forward despite it.
```

🚀 **Submit Response via Text or Voice**
🎤 **Speak or Upload Audio**

---

### 🗣 **Skill Training Feedback**

📌 **LLM Evaluation Response**

```text
‍🏫 Coach:
📖 Story Prompt: Share a fictional story about overcoming fear.

📌 LLM Evaluation
Thank you for providing this detailed critique of my spoken response. I'm excited to receive feedback on how I can improve my verbal communication skills.

Here's my breakdown of the evaluation criteria:

1️⃣ Clarity & Articulation:
* Strengths: I tried to use simple and clear language to convey the story, avoiding unnecessary jargon or complex vocabulary.
* Areas for Improvement: To enhance clarity, I could focus on pausing slightly between sentences to allow listeners to process the information. Additionally, I might consider using more descriptive phrases to paint a vivid picture in the listener's mind.

2️⃣ Confidence & Presence:
* Strengths: I attempted to convey confidence by standing up straight and making eye contact with the imaginary audience.
* Areas for Improvement: To further enhance presence, I could work on maintaining a consistent tone and pitch throughout the speech. This would help me feel more confident and assertive.

3️⃣ Engagement & Energy:
* Strengths: I tried to infuse some enthusiasm into my delivery by using words like "freedom" and "courage."
* Areas for Improvement: To increase engagement, I could experiment with varying my tone, pitch, and volume. For example, I might use a slightly softer tone when describing Lena's initial fear or a more forceful tone when discussing her triumph.

4️⃣ Structure & Coherence:
* Strengths: My story followed a logical sequence of events, making it easy to follow along.
* Areas for Improvement: To improve structure, I could consider using transitional phrases or words to connect ideas between sentences. This would create a smoother flow and make the speech feel more polished.

5️⃣ Persuasiveness & Impact:
* Strengths: I aimed to inspire my audience by highlighting the importance of facing fears and embracing courage.
* Areas for Improvement: To increase persuasiveness, I could use rhetorical devices like metaphors or analogies to make the message more relatable and memorable. Additionally, I might consider using more emotional appeals to connect with my listeners on a deeper level.

Overall, I'm pleased with the direction of my spoken response, but there's always room for improvement. Thank you for your detailed feedback and guidance!

Total Average Score:

1️⃣ Clarity & Articulation: 7/10
2️⃣ Confidence & Presence: 6.5/10
3️⃣ Engagement & Energy: 7.5/10
4️⃣ Structure & Coherence: 8/10
5️⃣ Persuasiveness & Impact: 7.5/10

Total Average Score: 7.3/10
```
### 📜 **Presentation Assessment**

📜 **Your Presentation Script**

```text
In today’s fast-paced world, effective communication is a vital skill. Our AI-powered coaching system enhances public speaking, storytelling, and conflict resolution skills through real-time feedback and intelligent assessments. Using advanced NLP techniques, it evaluates speech clarity, confidence, and content structure, providing actionable insights for improvement. Multi-threading ensures smooth performance, making interactions seamless. Whether for professional growth or personal development, this tool empowers users to communicate with impact. With interactive challenges and voice-based assessments, it creates a dynamic learning experience. Elevate your communication skills with AI-driven training—practice, improve, and excel in any conversation!
```
📌 **LLM Evaluation Response**

```text
🏫 Coach:

📌 LLM Evaluation
Overall Assessment Table

Criteria	   Score 🎯
Structure	    8/10
Delivery	    6/10
Content	            7/10
Overall Score       21/30
Detailed Feedback Section:

✅ 🌟 Strengths: The text effectively conveys the importance of effective communication in today's fast-paced world. The introduction is clear, and the overall tone is engaging.

🚀 ⚡ Areas for Improvement:

Structure (Score: 8/10)
The text follows a logical structure, with a clear introduction, body, and conclusion. However, some transitions between ideas could be smoother. Consider adding transitional phrases or words to enhance coherence.
Delivery (Score: 6/10)
The pacing feels somewhat rushed, particularly in the second half of the text. Try to expand on key points and provide more supporting evidence to maintain reader engagement.
Content (Score: 7/10)
The content is generally well-supported with facts and examples. However, some statements could be further developed or backed up with more specific data. Ensure that arguments are well-structured and avoid logical fallacies.
🔄 📝 Suggested Revisions:

Expand on Key Points:
In the first paragraph, consider adding a sentence or two to elaborate on the benefits of effective communication in today's fast-paced world.
In the second paragraph, provide more specific examples of how the AI-powered coaching system enhances public speaking, storytelling, and conflict resolution skills.
Smooth Transitions:
Use transitional phrases (e.g., "however," "in addition," "meanwhile") to connect ideas between paragraphs and create a smoother flow.
Supporting Evidence:
In the third paragraph, consider adding more specific data or statistics to support the claim that the AI-powered coaching system is effective in improving communication skills.
By addressing these areas for improvement, you can enhance the overall structure, delivery, and content of your text, making it even more engaging and persuasive.
```

---

## 📊 **Comprehensive LLM Benchmarking Report**
### **System Information:**

| **Property**   | **Value** |
|---------------|----------|
| **OS**        | Ubuntu 24.04 |
| **CPU**       | x86_64 |
| **Total RAM** | 30.96 GB |
| **Used RAM**  | 5.77 GB |
| **Available RAM** | 23.81 GB |

### 📊 **Model Performance Comparison:**

| **Model**         | **Quantization** | **Inference Time (s)** | **Memory Usage (GB)** | **Accuracy (%)** |
|------------------|---------------|------------------|----------------|--------------|
| **Llama2:7B**   | **F16**        | **17.07s**      | **19.3GB**      | **9.3%** |
| **DeepSeek-14B** | **Q6_K**       | **50.2s**      | **23.0GB**      | **10.8%** |
| **Mistral-7B**   | **INT8**       | **13.9s**      | **18.2GB**      | **8.7%** |
| **Llama3.2**     | **NF4**        | **3.2s**       | **16.5GB**      | **12.3%** |

🏆 **Best Models Based on Use Case:**  
- **Best for Accuracy:** **DeepSeek-14B (F16)**  
- **Best for Speed:** **Llama3.2 (NF4)**  
- **Best for Memory Efficiency:** **DeepSeek-1.5B (INT8)**  

📌 Run `python3.11 src/evaluation_analysis.py` to benchmark new models.

---

## 🔍 **LLM Selection & Implementation Strategy**
After comprehensive benchmarking and evaluation, we have **shortlisted Llama3.2 (NF4) as the optimal model** for the **LLM Verbal Skills Trainer**. The selection was based on **accuracy, inference time, and memory efficiency**.

📌 **Key Implementation Details for Llama3.2 (NF4):**

| **Feature**                        | **Implementation Details** |
|------------------------------------|--------------------------|
| ✅ **Correct API URL**             | `f"{OLLAMA_SERVER_URL}generate"` |
| ✅ **Uses Llama3.2 (NF4) Quantization** | `"quantization": "NF4"` |
| ✅ **LRU Caching for Performance** | `@cached(cache=response_cache) @lru_cache(maxsize=128)` |
| ✅ **Multiprocessing for Speed**   | `multiprocessing.Pool(processes=4)` |
| ✅ **Better Error Handling**       | Catches `requests.exceptions.RequestException` |

By leveraging **NF4 (Normalized Float 4) quantization**, **efficient caching**, and **multiprocessing**, we **optimized inference speed and system resource utilization** while ensuring **high-quality AI-driven verbal skill training**. 🚀

---

## ⚙️ **Configuration Details**
All **prompts and settings** are located in **`config/settings.py`**.  

### **Key Configurations in `settings.py`**
- ✅ **Model & API Configurations**
- ✅ **Skill Training Prompt Structures**
- ✅ **TTS and Speech Recognition Configurations**
- ✅ **LRU Cache & Performance Optimization Settings**

📌 **Tracking Information** is stored in **`config/task_tracking.json`**, which maintains the **history of user attempts, performance scores, and progress tracking**.

---

## 💡 **Final Thoughts**
Selecting the right LLM depends on your **use case and system resources**.

✅ **For Accuracy:** Choose **DeepSeek-14B (F16)**.  
✅ **For Speed:** Choose **Llama3.2 (NF4)**.  
✅ **For Memory Efficiency:** Choose **DeepSeek-1.5B (INT8)**.  

🚀 Ready to enhance your verbal skills? Start today! 💡