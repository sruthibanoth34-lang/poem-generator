import gradio as gr
from google import genai
 
client = genai.Client(api_key="AQ.Ab8RN6Jn_CUJ2EX0fSJlcqZrmUUrZn3q85Ti691jbk38spfCuA")
 
STYLES = [
    "Simple",
    "Rhyming",
    "Funny",
    "Short",
    "Long / Detailed",
    "Storytelling",
]
 
MOODS = [
    "Joyful",
    "Sad",
    "Romantic",
    "Mysterious",
    "Peaceful",
    "Angry",
    "Nostalgic",
    "Hopeful",
]
 
 
def generate_poem(topic, style, mood, lines):
    if not topic or not topic.strip():
        return "Please enter a topic or theme for the poem."
 
    prompt = (
        f"Write a poem about '{topic}'. "
        f"Make the style {style.lower()}. "
        f"The mood/tone should be {mood.lower()}. "
        f"Keep it around {int(lines)} lines. "
        f"Only return the poem text, no explanations or extra notes."
    )
 
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip() if response.text else "No poem was returned. Please try again."
    except Exception as e:
        return f"Error generating poem: {e}"
 
 
with gr.Blocks(title="AI Poem Generator") as demo:
    gr.Markdown("## AI Poem Generator")
    gr.Markdown("Enter a topic, pick a style and mood, and generate a poem.")
 
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(
                label="Topic / Theme",
                placeholder="e.g. the ocean at night, first love, autumn leaves...",
                lines=2,
            )
            style = gr.Dropdown(
                choices=STYLES, value=STYLES[0], label="Poem Style"
            )
            mood = gr.Dropdown(
                choices=MOODS, value=MOODS[0], label="Mood"
            )
            lines = gr.Slider(
                minimum=4, maximum=32, step=2, value=12, label="Approx. Number of Lines"
            )
            generate_btn = gr.Button("Generate Poem", variant="primary")
 
        with gr.Column():
            output = gr.Textbox(
                label="Your Poem",
                lines=18,
            )
 
    generate_btn.click(
        fn=generate_poem,
        inputs=[topic, style, mood, lines],
        outputs=output,
    )
 
if __name__ == "__main__":
    demo.launch()