import os
import openai
import gradio as gr

# 1. 必须先定义这个字典 [cite: 66-77]
MODEL_CONFIGS = {
    "阿里云-通义千问": {
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo"
    },
    "智谱AI-ChatGLM": {
        "api_key": os.getenv("ZHIPU_API_KEY"),
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "model": "glm-4"
    }
}

# 2. 定义交互函数
def interact_llm(chatbot, user_input, model_choice, temp, top_p):
    if not user_input:
        return chatbot, ""
    
    try:
        config = MODEL_CONFIGS[model_choice] # 这里会用到上面的变量 [cite: 66]
        client = openai.OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

        # 针对智谱 AI 的温度护栏：限制在 (0, 1.0) 之间
        current_temp = float(temp)
        if model_choice == "智谱AI-ChatGLM":
    # 智谱要求 (0, 1.0]，我们限制在 0.01 到 0.99
            current_temp = max(0.01, min(0.99, current_temp))
        else:
    # 阿里通义千问要求 [0, 2.0)，我们限制在 0 到 1.99
            current_temp = max(0.0, min(1.99, current_temp))
        
        # 构造消息历史
        messages = []
        for msg in chatbot:
            if isinstance(msg, dict):
                messages.append(msg)
            else:
                messages.append({"role": "user", "content": msg[0]})
                messages.append({"role": "assistant", "content": msg[1]})
        messages.append({"role": "user", "content": user_input})

        # 调用接口
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=current_temp,
            top_p=float(top_p) 
        )
        
        bot_reply = response.choices[0].message.content
        chatbot.append({"role": "user", "content": user_input})
        chatbot.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        chatbot.append({"role": "assistant", "content": f"发生错误：{str(e)}"})
    
    return chatbot, ""

# 3. 最后构建界面
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Multi-Model Comparison")
    
    with gr.Row():
        with gr.Column(scale=1):
            # 此时使用 MODEL_CONFIGS 就不会报错了 [cite: 66]
            model_selector = gr.Dropdown(
                choices=list(MODEL_CONFIGS.keys()), 
                value="阿里云-通义千问", 
                label="选择模型"
            )
            temp_slider = gr.Slider(0, 2, 1, step=0.1, label="温度 (Temperature)")
            top_p_slider = gr.Slider(0, 1.0, 0.7, step=0.05, label="核采样阈值 (Top-p)")
            reset_btn = gr.Button("🗑️ 清空对话")
        
        with gr.Column(scale=3):
            chatbot_ui = gr.Chatbot(label="聊天窗口") 
            msg_input = gr.Textbox(placeholder="输入问题并回车...", label="输入框")
            send_btn = gr.Button("🚀 发送", variant="primary")

    # 事件绑定
    send_btn.click(
        interact_llm, 
        inputs=[chatbot_ui, msg_input, model_selector, temp_slider, top_p_slider], 
        outputs=[chatbot_ui, msg_input]
    )
    msg_input.submit(
        interact_llm, 
        inputs=[chatbot_ui, msg_input, model_selector, temp_slider, top_p_slider], 
        outputs=[chatbot_ui, msg_input]
    )
    reset_btn.click(lambda: [], None, chatbot_ui)

if __name__ == "__main__":
    demo.launch(share=True)